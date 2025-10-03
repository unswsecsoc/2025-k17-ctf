FROM ubuntu:24.04 AS chroot

RUN /usr/sbin/userdel -r ubuntu && /usr/sbin/useradd --no-create-home -u 1000 user

RUN apt-get install coreutils

COPY flag /
COPY kaboom /app/binary

RUN printf '%s\n' '#!/bin/sh' \
  'exec /usr/bin/stdbuf -i0 -o0 -e0 /app/binary "$@"' \
  > /app/run && chmod +x /app/run

FROM pwn.red/jail
COPY --from=chroot / /srv
ENV JAIL_MEM=20M JAIL_TMP_SIZE=20M