#!/usr/bin/env sh

set -e

echo "Starting: Cloudflare Cache Purge"

echo "Running: purge.py"

python /src/purge.py
