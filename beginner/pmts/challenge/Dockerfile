FROM python:3.13.7-slim-trixie

RUN apt-get update
RUN apt-get install -y socat
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/chal
WORKDIR /opt/chal

COPY chall.py ./

ENV FLAG=K17CTF{s4Lt_4nD_p3pper_is_ov3rr4t3d}

RUN adduser chal
USER chal
CMD socat -v -T60 tcp-listen:1337,fork,reuseaddr system:"python3 chall.py 2>&1"