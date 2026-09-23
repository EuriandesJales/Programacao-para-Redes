#!/usr/bin/env bash

set -e

# Identifica a interface de rede ativa com rota padrao (excluindo loopback)
INTERFACE=$(ip route show default | awk '/default/ {print $5}' | head -n 1)

if [ -z "$INTERFACE" ]; then
    echo "[ERRO] Nenhuma interface de rede ativa encontrada."
    exit 1
fi

echo "[*] Interface detectada: $INTERFACE"

# 1. Limpeza de Cache DNS (Equivalente ao /flushdns)
echo "[*] Limpando cache DNS..."
if systemctl is-active --quiet systemd-resolved; then
    sudo resolvectl flush-caches
elif systemctl is-active --quiet nscd; then
    sudo nscd -i hosts
fi

# 2. Libera e Renova a Conexao (Equivalente ao /release e /renew)
echo "[*] Reiniciando a conexao na interface $INTERFACE..."
sudo nmcli device reapply "$INTERFACE" || sudo nmcli connection reload

# Alternativa: Forcar a reativaçao da interface
sudo nmcli device disconnect "$INTERFACE"
sleep 2
sudo nmcli device connect "$INTERFACE"

echo "[*] Operacao concluida. Novo estado da interface:"
ip -4 addr show dev "$INTERFACE"