# Container finding triage

Reviewed 2026-09-27 using Trivy 0.74.0 and the Debian security tracker. This
file is evidence for the local PyStarter backend image, not a general Debian
vulnerability waiver. The backend CI job checks the stated component absence
before applying `backend.vex.json`. Its package URLs include exact versions;
base updates that change those versions require a new review.

## Verified absent vulnerable code

- [CVE-2025-69720](https://security-tracker.debian.org/tracker/CVE-2025-69720)
  is in `infocmp`'s `analyze_string` CLI routine. The Dockerfile removes
  `/usr/bin/infocmp`. The curses libraries do not contain that CLI routine.
- [CVE-2026-78408](https://security-tracker.debian.org/tracker/CVE-2026-78408)
  is in `nsenter --join-cgroup`. The Dockerfile removes `/usr/bin/nsenter`.
- [CVE-2026-16742](https://security-tracker.debian.org/tracker/CVE-2026-16742)
  affects `systemd-homed`. That service is not installed; the flagged
  `libsystemd0` and `libudev1` packages share its source package only.
- [CVE-2026-9538](https://security-tracker.debian.org/tracker/CVE-2026-9538)
  affects Perl `Archive::Tar`. That module is not present in `perl-base`.

The CI assertions search `/usr` for each affected executable/module and fail
if any reappears. They also verify UID 10001 and the absence of setuid/setgid
files in `/usr/bin` and `/usr/sbin`. These four VEX statements do not suppress
unrelated CVEs or package versions. Use this file only with the backend image
built by this repository, not arbitrary Debian images.

## Findings still blocking the backend image gate

The source-package scan still reports these unfixed Debian Trixie issues:

- [CVE-2026-76642](https://security-tracker.debian.org/tracker/CVE-2026-76642),
  [CVE-2026-78409](https://security-tracker.debian.org/tracker/CVE-2026-78409),
  and [CVE-2026-78410](https://security-tracker.debian.org/tracker/CVE-2026-78410)
  affect privileged mount operations. Mount/umount CLIs and setuid permissions
  have been removed, and Compose drops capabilities and forbids new privileges.
  The underlying libmount code remains, so these are not suppressed.
- [CVE-2026-54369](https://security-tracker.debian.org/tracker/CVE-2026-54369)
  affects pathname-based ACL operations by a privileged caller. The runtime
  is non-root, but libacl remains installed; this finding is not suppressed.

Debian currently labels these issues minor and postpones stable fixes. This
reduces neither the recorded finding count nor the gate threshold. Updating
the runtime or explicitly accepting a documented residual risk is still needed
before claiming the image passes the high/critical scan. No `ignore-unfixed`
setting or blanket severity exclusion is enabled.

## Other fixes

Runtime pip was removed; it carried a vulnerable vendored msgpack version.
The backend now uses pure-Python psycopg with Debian's libpq instead of opaque
bundled PostgreSQL client libraries. Frontend Alpine libexpat was upgraded to
2.8.5-r0. Both runtime images use non-root users and digest-pinned base images;
build dependencies remain in separate stages.

PostgreSQL is derived from the pinned upstream 16.15 Alpine image. Its unused
`gosu` executable bundled a Go runtime with 22 high/critical findings. The image
and Compose run directly as `postgres`, so the derived image removes only that
helper. No upstream database files or package metadata are removed. The rebuilt
database and proxy images pass the high/critical scan.

Supported alternative Python runtime bases were evaluated without replacing
the working runtime. The current Bookworm slim image retains the same mount/ACL
issues and adds SQLite/Perl findings. The supported distroless Python Debian 13
image adds older system Python/libexpat findings and would require a new startup
path and libpq integration. Neither is a verified clean drop-in replacement.
