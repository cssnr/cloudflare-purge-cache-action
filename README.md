# Cloudflare Purge Cache Action

Coming Soon...

## Purge Cache

For more details see: [action.yaml](action.yaml)

### Inputs

| input  | description          |
|--------|----------------------|
| zone:  | Zone to Purge        |
| token: | Cloudflare API Token | 

### Short Example

```yaml
name: "Test Docker Stack Deploy"

on:
  push:

jobs:
  test:
    name: "Test"
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: "Purge Cache"
        uses: cssnr/cf-purge-cache-action@master
        with:
          zone: example.com
          token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```
