[![Tags](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/tags.yaml?logo=github&logoColor=white&label=tags)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/tags.yaml)
[![Test](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/test.yaml?logo=github&logoColor=white&label=test)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/test.yaml)
[![GitHub Release Version](https://img.shields.io/github/v/release/cssnr/cloudflare-purge-cache-action?logo=github)](https://github.com/cssnr/cloudflare-purge-cache-action/releases/latest)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/cssnr/cloudflare-purge-cache-action?logo=github&logoColor=white&label=updated)](https://github.com/cssnr/cloudflare-purge-cache-action/graphs/commit-activity)
[![Codeberg Last Commit](https://img.shields.io/gitea/last-commit/cssnr/cloudflare-purge-cache-action/master?gitea_url=https%3A%2F%2Fcodeberg.org%2F&logo=codeberg&logoColor=white&label=updated)](https://codeberg.org/cssnr/cloudflare-purge-cache-action)
[![GitHub Top Language](https://img.shields.io/github/languages/top/cssnr/cloudflare-purge-cache-action?logo=htmx&logoColor=white)](https://github.com/cssnr/cloudflare-purge-cache-action)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&logoColor=white)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)

# Cloudflare Purge Cache Action

Purge Cloudflare cache for a domain or list of domains with optional file/url filter.

For more details see: [action.yml](action.yml) and [src/main.py](src/main.py).

- [Inputs](#Inputs)
- [Outputs](#Outputs)
- [Examples](#Examples)
- [Support](#Support)
- [Contributing](#Contributing)

## Inputs

| input   | required | default | description                 |
| ------- | -------- | ------- | --------------------------- |
| token   | **Yes**  | -       | Cloudflare API Token        |
| domains | **Yes**  | -       | Domain(s) to Purge \*       |
| files   | No       | -       | Files to Purge \*           |
| prefix  | No       | -       | File Prefix to Add \*       |
| fail    | No       | all     | Fail Mode: [all, any, none] |
| summary | No       | true    | Add Summary to Job          |
| dry_run | No       | false   | Run Without Purging         |

**domains** - CSV or Newline Delimited list of zones to purge.

**files** - CSV or Newline Delimited list of files to purge.
This is applied to all `domains` and is limited to 30 files on the free plan and 500 for enterprise.

**prefix** - If provided, the `prefix` will be prepended to all the files. See
the [Cloudflare Purge by single-file](https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-single-file/)
documentation for more information.

With required inputs:

```yaml
- name: 'Purge Cache'
  uses: cssnr/cloudflare-purge-cache-action@v2
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    domains: cssnr.com,example.com
```

With all inputs:

```yaml
- name: 'Purge Cache'
  uses: cssnr/cloudflare-purge-cache-action@v2
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    domains: cssnr.com
    files: |
      favicon.ico
      static/logo.png
    prefix: 'https://cssnr.com/'
    fail: all
    summary: true
    dry_run: false
```

## Outputs

| output  | description             |
| ------- | ----------------------- |
| success | Successful Domains, CSV |
| failed  | Failed Domains, CSV     |

```yaml
- name: 'Purge Cache'
  id: purge
  uses: cssnr/cloudflare-purge-cache-action@v2
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    domains: cssnr.com,example.com

- name: 'Echo Output'
  run: |
    echo "success: '${{ steps.purge.outputs.success }}'"
    echo "failed: '${{ steps.purge.outputs.failed }}'"
```

## Examples

```yaml
name: 'Test Job'

on:
  push:

jobs:
  test:
    name: 'Test'
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: 'Purge Cache'
        uses: cssnr/cloudflare-purge-cache-action@v2
        with:
          token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          domains: |
            cssnr.com
            example.com
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
- [Stack Deploy Action](https://github.com/cssnr/stack-deploy-action)
- [Portainer Stack Deploy](https://github.com/cssnr/portainer-stack-deploy-action)
- [Mozilla Addon Update Action](https://github.com/cssnr/mozilla-addon-update-action)

For a full list of current projects to support visit: [https://cssnr.github.io/](https://cssnr.github.io/)

If you would like to submit a PR, please review the [CONTRIBUTING.md](CONTRIBUTING.md).
