[![Release](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/release.yaml?logo=github&logoColor=white&label=release)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/release.yaml)
[![Test](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/test.yaml?logo=github&logoColor=white&label=test)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/test.yaml)
[![Lint](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/lint.yaml?logo=github&logoColor=white&label=lint)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/lint.yaml)
[![GitHub Release Version](https://img.shields.io/github/v/release/cssnr/cloudflare-purge-cache-action?logo=github)](https://github.com/cssnr/cloudflare-purge-cache-action/releases/latest)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/cssnr/cloudflare-purge-cache-action?logo=github&logoColor=white&label=updated)](https://github.com/cssnr/cloudflare-purge-cache-action/graphs/commit-activity)
[![Codeberg Last Commit](https://img.shields.io/gitea/last-commit/cssnr/cloudflare-purge-cache-action/master?gitea_url=https%3A%2F%2Fcodeberg.org%2F&logo=codeberg&logoColor=white&label=updated)](https://codeberg.org/cssnr/cloudflare-purge-cache-action)
[![GitHub Top Language](https://img.shields.io/github/languages/top/cssnr/cloudflare-purge-cache-action?logo=htmx&logoColor=white)](https://github.com/cssnr/cloudflare-purge-cache-action)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&logoColor=white)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)

# Cloudflare Purge Cache Action

- [Inputs](#Inputs)
- [Outputs](#Outputs)
- [Examples](#Examples)
- [Support](#Support)
- [Contributing](#Contributing)

Purge Cloudflare cache for a zone or list of zones with optional file/url filter.

For more details see: [action.yml](action.yml) and [src/main.py](src/main.py).

## Inputs

| input    | required | default | description                            |
| -------- | :------: | ------- | -------------------------------------- |
| token    | **Yes**  | -       | Cloudflare API Token                   |
| zones    | **Yes**  | -       | Zones(s) to Purge \*                   |
| files    |    -     | -       | Files to Purge \*                      |
| prefix   |    -     | -       | File Prefix to Add \*                  |
| tags     |    -     | -       | Tags to Purge (Enterprise only) \*     |
| hosts    |    -     | -       | Hosts to Purge (Enterprise only) \*    |
| prefixes |    -     | -       | Prefixes to Purge (Enterprise only) \* |
| fail     |    -     | `all`   | Fail Mode: [`all`, `any`, `none`]      |
| summary  |    -     | `true`  | Add Summary to Job \*                  |
| dry_run  |    -     | `false` | Run Without Purging                    |

**zones** - CSV or Newline Delimited list of zones to purge.

**files** - CSV or Newline Delimited list of files to purge.
This is limited to 30 files on the free plan and 500 for enterprise.
For more information view docs for purge by
[file](https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-single-file/)

**prefix** - If provided, the `prefix` will be prepended to all the files.

**tags/hosts/prefixes** - CSV or Newline Delimited list of tags/hosts/prefixes to purge.
For more information view docs for purge by
[tags](https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-tags/#purge-cache-by-cache-tags-enterprise-only),
[hostname](https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-hostname/),
[prefix](https://developers.cloudflare.com/cache/how-to/purge-cache/purge_by_prefix/).

**summary** - Write a Summary for the job. To disable this set to `false`.

<details><summary>👀 View Example Job Summary</summary>

---

⚠️ Only 1/2 Zones Purged!

⚠️ Dry Run! Remove or disable `dry_run` to purge cache.

<details><summary>Purge Results</summary><table><tr><th>🚽</th><th>Zone</th></tr><tr><td>✅</td><td>cssnr.com</td></tr><tr><td>⛔</td><td>example.com</td></tr></table></details>

<details><summary>Inputs</summary><table><tr><th>Input</th><th>Value</th></tr><tr><td>zones</td><td>cssnr.com,example.com</td></tr><tr><td>files</td><td>-</td></tr><tr><td>prefix</td><td>-</td></tr><tr><td>fail</td><td>all</td></tr><tr><td>summary</td><td>true</td></tr><tr><td>dry_run</td><td>true</td></tr></table></details>

---

</details>

To see a workflow run you can view a recent
[test.yaml run](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/test.yaml) _(requires login)_.

With required inputs:

```yaml
- name: 'Purge Cache Action'
  uses: cssnr/cloudflare-purge-cache-action@v2
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    zones: cssnr.com,example.com
```

With all inputs:

```yaml
- name: 'Purge Cache Action'
  uses: cssnr/cloudflare-purge-cache-action@v2
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    zones: cssnr.com
    files: |
      favicon.ico
      static/logo.png
    prefix: 'https://cssnr.com/'
    tags: prod, dev
    prefixes: |
      example.com
      example.com/foo
    hosts: example.com, dev.example.com
    fail: all
    summary: true
    dry_run: false
```

## Outputs

| output  | description           |
| ------- | --------------------- |
| success | Successful Zones, CSV |
| failed  | Failed Zones, CSV     |

```yaml
- name: 'Purge Cache Action'
  id: purge
  uses: cssnr/cloudflare-purge-cache-action@v2
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    zones: cssnr.com,example.com

- name: 'Echo Output'
  run: |
    echo "success: '${{ steps.purge.outputs.success }}'"
    echo "failed: '${{ steps.purge.outputs.failed }}'"
```

## Examples

```yaml
name: 'Cloudflare Purge Cache'

on:
  push:

jobs:
  test:
    name: 'Test'
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: 'Purge Cache Action'
        uses: cssnr/cloudflare-purge-cache-action@v2
        with:
          token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          zones: |
            cssnr.com
            example.com
```

# Support

For general help or to request a feature, see:

- Q&A Discussion: https://github.com/cssnr/cloudflare-purge-cache-action/discussions/categories/q-a
- Request a Feature: https://github.com/cssnr/cloudflare-purge-cache-action/discussions/categories/feature-requests

If you are experiencing an issue/bug or getting unexpected results, you can:

- Report an Issue: https://github.com/cssnr/cloudflare-purge-cache-action/issues
- Chat with us on Discord: https://discord.gg/wXy6m2X8wY
- Provide General Feedback: [https://cssnr.github.io/feedback/](https://cssnr.github.io/feedback/?app=Cloudflare%20Purge%20Cache%20Action)

# Contributing

Currently, the best way to contribute to this project is to star this project on GitHub.

If you would like to submit a PR, please review the [CONTRIBUTING.md](CONTRIBUTING.md).

Additionally, you can support other GitHub Actions I have published:

- [Stack Deploy Action](https://github.com/cssnr/stack-deploy-action?tab=readme-ov-file#readme)
- [Portainer Stack Deploy](https://github.com/cssnr/portainer-stack-deploy-action?tab=readme-ov-file#readme)
- [VirusTotal Action](https://github.com/cssnr/virustotal-action?tab=readme-ov-file#readme)
- [Mirror Repository Action](https://github.com/cssnr/mirror-repository-action?tab=readme-ov-file#readme)
- [Update Version Tags Action](https://github.com/cssnr/update-version-tags-action?tab=readme-ov-file#readme)
- [Update JSON Value Action](https://github.com/cssnr/update-json-value-action?tab=readme-ov-file#readme)
- [Parse Issue Form Action](https://github.com/cssnr/parse-issue-form-action?tab=readme-ov-file#readme)
- [Cloudflare Purge Cache Action](https://github.com/cssnr/cloudflare-purge-cache-action?tab=readme-ov-file#readme)
- [Mozilla Addon Update Action](https://github.com/cssnr/mozilla-addon-update-action?tab=readme-ov-file#readme)
- [Docker Tags Action](https://github.com/cssnr/docker-tags-action?tab=readme-ov-file#readme)

For a full list of current projects to support visit: [https://cssnr.github.io/](https://cssnr.github.io/)
