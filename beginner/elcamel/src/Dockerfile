FROM python:3.13.7-slim-trixie

RUN apt-get update
RUN apt-get install -y socat
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/chal
WORKDIR /opt/chal

RUN python3 -m pip install sympy

COPY secret.py chall.py ./

RUN adduser chal
USER chal
CMD socat -v -T60 tcp-listen:1337,fork,reuseaddr system:"python3 chall.py 2>&1"