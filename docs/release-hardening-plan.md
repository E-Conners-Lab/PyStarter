# Local release hardening — September 27, 2026

Target: the current 1.0.7 code, distributed for individuals to run locally. The owner explicitly excludes internet hosting. Work is on codex/public-release-hardening, based on 35d5500. Existing user data must remain usable; upgrading intentionally invalidates old sessions. No cloud service or remote code execution service is introduced.

## Acceptance and scope

First prove the existing local register → edit → run → submit → logout loop and the security regressions. Then correct cookie authentication, execution lifecycle, dependency/CI failures, request boundaries, and packaging; finish with clean-install backend, frontend, and browser checks. Gates are observable test/scanner results, not a promise of absolute safety. No internet-classroom claim, new curriculum feature, or untested published image is included.

Trust boundaries: browser input is untrusted at the API; the server owns identity, grading and progress. Submitted Python is trusted local code with the user's OS permissions, not a hostile-code sandbox. Its subprocess is for bounded lifecycle/reliability only. Docker limits access to the container but is not a per-execution security boundary. Optional AI receives only bounded/redacted user text after explicit API-key configuration; model output is rendered as text/markdown and never executed. PostgreSQL and application secrets stay backend-side. The download is loopback-only by default.

## Independent work and tests

- Auth: write failing tests for missing/invalid CSRF, refresh with expired access cookies, logout cookie routing and revocation, password reset invalidation, and cookie flags; then fix backend and browser client together. Use standard Django CSRF/SimpleJWT, shared lockout state, and Argon2id.
- Execution: write failing tests for output floods, descendants retaining stdout, malformed replies, generic errors and normal beginner code; enforce process-group termination, bounded reads, private temporary cwd, and limits. Native Windows execution uses Docker; do not pretend POSIX job controls are portable.
- Dependencies/CI: inspect registry advisories and licenses, use compatible fixed exact pins with committed locks, frozen builds, pinned action SHAs and read-only workflow permissions. Security scans gate changes. Keep build-only packages out of runtime images.
- API/UI/config: validate JSON and AI field lengths/types, bound/redact AI prompt text, retain model-output-as-data behavior, add correlation IDs and no-store/version headers, bundle Monaco locally so CSP does not depend on an external CDN, and align Docker/frontend ports.
- Delivery: document the local-only boundary, verify clean-install instructions, review the final diff, commit without bypassing hooks, and push a reviewable branch/PR. A new downloadable image must be built and verified separately before any claim that an old release contains these fixes.

## Ordering and recovery

Tests precede each implementation. CSRF bootstrap and client-header support land together with server enforcement. New token claims invalidate earlier sessions; existing accounts/progress remain. Migrations are additive. Dependency locks are regenerated before testing frozen installs. Review source and artifact provenance before release changes. On any failed gate, retain the prior release artifact and do not describe the new code as verified. Revert the hardening branch to roll back code; review migrations before any database rollback.

## Identity table

| Identity | System | Needs | Must not have |
|---|---|---|---|
| Local reviewer | GitHub | read repo/settings; push review branch | force-push/rewrite public history |
| CI checks | GitHub | read source | repository write permissions or production secrets |
| Application | local database | application tables and required migrations | host root or Docker socket |
| Code subprocess | local container | execute trusted local exercises | advertised isolation from its own OS identity |
| Optional AI client | configured provider | inference only | account administration |

## PLAN and SYS self-review

PASS: PLAN-01/02/03 (existing vertical loop first, bounded security scope), PLAN-05 (settings/serializers and committed locks canonical), PLAN-07 (ordering above), PLAN-08/09 (explicit trust boundaries and honest execution claims), PLAN-11 (server-only session tokens and solution handling), PLAN-12/13/14 (registry/advisory/license review required before dependency changes), PLAN-15 (tests/scans/build/browser gate). N/A PLAN-04: no binary/units contract. PLAN-06 PASS: API remains v1, additive migrations and explicit new token validation invalidate unsupported sessions. PLAN-10 N/A: no promised performance or cost target; time/output limits are enforcement values tested directly.

PASS: SYS-01 (local single-deploy), SYS-03/04/06/07 (browser → authenticated Django → database/executor/optional AI boundaries above), SYS-11 (existing models canonical), SYS-12 (v1 retained, headers added, no published field removals intended), SYS-13 (server-authoritative progress; shared auth counters need atomic updates), SYS-14 (deadline/provider/auth failure modes and recovery), SYS-15 (observable gates). SYS-02 PASS: one local learner is the intended load; no scale claim. SYS-05 N/A: no new certificate infrastructure, local HTTP loopback only; TLS required if deployment shape changes. SYS-08/09 N/A: no new growing-data hot path or cache beyond bounded security counters. SYS-10 PASS: subprocess is for lifecycle separation; no async-throughput claim.

All 38 SEC/AI controls will be classified in the final verification record. File uploads, signed object URLs, Kubernetes, LLM tools and RAG are N/A because absent. Operational remote branch protection/signatures/secret push protection must be checked separately; unavailable evidence is not a PASS. CI and the report must distinguish scanner findings from demonstrated reachability.
