import os
import re
from pprint import pformat, pprint
from typing import Any, Dict, List, Optional

import requests


# version = open("version.txt").read().strip() if os.path.isfile("version.txt") else "Local Source"
# print(f"🏳️ Starting Cloudflare Purge Cache Action - {version}")

version = os.environ.get("GITHUB_ACTION_REF") or "Local Source"
if os.path.isfile("/src/version.txt"):
    with open("/src/version.txt", "r") as f:
        version = f.read().strip()
print(f"🏳️ Starting Cloudflare Purge Cache Action - {version}")

input_notice = 'You are using a deprecated input "{old}". Change this to input "{new}" before it is removed in v3.'

# Inputs

print("::group::Inputs")

input_token = os.environ["INPUT_TOKEN"].strip()
print(f"input_token: \033[36;1m{input_token}")

input_zones: str = (
    os.environ.get("INPUT_ZONES", "") or os.environ.get("INPUT_ZONE", "") or os.environ.get("INPUT_DOMAINS", "")
)
input_zones = input_zones.strip()
print(f"input_zones: \033[36;1m{repr(input_zones)}")
# TODO: These checks are only needed for backwards compatibility w/ INPUT_ZONE/INPUT_DOMAINS
if not input_zones:
    raise ValueError("No Zones Provided to Purge.")
if os.environ.get("INPUT_ZONE"):
    print(f"::notice::{input_notice.format(old='zone', new='zones')}")
if os.environ.get("INPUT_DOMAINS"):
    print(f"::notice::{input_notice.format(old='domains', new='zones')}")

input_files = os.environ.get("INPUT_FILES", "").strip()
print(f"input_files: \033[36;1m{repr(input_files)}")
input_prefix = os.environ.get("INPUT_PREFIX", "").strip()
print(f"input_prefix: \033[36;1m{input_prefix}")

input_tags = os.environ.get("INPUT_TAGS", "").strip()
print(f"input_tags: \033[36;1m{repr(input_tags)}")
input_hosts = os.environ.get("INPUT_HOSTS", "").strip()
print(f"input_hosts: \033[36;1m{repr(input_hosts)}")
input_prefixes = os.environ.get("INPUT_PREFIXES", "").strip()
print(f"input_prefixes: \033[36;1m{repr(input_prefixes)}")

input_fail = os.environ.get("INPUT_FAIL", "").strip().lower()
print(f"input_fail: \033[36;1m{input_fail}")
input_summary = os.environ.get("INPUT_SUMMARY", "").strip().lower()
print(f"input_summary: \033[36;1m{input_summary}")
input_dry_run = os.environ.get("INPUT_DRY_RUN", "").strip().lower()
print(f"input_dry_run: \033[36;1m{input_dry_run}")
if input_dry_run in ["y", "yes", "true", "on"]:
    print("::warning::Dry Run is enabled and no cache is being purged!")

print("::endgroup::")  # Inputs


# TODO: Split cloudflare class/functions into its own file

base_url = "https://api.cloudflare.com/client/v4/{0}"
headers = {"Authorization": f"Bearer {input_token}"}


def get_zones(zone_name: str = "") -> Optional[list]:
    zones_url = base_url.format("zones")
    # print(f"get_zones: {zones_url}")
    params: Dict[str, Any] = {"per_page": 50, "page": 1}
    if zone_name:
        print(f"\033[33;1mFiltering zones for: \033[0m{zone_name}")
        params["name"] = zone_name
    # print(f"params: {params}")
    zone_list = []
    while True:
        response = requests.get(zones_url, headers=headers, params=params)
        # print(f"response.status_code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        # print(f'result_info: {data["result_info"]}')
        # print(f'messages/errors: {data["messages"]} / {data["errors"]}')
        zone_list.extend(data["result"])
        if params["page"] < data["result_info"]["total_pages"]:
            params["page"] += 1
            continue
        return zone_list


def get_zone(zone_list: Optional[List[dict]], zone_name: str) -> Optional[dict]:
    if zone_list:
        for z in zone_list:
            if z["name"] == zone_name:
                return z
    return None


# Variables

zones: list = [x.strip() for x in re.split("[,|\n]", input_zones)]
total = len(zones)
print(f"Parsed {total} Zones \n  \033[35;1m{zones}")

purge_data: Dict[str, Any] = {}

if input_files:
    files: list = [f"{input_prefix}{x.strip()}" for x in re.split("[,|\n]", input_files)]
    files_count = len(files)
    print(f"::group::Parsed {files_count} Files")
    if input_prefix:
        print(f"Added prefix to files: {input_prefix}")
    pad = len(str(files_count))
    for i, file in enumerate(files, 1):
        print(f"{i:0{pad}d}: {file}")
    print("::endgroup::")  # File Paths
    purge_data = {"files": files}

if input_tags:
    tags: list = [x.strip() for x in re.split("[,|\n]", input_tags)]
    print(f"Parsed {len(tags)} Tags \n  \033[35;1m{tags}")
    purge_data = {"tags": tags}
if input_hosts:
    hosts: list = [x.strip() for x in re.split("[,|\n]", input_hosts)]
    print(f"Parsed {len(hosts)} Hosts \n  \033[35;1m{hosts}")
    purge_data = {"hosts": hosts}
if input_prefixes:
    prefixes: list = [x.strip() for x in re.split("[,|\n]", input_prefixes)]
    print(f"Parsed {len(prefixes)} Prefixes \n  \033[35;1m{prefixes}")
    purge_data = {"prefixes": prefixes}

if not purge_data:
    print("Purging Everything...")
    purge_data = {"purge_everything": True}

print("::group::Purge Data")
print(f"\033[35;1m{pformat(purge_data)}")
print("::endgroup::")  # Purge Data


# Action

# TODO: Allow also purging by zone ID
# if only 1 zone is provided, use a filter when getting zones
all_zones: Optional[list] = get_zones(zones[0] if total == 1 else "")
# print(all_zones)  # sensitive information


success: List[str] = []
results: Dict[str, Optional[Any]] = dict.fromkeys(zones)

for name in zones:
    try:
        print(f"⌛ Processing: \033[36;1m{name}")
        zone: Optional[dict] = get_zone(all_zones, name)
        # print(f"zone: {zone}")  # sensitive information
        if not zone:
            # print(f"\033[33;1mZone Not Found: \033[0m{zone}")
            print("\033[33;1m  Zone Not Found")
            continue

        if input_dry_run in ["y", "yes", "true", "on"]:
            # print(f"\033[34;1mDry Run Enabled: \033[0m{zone}")
            print("\033[34;1m  Dry Run Enabled")
            success.append(name)
            continue

        # Perform Purge
        url: str = base_url.format(f"zones/{zone['id']}/purge_cache")
        r = requests.post(url, headers=headers, json=purge_data)
        # print(f"r.status_code: {r.status_code}")
        r.raise_for_status()
        # print(f"Cache Purged: {zone}")
        result = r.json()
        results[name] = result
        if result["success"]:
            success.append(name)
            print("\033[32;1m  Purge Successful")
        else:
            print("\033[31;1m  Purge Failed")
            print("  " + result)

    except Exception as error:
        # print(f"⛔ Error: \033[31m{error}")
        print("\033[31;1m  Error Purging")
        print("  " + str(error))
        results[name] = error
        continue


# Results

failed: List[str] = []
results_table = ["<table><tr><th>🚽</th><th>Zone</th></tr>"]
for name in zones:
    if name not in success:
        results_table.append(f"<tr><td>⛔</td><td>{name}</td></tr>")
        failed.append(name)
        print(f"::error::Failed to purge zone: {name}")
    else:
        results_table.append(f"<tr><td>✅</td><td>{name}</td></tr>")
results_table.append("</table>")

print("::group::Results")
# print(f"results_table: {results_table}")
# print(f"success: \033[32;1m{success}")
# print(f"failed: \033[31;1m{failed}")
# pprint(results)
for zone, result in results.items():  # type: ignore
    if zone in success:
        print(f"\033[32;1m{zone}")
    else:
        print(f"\033[31;1m{zone}")
    pprint(result)
print("::endgroup::")


# Outputs

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    # noinspection PyTypeChecker
    print(f"success={','.join(success)}", file=f)
    # noinspection PyTypeChecker
    print(f"failed={','.join(failed)}", file=f)


# Summary

if input_summary in ["y", "yes", "true", "on"]:
    print("📝 Writing Job Summary")
    inputs_table = ["<table><tr><th>Input</th><th>Value</th></tr>"]
    for x in ["zones", "files", "prefix", "fail", "summary", "dry_run"]:
        value = globals()[f"input_{x}"]
        inputs_table.append(f"<tr><td>{x}</td><td>{value or '-'}</td></tr>")
    inputs_table.append("</table>")
    # print(f"inputs_table: {inputs_table}")

    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        # noinspection PyTypeChecker
        print("## Cloudflare Purge Cache Action", file=f)
        if len(success) == total:
            # noinspection PyTypeChecker
            print(f"✅ All {total} Zones(s) were Successfully Purged.", file=f)
        elif not success:
            # noinspection PyTypeChecker
            print(f"⛔ All {total} Zones(s) Failed to Purge!", file=f)
        else:
            # noinspection PyTypeChecker
            print(f"⚠️ Only {len(failed)}/{total} Zones Purged!", file=f)
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


# Finish

if input_dry_run in ["y", "yes", "true", "on"]:
    print("\033[33mThis was a Dry Run! Remove or disable `dry_run` to purge cache.")

if len(success) == total:
    print("✅ \033[32;1mSuccessfully Purged All Zones")
elif not success:
    print(f"⛔ \033[31;1mAll {total} Cache Purges Failed")
    if input_fail in ["all", "any"]:
        raise ValueError(f"All {total} Cache Purges Failed!")
else:
    print(f"Successful zones: \033[32;1m{success}")
    print(f"Failed zones: \033[31;1m{failed}")
    print(f"⚠️ \033[33;1mPurged Zones: {len(success)}/{total}")
    if input_fail in ["any"]:
        raise ValueError(f"Only Purged {len(success)}/{total} Zones!")
