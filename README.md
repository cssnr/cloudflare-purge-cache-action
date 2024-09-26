[![Tags](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/tags.yaml?logo=github&logoColor=white&label=tags)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/tags.yaml)
[![Test](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/test.yaml?logo=github&logoColor=white&label=test)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/test.yaml)
[![GitHub Release Version](https://img.shields.io/github/v/release/cssnr/cloudflare-purge-cache-action?logo=github)](https://github.com/cssnr/cloudflare-purge-cache-action/releases/latest)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/cssnr/cloudflare-purge-cache-action?logo=github&logoColor=white&label=updated)](https://github.com/cssnr/cloudflare-purge-cache-action/graphs/commit-activity)
[![Codeberg Last Commit](https://img.shields.io/gitea/last-commit/cssnr/cloudflare-purge-cache-action/master?gitea_url=https%3A%2F%2Fcodeberg.org%2F&logo=codeberg&logoColor=white&label=updated)](https://codeberg.org/cssnr/cloudflare-purge-cache-action)
[![GitHub Top Language](https://img.shields.io/github/languages/top/cssnr/cloudflare-purge-cache-action?logo=htmx&logoColor=white)](https://github.com/cssnr/cloudflare-purge-cache-action)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&logoColor=white)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)

# Cloudflare Purge Cache Action

Purge Cloudflare Cache for a Domain or list of Domains.

For more details see: [action.yaml](action.yaml) and [src/main.py](src/main.py).

- [Inputs](#Inputs)
- [Examples](#Examples)
- [Support](#Support)
- [Contributing](#Contributing)

## Inputs

| input   | required | default | description          |
| ------- | -------- | ------- | -------------------- |
| token   | **Yes**  | -       | Cloudflare API Token |
| domains | **Yes**  | -       | Domain(s) to Purge   |

```yaml
- name: 'Purge Cache'
  uses: cssnr/cloudflare-purge-cache-action@master
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    domains: example.com
```

## Examples

```yaml
name: 'Test Purge Cache'

on:
  push:

jobs:
  test:
    name: 'Test'
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: 'Purge Cache'
        uses: cssnr/cloudflare-purge-cache-action@master
        with:
          token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          domains: |
            example.com
            test.example.com
```

# Support

For general help or to request a feature, see:

- Q&A Discussion: https://github.com/cssnr/portainer-stack-deploy-action/discussions/categories/q-a
- Request a Feature: https://github.com/cssnr/portainer-stack-deploy-action/discussions/categories/feature-requests

If you are experiencing an issue/bug or getting unexpected results, you can:

- Report an Issue: https://github.com/cssnr/portainer-stack-deploy-action/issues
- Chat with us on Discord: https://discord.gg/wXy6m2X8wY
- Provide General
  Feedback: [https://cssnr.github.io/feedback/](https://cssnr.github.io/feedback/?app=Portainer%20Stack%20Deploy)

# Contributing

Currently, the best way to contribute to this project is to star this project on GitHub.

Additionally, you can support other GitHub Actions I have published:

- [VirusTotal Action](https://github.com/cssnr/virustotal-action)
- [Update Version Tags Action](https://github.com/cssnr/update-version-tags-action)
- [Update JSON Value Action](https://github.com/cssnr/update-json-value-action)
- [Parse Issue Form Action](https://github.com/cssnr/parse-issue-form-action)
- [Mirror Repository Action](https://github.com/cssnr/mirror-repository-action)
- [Portainer Stack Deploy](https://github.com/cssnr/portainer-stack-deploy-action)
- [Mozilla Addon Update Action](https://github.com/cssnr/mozilla-addon-update-action)

For a full list of current projects to support visit: [https://cssnr.github.io/](https://cssnr.github.io/)
