#!/usr/bin/env bash

_IMAGE=$(grep -o 'ghcr.io/.*' action.yml | sed 's/".*//')
echo "Using image: ${_IMAGE}"
docker build src --platform linux/amd64 --tag "${_IMAGE}"
act -j test -e event.json --action-offline-mode "$@"
