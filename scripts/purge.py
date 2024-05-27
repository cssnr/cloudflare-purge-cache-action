import os
import requests


base_url = 'https://api.cloudflare.com/client/v4/{0}'
input_zone = os.environ['INPUT_ZONE']
input_token = os.environ['INPUT_TOKEN']
headers = {"Authorization": f"Bearer {input_token}"}

# print(os.environ)


print('--- Getting Zones ---')

url = base_url.format(f'zones')
print(url)
r = requests.get(url, headers=headers, params={'per_page': 50})
print(r.status_code)
r.raise_for_status()
result = r.json()['result']

for zone in result:
    if zone['name'] == input_zone:
        break
else:
    raise ValueError('Zone Not Found.')

print(zone)


print('--- Purging Cache ---')

url = base_url.format(f"zones/{zone['id']}/purge_cache")
print(url)
r = requests.post(url, headers=headers, json={'purge_everything': True})
print(r.status_code)
r.raise_for_status()

print('--- Cache Purge Success ---')
print(r.json())
