#!/bin/bash
#
# monitor_processos.sh
# Monitoramento de processos em tempo real com heurísticas de detecção
# de atividade suspeita (possível malware/exploit rodando).
#
# IMPORTANTE: Este script usa HEURÍSTICAS (regras de comportamento comum
# de malware). Ele NÃO substitui um antivírus/EDR real. Pode gerar falsos
# positivos (ex: um script legítimo rodando em /tmp) e falsos negativos
# (malware sofisticado que evita essas regras). Use como camada extra de
# vigilância, não como única defesa.
#
# Uso:
#   sudo ./monitor_processos.sh [opções]
#
# Opções:
#   -n <segundos>    Intervalo entre verificações (padrão: 5)
#   -c <percentual>  Limite de CPU para alerta (padrão: 80)
#   -o <arquivo>     Arquivo de log (padrão: ./alertas_processos.log)
#   -1               Executa uma única verificação e sai (não fica em loop)
#   -h               Ajuda
#
# Recomendado rodar como root (sudo) para ver todos os processos e conexões.

set -uo pipefail

INTERVALO=5
LIMITE_CPU=80
LOG_FILE="./alertas_processos.log"
UMA_VEZ=false

# Diretórios de onde binários raramente deveriam ser executados
DIRS_SUSPEITOS_REGEX='^/tmp/|^/dev/shm/|^/var/tmp/|^/run/user/[0-9]+/|^/dev/mqueue/'

# Nomes de processos frequentemente usados para disfarçar malware/mineradores
# (isso é apenas um sinal de alerta, não uma prova)
NOMES_SUSPEITOS_REGEX='xmrig|kdevtmpfsi|kinsing|watchdogs|\.\/|networkservicce|systemdd|cronjobb|\bnc\b|ncat|\bmineração\b'

while getopts "n:c:o:1h" opt; do
    case $opt in
        n) INTERVALO="$OPTARG" ;;
        c) LIMITE_CPU="$OPTARG" ;;
        o) LOG_FILE="$OPTARG" ;;
        1) UMA_VEZ=true ;;
        h)
            grep '^#' "$0" | sed -n '2,22p' | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *) exit 1 ;;
    esac
done

if [[ $EUID -ne 0 ]]; then
    echo "Aviso: rodando sem privilégios de root. A visibilidade de processos de outros usuários e conexões de rede será limitada."
    echo "Recomenda-se: sudo $0"
    echo ""
    sleep 2
fi

touch "$LOG_FILE" 2>/dev/null || { echo "Não foi possível criar o arquivo de log: $LOG_FILE"; exit 1; }

alerta() {
    local nivel="$1"
    local msg="$2"
    local cor_reset="\033[0m"
    local cor
    case "$nivel" in
        ALTO) cor="\033[1;31m" ;;
        MEDIO) cor="\033[1;33m" ;;
        *) cor="\033[1;36m" ;;
    esac
    local linha="[$(date '+%Y-%m-%d %H:%M:%S')] [$nivel] $msg"
    echo -e "${cor}${linha}${cor_reset}"
    echo "$linha" >> "$LOG_FILE"
}

# Guarda o "estado anterior" de PIDs já alertados para não repetir o mesmo alerta a cada ciclo
declare -A JA_ALERTADO

verificar_processos() {
    # Percorre todos os processos com PID, %CPU, %MEM, usuário, caminho do executável e comando
    while IFS=$'\t' read -r pid usuario pcpu pmem comando; do
        [[ -z "$pid" || "$pid" == "PID" ]] && continue

        local chave_alerta=""
        local exe_path=""
        local exe_deletado=false

        # Caminho real do binário em execução (via /proc)
        if [[ -r "/proc/$pid/exe" ]]; then
            exe_path=$(readlink -f "/proc/$pid/exe" 2>/dev/null)
            [[ "$exe_path" == *"(deleted)"* ]] && exe_deletado=true
        fi

        # --- Heurística 1: processo rodando de diretório suspeito (/tmp, /dev/shm, etc) ---
        if [[ -n "$exe_path" && "$exe_path" =~ $DIRS_SUSPEITOS_REGEX ]]; then
            chave_alerta="dir_$pid"
            if [[ -z "${JA_ALERTADO[$chave_alerta]:-}" ]]; then
                alerta "ALTO" "PID $pid ($comando) — usuário '$usuario' — executando binário de diretório suspeito: $exe_path"
                JA_ALERTADO[$chave_alerta]=1
            fi
        fi

        # --- Heurística 2: binário apagado do disco mas ainda rodando (técnica de evasão comum) ---
        if $exe_deletado; then
            chave_alerta="del_$pid"
            if [[ -z "${JA_ALERTADO[$chave_alerta]:-}" ]]; then
                alerta "ALTO" "PID $pid ($comando) — usuário '$usuario' — binário foi DELETADO do disco mas o processo continua rodando: $exe_path"
                JA_ALERTADO[$chave_alerta]=1
            fi
        fi

        # --- Heurística 3: nome de processo bate com lista de mineradores/malware conhecidos ---
        if [[ "$comando" =~ $NOMES_SUSPEITOS_REGEX ]]; then
            chave_alerta="nome_$pid"
            if [[ -z "${JA_ALERTADO[$chave_alerta]:-}" ]]; then
                alerta "ALTO" "PID $pid — nome/comando corresponde a padrão conhecido de malware/minerador: '$comando'"
                JA_ALERTADO[$chave_alerta]=1
            fi
        fi

        # --- Heurística 4: uso de CPU acima do limite configurado ---
        local pcpu_int=${pcpu%.*}
        if [[ "$pcpu_int" =~ ^[0-9]+$ ]] && (( pcpu_int >= LIMITE_CPU )); then
            chave_alerta="cpu_$pid"
            if [[ -z "${JA_ALERTADO[$chave_alerta]:-}" ]]; then
                alerta "MEDIO" "PID $pid ($comando) — usuário '$usuario' — uso de CPU elevado: ${pcpu}% (limite: ${LIMITE_CPU}%)"
                JA_ALERTADO[$chave_alerta]=1
            fi
        fi

        # --- Heurística 5: processo escutando/conectado a portas fora do comum, com nome mascarado ---
        # (verifica se o processo tem conexões de rede e se o nome contém espaço extra ou caracteres estranhos que imitam nomes do sistema)
        if [[ "$comando" =~ ^[[:space:]] || "$comando" =~ [[:space:]]{2,} ]]; then
            chave_alerta="nomeestranho_$pid"
            if [[ -z "${JA_ALERTADO[$chave_alerta]:-}" ]]; then
                alerta "MEDIO" "PID $pid — nome de processo contém espaçamento incomum (possível tentativa de disfarce): '$comando'"
                JA_ALERTADO[$chave_alerta]=1
            fi
        fi

    done < <(ps -eo pid=,user=,pcpu=,pmem=,comm= --no-headers | awk '{printf "%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, $4, $5}')
}

verificar_conexoes_novas() {
    if ! command -v ss &>/dev/null; then
        return
    fi
    # Processos com conexões ESTABELECIDAS cujo binário já não existe mais no disco,
    # ou que escutam em portas altas incomuns associadas a backdoors/reverse shells
    while IFS= read -r linha; do
        local pid
        pid=$(echo "$linha" | grep -oP '(?<=pid=)[0-9]+' | head -1)
        [[ -z "$pid" ]] && continue

        local porta_local
        porta_local=$(echo "$linha" | awk '{print $5}' | sed -E 's/.*:([0-9]+)$/\1/')

        # Portas comumente associadas a reverse shells / RATs (heurística fraca, apenas um sinal a mais)
        if [[ "$porta_local" =~ ^(4444|1337|31337|6666|6667|12345|54321)$ ]]; then
            local chave_alerta="porta_${pid}_${porta_local}"
            if [[ -z "${JA_ALERTADO[$chave_alerta]:-}" ]]; then
                alerta "MEDIO" "PID $pid — conexão/escuta na porta $porta_local, comumente associada a reverse shells/backdoors. Verifique manualmente."
                JA_ALERTADO[$chave_alerta]=1
            fi
        fi
    done < <(ss -tanp 2>/dev/null | grep -E 'ESTAB|LISTEN')
}

echo "=========================================="
echo " Monitor de Processos Suspeitos — Iniciado"
echo " Intervalo: ${INTERVALO}s | Limite CPU: ${LIMITE_CPU}% | Log: $LOG_FILE"
echo " Pressione Ctrl+C para parar"
echo "=========================================="

trap 'echo -e "\nMonitoramento encerrado. Alertas salvos em: $LOG_FILE"; exit 0' SIGINT SIGTERM

if $UMA_VEZ; then
    verificar_processos
    verificar_conexoes_novas
    exit 0
fi

while true; do
    verificar_processos
    verificar_conexoes_novas
    sleep "$INTERVALO"
done