# Security

PyStarter is MIT licensed and **not actively maintained**. There is no security
response process: no advisory feed, no patch SLA, no guarantee that a reported
issue is ever fixed. If you deploy it, you own its security. Fork it and patch
your fork.

## The code sandbox is not a security boundary

PyStarter runs student-submitted Python. It restricts that code with an import
allowlist, a builtins blocklist, a separate OS process, resource limits, and an
execution deadline.

**Those restrictions are defeatable, and you should assume they will be.** The
Python-level restrictions in particular can be escaped: submitted code can reach
real builtins through ordinary object attributes and import modules that are not
on the allowlist. This is a known property of restricting Python inside Python,
not a bug with a pending fix.

What actually contains an escape today:

| Control | What it gives you |
|---|---|
| Separate subprocess | An escape does not land in the Django process, its database connection, or its request context |
| Scrubbed environment | The child sees `PATH`, `HOME`, `LANG` only — no API keys, no `DJANGO_SECRET_KEY`, no database password |
| `subprocess` deadline | A runaway or infinite loop is killed rather than occupying a worker |
| Resource limits | Memory and recursion caps on the child |
| Non-root container user | An escape inside Docker is not root |

What still is **not** contained: escaped code runs as the application's OS user,
with that user's filesystem access and outbound network access. There is no
seccomp profile, no user namespace, no network namespace, and no filesystem
isolation beyond ordinary Unix permissions.

## Deploy accordingly

- **Intended use is local or small-group, with people you trust.** The default
  `docker compose` binds to `127.0.0.1` for this reason.
- **Do not expose this to the public internet**, and do not run it with open
  registration for strangers. Signup is public by default; anyone with an account
  can execute code.
- **If you must run it multi-user**, put real isolation underneath the executor —
  a container or microVM per execution (gVisor, Firecracker, nsjail), a dedicated
  unprivileged user, no outbound network, a read-only filesystem — and treat the
  in-process restrictions as defense in depth only.
- **Run it on a host you can afford to lose.** Do not co-locate it with data or
  credentials that matter.
- **Keep dependencies patched yourself.** The published images are snapshots and
  will drift; rebuild from source with updated pins.

## Reporting

There is no monitored channel. Open a public GitHub issue if you want other users
to see it, but expect no response. For anything serious, the useful action is to
fix it in your fork and, if you like, open a PR so others can find the patch.
