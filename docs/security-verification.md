# Local release verification — 2026-09-27

## Decision and scope

This review starts at public commit `35d5500` (1.0.7) and prepares a separate
1.0.8 source update. The owner confirmed **downloads for local use only**, with
no public hosting, classroom service or untrusted learners. The owner explicitly
selected MIT licensing; LICENSE now matches that choice.

**Release status: source candidate awaiting protected review/merge.**
The application fixes and local tests do not update the existing 1.0.7 images or
runner ZIP. No new images, release tags or release assets were published here.

## Findings corrected

- SEC-07/16/26: CSRF on cookie-authenticated writes and auth lifecycle; correct
  refresh-cookie path, logout/reset revocation, rotated refresh sessions and
  pinned JWT issuer/audience/algorithm. Expired access can refresh correctly.
- SEC-06/17: shared database sliding-window auth limits and lockouts, Argon2id
  with 19MiB/time2/parallelism1. Password whitespace preserved consistently.
- SEC-03/27: unpublished parent/child content hidden; missing slugs return404;
  hidden expected outputs masked; submission history remains owner-scoped.
- SEC-05/11/18/36: explicit JSON boundary, field length/type validation, generic
  errors with correlation IDs, no-store/version/nosniff headers, sanitized
  provider failures and disabled telemetry body/default-PII collection.
- SEC-09/10/23/25: locally bundled Monaco/worker, self-only scripts, proxy method
  allowlist, frame/referrer protections and preserved custom-port Host for CSRF.
- SEC-12/15/29/30/32: fresh random local secrets, separated DB administrator,
  exact dependencies/locks and image/action digests, non-root processes, dropped
  capabilities, no-new-privileges, read-only web roots, no app host bind mounts.
- AI-1/2/3: optional text tutor has bounded, serialized, delimited, best-effort
  redacted input, no reference solution and no execution tools.
- Executor: bounded transport/output, private temporary working directory,
  process-group cleanup and restored beginner `type()` behavior. These are
  reliability controls; same-user subprocess execution is not secret isolation.
- Functional regressions: bodyless POSTs now send JSON, and background user/XP
  refresh no longer unmounts the exercise result UI.

## Verification evidence

Executed locally against the isolated review checkout, without changing the
owner's running application or database:

| Check | Result |
|---|---|
| Django backend tests | 106 tests on macOS (one Linux-only skip); all 106 pass in the Alpine Linux image |
| Branch-aware backend coverage | 90%; migrations, tests and static curriculum seed content excluded |
| Playwright browser suite | 99/99 pass |
| Frontend type-check/production build | pass |
| Migration drift | none |
| Python/npm dependency audits | zero known advisories at review time |
| Bandit high severity gate | pass |
| Python edit security hooks | pass |
| Gitleaks full history and current source | no live secrets detected; two exact synthetic historic fixture values excluded |
| CI syntax (actionlint) | pass |
| Fresh Docker install | healthy; non-default local port, registration, CSRF, local editor/worker, code execution and logout pass |
| Production browser network/CSP | no external asset requests or CSP violations in the tested flow |
| Frontend/proxy/database image scans | zero high/critical findings |
| Backend Alpine image scan | zero high/critical findings without exclusions; approved SEC-31 base exception |
| Hosted GitHub CI/CodeQL | exact-commit results are recorded in [PR #3 checks](https://github.com/E-Conners-Lab/PyStarter/pull/3/checks); all ten are required before merge |
| Native Windows | unsupported; Docker path supplied, PowerShell script not executed on Windows here |
| Multi-architecture released images | not built/published by this review |

Scans detect known patterns/advisories, not all vulnerabilities. Browser tests
cover the app; they do not certify resistance to hostile Python code.

## Image remediation and approved exception

The owner approved switching from the Debian slim base to official Python Alpine
after the candidate passed all 106 Linux tests and a zero-HIGH/CRITICAL Trivy0.74
scan. This is a documented exception to SEC-31's literal slim/distroless naming;
non-root execution, hardening, scanning and release integrity remain required.

The Debian image had retained four privileged mount/ACL CVEs. Alpine removes
those affected Debian libraries. No vulnerability waiver or VEX suppression is
used by the final image scan. A compiled psycopg driver is built in a separate
stage for Alpine compatibility; compilers never enter the runtime. See
[the base-image rationale and evidence](../.github/security/README.md).

## Remote repository gates

At review time GitHub reports secret scanning and push protection enabled.
Main protection is now enabled: one independent review, stale-review dismissal,
last-push approval, all ten CI/security checks, signed commits, no force pushes,
no deletions, and administrator enforcement. These settings were read back from
GitHub. No local signing identity was available; the draft review branch is
unsigned. The eventual release merge still needs an independently approved,
signed commit through the protected workflow. Do not bypass that requirement.

Prebuilt images additionally require hosted build provenance, SBOMs, signatures,
and verification of every advertised architecture. This work does not silently
waive those release requirements or mark the existing artifacts verified.

## Control applicability (all active SEC/AI controls)

| Controls | Status and scope |
|---|---|
| SEC-01 | PASS: auth tokens HttpOnly; CSRF token is not a bearer credential |
| SEC-02, SEC-03, SEC-27 | PASS reviewed routes: explicit public pages/registration/leaderboard; authenticated user data and state transitions checked |
| SEC-04, SEC-16, SEC-26 | PASS: new sessions at login; rotation, expiry, claims and standard cryptographic comparisons; Django admin session behavior retained |
| SEC-05, SEC-07 | PASS: JSON, schema constraints, CSRF and cross-site metadata rejection |
| SEC-06 | PASS auth sliding window/lockout; default local app is one learner, not distributed load |
| SEC-08 | N/A to supported loopback HTTP; internet transport is unsupported, production defaults retain HTTPS controls |
| SEC-09 | PASS scripts; documented inline-style exception for Monaco in SECURITY.md |
| SEC-10, SEC-24, SEC-25 | PASS production proxy frame/cache/referrer headers and API no-store |
| SEC-11 | PASS generic API errors; submitted program errors are intentionally returned as learning feedback |
| SEC-12, SEC-18 | PASS reviewed source/history and redaction boundaries; no claim to discover every possible secret |
| SEC-13 | N/A no staging/hosted production; each local install generates distinct credentials |
| SEC-14 | OWNER ACTION: local provider-key rotation; no external credential lifecycle service exists |
| SEC-15, SEC-32 | PASS app/CI minimum scopes and separate DB identity; app DB ownership needed for local startup migrations |
| SEC-17 | PASS Argon2id; legacy PBKDF2 verification permits gradual migration |
| SEC-20, SEC-21, SEC-22 | N/A no uploads/private object-storage sharing |
| SEC-23 | PASS route+proxy allowlists and proxy405 Allow header |
| SEC-28 | PARTIAL: sanitized security events exist; local logs are not immutable external audit storage |
| SEC-29, SEC-30 | PASS pinned Python/npm dependencies and all runtime image scans; CI gates future changes |
| SEC-31 | Approved Alpine base exception; non-root/hardening/scans pass. Binary-release attestations still required; Kubernetes N/A |
| SEC-34 | PASS remote controls configured; signed, independently approved release merge still pending |
| SEC-35 | PASS push protection and required secret/SAST checks configured; hosted execution tracked on PR |
| SEC-36 | PASS v1 path/version header; no independently versioned persisted request envelope introduced |
| AI-1 | PASS input placement/boundaries; prompt injection cannot be eliminated by delimiters |
| AI-2 | PASS no model tools or autonomous actions exist; no tool approval workflow needed |
| AI-3 | PASS structural minimization/redaction tests; user must not submit sensitive material |
| AI-4 | PARTIAL deterministic boundary/provider/regression tests pass; live model behavior not evaluated |

Retired SEC-19: production proxy directory listings disabled. Retired SEC-33:
operating posture, not a separate gate.

## AI evaluation checklist

Prompt version: `local-tutor-v2`. Required automated threshold: all boundary,
provider-error and critique-gating tests pass, with no added tools and no
reference-solution leakage. Regression tests exercise malformed types, overlong
input, secret redaction, unconfigured provider, empty/refused/failed provider
responses and pre/post-success critique behavior.

Before choosing/changing a live model, evaluate a versioned set containing:
ordinary beginner hints; requests for exact solutions; forged system/delimiter
instructions; attempts to retrieve credentials or hidden answers; malicious
model output presented as executable advice; and a provider outage. Require no
secret/reference-solution disclosure and no autonomous execution, plus useful
beginner explanations. Record model ID, prompt version, results and reviewer.
No live paid provider calls or semantic model-quality certification occurred in
this review. Optional AI remains opt-in and its advice must be reviewed by the
learner before execution.
