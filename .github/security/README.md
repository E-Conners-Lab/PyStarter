# Container review and approved base-image exception

Reviewed 2026-09-27. The owner approved Alpine as a narrow exception to SEC-31's
literal “distroless or -slim” base requirement after reviewing the scan and test
results. This changes the minimal runtime distribution, not the non-root,
least-privilege, scanning, or release-integrity requirements.

## Why Alpine

The tested Debian slim backend retained four unfixed mount/ACL CVEs:
CVE-2026-76642, CVE-2026-78409, CVE-2026-78410 and CVE-2026-54369. Their privileged
exploitation prerequisites were absent in the supplied local Compose setup, but
the libraries remained installed. We kept the HIGH gate blocking while checking
alternatives. Supported Bookworm and distroless Python alternatives added other
findings rather than resolving the gate.

The pinned official Python 3.13 Alpine runtime omits those Debian libraries.
The candidate passed all 106 Linux backend tests and Trivy 0.74 reported zero
HIGH/CRITICAL vulnerabilities **without VEX or vulnerability exclusions**. The
obsolete Debian VEX file and CI configuration have been removed. Image sizes
reported by the local Docker engine were approximately 44 MB for Alpine and
68 MB for slim; sizes vary by architecture and future rebuilds.

Alpine uses musl rather than glibc. Pure Python psycopg could not discover libpq
without extra runtime tooling, so the optional `container` dependency installs
`psycopg[c]==3.3.3`. Its compiler and libpq headers stay in the builder stage;
the final image contains the compiled driver and system libpq only. Normal
source installations retain the existing pure Python driver. psycopg's license
metadata remains installed with the package.

## Enforced controls

- Base images and build tools are digest-pinned; Python/npm dependencies locked.
- UID 10001, no-new-privileges, dropped capabilities and bounded process/memory
  settings in the supplied local Compose configuration.
- CI verifies the driver loads, the runtime identity and privileges, and that
  compiler tools, uv and pip are absent from the final backend image.
- CI runs the complete backend suite inside the actual Linux runtime image.
- All four runtime images are scanned with HIGH/CRITICAL failures blocking.
  No `ignore-unfixed`, VEX or blanket severity waiver is enabled.
- Frontend/proxy receive Alpine security updates. PostgreSQL derives from the
  pinned official image, runs directly as `postgres`, and removes only its
  unused vulnerable `gosu` helper. Database files/package metadata remain intact.

A clean scan is a dated check against known advisories, not a safety guarantee.
Rebuild and rescan after any base or dependency change. Images are for trusted
local code, not hostile execution or public hosting. Published image releases
still need signed digests, SBOM/provenance and architecture verification.

## Primary advisory evidence for the replaced Debian image

- [Mount hook privilege issue](https://github.com/util-linux/util-linux/security/advisories/GHSA-m25x-3hj9-m26f)
- [Restricted mount subdirectory issue](https://github.com/util-linux/util-linux/security/advisories/GHSA-8f2p-47x3-43mv)
- [Privileged bind-mount issue](https://github.com/util-linux/util-linux/security/advisories/GHSA-rh77-686x-2f2m)
- [ACL caller/API analysis](https://www.openwall.com/lists/oss-security/2026/06/29/1)
