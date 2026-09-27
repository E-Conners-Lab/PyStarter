# Security

PyStarter is MIT licensed and intended for one person's local learning on their
own machine. It is not actively maintained; there is no promised patch schedule
or monitored security response channel. Keep your installation and dependencies
updated. See [the verification record](docs/security-verification.md) for the
scope and outstanding release gates of this review.

## Run only code you trust

Submitted Python runs as the backend's OS user. Python import/builtin
restrictions are bypassable. A separate process and a scrubbed child environment
**do not protect backend secrets**: escaped code may access same-user files,
process information, database credentials, network services, and application data.
Do not paste or run untrusted code, including code suggested by an AI tutor.
Do not load this application with valuable credentials or private source code.

Timeouts and output limits handle ordinary mistakes. The parent terminates the
job's process group, but deliberately detached descendants can evade that group.
Linux enforces memory/process resource limits; macOS does not provide the same
memory guarantees. Native Windows execution is unsupported: use Linux containers
in Docker Desktop. Docker uses a non-root backend, drops capabilities, disables
privilege escalation, and mounts no host working directory into the backend.
These reduce exposure; they do not make hostile multi-user execution safe.

## Local deployment only

- Keep the web port on `127.0.0.1`. Do not expose it to a LAN, public internet,
  reverse tunnel, classroom, or untrusted users. Registration is public to
  anyone who can reach the service.
- Local HTTP is an explicit exception to HTTPS/Secure-cookie/HSTS requirements.
  The supplied Compose configuration is loopback-only. Internet hosting is not
  supported by this release.
- Use a unique password. Authentication cookies are HttpOnly and SameSite=Strict;
  writes require CSRF tokens. Access expires after 30 minutes and refresh after
  seven days with rotation. Logout/reset revoke affected sessions server-side.
- Keep `.env`, databases, backups, and API keys private. Fresh Docker installs
  generate separate application, DB administrator, and DB application secrets.
  Rotate provider keys in the provider console and replace your local setting;
  changing the Django signing key signs everyone out.
- AI is optional. Provider requests include submitted code and lesson context.
  Pattern redaction cannot identify every secret or personal detail. No tools
  are granted to the tutor. Telemetry is off by default; optional backend Sentry
  disables request-body and default PII capture.
- Production CSP permits inline **styles** for Monaco's dynamic positioning and
  syntax rendering. Scripts remain self-only, with no unsafe-inline/unsafe-eval;
  editor code and workers are bundled locally. This style-only exception does
  not authorize injecting untrusted HTML.

Real isolation for untrusted learners would require a separately designed
execution service with per-job identities, filesystem/network isolation,
resource accounting and an independent security review. It is out of scope here.

## Reporting and release integrity

There is no monitored reporting channel or patch SLA. GitHub issues and pull
requests may go unanswered; never post credentials or private data in an issue.
A fix in source does not repair old release ZIPs or images. Use a reviewed commit
and verified artifacts. Do not treat this review as a guarantee against all bugs.
