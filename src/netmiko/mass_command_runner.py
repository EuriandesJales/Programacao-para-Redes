#!/usr/bin/env python3
"""
mass_command_runner.py

Executa o(s) mesmo(s) comando(s) em vários dispositivos de rede
simultaneamente, usando Netmiko + threads. Ideal para tarefas como:
verificar versão, aplicar um comando de diagnóstico, coletar dados
de vários switches/roteadores de uma vez.

Requisitos:
    pip install netmiko

Uso:
    python3 mass_command_runner.py \
        --inventory devices.yaml \
        --commands "show version" "show ip interface brief" \
        --output-dir resultados/ \
        --max-workers 10

Formato do devices.yaml: mesmo formato do backup_configs.py
"""

import argparse
import os
import sys
import datetime
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


def log(msg: str) -> None:
    print(f"[mass-cmd] {msg}", flush=True)


def load_inventory(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_commands_on_device(device: dict, commands: list) -> dict:
    name = device.get("name", device["host"])
    conn_params = {
        "device_type": device["device_type"],
        "host": device["host"],
        "username": device["username"],
        "password": device["password"],
        "secret": device.get("secret", ""),
        "port": device.get("port", 22),
    }

    result = {"name": name, "host": device["host"], "success": False, "output": "", "error": None}

    try:
        with ConnectHandler(**conn_params) as conn:
            if device.get("secret"):
                conn.enable()
            outputs = []
            for cmd in commands:
                out = conn.send_command(cmd, read_timeout=30)
                outputs.append(f"$ {cmd}\n{out}\n")
            result["output"] = "\n".join(outputs)
            result["success"] = True

    except NetmikoAuthenticationException:
        result["error"] = "Falha de autenticação"
    except NetmikoTimeoutException:
        result["error"] = "Timeout de conexão"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Executa comandos em massa em dispositivos de rede.")
    parser.add_argument("--inventory", required=True, help="Arquivo YAML de dispositivos")
    parser.add_argument("--commands", nargs="+", required=True, help="Um ou mais comandos a executar")
    parser.add_argument("--output-dir", default="resultados", help="Diretório para salvar os resultados")
    parser.add_argument("--max-workers", type=int, default=10, help="Conexões simultâneas")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    devices = load_inventory(args.inventory)
    log(f"{len(devices)} dispositivo(s) carregado(s). Executando {len(args.commands)} comando(s) em paralelo...")

    results = []
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {
            executor.submit(run_commands_on_device, device, args.commands): device
            for device in devices
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "✅" if result["success"] else "❌"
            log(f"{status} {result['name']} ({result['host']})" +
                (f" - {result['error']}" if result["error"] else ""))

    # Salva relatório consolidado
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(args.output_dir, f"relatorio_{timestamp}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(f"{'=' * 60}\n")
            f.write(f"Dispositivo: {r['name']} ({r['host']})\n")
            f.write(f"{'=' * 60}\n")
            if r["success"]:
                f.write(r["output"] + "\n")
            else:
                f.write(f"ERRO: {r['error']}\n")
            f.write("\n")

    sucesso = sum(1 for r in results if r["success"])
    falha = len(results) - sucesso
    log(f"Concluído: {sucesso} sucesso(s), {falha} falha(s). Relatório: {report_path}")
    sys.exit(0 if falha == 0 else 1)


if __name__ == "__main__":
    main()
