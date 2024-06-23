FROM python:3.11-alpine

#COPY docker-entrypoint.sh /
#COPY src/ /src
#RUN chmod +x docker-entrypoint.sh /src/*

COPY --chmod=0755 docker-entrypoint.sh /
COPY --chmod=0755 src/ /src

RUN python -m pip install requests

ENTRYPOINT ["/docker-entrypoint.sh"]
