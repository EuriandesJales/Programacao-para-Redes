# ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1 # para pegar o IP da interface de rede

/* Script feito para escanear a rede local e identificar dispositivos ativos usando o protocolo ARP tenta resolver os nomes de host  */
# Ajuste o prefixo do IP conforme sua sub-rede (ex: 192.168.1)
PREFIX="192.168.1"

# Envia 1 ping com timeout de 1s para cada IP em paralelo (silencioso)
for ip in $(seq 1 254); do
  ping -c 1 -w 1 ${PREFIX}.${ip} > /dev/null 2>&1 &
done; wait

# Lê a tabela ARP do Kernel para listar os IPs ativos com MAC e tentar resolver o hostname
echo -e "IP\t\t\tMAC Address\t\tHostname"
echo "------------------------------------------------------------------"
arp -an | grep -v "incomplete" | while read -r line; do
  ip=$(echo "$line" | awk -F '[()]' '{print $2}')
  mac=$(echo "$line" | awk '{print $4}')
  # Tenta resolver o hostname via getent/hosts
  host=$(getent hosts "$ip" | awk '{print $2}')
  [ -z "$host" ] && host="N/A"
  echo -e "${ip}\t\t${mac}\t${host}"
done