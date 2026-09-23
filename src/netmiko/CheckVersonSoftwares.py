import concurrent.futures
from netmiko import ConnectHandler

# 1. LISTA DE VERSÕES ESPERADAS / HOMOLOGADAS (Baseline)
EXPECTED_VERSIONS = {
    "openssh-server": "1:9.6p1-3ubuntu13.5",
    "curl": "8.5.0-2ubuntu10.6",
    "nginx": "1.24.0-2ubuntu7.1",
    "python3": "3.12.3-0ubuntu2"
}

# 2. INVENTÁRIO DE HOSTS
HOSTS = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12",
]

SSH_USER = "admin"
SSH_PASS = "SuaSenhaSegura"

def check_host_compliance(ip):
    device = {
        'device_type': 'linux',
        'host': ip,
        'username': SSH_USER,
        'password': SSH_PASS,
        'timeout': 10,
    }

    results = {
        "ip": ip,
        "hostname": "UNKNOWN",
        "status": "OK",
        "packages": {}
    }

    try:
        connection = ConnectHandler(**device)
        results["hostname"] = connection.send_command("hostname").strip()

        # Verifica cada software da baseline no host
        for pkg, exp_ver in EXPECTED_VERSIONS.items():
            # Comando otimizado para Debian/Ubuntu (dpkg-query)
            # Para Arch/CachyOS use: f"pacman -Q {pkg} | awk '{{print $2}}'"
            # Para RHEL/CentOS use: f"rpm -q --queryformat '%{{VERSION}}-%{{RELEASE}}' {pkg}"
            cmd = f"dpkg-query -W -f='${{Version}}' {pkg} 2>/dev/null || echo 'NOT_INSTALLED'"
            installed_ver = connection.send_command(cmd).strip()

            is_compliant = (installed_ver == exp_ver)

            results["packages"][pkg] = {
                "installed": installed_ver,
                "expected": exp_ver,
                "compliant": is_compliant
            }

        connection.disconnect()

    except Exception as e:
        results["status"] = f"ERRO SSH: {str(e)}"

    return results

def main():
    print(f"[*] Iniciando verificação de conformidade em {len(HOSTS)} hosts...\n")

    # Execução paralela (até 10 threads simultâneas)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        host_results = list(executor.map(check_host_compliance, HOSTS))

    # Relatório no Terminal
    non_compliant_count = 0

    for res in host_results:
        print(f"==================================================")
        print(f"Host: {res['hostname']} ({res['ip']})")
        
        if "ERRO" in res["status"]:
            print(f" Status: \033[91m{res['status']}\033[0m")
            continue

        host_compliant = True
        for pkg, data in res["packages"].items():
            if data["compliant"]:
                status_str = "\033[92m[OK - ATUALIZADO]\033[0m"
            else:
                status_str = f"\033[91m[DIVERGENTE]\033[0m (Instalada: {data['installed']} | Esperada: {data['expected']})"
                host_compliant = False

            print(f"  - {pkg}: {status_str}")

        if not host_compliant:
            non_compliant_count += 1

    print("\n==================================================")
    print(f"Resumo: {len(HOSTS) - non_compliant_count}/{len(HOSTS)} hosts 100% em conformidade.")

if __name__ == "__main__":
    main()