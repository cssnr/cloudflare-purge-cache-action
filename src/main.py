import os
import re
import requests
from tomlkit import table

print("🏳️ Starting Cloudflare Purge Cache Action")


# Inputs

input_token = os.environ["INPUT_TOKEN"].strip()
# print(f"input_token: \033[35;1m{input_token}")
input_domains = os.environ.get("INPUT_DOMAINS") or os.environ.get("INPUT_ZONE")
input_domains = input_domains.strip()
print(f"input_domains: \033[35;1m{repr(input_domains)}")
if not input_domains:
    # TODO: This check is only needed for backwards compatibility
    raise ValueError("No Domains Provided to Purge.")
input_summary = os.environ.get("INPUT_SUMMARY", "").strip()
print(f"input_summary: \033[35;1m{input_summary}")
input_dry_run = os.environ.get("INPUT_DRY_RUN", "").strip().lower()
print(f"input_dry_run: \033[35;1m{input_dry_run}")

base_url = "https://api.cloudflare.com/client/v4/{0}"
headers = {"Authorization": f"Bearer {input_token}"}


# TODO: Split cloudflare class/functions into its own file


def get_zones(name: str = "") -> list:
    zones_url = base_url.format("zones")
    # print(f"get_zones: {zones_url}")
    params = {"per_page": 50, "page": 1}
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


def get_zone(all_zones: list, zone_name: str) -> dict:
    for z in all_zones:
        if z["name"] == zone_name:
            return z


# Action

domains: list = [x.strip() for x in re.split("[,|\n]", input_domains)]
print(f"domains: \033[36;1m{domains}")

zones: list = get_zones(domains[0] if len(domains) == 1 else "")
# print(zones)

print(f"⌛ Processing {len(domains)} Domain(s)")

success = []
for domain in domains:
    try:
        print(f"-- \033[36;1m{domain}")
        zone: dict = get_zone(zones, domain)
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
        r = requests.post(url, headers=headers, json={"purge_everything": True})
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

results = ["<table><tr><th>🚽</th><th>Zone</th></tr>"]
failed = []
for domain in domains:
    if domain not in success:
        results.append(f"<tr><td>⛔</td><td>{domain}</td></tr>")
        failed.append(domain)
        print(f"::warning::Failed to purge domain: {domain}")
    else:
        results.append(f"<tr><td>✅</td><td>{domain}</td></tr>")
results.append("</table>")

print(f"success: \033[32;1m{success}")
print(f"failed: \033[31;1m{failed}")


# Outputs

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    print(f"success={','.join(success)}", file=f)
    print(f"failed={','.join(failed)}", file=f)


# Summary

if input_summary in ["y", "yes", "true", "on"]:
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        print("### Cloudflare Purge Cache Action", file=f)
        print(
            f"✅ Success: {len(success) or 'None'}  \n⛔ Failed: {len(failed) or 'None'}",
            file=f,
        )
        print(f"<details><summary>Results</summary>{results}", file=f)
        print(
            f"<details><summary>Inputs</summary><table><tr><th>Input</th><th>Value</th></tr><tr><td>domains</td><td>{input_domains}</td></tr><tr><td>summary</td><td>{input_summary}</td></tr><tr><td>dry_run</td><td>{input_dry_run}</td></tr></table></details>\n",  # noqa: E501
            file=f,
        )
        print(
            "[Report an issue or request a feature](https://github.com/cssnr/cloudflare-purge-cache-action/issues)",
            file=f,
        )


if not success:
    print(f"⛔ \033[31;1mAll {len(domains)} Cache Purges Failed!")
    raise ValueError(f"All {len(domains)} Zone Cache Purges Failed!")

if len(success) == len(domains):
    print("✅ \033[32;1mSuccessfully Purged All Domains Cache")
else:
    print(f"Successful domains: \033[32;1m{success}")
    print(f"Failed domains: \033[31;1m{failed}")
    print(f"⚠️ \033[33;1mPurged Domains: {len(success)}/{len(domains)}")
