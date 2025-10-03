FROM ubuntu:24.04 AS chroot

# ubuntu24 includes the ubuntu user by default
RUN /usr/sbin/userdel -r ubuntu && /usr/sbin/useradd --no-create-home -u 1000 user

RUN apt-get install coreutils

COPY flag /
COPY src/processor ./app/binary
COPY src/calculator ./app/calculator

RUN printf '%s\n' '#!/bin/sh' \
  'exec /usr/bin/stdbuf -i0 -o0 -e0 /app/binary "$@"' \
  > /app/run && chmod +x /app/run

# use the jail base image
FROM pwn.red/jail
# copy the root files from any Docker image
COPY --from=chroot / /srv
ENV JAIL_MEM=20M JAIL_TMP_SIZE=20M