import os
import re
import requests


print("🏳️ Starting Cloudflare Purge Cache Action")


# Inputs

input_token: str = os.environ["INPUT_TOKEN"]
input_domains: str = os.environ.get("INPUT_DOMAINS") or os.environ.get("INPUT_ZONE")
input_domains = input_domains.strip()
print(f"input_domains: \u001b[36;1m{repr(input_domains)}")
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
print(f"domains: \u001b[36;1m{domains}")
zones: list = get_zones()
# print(f'zones: {zones}')

success = []

print(f"⌛ Processing {len(domains)} Domain(s)")
for domain in domains:
    try:
        print(f"Purging: \u001b[36;1m{domain}")
        zone: dict = get_zone(zones, domain)
        if not zone:
            print(f"⚠️ \u001b[33;1mWarning: Zone Not Found: \u001b[36;1m{zone}")
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
        print(f"⛔️ Error Purging: \u001b[36;1m{domain}: \u001b[32;1m{error}")
        continue


# Results

if not success:
    raise ValueError("All Zone Cache Purges Failed!")

if len(success) == len(domains):
    print(f"✅ \u001b[32;1mSuccessfully Purged {len(domains)} Domains")
else:
    for domain in domains:
        if domain not in success:
            print(f"::warning::Failed to purge domain: {domain}")
    print(f"⚠️ \u001b[33;1mPurged Domains: \u001b[37;1m{len(success)}/{len(domains)}")
    print(f"\u001b[32;1mSuccessful domains: \u001b[36;1m{success}")
