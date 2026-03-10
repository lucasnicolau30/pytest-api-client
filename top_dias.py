import requests, json

url = "http://172.16.40.100:8030/placas/top-dias"
resp = requests.get(url, headers={"accept": "application/json"})
print(resp.status_code)
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))