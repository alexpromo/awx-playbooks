import requests
import json

ZABBIX_URL = "http://192.168.1.14/api_jsonrpc.php"
ZABBIX_TOKEN = "cfbf448e275112250c7fe06ef9e84505fe5ea46b880cc3e46c7671267d5cb432"
GROUP_ID = "30"  # <-- seu grupo

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ZABBIX_TOKEN}"
}


payload = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": ["host"],
        "selectInterfaces": ["ip"],
        "groupids": [GROUP_ID]   # <-- AQUI É O SEGREDO
    },
    "id": 1
}

response = requests.post(ZABBIX_URL, headers=headers, json=payload).json()

print("DEBUG:", response)

hosts = response.get("result", [])

inventory = {
    "all": {
        "hosts": []
    }
}

for h in hosts:
    for i in h.get("interfaces", []):
        if i.get("ip"):
            inventory["all"]["hosts"].append(i["ip"])

print(json.dumps(inventory, indent=2))
