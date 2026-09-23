
Ssh paralelo · SH
#!/bin/bash
#
# ssh_paralelo.sh
# Conecta via SSH em vários hosts SIMULTANEAMENTE e executa um conjunto de
# comandos, mostrando a saída de cada máquina EM TEMPO REAL (linha a linha,
# assim que ela chega), prefixada com o nome do host e uma cor própria.
# Nenhum host espera o outro terminar.
#
# Uso:
#   ./ssh_paralelo.sh -f hosts.txt -c "comando1; comando2"
#   ./ssh_paralelo.sh -f hosts.txt -C script_remoto.sh
#
# Opções:
#   -f <arquivo>     Arquivo com a lista de hosts, um por linha (obrigatório)
#                    Cada linha pode ser um hostname (resolvido via DNS) ou IP.
#                    Formatos aceitos por linha:
#                       host
#                       usuario@host
#                       usuario@host:porta
#                    Linhas vazias ou iniciadas com # são ignoradas.
#   -c <comandos>    String com o(s) comando(s) a executar (separados por ; ou &&)
#   -C <arquivo>     Script local a ser enviado e executado remotamente (alternativa a -c)
#   -u <usuario>     Usuário padrão SSH quando o host não define "usuario@" (padrão: $USER)
#   -k <chave>       Caminho da chave privada SSH (ex: ~/.ssh/id_rsa)
#   -p <porta>       Porta SSH padrão (padrão: 22)
#   -j <n>           Máximo de conexões simultâneas (padrão: 0 = sem limite)
#   -t <segundos>    Timeout de conexão SSH (padrão: 10)
#   -o <diretorio>   Diretório para salvar os logs (padrão: ./ssh_logs_<timestamp>)
#   -s               Modo silencioso: sem cores/streaming ao vivo, só resumo final
#   -h               Ajuda
#
# Exemplo de hosts.txt:
#   servidor1.exemplo.com
#   admin@192.168.1.10
#   deploy@192.168.1.20:2222
#
# Requer acesso SSH já configurado (idealmente autenticação por chave, sem
# senha) para os hosts, já que a execução é em paralelo e não há como
# digitar senha interativamente para várias conexões ao mesmo tempo.
 
set -uo pipefail
 
ARQUIVO_HOSTS=""
COMANDOS=""
ARQUIVO_COMANDOS=""
USUARIO_PADRAO="${USER:-root}"
CHAVE_SSH=""
PORTA_PADRAO=22
MAX_PARALELO=0
TIMEOUT=10
DIR_LOGS="./ssh_logs_$(date +%Y%m%d_%H%M%S)"
MODO_SILENCIOSO=false
 
# Cores ANSI usadas ciclicamente para diferenciar hosts na tela
CORES=(31 32 33 34 35 36 91 92 93 94 95 96)
 
uso() {
    grep '^#' "$0" | sed -n '2,33p' | sed 's/^# \{0,1\}//'
    exit 0
}
 
while getopts "f:c:C:u:k:p:j:t:o:sh" opt; do
    case $opt in
        f) ARQUIVO_HOSTS="$OPTARG" ;;
        c) COMANDOS="$OPTARG" ;;
        C) ARQUIVO_COMANDOS="$OPTARG" ;;
        u) USUARIO_PADRAO="$OPTARG" ;;
        k) CHAVE_SSH="$OPTARG" ;;
        p) PORTA_PADRAO="$OPTARG" ;;
        j) MAX_PARALELO="$OPTARG" ;;
        t) TIMEOUT="$OPTARG" ;;
        o) DIR_LOGS="$OPTARG" ;;
        s) MODO_SILENCIOSO=true ;;
        h) uso ;;
        *) uso ;;
    esac
done
 
if [[ -z "$ARQUIVO_HOSTS" ]]; then
    echo "Erro: informe o arquivo de hosts com -f <arquivo>"
    uso
fi
if [[ ! -f "$ARQUIVO_HOSTS" ]]; then
    echo "Erro: arquivo de hosts '$ARQUIVO_HOSTS' não encontrado."
    exit 1
fi
if [[ -z "$COMANDOS" && -z "$ARQUIVO_COMANDOS" ]]; then
    echo "Erro: informe os comandos com -c \"comando\" ou -C arquivo_de_comandos.sh"
    exit 1
fi
if [[ -n "$ARQUIVO_COMANDOS" && ! -f "$ARQUIVO_COMANDOS" ]]; then
    echo "Erro: arquivo de comandos '$ARQUIVO_COMANDOS' não encontrado."
    exit 1
fi
if ! command -v ssh &>/dev/null; then
    echo "Erro: comando 'ssh' não encontrado neste sistema."
    exit 1
fi
 
mkdir -p "$DIR_LOGS"
 
OPCOES_SSH=(-o StrictHostKeyChecking=accept-new -o BatchMode=yes -o ConnectTimeout="$TIMEOUT")
[[ -n "$CHAVE_SSH" ]] && OPCOES_SSH+=(-i "$CHAVE_SSH")
 
PIDS=()
HOSTS_POR_PID=()
 
# Dado "usuario@host:porta" (ou variações), separa em variáveis globais
# USUARIO_R, HOST_R, PORTA_R
parsear_host() {
    local entrada="$1"
    USUARIO_R="$USUARIO_PADRAO"
    HOST_R="$entrada"
    PORTA_R="$PORTA_PADRAO"
 
    if [[ "$HOST_R" == *"@"* ]]; then
        USUARIO_R="${HOST_R%%@*}"
        HOST_R="${HOST_R#*@}"
    fi
    if [[ "$HOST_R" == *:* ]]; then
        PORTA_R="${HOST_R##*:}"
        HOST_R="${HOST_R%%:*}"
    fi
}
 
caminho_log() {
    local entrada="$1"
    parsear_host "$entrada"
    local nome_log
    nome_log=$(echo "${USUARIO_R}_${HOST_R}_${PORTA_R}" | tr -c 'A-Za-z0-9_.-' '_')
    echo "$DIR_LOGS/${nome_log}.log"
}
 
# Executa em UM host, transmitindo a saída em tempo real (linha a linha)
# Parâmetros: $1 = entrada do host (linha do arquivo)   $2 = cor ANSI
executar_no_host() {
    local entrada="$1"
    local cor="$2"
    parsear_host "$entrada"
    local usuario="$USUARIO_R" host="$HOST_R" porta="$PORTA_R"
    local log_file
    log_file=$(caminho_log "$entrada")
    local rotulo="${usuario}@${host}:${porta}"
    local codigo_saida
 
    registrar_linha() {
        local texto="$1"
        local linha_formatada="[$(date '+%H:%M:%S')] [$rotulo] $texto"
        if $MODO_SILENCIOSO; then
            :
        else
            echo -e "\033[1;${cor}m${linha_formatada}\033[0m"
        fi
        echo "$linha_formatada" >> "$log_file"
    }
 
    registrar_linha ">>> Conectando..."
 
    if [[ -n "$ARQUIVO_COMANDOS" ]]; then
        ssh "${OPCOES_SSH[@]}" -p "$porta" "${usuario}@${host}" 'bash -s' < "$ARQUIVO_COMANDOS" 2>&1 \
            | while IFS= read -r linha; do registrar_linha "$linha"; done
    else
        ssh "${OPCOES_SSH[@]}" -p "$porta" "${usuario}@${host}" "$COMANDOS" 2>&1 \
            | while IFS= read -r linha; do registrar_linha "$linha"; done
    fi
    codigo_saida=${PIPESTATUS[0]}
 
    registrar_linha ">>> Finalizado (código de saída: $codigo_saida)"
    echo "$codigo_saida" > "${log_file}.exit"
}
 
aguardar_vaga() {
    if [[ "$MAX_PARALELO" -gt 0 ]]; then
        while [[ "$(jobs -rp | wc -l)" -ge "$MAX_PARALELO" ]]; do
            sleep 0.2
        done
    fi
}
 
echo "=========================================="
echo " Execução SSH em Paralelo — Tempo Real"
echo " Arquivo de hosts: $ARQUIVO_HOSTS"
echo " Logs em: $DIR_LOGS"
[[ "$MAX_PARALELO" -gt 0 ]] && echo " Paralelismo máximo: $MAX_PARALELO"
$MODO_SILENCIOSO && echo " Modo silencioso ativado (sem streaming ao vivo)"
echo "=========================================="
echo ""
 
TOTAL=0
IDX=0
while IFS= read -r linha || [[ -n "$linha" ]]; do
    linha="$(echo "$linha" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [[ -z "$linha" || "$linha" == \#* ]] && continue
 
    aguardar_vaga
    cor="${CORES[$((IDX % ${#CORES[@]}))]}"
    executar_no_host "$linha" "$cor" &
    PIDS+=("$!")
    HOSTS_POR_PID+=("$linha")
    ((TOTAL++))
    ((IDX++))
done < "$ARQUIVO_HOSTS"
 
if [[ "$TOTAL" -eq 0 ]]; then
    echo "Nenhum host válido encontrado em '$ARQUIVO_HOSTS'."
    exit 1
fi
 
wait "${PIDS[@]}" 2>/dev/null
 
echo ""
echo "=========================================="
echo " Resumo"
echo "=========================================="
 
SUCESSOS=0
FALHAS=0
for host in "${HOSTS_POR_PID[@]}"; do
    log_file=$(caminho_log "$host")
    codigo="?"
    [[ -f "${log_file}.exit" ]] && codigo=$(cat "${log_file}.exit")
 
    if [[ "$codigo" == "0" ]]; then
        echo "  [OK]    $host"
        ((SUCESSOS++))
    else
        echo "  [FALHA] $host (código: $codigo) — veja $log_file"
        ((FALHAS++))
    fi
done
 
echo ""
echo "Total: $TOTAL | Sucesso: $SUCESSOS | Falha: $FALHAS"
echo "Logs completos em: $DIR_LOGS"
 
[[ "$FALHAS" -gt 0 ]] && exit 1
exit 0
 
