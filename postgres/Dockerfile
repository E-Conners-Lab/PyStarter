# Keep the supported upstream database and remove an unused privilege helper.
FROM postgres:16.15-alpine3.24@sha256:721873c34ceb9f8d8fc265984940dc982404c105f19ad51be9fdc5970a6080ea
USER root
# Compose and this image start directly as postgres. The root-only gosu branch
# in the upstream entrypoint is unreachable and the old bundled Go runtime is unnecessary.
RUN rm /usr/local/bin/gosu
USER postgres
