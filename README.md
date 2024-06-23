[![Tags](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/tags.yaml/badge.svg)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/tags.yaml)

# Cloudflare Purge Cache Action

Purge Cloudflare Cache for Domains.

For more details see: [action.yaml](action.yaml)

### Inputs

| input   | required | default | description             |
|---------|----------|---------|-------------------------|
| token   | Yes      | -       | Cloudflare API Token    |
| domains | Yes      | -       | Domain(s) to Purge      |
| zone    | No       | -       | Deprecated: DO NOT USE! |

```yaml
  - name: "Purge Cache"
    uses: cssnr/cloudflare-purge-cache-action@master
    with:
      token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
      domains: example.com
```

### Examples

```yaml
name: "Test Purge Cache"

on:
  push:

jobs:
  test:
    name: "Test"
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: "Purge Cache"
        uses: cssnr/cloudflare-purge-cache-action@master
        with:
          token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          domains: |
            example.com
            test.example.com
```
