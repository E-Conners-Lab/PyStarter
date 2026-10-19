// Fails CI on any npm advisory, at any severity, unless audit-allowlist.json
// waives that exact GHSA id with a reason and an expiry date. Waivers expire so
// an accepted risk gets re-examined instead of silently living forever.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const SUPPORTED_SCHEMA_VERSION = 1;
// The gate only understands this npm audit --json shape; anything else fails closed.
const SUPPORTED_AUDIT_REPORT_VERSION = 2;
const MAX_WAIVER_DAYS = 180;
const DAY_MS = 24 * 60 * 60 * 1000;
const GHSA_ID = /^GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}$/;
const GHSA_FROM_URL = /\/(GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4})$/;

function parseDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
  const date = new Date(`${value}T00:00:00Z`);
  // Rejects impossible dates such as 2026-02-30 or 9999-99-99.
  return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value ? date : null;
}

function validateAudit(audit) {
  if (audit.error) return `npm audit did not complete: ${JSON.stringify(audit.error)}`;
  if (audit.auditReportVersion !== SUPPORTED_AUDIT_REPORT_VERSION) {
    return `npm audit auditReportVersion ${audit.auditReportVersion} is not supported`;
  }
  const { vulnerabilities } = audit;
  if (typeof vulnerabilities !== 'object' || vulnerabilities === null || Array.isArray(vulnerabilities)) {
    return 'npm audit report has no vulnerabilities object';
  }
  return null;
}

function validateWaiver(entry) {
  const problems = [];
  if (!GHSA_ID.test(entry.id ?? '')) problems.push('id must be a GHSA id');
  if (typeof entry.reason !== 'string' || entry.reason.trim() === '') problems.push('reason is required');
  const reviewed = parseDate(entry.reviewed);
  const expires = parseDate(entry.expires);
  if (!reviewed) problems.push('reviewed must be a real YYYY-MM-DD date');
  if (!expires) problems.push('expires must be a real YYYY-MM-DD date');
  if (reviewed && expires && (expires - reviewed) / DAY_MS > MAX_WAIVER_DAYS) {
    problems.push(`expires is more than ${MAX_WAIVER_DAYS} days after reviewed`);
  }
  return problems.map((problem) => `waiver ${entry.id ?? '(no id)'}: ${problem}`);
}

function validateAllowlist(allowlist) {
  if (allowlist.schemaVersion !== SUPPORTED_SCHEMA_VERSION) {
    return { failures: [`audit-allowlist.json schemaVersion ${allowlist.schemaVersion} is not supported`] };
  }
  if (!Array.isArray(allowlist.advisories)) {
    return { failures: ['audit-allowlist.json advisories must be an array'] };
  }
  const failures = [];
  const waivers = new Map();
  for (const entry of allowlist.advisories) {
    const problems = validateWaiver(entry);
    failures.push(...problems);
    if (waivers.has(entry.id)) failures.push(`waiver ${entry.id}: listed more than once`);
    // An invalid waiver is reported above and never counts as a waiver.
    else if (problems.length === 0) waivers.set(entry.id, entry);
  }
  return { failures, waivers };
}

function collectAdvisories(audit) {
  const advisories = new Map();
  const unidentified = [];
  for (const vulnerability of Object.values(audit.vulnerabilities)) {
    for (const via of vulnerability.via ?? []) {
      // String entries only point at another vulnerable package; the advisory
      // itself is listed as an object under that package.
      if (typeof via !== 'object' || via === null) continue;
      const id = GHSA_FROM_URL.exec(via.url ?? '')?.[1];
      if (id) advisories.set(id, { id, package: via.name, severity: via.severity });
      else unidentified.push(`advisory ${via.source ?? '?'} (${via.name}, ${via.severity}) has no GHSA id`);
    }
  }
  return { advisories, unidentified };
}

export function evaluate(audit, allowlist, today) {
  const auditProblem = validateAudit(audit);
  if (auditProblem) return { failures: [auditProblem], warnings: [] };
  const { failures, waivers } = validateAllowlist(allowlist);
  if (!waivers) return { failures, warnings: [] };

  const warnings = [];
  const { advisories, unidentified } = collectAdvisories(audit);
  failures.push(...unidentified);
  if ((audit.metadata?.vulnerabilities?.total ?? 0) > 0 && advisories.size + unidentified.length === 0) {
    failures.push('npm audit counted vulnerabilities but the gate parsed none');
  }

  for (const advisory of advisories.values()) {
    const label = `${advisory.id} (${advisory.package}, ${advisory.severity})`;
    const waiver = waivers.get(advisory.id);
    if (!waiver) {
      failures.push(`${label} is not allowlisted`);
    } else if (waiver.expires < today) {
      failures.push(`${label} waiver expired on ${waiver.expires}; fix it or re-review the waiver`);
    }
  }
  for (const id of waivers.keys()) {
    if (!advisories.has(id)) warnings.push(`${id} is allowlisted but no longer reported; remove the waiver`);
  }
  return { failures, warnings };
}

function runAudit() {
  try {
    return execFileSync('npm', ['audit', '--json'], { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 });
  } catch (error) {
    // npm audit exits non-zero whenever it finds anything; the JSON is still on stdout.
    if (error.stdout) return error.stdout;
    throw error;
  }
}

function main() {
  const allowlistPath = fileURLToPath(new URL('../audit-allowlist.json', import.meta.url));
  const allowlist = JSON.parse(readFileSync(allowlistPath, 'utf8'));
  const audit = JSON.parse(runAudit());
  const today = new Date().toISOString().slice(0, 10);
  const { failures, warnings } = evaluate(audit, allowlist, today);

  for (const warning of warnings) console.warn(`warning: ${warning}`);
  for (const waiver of allowlist.advisories ?? []) {
    console.log(`waived until ${waiver.expires}: ${waiver.id} (${waiver.package})`);
  }
  if (failures.length > 0) {
    for (const failure of failures) console.error(`error: ${failure}`);
    process.exit(1);
  }
  console.log('npm audit gate passed');
}

if (process.argv[1] === fileURLToPath(import.meta.url)) main();
