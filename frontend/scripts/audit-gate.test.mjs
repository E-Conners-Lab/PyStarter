import { test } from 'node:test';
import assert from 'node:assert/strict';
import { evaluate } from './audit-gate.mjs';

const TODAY = '2026-10-19';

function report(...advisories) {
  const vulnerabilities = {};
  for (const [name, ghsa, severity] of advisories) {
    vulnerabilities[name] = {
      name,
      severity,
      via: [{ name, severity, url: `https://github.com/advisories/${ghsa}` }],
    };
  }
  const total = Object.keys(vulnerabilities).length;
  return { auditReportVersion: 2, vulnerabilities, metadata: { vulnerabilities: { total } } };
}

const CLEAN = report();

function allowlist(...entries) {
  return {
    schemaVersion: 1,
    advisories: entries.map(([id, expires, reviewed = TODAY]) => ({
      id,
      package: 'pkg',
      expires,
      reviewed,
      reason: 'test',
    })),
  };
}

test('passes a clean report', () => {
  const result = evaluate(CLEAN, allowlist(), TODAY);
  assert.deepEqual(result.failures, []);
});

test('fails on an advisory that is not allowlisted, at any severity', () => {
  const result = evaluate(report(['dompurify', 'GHSA-aaaa-bbbb-cccc', 'low']), allowlist(), TODAY);
  assert.equal(result.failures.length, 1);
  assert.match(result.failures[0], /GHSA-aaaa-bbbb-cccc/);
});

test('passes an advisory waived until a future date', () => {
  const result = evaluate(
    report(['braces', 'GHSA-aaaa-bbbb-cccc', 'high']),
    allowlist(['GHSA-aaaa-bbbb-cccc', '2026-12-31']),
    TODAY,
  );
  assert.deepEqual(result.failures, []);
});

test('fails an advisory whose waiver has expired', () => {
  const result = evaluate(
    report(['braces', 'GHSA-aaaa-bbbb-cccc', 'high']),
    allowlist(['GHSA-aaaa-bbbb-cccc', '2026-10-18', '2026-09-01']),
    TODAY,
  );
  assert.equal(result.failures.length, 1);
  assert.match(result.failures[0], /expired/);
});

test('counts an advisory once when several packages inherit it', () => {
  const audit = report(['braces', 'GHSA-aaaa-bbbb-cccc', 'high']);
  audit.vulnerabilities.micromatch = { name: 'micromatch', severity: 'high', via: ['braces'] };
  const result = evaluate(audit, allowlist(), TODAY);
  assert.equal(result.failures.length, 1);
});

test('warns about waivers that no longer match anything', () => {
  const result = evaluate(CLEAN, allowlist(['GHSA-aaaa-bbbb-cccc', '2026-12-31']), TODAY);
  assert.deepEqual(result.failures, []);
  assert.equal(result.warnings.length, 1);
});

test('fails closed when npm audit reports an error', () => {
  const result = evaluate({ error: { code: 'ENOTFOUND' } }, allowlist(), TODAY);
  assert.equal(result.failures.length, 1);
});

test('fails closed on an unsupported allowlist schema version', () => {
  const result = evaluate(CLEAN, { schemaVersion: 2, advisories: [] }, TODAY);
  assert.equal(result.failures.length, 1);
  assert.match(result.failures[0], /schemaVersion/);
});

test('fails closed on a waiver without a valid expiry date', () => {
  const result = evaluate(
    report(['braces', 'GHSA-aaaa-bbbb-cccc', 'high']),
    allowlist(['GHSA-aaaa-bbbb-cccc', 'someday']),
    TODAY,
  );
  assert.ok(result.failures.some((failure) => /expires/.test(failure)));
});

test('fails closed on an unknown audit report version', () => {
  const result = evaluate({ auditReportVersion: 3, advisories: { x: {} } }, allowlist(), TODAY);
  assert.equal(result.failures.length, 1);
  assert.match(result.failures[0], /auditReportVersion/);
});

test('fails closed when the report counts vulnerabilities but none are parsed', () => {
  const audit = { auditReportVersion: 2, vulnerabilities: {}, metadata: { vulnerabilities: { total: 3 } } };
  const result = evaluate(audit, allowlist(), TODAY);
  assert.equal(result.failures.length, 1);
});

test('fails an advisory that has no GHSA id', () => {
  const audit = report(['pkg', 'GHSA-aaaa-bbbb-cccc', 'high']);
  audit.vulnerabilities.pkg.via = [{ name: 'pkg', severity: 'high', source: 1234 }];
  const result = evaluate(audit, allowlist(), TODAY);
  assert.equal(result.failures.length, 1);
  assert.match(result.failures[0], /no GHSA id/);
});

test('fails a waiver with an impossible calendar date', () => {
  const result = evaluate(CLEAN, allowlist(['GHSA-aaaa-bbbb-cccc', '9999-99-99']), TODAY);
  assert.ok(result.failures.some((failure) => /expires/.test(failure)));
});

test('fails a waiver longer than 180 days from its review', () => {
  const result = evaluate(CLEAN, allowlist(['GHSA-aaaa-bbbb-cccc', '2027-06-01']), TODAY);
  assert.ok(result.failures.some((failure) => /180 days/.test(failure)));
});

test('fails a waiver without a reason', () => {
  const list = allowlist(['GHSA-aaaa-bbbb-cccc', '2026-12-31']);
  delete list.advisories[0].reason;
  const result = evaluate(CLEAN, list, TODAY);
  assert.ok(result.failures.some((failure) => /reason/.test(failure)));
});

test('fails on duplicate waiver ids', () => {
  const list = allowlist(['GHSA-aaaa-bbbb-cccc', '2026-12-31'], ['GHSA-aaaa-bbbb-cccc', '2026-11-30']);
  const result = evaluate(CLEAN, list, TODAY);
  assert.ok(result.failures.some((failure) => /more than once/.test(failure)));
});

test('fails closed when the allowlist has no advisories array', () => {
  const result = evaluate(CLEAN, { schemaVersion: 1 }, TODAY);
  assert.equal(result.failures.length, 1);
});
