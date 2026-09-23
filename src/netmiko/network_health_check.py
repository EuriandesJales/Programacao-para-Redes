#!/usr/bin/env python3
"""
network_health_check.py

Testa conectividade SSH, coleta versão do SO e uptime de uma lista de
dispositivos de rede via Netmiko, gerando um relatório resumido em
formato tabela (útil para rodar antes de uma manutenção, ou como
verificação diária de saúde da rede).

Requisitos:
    pip install netmiko tabulate

Uso:
    python3 network_health_check.py --inventory devices.yaml

Formato do devices.yaml: mesmo formato do backup_configs.py
"""

import argparse
import sys
import re
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from tabulate import tabulate

# Comando de versão por tipo de dispositivo
VERSION_COMMANDS = {
    "cisco_ios": "show version",
    "cisco_xe": "show version",
    "cisco_nxos": "show version",
    "juniper_junos": "show version",
    "arista_eos": "show version",
    "huawei": "display version",
    "mikrotik_routeros": "/system resource print",
}


def load_inventory(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_uptime(output: str) -> str:
    """Tenta extrair a linha de uptime de forma genérica entre fabricantes."""
    match = re.search(r"uptime is (.+)", output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"[Uu]ptime[:\s]+([^\n]+)", output)
    return match.group(1).strip() if match else "N/D"


def check_device(device: dict) -> dict:
    name = device.get("name", device["host"])
    device_type = device["device_type"]
    command = VERSION_COMMANDS.get(device_type, "show version")

    conn_params = {
        "device_type": device_type,
        "host": device["host"],
        "username": device["username"],
        "password": device["password"],
        "secret": device.get("secret", ""),
        "port": device.get("port", 22),
        "timeout": 10,
    }

    row = {
        "Dispositivo": name,
        "IP": device["host"],
        "Status": "❌ OFFLINE",
        "Uptime": "-",
        "Detalhe": "-",
    }

    try:
        with ConnectHandler(**conn_params) as conn:
            output = conn.send_command(command, read_timeout=20)
            row["Status"] = "✅ ONLINE"
            row["Uptime"] = extract_uptime(output)
            row["Detalhe"] = "OK"

    except NetmikoAuthenticationException:
        row["Detalhe"] = "Falha de autenticação"
    except NetmikoTimeoutException:
        row["Detalhe"] = "Timeout / sem resposta"
    except Exception as e:
        row["Detalhe"] = str(e)[:50]

    return row


def main():
    parser = argparse.ArgumentParser(description="Health check em massa de dispositivos de rede.")
    parser.add_argument("--inventory", required=True, help="Arquivo YAML de dispositivos")
    parser.add_argument("--max-workers", type=int, default=10, help="Conexões simultâneas")

    args = parser.parse_args()
    devices = load_inventory(args.inventory)

    print(f"Verificando {len(devices)} dispositivo(s)...\n")

    rows = []
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = [executor.submit(check_device, d) for d in devices]
        for future in as_completed(futures):
            rows.append(future.result())

    # Ordena por status (offline primeiro, pra chamar atenção)
    rows.sort(key=lambda r: r["Status"])

    print(tabulate(rows, headers="keys", tablefmt="grid"))

    offline = sum(1 for r in rows if "OFFLINE" in r["Status"])
    print(f"\nResumo: {len(rows) - offline}/{len(rows)} online.")
    sys.exit(0 if offline == 0 else 1)


if __name__ == "__main__":
    main()
