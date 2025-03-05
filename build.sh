#!/usr/bin/env bash

[[ ! -f "action.yaml" ]] && echo "Wrong Directory" && exit 1
_IMAGE=$(grep -o 'ghcr.io/.*' action.yaml | sed 's/".*//')
echo "Using image: ${_IMAGE}"
echo "Local Build" > src/version.txt
docker build src --platform linux/amd64 --tag "${_IMAGE}"
rm src/version.txt
act -j test -e event.json --action-offline-mode "$@"
