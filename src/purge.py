import os
import requests

input_token = os.environ['INPUT_TOKEN']
input_domains = os.environ['INPUT_DOMAINS'] or os.environ['INPUT_ZONE']

base_url = 'https://api.cloudflare.com/client/v4/{0}'
headers = {"Authorization": f"Bearer {input_token}"}


# TODO: If only 1 domain is provided, use a `match` param filter that domain
# def get_zones() -> list:
#     url = base_url.format('zones')
#     print(url)
#     r = requests.get(url, headers=headers, params={'per_page': 50})
#     print(r.status_code)
#     r.raise_for_status()
#     return r.json()['result']

def get_zones() -> list:
    zones_url = base_url.format('zones')
    print(f'zones_url: {zones_url}')
    page = 1
    results = []
    while True:
        print(f'Processing Page: {page}')
        params = {'per_page': 50, 'page:': page}
        response = requests.get(zones_url, headers=headers, params=params)
        print(response.status_code)
        response.raise_for_status()
        data = response.json()
        print(f'result_info: {data["result_info"]}')
        print(f'messages/errors: {data["messages"]} / {data["errors"]}')
        results.extend(data['result'])
        if page < data['result_info']['total_pages']:
            page += 1
            continue
        return results


def get_zone(all_zones: list, zone_name: str) -> dict:
    for z in all_zones:
        if z['name'] == zone_name:
            return z


print('Starting Cloudflare Purge Cache Action')
domains: list = [x.strip() for x in input_domains.split()]
print(f'domains: {domains}')
zones: list = get_zones()
# print(f'zones: {zones}')

success = []

for domain in domains:
    try:
        print(f'Processing Domain: {domain}')
        zone: dict = get_zone(zones, domain)
        if not zone:
            print(f'Warning: Zone Not Found: {zone}')
            continue
        print(f'zone: {zone["id"]}')
        url = base_url.format(f"zones/{zone['id']}/purge_cache")
        print(f'url: {url}')
        r = requests.post(url, headers=headers, json={'purge_everything': True})
        print(f'r.status_code: {r.status_code}')
        r.raise_for_status()
        print(f'Cache Purged: {domain}')
        result = r.json()
        print(f'Result: {result}')
        if result['success']:
            success.append(domain)
    except Exception as error:
        print(f'Error Purging: {domain}: {error}')
        continue

if not success:
    raise ValueError('All Zone Cache Purges Failed!')

print(f'Purged {len(success)}/{len(domains)} domains: {success}')
