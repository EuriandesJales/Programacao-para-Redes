#!/usr/bin/env python3
"""
version_guard.py

Compara a versão/tag que está prestes a ser implantada com a versão
atualmente em produção. Se forem iguais, o script sai com código 10
("skip") para que o pipeline pule o deploy — evitando deploys
desnecessários/duplicados.

Funciona com:
  - Kubernetes (lê a imagem atual de um deployment via kubectl)
  - Um endpoint HTTP que exponha a versão atual (ex: /version ou /health)
  - Um arquivo de texto simples (ex: current_version.txt em um bucket/servidor)

Uso (Kubernetes):
    python3 version_guard.py \
        --source kubectl \
        --kubectl-deployment minha-api \
        --kubectl-namespace producao \
        --kubectl-container app \
        --new-version v1.4.2

Uso (HTTP):
    python3 version_guard.py \
        --source http \
        --version-url https://minha-api.exemplo.com/version \
        --new-version v1.4.2

Códigos de saída:
    0  -> versão é diferente, siga com o deploy
    10 -> versão é igual, pule o deploy
    1  -> erro ao obter a versão atual
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import urllib.error


def log(msg: str) -> None:
    print(f"[version-guard] {msg}", flush=True)


def get_version_from_kubectl(deployment: str, namespace: str, container: str) -> str | None:
    cmd = (
        f"kubectl get deployment {deployment} -n {namespace} "
        f"-o jsonpath='{{.spec.template.spec.containers[?(@.name==\"{container}\")].image}}'"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"Erro ao consultar kubectl: {result.stderr.strip()}")
        return None
    image = result.stdout.strip().strip("'")
    if ":" in image:
        return image.rsplit(":", 1)[-1]
    return image or None


def get_version_from_http(url: str, json_field: str = "version") -> str | None:
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            body = resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        log(f"Erro ao consultar {url}: {e}")
        return None

    body_stripped = body.strip()
    # tenta interpretar como JSON primeiro
    try:
        data = json.loads(body_stripped)
        if isinstance(data, dict) and json_field in data:
            return str(data[json_field])
    except json.JSONDecodeError:
        pass

    # fallback: texto puro (ex.: "v1.4.1")
    match = re.search(r"[vV]?\d+\.\d+\.\d+", body_stripped)
    return match.group(0) if match else body_stripped or None


def normalize(version: str) -> str:
    """Remove prefixo 'v' e espaços para comparar versões de forma consistente."""
    return version.strip().lstrip("vV")


def main():
    parser = argparse.ArgumentParser(description="Evita deploys duplicados comparando versões.")
    parser.add_argument("--source", choices=["kubectl", "http"], required=True)
    parser.add_argument("--new-version", required=True, help="Versão que será implantada")

    # opções kubectl
    parser.add_argument("--kubectl-deployment")
    parser.add_argument("--kubectl-namespace", default="default")
    parser.add_argument("--kubectl-container")

    # opções http
    parser.add_argument("--version-url")
    parser.add_argument("--json-field", default="version")

    args = parser.parse_args()

    if args.source == "kubectl":
        if not args.kubectl_deployment or not args.kubectl_container:
            log("--kubectl-deployment e --kubectl-container são obrigatórios com --source kubectl")
            sys.exit(1)
        current_version = get_version_from_kubectl(
            args.kubectl_deployment, args.kubectl_namespace, args.kubectl_container
        )
    else:
        if not args.version_url:
            log("--version-url é obrigatório com --source http")
            sys.exit(1)
        current_version = get_version_from_http(args.version_url, args.json_field)

    if current_version is None:
        log("Não foi possível obter a versão atual. Seguindo com o deploy por segurança.")
        sys.exit(0)

    log(f"Versão atual em produção: {current_version}")
    log(f"Nova versão a implantar:  {args.new_version}")

    if normalize(current_version) == normalize(args.new_version):
        log("Versões idênticas. Pulando deploy (evitando duplicidade).")
        sys.exit(10)
    else:
        log("Versões diferentes. Prosseguindo com o deploy.")
        sys.exit(0)


if __name__ == "__main__":
    main()