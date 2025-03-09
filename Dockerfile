FROM python:3.13-alpine

LABEL org.opencontainers.image.source="https://github.com/cssnr/cloudflare-purge-cache-action"
LABEL org.opencontainers.image.description="Cloudflare Purge Zone Cache Action"
LABEL org.opencontainers.image.authors="smashedr"

ENV TZ=UTC
ENV PYTHONDONTWRITEBYTECODE=1

#COPY --from=python /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
#COPY --from=python /usr/local/bin/ /usr/local/bin/

COPY requirements.txt /
RUN python -m pip install --no-cache-dir -r /requirements.txt

COPY src /src
ENTRYPOINT ["python", "/src/main.py"]
