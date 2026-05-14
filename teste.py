#!/usr/bin/env python3

import json
import subprocess

network = "192.168.104.0/24"

try:
    scan = subprocess.check_output(
        ["nmap", "-p", "5985", "--open", network, "-oG", "-"]
    ).decode()

    hosts = []

    for line in scan.splitlines():
        if "5985/open" in line:
            ip = line.split()[1]
            hosts.append(ip)

    inventory = {
        "all": {
            "hosts": hosts,
            "vars": {
                "ansible_connection": "winrm",
                "ansible_port": 5985,
                "ansible_winrm_transport": "ntlm",
                "ansible_winrm_server_cert_validation": "ignore"
            }
        }
    }

    print(json.dumps(inventory, indent=2))

except Exception as e:
    print(json.dumps({
        "_meta": {
            "hostvars": {}
        },
        "all": {
            "hosts": []
        },
        "error": str(e)
    }))
