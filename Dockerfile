FROM python:3.11-alpine

RUN python -m pip install requests

COPY --chmod=0755 docker-entrypoint.sh /
COPY --chmod=0755 scripts/ /scripts

ENTRYPOINT ["/docker-entrypoint.sh"]
