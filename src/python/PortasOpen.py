import concurrent.futures
from netmiko import ConnectHandler

# Parâmetros de autenticação (ou use chaves SSH)
SSH_USER = "admin"
SSH_PASS = "SuaSenhaAqui"

def audit_host(ip):
    device = {
        'device_type': 'linux',
        'host': ip,
        'username': SSH_USER,
        'password': SSH_PASS,
        'timeout': 10,
    }
    
    try:
        connection = ConnectHandler(**device)
        
        # Coleta o hostname real do servidor
        hostname = connection.send_command("hostname").strip()
        
        # Coleta portas TCP e UDP escutando (Apenas coluna Local Address:Port)
        cmd = "ss -tuln | awk 'NR>1 {print $5}' | sort -u"
        output = connection.send_command(cmd)
        
        connection.disconnect()
        
        ports = [p for p in output.splitlines() if p]
        return {"ip": ip, "hostname": hostname, "ports": ports, "status": "OK"}
        
    except Exception as e:
        return {"ip": ip, "hostname": "N/A", "ports": [], "status": f"ERRO: {str(e)}"}

def main():
    with open("hosts.txt") as f:
        hosts = [line.strip() for line in f if line.strip()]

    print(f"[*] Iniciando auditoria em {len(hosts)} servidores...\n")

    # Execução paralela com ThreadPoolExecutor para alto desempenho
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(audit_host, hosts))

    # Exibição dos Resultados
    for res in results:
        print(f"==========================================")
        print(f"Host: {res['hostname']} ({res['ip']})")
        print(f"Status: {res['status']}")
        if res['ports']:
            print("Portas Escutando (LISTEN):")
            for port in res['ports']:
                print(f"  - {port}")
        print()

if __name__ == "__main__":
    main()