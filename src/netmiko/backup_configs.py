#!/usr/bin/env python3
"""
backup_configs.py

Conecta em uma lista de dispositivos de rede via Netmiko e salva o
'show running-config' (ou equivalente) de cada um em um arquivo separado,
com timestamp. Útil para backups diários/semanais automatizados.

Requisitos:
    pip install netmiko

Uso:
    1. Preencha o arquivo devices.yaml (ou ajuste DEVICES abaixo) com os
       dados dos dispositivos.
    2. python3 backup_configs.py --inventory devices.yaml --output-dir backups/

Formato esperado do devices.yaml:
    - host: 192.168.1.1
      device_type: cisco_ios
      username: admin
      password: SENHA_AQUI
      name: switch-core-01
    - host: 192.168.1.2
      device_type: juniper_junos
      username: admin
      password: SENHA_AQUI
      name: router-borda-01

Dica de segurança: em produção, NÃO deixe senha em texto plano no YAML.
Use variáveis de ambiente, Vault, ou getpass().
"""

import argparse
import os
import sys
import datetime
import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Comando de backup por tipo de dispositivo
BACKUP_COMMANDS = {
    "cisco_ios": "show running-config",
    "cisco_xe": "show running-config",
    "cisco_nxos": "show running-config",
    "juniper_junos": "show configuration | display set",
    "arista_eos": "show running-config",
    "huawei": "display current-configuration",
    "mikrotik_routeros": "/export",
}


def log(msg: str) -> None:
    print(f"[backup] {msg}", flush=True)


def load_inventory(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def backup_device(device: dict, output_dir: str) -> bool:
    name = device.get("name", device["host"])
    device_type = device["device_type"]
    command = BACKUP_COMMANDS.get(device_type, "show running-config")

    conn_params = {
        "device_type": device_type,
        "host": device["host"],
        "username": device["username"],
        "password": device["password"],
        "secret": device.get("secret", ""),
        "port": device.get("port", 22),
    }

    try:
        log(f"Conectando em {name} ({device['host']})...")
        with ConnectHandler(**conn_params) as conn:
            if device.get("secret"):
                conn.enable()
            output = conn.send_command(command, read_timeout=30)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"{name}_{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)

        log(f"✅ Backup de {name} salvo em {filename}")
        return True

    except NetmikoAuthenticationException:
        log(f"❌ Falha de autenticação em {name}")
    except NetmikoTimeoutException:
        log(f"❌ Timeout ao conectar em {name}")
    except Exception as e:
        log(f"❌ Erro inesperado em {name}: {e}")

    return False


def main():
    parser = argparse.ArgumentParser(description="Backup em massa de configs via Netmiko.")
    parser.add_argument("--inventory", required=True, help="Caminho do arquivo YAML de dispositivos")
    parser.add_argument("--output-dir", default="backups", help="Diretório onde salvar os backups")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    devices = load_inventory(args.inventory)
    log(f"{len(devices)} dispositivo(s) carregado(s) do inventário.")

    sucesso, falha = 0, 0
    for device in devices:
        if backup_device(device, args.output_dir):
            sucesso += 1
        else:
            falha += 1

    log(f"Concluído: {sucesso} sucesso(s), {falha} falha(s).")
    sys.exit(0 if falha == 0 else 1)


if __name__ == "__main__":
    main()
