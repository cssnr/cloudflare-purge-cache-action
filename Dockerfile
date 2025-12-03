FROM python:3.13-alpine

ENV TZ=UTC
ENV PYTHONDONTWRITEBYTECODE=1

LABEL org.opencontainers.image.source="https://github.com/cssnr/cloudflare-purge-cache-action"
LABEL org.opencontainers.image.description="Cloudflare Purge Zone Cache Action"
LABEL org.opencontainers.image.authors="smashedr"

#COPY --from=python /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
#COPY --from=python /usr/local/bin/ /usr/local/bin/

COPY pyproject.toml /
# hadolint ignore=DL3013
RUN python -m pip install --no-cache-dir --group prod

COPY src /src

ARG VERSION="Local Source"
ENV APP_VERSION="${VERSION}"
LABEL org.opencontainers.image.version="${VERSION}"

ENTRYPOINT ["python", "/src/main.py"]
