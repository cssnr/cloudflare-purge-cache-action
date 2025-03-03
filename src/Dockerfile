FROM python:3.13-alpine

LABEL org.opencontainers.image.source="https://github.com/cssnr/cloudflare-purge-cache-action"
LABEL org.opencontainers.image.description="Cloudflare Purge Zone Cache Action"
LABEL org.opencontainers.image.authors="smashedr"

COPY requirements.txt /
RUN python -m pip install -Ur requirements.txt

COPY . /src
ENTRYPOINT ["python", "/src/main.py"]
