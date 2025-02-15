import os
import re
import requests
import text_formatting as tf


print("🏳️ Starting Cloudflare Purge Cache Action")


# Inputs

input_token: str = os.environ["INPUT_TOKEN"]
input_domains: str = os.environ.get("INPUT_DOMAINS") or os.environ.get("INPUT_ZONE")
input_domains = input_domains.strip()
print(f"input_domains: {tf.purple}{repr(input_domains)}")
if not input_domains:
    raise ValueError("No Domains Provided to Purge.")

base_url = "https://api.cloudflare.com/client/v4/{0}"
headers = {"Authorization": f"Bearer {input_token}"}


# TODO: Split cloudflare class/functions into its own file
# TODO: If only 1 domain is provided use this function vs get_zones
# def get_zones_single(zone_name: str) -> list:
#     zones_url = base_url.format("zones")
#     print(f"zones_url: {zones_url}")
#     params = {"name": zone_name}
#     response = requests.get(zones_url, headers=headers, params=params)
#     print(response.status_code)
#     response.raise_for_status()
#     data = response.json()
#     print(f"data: {data}")
#     if not data["result"]:
#         raise ValueError(f"No zones returned for name: {zones_url}")
#     return data["result"]


def get_zones() -> list:
    zones_url = base_url.format("zones")
    # print(f"get_zones: {zones_url}")
    page = 1
    results = []
    while True:
        # print(f"page: {page}")
        params = {"per_page": 50, "page:": page}
        response = requests.get(zones_url, headers=headers, params=params)
        # print(f"response.status_code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        # print(f'result_info: {data["result_info"]}')
        # print(f'messages/errors: {data["messages"]} / {data["errors"]}')
        results.extend(data["result"])
        if page < data["result_info"]["total_pages"]:
            page += 1
            continue
        return results


def get_zone(all_zones: list, zone_name: str) -> dict:
    for z in all_zones:
        if z["name"] == zone_name:
            return z


# Action

domains: list = [x.strip() for x in re.split("[,|\n]", input_domains)]
print(f"domains: {tf.cyan}{domains}")
zones: list = get_zones()
# print(f'zones: {zones}')

success = []

print(f"⌛ Processing {len(domains)} Domain(s)")
for domain in domains:
    try:
        print(f"Purging: {tf.cyan}{domain}")
        zone: dict = get_zone(zones, domain)
        if not zone:
            print(f"⚠️ {tf.yellow}Warning: Zone Not Found: {tf.cyan}{domain}")
            continue
        # print(f'zone: {zone["id"]}')
        url: str = base_url.format(f"zones/{zone['id']}/purge_cache")
        # print(f"url: {url}")

        # Perform Purge
        r = requests.post(url, headers=headers, json={"purge_everything": True})
        # print(f"r.status_code: {r.status_code}")
        r.raise_for_status()
        # print(f"Cache Purged: {domain}")
        result = r.json()
        print(f"Result: {result}")
        if result["success"]:
            success.append(domain)

    except Exception as error:
        print(f"⛔️ Error Purging: {tf.cyan}{domain}: {tf.yellow}{error}")
        continue


# Results

if not success:
    print(f"⛔️ {tf.red}All {len(domains)} Cache Purges Failed!")
    raise ValueError("All Zone Cache Purges Failed!")

failed = []

if len(success) == len(domains):
    print(f"✅ {tf.green}Successfully Purged All {len(domains)} domains")
else:
    for domain in domains:
        if domain not in success:
            failed.append(domain)
            print(f"::warning::Failed to purge domain: {domain}")
    print(f"⚠️ {tf.yellow}Purged domains: {tf.rst}{len(success)}/{len(domains)}")
    print(f"{tf.green}Successful domains: {tf.cyan}{success}")
    print(f"{tf.red}Failed domains: {tf.cyan}{failed}")
