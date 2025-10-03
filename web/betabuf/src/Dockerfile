FROM python:3.13.7-slim-trixie

RUN pip install --no-cache-dir flask waitress protobuf

WORKDIR /app
COPY . .

USER nobody

ENV SIGNING_KEY="016f6f74b9f803ca3a5210d04b16c0f70757d31fbf2290c82d3247633a53f698"
ENV FLAG='K17{im_addicted_to_th3_thrill_of_bl1ndly_tru$ting_us3r_input}'

CMD waitress-serve --listen "0.0.0.0:1337" --trusted-proxy '*' --trusted-proxy-headers 'x-forwarded-for x-forwarded-proto x-forwarded-port' --log-untrusted-proxy-headers --clear-untrusted-proxy-headers --threads 4 main:app
