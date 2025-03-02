import os
import re
from typing import Any, Dict, List, Optional

import requests


version = open("version.txt").read().strip() if os.path.isfile("version.txt") else "Dev Build"
print(f"🏳️ Starting Cloudflare Purge Cache Action - {version}")


# Inputs

input_token = os.environ["INPUT_TOKEN"].strip()
# print(f"input_token: \033[35;1m{input_token}")
input_domains: str = os.environ.get("INPUT_DOMAINS", "") or os.environ.get("INPUT_ZONE", "")
input_domains = input_domains.strip()
print(f"input_domains: \033[35;1m{repr(input_domains)}")
# TODO: These checks are only needed for backwards compatibility w/ INPUT_ZONE
if not input_domains:
    raise ValueError("No Domains Provided to Purge.")
if os.environ.get("INPUT_ZONE"):
    print("::notice::Notice: You are using a deprecated input 'zone'. Please change this to 'domains' ASAP!")

input_files = os.environ.get("INPUT_FILES", "").strip()
print(f"input_files: \033[35;1m{repr(input_files)}")
input_prefix = os.environ.get("INPUT_PREFIX", "").strip()
print(f"input_prefix: \033[35;1m{input_prefix}")

input_fail = os.environ.get("INPUT_FAIL", "").strip().lower()
print(f"input_fail: \033[35;1m{input_fail}")

input_summary = os.environ.get("INPUT_SUMMARY", "").strip().lower()
print(f"input_summary: \033[35;1m{input_summary}")
input_dry_run = os.environ.get("INPUT_DRY_RUN", "").strip().lower()
print(f"input_dry_run: \033[35;1m{input_dry_run}")
if input_dry_run in ["y", "yes", "true", "on"]:
    print("::notice::Notice: Dry Run is enabled and no cache is being purged!")

base_url = "https://api.cloudflare.com/client/v4/{0}"
headers = {"Authorization": f"Bearer {input_token}"}


# TODO: Split cloudflare class/functions into its own file


def get_zones(name: str = "") -> Optional[list]:
    zones_url = base_url.format("zones")
    # print(f"get_zones: {zones_url}")
    params: Dict[str, Any] = {"per_page": 50, "page": 1}
    if name:
        print(f"using filter: \033[33;1m{name}")
        params["name"] = name
    # print(f"params: {params}")
    results = []
    while True:
        response = requests.get(zones_url, headers=headers, params=params)
        # print(f"response.status_code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        # print(f'result_info: {data["result_info"]}')
        # print(f'messages/errors: {data["messages"]} / {data["errors"]}')
        results.extend(data["result"])
        if params["page"] < data["result_info"]["total_pages"]:
            params["page"] += 1
            continue
        return results


def get_zone(all_zones: Optional[List[dict]], zone_name: str) -> Optional[dict]:
    if all_zones:
        for z in all_zones:
            if z["name"] == zone_name:
                return z
    return None


# Action

domains: list = [x.strip() for x in re.split("[,|\n]", input_domains)]
print(f"domains: \033[36;1m{domains}")

purge_data: Dict[str, Any]

if input_files:
    files: list = [f"{input_prefix}{x.strip()}" for x in re.split("[,|\n]", input_files)]
    # print(f"files: \033[36;1m{files}")
    purge_data = {"files": files}
else:
    purge_data = {"purge_everything": True}
# print(f"purge_data: {purge_data}")

zones: Optional[list] = get_zones(domains[0] if len(domains) == 1 else "")
# print(zones)

print(f"⌛ Processing {len(domains)} Domain(s)")

success = []
for domain in domains:
    try:
        print(f"-- \033[36;1m{domain}")
        zone: Optional[dict] = get_zone(zones, domain)
        if not zone:
            print("\033[33;1mZone Not Found!")
            continue
        # print(f'zone: {zone["id"]}')
        url: str = base_url.format(f"zones/{zone['id']}/purge_cache")
        # print(f"url: {url}")

        if input_dry_run in ["y", "yes", "true", "on"]:
            print("\033[34;1mDry Run Enabled.")
            success.append(domain)
            continue

        # Perform Purge
        r = requests.post(url, headers=headers, json=purge_data)
        # print(f"r.status_code: {r.status_code}")
        r.raise_for_status()
        # print(f"Cache Purged: {domain}")
        result = r.json()
        print(result)
        if result["success"]:
            success.append(domain)

    except Exception as error:
        print(f"\033[31;1mError Purging: \033[31m{error}")
        continue


# Results

results_table = ["<table><tr><th>🚽</th><th>Zone</th></tr>"]
failed = []
for domain in domains:
    if domain not in success:
        results_table.append(f"<tr><td>⛔</td><td>{domain}</td></tr>")
        failed.append(domain)
        print(f"::warning::Failed to purge domain: {domain}")
    else:
        results_table.append(f"<tr><td>✅</td><td>{domain}</td></tr>")
results_table.append("</table>")
# print(f"results_table: {results_table}")

# print(f"success: \033[32;1m{success}")
# print(f"failed: \033[31;1m{failed}")


# Outputs

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    # noinspection PyTypeChecker
    print(f"success={','.join(success)}", file=f)
    # noinspection PyTypeChecker
    print(f"failed={','.join(failed)}", file=f)


# Summary
# TODO: Collect errors and add to Summary

if input_summary in ["y", "yes", "true", "on"]:
    inputs_table = ["<table><tr><th>Input</th><th>Value</th></tr>"]
    for x in ["domains", "files", "prefix", "fail", "summary", "dry_run"]:
        value = globals()[f"input_{x}"]
        inputs_table.append(f"<tr><td>{x}</td><td>{value or '-'}</td></tr>")
    inputs_table.append("</table>")
    # print(f"inputs_table: {inputs_table}")

    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        # noinspection PyTypeChecker
        print("## Cloudflare Purge Cache Action", file=f)
        if len(success) == len(domains):
            # noinspection PyTypeChecker
            print(f"✅ All {len(domains)} Domain(s) were Successfully Purged.", file=f)
        elif not success:
            # noinspection PyTypeChecker
            print(f"⛔ All {len(domains)} Domain(s) Failed to Purge!", file=f)
        else:
            # noinspection PyTypeChecker
            print(f"⚠️ Only {len(failed)}/{len(domains)} Domains Purged!", file=f)
        if input_dry_run in ["y", "yes", "true", "on"]:
            # noinspection PyTypeChecker
            print("\n⚠️ Dry Run! Remove or disable `dry_run` to purge cache.", file=f)
        # noinspection PyTypeChecker
        print(f"<details><summary>Purge Results</summary>{''.join(results_table)}</details>\n", file=f)
        # noinspection PyTypeChecker
        print(f"<details><summary>Inputs</summary>{''.join(inputs_table)}</details>\n", file=f)
        url = "https://github.com/cssnr/cloudflare-purge-cache-action"
        # noinspection PyTypeChecker
        print(f"[Report an issue or request a feature]({url}?tab=readme-ov-file#readme)\n\n---", file=f)


if len(success) == len(domains):
    print("✅ \033[32;1mSuccessfully Purged All Domains")
elif not success:
    print(f"⛔ \033[31;1mAll {len(domains)} Cache Purges Failed")
    if input_fail in ["all", "any"]:
        raise ValueError(f"All {len(domains)} Cache Purges Failed!")
else:
    print(f"Successful domains: \033[32;1m{success}")
    print(f"Failed domains: \033[31;1m{failed}")
    print(f"⚠️ \033[33;1mPurged Domains: {len(success)}/{len(domains)}")
    if input_fail in ["any"]:
        raise ValueError(f"Only Purged {len(success)}/{len(domains)} Domains!")
