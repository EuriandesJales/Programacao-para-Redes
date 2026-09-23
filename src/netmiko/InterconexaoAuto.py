import concurrent.futures
import ipaddress
from netmiko import ConnectHandler

# 1. CÁLCULO DE REDE AUTOMÁTICO (Terceirizado para a biblioteca ipaddress)
base_net = ipaddress.ip_network("10.0.0.0/16")
subnets = list(base_net.subnets(new_prefix=30))

# Definição dos links baseada nos cálculos
link_r1_r2 = subnets[0]  # 10.0.0.0/30
link_r2_r3 = subnets[1]  # 10.0.0.4/30

# IPs das interfaces ponto a ponto
r1_eth0_ip = link_r1_r2[1]  # 10.0.0.1
r2_eth0_ip = link_r1_r2[2]  # 10.0.0.2

r2_eth1_ip = link_r2_r3[1]  # 10.0.0.5
r3_eth0_ip = link_r2_r3[2]  # 10.0.0.6

# 2. MAPEAMENTO DE DISPOSITIVOS E COMANDOS DINÂMICOS
DEVICES = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.10",
        "username": "admin",
        "password": "SuaSenhaSegura",
        "name": "R1",
        "configs": [
            "interface GigabitEthernet0/0",
            f" ip address {r1_eth0_ip} {link_r1_r2.netmask}",
            " no shutdown",
            "interface Loopback0",
            " ip address 192.168.1.1 255.255.255.255",
            # Rota estática para alcançar a Loopback do R3 passando pelo R2
            f"ip route 192.168.3.1 255.255.255.255 {r2_eth0_ip}",
        ],
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.20",
        "username": "admin",
        "password": "SuaSenhaSegura",
        "name": "R2",
        "configs": [
            "interface GigabitEthernet0/0",
            f" ip address {r2_eth0_ip} {link_r1_r2.netmask}",
            " no shutdown",
            "interface GigabitEthernet0/1",
            f" ip address {r2_eth1_ip} {link_r2_r3.netmask}",
            " no shutdown",
            "interface Loopback0",
            " ip address 192.168.2.1 255.255.255.255",
            # R2 atua como router intermediário (rotas estáticas para R1 e R3)
            f"ip route 192.168.1.1 255.255.255.255 {r1_eth0_ip}",
            f"ip route 192.168.3.1 255.255.255.255 {r3_eth0_ip}",
        ],
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.30",
        "username": "admin",
        "password": "SuaSenhaSegura",
        "name": "R3",
        "configs": [
            "interface GigabitEthernet0/0",
            f" ip address {r3_eth0_ip} {link_r2_r3.netmask}",
            " no shutdown",
            "interface Loopback0",
            " ip address 192.168.3.1 255.255.255.255",
            # Rota estática para alcançar a Loopback do R1 passando pelo R2
            f"ip route 192.168.1.1 255.255.255.255 {r2_eth1_ip}",
        ],
    },
]


# 3. FUNÇÃO DE APLICAÇÃO VIA NETMIKO
def aplicar_configuracao(dev_info):
    name = dev_info.pop("name")
    configs = dev_info.pop("configs")

    print(f"[*] Conectando em {name} ({dev_info['host']})...")

    try:
        connection = ConnectHandler(**dev_info)

        # Envia a lista de comandos dentro do modo de configuração global
        output = connection.send_config_set(configs)

        # Salva as alterações na NVRAM (copy running-config startup-config)
        connection.save_config()
        connection.disconnect()

        return f"[SUCESSO] {name} configurado com sucesso.\nDetalhes:\n{output}"

    except Exception as e:
        return f"[ERRO] Falha ao configurar {name}: {str(e)}"


# 4. EXECUÇÃO PARALELA (ThreadPoolExecutor)
def main():
    print("[*] Iniciando provisionamento em massa de rotas e interfaces...\n")

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(DEVICES)
    ) as executor:
        results = executor.map(aplicar_configuracao, DEVICES)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()