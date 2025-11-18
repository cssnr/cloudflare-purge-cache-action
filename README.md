[![GitHub Tag Major](https://img.shields.io/github/v/tag/cssnr/cloudflare-purge-cache-action?sort=semver&filter=!v*.*&logo=git&logoColor=white&labelColor=585858&label=%20)](https://github.com/cssnr/cloudflare-purge-cache-action/tags)
[![GitHub Tag Minor](https://img.shields.io/github/v/tag/cssnr/cloudflare-purge-cache-action?sort=semver&filter=!v*.*.*&logo=git&logoColor=white&labelColor=585858&label=%20)](https://github.com/cssnr/cloudflare-purge-cache-action/releases)
[![GitHub Release Version](https://img.shields.io/github/v/release/cssnr/cloudflare-purge-cache-action?logo=git&logoColor=white&labelColor=585858&label=%20)](https://github.com/cssnr/cloudflare-purge-cache-action/releases/latest)
[![Action Run Using](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcssnr%2Fcloudflare-purge-cache-action%2Frefs%2Fheads%2Fmaster%2Faction.yaml&query=%24.runs.using&logo=githubactions&logoColor=white&label=runs)](https://github.com/cssnr/cloudflare-purge-cache-action/blob/master/action.yaml)
[![Image Size](https://badges.cssnr.com/ghcr/size/cssnr/cloudflare-purge-cache-action)](https://github.com/cssnr/cloudflare-purge-cache-action/pkgs/container/cloudflare-purge-cache-action)
[![Image Latest](https://badges.cssnr.com/ghcr/tags/cssnr/cloudflare-purge-cache-action/latest)](https://github.com/cssnr/cloudflare-purge-cache-action/pkgs/container/cloudflare-purge-cache-action)
[![YAML Version](https://badges.cssnr.com/yaml/https%3A%2F%2Fraw.githubusercontent.com%2Fcssnr%2Fcloudflare-purge-cache-action%2Frefs%2Fheads%2Fmaster%2Faction.yaml/%24.runs.image?split=:&index=2&label=action.yaml)](https://github.com/cssnr/cloudflare-purge-cache-action/blob/master/action.yaml#L65)
[![Workflow Release](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/release.yaml?logo=cachet&label=release)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/release.yaml)
[![Workflow Test](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/test.yaml?logo=cachet&label=test)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/test.yaml)
[![Workflow Lint](https://img.shields.io/github/actions/workflow/status/cssnr/cloudflare-purge-cache-action/lint.yaml?logo=cachet&label=lint)](https://github.com/cssnr/cloudflare-purge-cache-action/actions/workflows/lint.yaml)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/cssnr/cloudflare-purge-cache-action?logo=github&label=updated)](https://github.com/cssnr/cloudflare-purge-cache-action/pulse)
[![Codeberg Last Commit](https://img.shields.io/gitea/last-commit/cssnr/cloudflare-purge-cache-action/master?gitea_url=https%3A%2F%2Fcodeberg.org%2F&logo=codeberg&logoColor=white&label=updated)](https://codeberg.org/cssnr/cloudflare-purge-cache-action)
[![GitHub Repo Size](https://img.shields.io/github/repo-size/cssnr/cloudflare-purge-cache-action?logo=bookstack&logoColor=white&label=repo%20size)](https://github.com/cssnr/cloudflare-purge-cache-action?tab=readme-ov-file#readme)
[![GitHub Top Language](https://img.shields.io/github/languages/top/cssnr/cloudflare-purge-cache-action?logo=htmx)](https://github.com/cssnr/cloudflare-purge-cache-action)
[![GitHub Contributors](https://img.shields.io/github/contributors-anon/cssnr/cloudflare-purge-cache-action?logo=github)](https://github.com/cssnr/cloudflare-purge-cache-action/graphs/contributors)
[![GitHub Discussions](https://img.shields.io/github/discussions/cssnr/cloudflare-purge-cache-action?logo=github)](https://github.com/cssnr/cloudflare-purge-cache-action/discussions)
[![GitHub Forks](https://img.shields.io/github/forks/cssnr/cloudflare-purge-cache-action?style=flat&logo=github)](https://github.com/cssnr/cloudflare-purge-cache-action/forks)
[![GitHub Repo Stars](https://img.shields.io/github/stars/cssnr/cloudflare-purge-cache-action?style=flat&logo=github)](https://github.com/cssnr/cloudflare-purge-cache-action/stargazers)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&label=org%20stars)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-72a5f2?logo=kofi&label=support)](https://ko-fi.com/cssnr)

# Cloudflare Purge Cache Action

- [Inputs](#Inputs)
- [Outputs](#Outputs)
- [Examples](#Examples)
- [Tags](#Tags)
- [Support](#Support)
- [Contributing](#Contributing)

Purge Cloudflare cache for a zone or list of zones with optional filters including files, prefixes, tags, and hosts.

Loaded with [Options](#inputs) including job summary, fail mode, dry run, custom files prefix and [Outputs](#outputs).

```yaml
- name: 'Purge Cache Action'
  uses: cssnr/cloudflare-purge-cache-action@v2
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    zones: cssnr.com,example.com
```

For more details see: [action.yaml](action.yaml) and [src/main.py](src/main.py).

## Inputs

| Input     | Default    | Short&nbsp;Description&nbsp;of&nbsp;the&nbsp;Input&nbsp;Value |
| :-------- | :--------- | :------------------------------------------------------------ |
| **token** | _Required_ | Cloudflare API Token [⤵️](#token)                             |
| **zones** | _Required_ | Zone Names to Purge [⤵️](#zones)                              |
| files     | -          | Files to Purge [⤵️](#files)                                   |
| prefix    | -          | Prefix Prepended to `files` [⤵️](#prefix)                     |
| tags      | -          | Tags to Purge (Enterprise) [⤵️](#tagshostsprefixes)           |
| hosts     | -          | Hosts to Purge (Enterprise) [⤵️](#tagshostsprefixes)          |
| prefixes  | -          | Prefixes to Purge (Enterprise) [⤵️](#tagshostsprefixes)       |
| fail      | `all`      | Fail Mode: [`all`, `any`, `none`] [⤵️](#fail)                 |
| dry_run   | `false`    | Run Without Purging [⤵️](#dry_run)                            |
| summary   | `true`     | Add Summary to Job [⤵️](#summary)                             |

### token

You need a [Cloudflare Token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/) with the permission `Zone.Cache Purge`.

### zones

CSV or Newline Delimited list of zone names to purge.

<details><summary>View <b>CSV and Newline Delimited</b> Examples</summary>

---

CSV - Comma Seperated Value:

```yaml
zones: cssnr.com,example.com
```

Newline Delimited:

```yaml
zones: |
  cssnr.com
  example.com
```

---

</details>

### files

CSV or Newline Delimited list of files to purge.
This is limited to 30 files on the free plan and 500 for enterprise.
For more information view docs for purge by [file](https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-single-file/).

### prefix

If provided, the `prefix` will be prepended to all the `files`. Useful for generating full links from file paths.

### tags/hosts/prefixes

_Enterprise Only._ CSV or Newline Delimited list of `tags`, `hosts` or `prefixes` to purge.
For more information view docs for purge by [tags](https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-tags/), [hostname](https://developers.cloudflare.com/cache/how-to/purge-cache/purge-by-hostname/), [prefix](https://developers.cloudflare.com/cache/how-to/purge-cache/purge_by_prefix/).

### fail

When purging multiple domains, set when the action should fail.
Options are `all`, `any` or `none`. Default is `all`.

### dry_run

With this enabled it will only output the results and not purge any cache.

### summary

Write a Summary for the job. To disable this set to `false`.

<details><summary>👀 View Example Job Summary</summary>

---

⚠️ Only 1/2 Zones Purged!

⚠️ Dry Run! Remove or disable `dry_run` to purge cache.

<details><summary>Purge Results</summary><table><tr><th>🚽</th><th>Zone</th></tr><tr><td>✅</td><td>cssnr.com</td></tr><tr><td>⛔</td><td>example.com</td></tr></table></details>

<details><summary>Inputs</summary>

```yaml
zones: cssnr.com,example.com
files:
prefix:
tags:
hosts:
prefixes:
fail: all
summary: true
dry_run: true
```

</details>

---

</details>

&nbsp;

View the [Examples](#examples) to see more...

## Outputs

| Output  | Output&nbsp;Description |
| :------ | :---------------------- |
| success | Successful Zones, CSV   |
| failed  | Failed Zones, CSV       |

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

With minimal inputs, this will **purge everything**:

```yaml
- name: 'Purge Cache Action'
  uses: cssnr/cloudflare-purge-cache-action@v2
  with:
    token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    zones: cssnr.com,example.com
```

To limit what is purged, specify either `files`, `tags`, `hosts`, or `prefixes`.

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
    hosts: example.com, dev.example.com
    prefixes: |
      example.com
      example.com/foo
    fail: all
    summary: true
    dry_run: false
```

Workflow Example.

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

For more examples, you can check out other projects using this action:  
https://github.com/cssnr/cloudflare-purge-cache-action/network/dependents

## Tags

The following rolling [tags](https://github.com/cssnr/cloudflare-purge-cache-action/tags) are maintained.

| Version&nbsp;Tag                                                                                                                                                                                                                           | Rolling | Bugs | Feat. |   Name    |  Target  | Example  |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----: | :--: | :---: | :-------: | :------: | :------- |
| [![GitHub Tag Major](https://img.shields.io/github/v/tag/cssnr/cloudflare-purge-cache-action?sort=semver&filter=!v*.*&style=for-the-badge&label=%20&color=44cc10)](https://github.com/cssnr/cloudflare-purge-cache-action/releases/latest) |   ✅    |  ✅  |  ✅   | **Major** | `vN.x.x` | `vN`     |
| [![GitHub Tag Minor](https://img.shields.io/github/v/tag/cssnr/cloudflare-purge-cache-action?sort=semver&filter=!v*.*.*&style=for-the-badge&label=%20&color=blue)](https://github.com/cssnr/cloudflare-purge-cache-action/releases/latest) |   ✅    |  ✅  |  ❌   | **Minor** | `vN.N.x` | `vN.N`   |
| [![GitHub Release](https://img.shields.io/github/v/release/cssnr/cloudflare-purge-cache-action?style=for-the-badge&label=%20&color=red)](https://github.com/cssnr/cloudflare-purge-cache-action/releases/latest)                           |   ❌    |  ❌  |  ❌   | **Micro** | `vN.N.N` | `vN.N.N` |

You can view the release notes for each version on the [releases](https://github.com/cssnr/cloudflare-purge-cache-action/releases) page.

The **Major** tag is recommended. It is the most up-to-date and always backwards compatible.
Breaking changes would result in a **Major** version bump. At a minimum you should use a **Minor** tag.

# Support

For general help or to request a feature, see:

- Q&A Discussion: https://github.com/cssnr/cloudflare-purge-cache-action/discussions/categories/q-a
- Request a Feature: https://github.com/cssnr/cloudflare-purge-cache-action/discussions/categories/feature-requests

If you are experiencing an issue/bug or getting unexpected results, you can:

- Report an Issue: https://github.com/cssnr/cloudflare-purge-cache-action/issues
- Chat with us on Discord: https://discord.gg/wXy6m2X8wY
- Provide General Feedback: [https://cssnr.github.io/feedback/](https://cssnr.github.io/feedback/?app=Cloudflare%20Purge%20Cache%20Action)

For more information, see the CSSNR [SUPPORT.md](https://github.com/cssnr/.github/blob/master/.github/SUPPORT.md#support).

# Contributing

If you would like to submit a PR, please review the [CONTRIBUTING.md](#contributing-ov-file).

Please consider making a donation to support the development of this project
and [additional](https://cssnr.com/) open source projects.

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cssnr)

Additionally, you can support other [GitHub Actions](https://actions.cssnr.com/) I have published:

- [Stack Deploy Action](https://github.com/cssnr/stack-deploy-action?tab=readme-ov-file#readme)
- [Portainer Stack Deploy Action](https://github.com/cssnr/portainer-stack-deploy-action?tab=readme-ov-file#readme)
- [Docker Context Action](https://github.com/cssnr/docker-context-action?tab=readme-ov-file#readme)
- [Actions Up Action](https://github.com/cssnr/actions-up-action?tab=readme-ov-file#readme)
- [Zensical Action](https://github.com/cssnr/zensical-action?tab=readme-ov-file#readme)
- [VirusTotal Action](https://github.com/cssnr/virustotal-action?tab=readme-ov-file#readme)
- [Mirror Repository Action](https://github.com/cssnr/mirror-repository-action?tab=readme-ov-file#readme)
- [Update Version Tags Action](https://github.com/cssnr/update-version-tags-action?tab=readme-ov-file#readme)
- [Docker Tags Action](https://github.com/cssnr/docker-tags-action?tab=readme-ov-file#readme)
- [Update JSON Value Action](https://github.com/cssnr/update-json-value-action?tab=readme-ov-file#readme)
- [JSON Key Value Check Action](https://github.com/cssnr/json-key-value-check-action?tab=readme-ov-file#readme)
- [Parse Issue Form Action](https://github.com/cssnr/parse-issue-form-action?tab=readme-ov-file#readme)
- [Cloudflare Purge Cache Action](https://github.com/cssnr/cloudflare-purge-cache-action?tab=readme-ov-file#readme)
- [Mozilla Addon Update Action](https://github.com/cssnr/mozilla-addon-update-action?tab=readme-ov-file#readme)
- [Package Changelog Action](https://github.com/cssnr/package-changelog-action?tab=readme-ov-file#readme)
- [NPM Outdated Check Action](https://github.com/cssnr/npm-outdated-action?tab=readme-ov-file#readme)
- [Label Creator Action](https://github.com/cssnr/label-creator-action?tab=readme-ov-file#readme)
- [Algolia Crawler Action](https://github.com/cssnr/algolia-crawler-action?tab=readme-ov-file#readme)
- [Upload Release Action](https://github.com/cssnr/upload-release-action?tab=readme-ov-file#readme)
- [Check Build Action](https://github.com/cssnr/check-build-action?tab=readme-ov-file#readme)
- [Web Request Action](https://github.com/cssnr/web-request-action?tab=readme-ov-file#readme)
- [Get Commit Action](https://github.com/cssnr/get-commit-action?tab=readme-ov-file#readme)

<details><summary>❔ Unpublished Actions</summary>

These actions are not published on the Marketplace, but may be useful.

- [cssnr/create-files-action](https://github.com/cssnr/create-files-action?tab=readme-ov-file#readme) - Create various files from templates.
- [cssnr/draft-release-action](https://github.com/cssnr/draft-release-action?tab=readme-ov-file#readme) - Keep a draft release ready to publish.
- [cssnr/env-json-action](https://github.com/cssnr/env-json-action?tab=readme-ov-file#readme) - Convert env file to json or vice versa.
- [cssnr/push-artifacts-action](https://github.com/cssnr/push-artifacts-action?tab=readme-ov-file#readme) - Sync files to a remote host with rsync.
- [smashedr/update-release-notes-action](https://github.com/smashedr/update-release-notes-action?tab=readme-ov-file#readme) - Update release notes.
- [smashedr/combine-release-notes-action](https://github.com/smashedr/combine-release-notes-action?tab=readme-ov-file#readme) - Combine release notes.

---

</details>

<details><summary>📝 Template Actions</summary>

These are basic action templates that I use for creating new actions.

- [javascript-action](https://github.com/smashedr/javascript-action?tab=readme-ov-file#readme) - JavaScript
- [typescript-action](https://github.com/smashedr/typescript-action?tab=readme-ov-file#readme) - TypeScript
- [py-test-action](https://github.com/smashedr/py-test-action?tab=readme-ov-file#readme) - Dockerfile Python
- [test-action-uv](https://github.com/smashedr/test-action-uv?tab=readme-ov-file#readme) - Dockerfile Python UV
- [docker-test-action](https://github.com/smashedr/docker-test-action?tab=readme-ov-file#readme) - Docker Image Python

Note: The `docker-test-action` builds, runs and pushes images to [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

---

</details>

For a full list of current projects visit: [https://cssnr.github.io/](https://cssnr.github.io/)
