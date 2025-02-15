import os
import re
import requests
from rich import print


print(":white_flag-emoji: Starting Cloudflare Purge Cache Action")


# Inputs

input_token = os.environ["INPUT_TOKEN"].strip()
# print(f"input_token: [b magenta]{input_token}")
input_domains = os.environ.get("INPUT_DOMAINS") or os.environ.get("INPUT_ZONE")
input_domains = input_domains.strip()
print(f"input_domains: [b magenta]{repr(input_domains)}")
if not input_domains:
    raise ValueError("No Domains Provided to Purge.")
input_dry_run = os.environ.get("INPUT_DRY_RUN", "").strip().lower()
print(f"input_dry_run: [b magenta]{input_dry_run}")

base_url = "https://api.cloudflare.com/client/v4/{0}"
headers = {"Authorization": f"Bearer {input_token}"}


# TODO: Split cloudflare class/functions into its own file


def get_zones(name: str = "") -> list:
    zones_url = base_url.format("zones")
    # print(f"get_zones: {zones_url}")
    params = {"per_page": 50, "page": 1}
    if name:
        print(f"zone filter: [b yellow]{name}")
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
print(f"domains: [b magenta]{domains}")

print(f":hourglass: Processing {len(domains)} Domain")

zones: list = get_zones(domains[0] if len(domains) == 1 else "")
# print(zones)

success = []
for domain in domains:
    try:
        print(f" Purging: [b magenta]{domain}")
        zone: dict = get_zone(zones, domain)
        if not zone:
            print(f" :warning: [b yellow]Warning: Zone Not Found: [b magenta]{domain}")
            continue
        # print(f'zone: {zone["id"]}')
        url: str = base_url.format(f"zones/{zone['id']}/purge_cache")
        # print(f"url: {url}")

        if input_dry_run in ["y", "yes", "true", "on"]:
            print(" [b yellow]Dry Run enabled, not purging...")
            success.append(domain)
            continue

        # Perform Purge
        r = requests.post(url, headers=headers, json={"purge_everything": True})
        # print(f"r.status_code: {r.status_code}")
        r.raise_for_status()
        # print(f"Cache Purged: {domain}")
        result = r.json()
        print(result)  # print as formatted string for non-pretty
        if result["success"]:
            success.append(domain)

    except Exception as error:
        print(f" :no_entry: Error Purging: [b magenta]{domain}: [b yellow]{error}")
        continue


# Results

if not success:
    print(f":no_entry: [b red]All {len(domains)} Cache Purges Failed!")
    raise ValueError("All Zone Cache Purges Failed!")

failed = []

if len(success) == len(domains):
    print(":white_check_mark: [b green]Successfully Purged All Domains")
else:
    for domain in domains:
        if domain not in success:
            failed.append(domain)
            print(f"::warning::Failed to purge domain: {domain}")
    print(f"[b green]Successful domains: [b magenta]{success}")
    print(f"[b red]Failed domains: [b magenta]{failed}")
    print(f":warning: [b yellow]Purged domains:[/] {len(success)}/{len(domains)}")
