#!/usr/bin/env bash

set -e

[[ ! -f "action.yaml" ]] && echo "Wrong Directory" && exit 1
_IMAGE=$(grep -o 'ghcr.io/.*' action.yaml | sed 's/".*//')
echo "Using image: ${_IMAGE}"
docker build --tag "${_IMAGE}" .
act -j test -e event.json --action-offline-mode "$@"
