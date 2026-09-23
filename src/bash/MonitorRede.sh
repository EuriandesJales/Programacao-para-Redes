#!/bin/bash
#
# analise_trafego.sh
# Script de análise de tráfego de rede em Linux
#
# Uso:
#   ./analise_trafego.sh [opções]
#
# Opções:
#   -i <interface>   Interface de rede a analisar (padrão: detectada automaticamente)
#   -t <segundos>    Duração da captura de banda (padrão: 5)
#   -o <arquivo>     Salvar relatório em arquivo (opcional)
#   -h               Mostrar ajuda
#
# Requisitos recomendados (o script funciona parcialmente sem eles):
#   ss, ip, awk, sed  -> geralmente já vêm no sistema
#   vnstat            -> estatísticas históricas de banda (opcional)
#   iftop             -> top talkers em tempo real (opcional)
#   tcpdump           -> captura de pacotes (opcional, requer root)

set -euo pipefail

INTERFACE=""
DURACAO=5
ARQUIVO_SAIDA=""

log() {
    if [[ -n "$ARQUIVO_SAIDA" ]]; then
        echo -e "$1" | tee -a "$ARQUIVO_SAIDA"
    else
        echo -e "$1"
    fi
}

uso() {
    grep '^#' "$0" | sed -n '2,20p' | sed 's/^# \{0,1\}//'
    exit 0
}

while getopts "i:t:o:h" opt; do
    case $opt in
        i) INTERFACE="$OPTARG" ;;
        t) DURACAO="$OPTARG" ;;
        o) ARQUIVO_SAIDA="$OPTARG" ;;
        h) uso ;;
        *) uso ;;
    esac
done

# Detecta a interface padrão (a usada pela rota default) se não informada
if [[ -z "$INTERFACE" ]]; then
    INTERFACE=$(ip route show default 2>/dev/null | awk '/default/ {print $5; exit}')
    if [[ -z "$INTERFACE" ]]; then
        echo "Não foi possível detectar a interface automaticamente. Use -i <interface>."
        exit 1
    fi
fi

[[ -n "$ARQUIVO_SAIDA" ]] && > "$ARQUIVO_SAIDA"

log "=========================================="
log " Relatório de Análise de Tráfego de Rede"
log " Data: $(date '+%Y-%m-%d %H:%M:%S')"
log " Interface: $INTERFACE"
log "=========================================="

# 1. Informações gerais da interface
log "\n--- 1. Informações da Interface ---"
if command -v ip &>/dev/null; then
    ip -s link show "$INTERFACE" 2>/dev/null | tee -a "${ARQUIVO_SAIDA:-/dev/stdout}" >/dev/null || true
    ip -s link show "$INTERFACE" 2>/dev/null | while read -r linha; do log "$linha"; done
fi

# 2. Conexões ativas (resumo por estado)
log "\n--- 2. Conexões TCP por Estado ---"
if command -v ss &>/dev/null; then
    ss -tan | awk 'NR>1 {print $1}' | sort | uniq -c | sort -rn | while read -r linha; do
        log "$linha"
    done
else
    log "Comando 'ss' não encontrado."
fi

# 3. Top 10 conexões ativas (origem/destino)
log "\n--- 3. Top 10 Conexões Ativas (local <-> remoto) ---"
if command -v ss &>/dev/null; then
    ss -tunap 2>/dev/null | awk 'NR>1 {print $5, $6}' | sort | uniq -c | sort -rn | head -10 | while read -r linha; do
        log "$linha"
    done
fi

# 4. Portas locais mais utilizadas
log "\n--- 4. Portas Locais Mais Usadas ---"
if command -v ss &>/dev/null; then
    ss -tan | awk 'NR>1 {print $4}' | sed -E 's/.*:([0-9]+)$/\1/' | sort | uniq -c | sort -rn | head -10 | while read -r linha; do
        log "$linha"
    done
fi

# 5. Processos com mais conexões (requer privilégios para ver todos)
log "\n--- 5. Processos com Mais Conexões de Rede ---"
if command -v ss &>/dev/null; then
    if ss -tanp 2>/dev/null | grep -q users; then
        ss -tanp 2>/dev/null | grep -oP '(?<=\(\(")[^"]+' | sort | uniq -c | sort -rn | head -10 | while read -r linha; do
            log "$linha"
        done
    else
        log "Execute como root (sudo) para ver processos associados às conexões."
    fi
fi

# 6. Medição de banda (RX/TX) durante um intervalo
log "\n--- 6. Uso de Banda em ${DURACAO}s (Interface: $INTERFACE) ---"
RX1=$(cat /sys/class/net/"$INTERFACE"/statistics/rx_bytes 2>/dev/null || echo 0)
TX1=$(cat /sys/class/net/"$INTERFACE"/statistics/tx_bytes 2>/dev/null || echo 0)
sleep "$DURACAO"
RX2=$(cat /sys/class/net/"$INTERFACE"/statistics/rx_bytes 2>/dev/null || echo 0)
TX2=$(cat /sys/class/net/"$INTERFACE"/statistics/tx_bytes 2>/dev/null || echo 0)

RX_DIFF=$((RX2 - RX1))
TX_DIFF=$((TX2 - TX1))
RX_KBPS=$(awk "BEGIN {printf \"%.2f\", $RX_DIFF/1024/$DURACAO}")
TX_KBPS=$(awk "BEGIN {printf \"%.2f\", $TX_DIFF/1024/$DURACAO}")

log "Download: ${RX_KBPS} KB/s"
log "Upload:   ${TX_KBPS} KB/s"

# 7. Sugestões de ferramentas adicionais, se ausentes
log "\n--- 7. Ferramentas Opcionais ---"
for ferramenta in vnstat iftop tcpdump nload; do
    if ! command -v "$ferramenta" &>/dev/null; then
        log "Sugestão: instale '$ferramenta' para análises mais avançadas (ex: sudo apt install $ferramenta)"
    else
        log "'$ferramenta' está instalado."
    fi
done

log "\n=========================================="
log " Fim do relatório"
log "=========================================="

if [[ -n "$ARQUIVO_SAIDA" ]]; then
    echo "Relatório salvo em: $ARQUIVO_SAIDA"
fi