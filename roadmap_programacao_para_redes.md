# Roadmap de Estudos — Programação para Redes de Computadores

**Foco:** Automação com Shell Script e Python, fundamentos de Sysadmin e cultura DevOps.

Este roadmap reorganiza a ementa em uma sequência lógica de aprendizado, agrupada em 5 fases progressivas. A lógica é: primeiro construir a base (lógica de programação + terminal Linux), depois consolidar automação local com Shell Script, avançar para automação de redes com Python, e só então subir o nível de abstração com APIs de rede e Infraestrutura como Código (IaC).

---

## Fase 0 — Pré-requisitos rápidos (antes de tudo)
Se você ainda não tem familiaridade com o terminal, comece aqui. Se já manja de Linux básico, pode pular direto para a Fase 1.

- Instalar uma distro Linux (nativa, VM ou WSL) — recomendado: Ubuntu
- Comandos essenciais: `ls`, `cd`, `pwd`, `cat`, `grep`, `find`, `chmod`, `ps`, `top`
- Editor de terminal (vim, nano ou VS Code com terminal integrado)
- Conceitos de rede básicos: IP, máscara, gateway, DNS, portas (revisão, se já viu isso antes)

---

## Fase 1 — Fundamentos de Programação para Redes
*Corresponde ao bloco 1 da ementa*

**Objetivo:** sair sabendo ler e escrever lógica de programação em Python e Shell.

1. **1.1 Introdução à programação para redes**
   - O que é automação de rede e por que ela existe (escala, erro humano, repetibilidade)
   - Diferença entre configuração manual vs. programática
   - Panorama das ferramentas que serão usadas no curso (Python, Bash, SSH, Netmiko, Ansible, Terraform)

2. **1.2 Fundamentos da linguagem Python e Shell Script**
   - Sintaxe básica de Python: variáveis, tipos, operadores
   - Sintaxe básica de Shell Script: shebang (`#!/bin/bash`), variáveis, permissões de execução
   - Entrada e saída de dados (`input()`, `print()`, `echo`, `read`)
   - Funções em ambas as linguagens

3. **1.3 Estruturas de controle e manipulação de arquivos**
   - `if/else`, `for`, `while` em Python e Shell
   - Leitura e escrita de arquivos (`open()` em Python; redirecionamento `>`, `>>`, `<` em Shell)
   - Tratamento básico de erros (`try/except`; `exit codes` em Shell)

**Checkpoint da Fase 1:** você deve conseguir escrever um script (em Python ou Shell) que leia um arquivo de texto, processe linha por linha com uma estrutura condicional, e grave um resultado em outro arquivo.

---

## Fase 2 — Automação de Redes com Shell Script
*Corresponde ao bloco 2 da ementa*

**Objetivo:** aplicar a lógica aprendida diretamente sobre o sistema operacional e a rede, usando Shell.

1. **2.1 Uso do terminal Linux para automação**
   - Encadeamento de comandos (`|`, `&&`, `||`)
   - Agendamento de tarefas com `cron` / `crontab`
   - Variáveis de ambiente

2. **2.2 Configuração de interfaces de rede via script**
   - Comandos `ip`, `ifconfig`, `nmcli`
   - Scripts para subir/derrubar interfaces e configurar IP estático

3. **2.3 Monitoramento de tráfego e logs**
   - Ferramentas: `tcpdump`, `netstat`/`ss`, `iftop`
   - Análise de logs com `grep`, `awk`, `sed`
   - Scripts simples de alerta (ex: notificar se uma interface cair)

4. **2.4 Execução de comandos remotos com SSH**
   - Autenticação por chave pública/privada
   - `ssh` para execução remota de comandos
   - `scp`/`rsync` para transferência de arquivos entre hosts

**Checkpoint da Fase 2:** um script Shell que se conecta via SSH a um host remoto, coleta uma informação (ex: uso de disco ou status de interface) e grava um log local com timestamp.

---

## Fase 3 — Gerenciamento de Redes via Programação (Python)
*Corresponde ao bloco 3 da ementa — aqui o curso sobe de nível, saindo do Shell puro para bibliotecas Python especializadas em rede*

**Objetivo:** usar Python para interagir programaticamente com dispositivos de rede (roteadores, switches).

1. **3.1 Uso de APIs para automação de redes (Netmiko, Paramiko)**
   - `Paramiko`: biblioteca de baixo nível para SSH em Python
   - `Netmiko`: camada sobre o Paramiko voltada para dispositivos de rede (Cisco, Juniper etc.)
   - Diferença entre CLI scraping e APIs estruturadas (REST/NETCONF — visão geral)

2. **3.2 Gerenciamento de dispositivos de rede via script**
   - Conectar, autenticar e enviar comandos de configuração a múltiplos dispositivos
   - Loop de automação sobre uma lista de IPs/hosts (inventário simples)

3. **3.3 Extração e análise de informações de configuração**
   - Coletar `show running-config`, tabelas de rota, tabelas ARP
   - Parsing de saída com regex ou bibliotecas como `TextFSM`/`ntc-templates`

4. **3.4 Automação de backups e atualizações**
   - Script para backup periódico de configurações (salvando com data/hora)
   - Rotina de atualização de firmware/software (visão geral do processo)

**Checkpoint da Fase 3:** um script Python com Netmiko que conecta em 2+ dispositivos (reais ou simulados em GNS3/EVE-NG/Cisco Packet Tracer), extrai a configuração atual e salva um backup versionado por data.

---

## Fase 4 — Infraestrutura como Código (IaC) e Cultura DevOps
*Corresponde ao bloco 4 da ementa*

**Objetivo:** dar o salto de "escrever scripts que automatizam tarefas" para "declarar o estado desejado da infraestrutura", que é o cerne do DevOps.

1. **4.1 Ferramentas de automação (Terraform, Ansible)**
   - **Ansible** (procedural/declarativo, sem agente): playbooks YAML, inventário, módulos de rede (`ios_config`, `junos_config` etc.)
   - **Terraform** (declarativo, foco em provisionamento): conceitos de provider, resource, state
   - Quando usar cada ferramenta (Ansible tende a ser mais usado para configuração de rede; Terraform para provisionamento de infraestrutura)

2. **Fundamentos de cultura DevOps** (complemento natural ao bloco 4, mesmo que não esteja explícito na ementa)
   - Conceito de Infraestrutura como Código: versionamento (Git) da configuração de rede
   - Integração contínua aplicada a rede (pipeline simples validando configs antes de aplicar)
   - Idempotência: por que rodar o mesmo playbook duas vezes não deve quebrar nada

**Checkpoint da Fase 4:** um playbook Ansible que configura uma interface de rede em um ou mais dispositivos simulados, e um `.tf` simples que provisiona um recurso básico (ex: uma VM ou rede virtual).

---

## Projeto final sugerido
Integrar todas as fases num único fluxo, por exemplo:
1. Script Python com Netmiko faz backup diário das configs de uma topologia simulada.
2. Um playbook Ansible aplica uma mudança de configuração padronizada em todos os dispositivos.
3. Os backups e logs são versionados em um repositório Git.
4. Um script Shell com `cron` dispara todo esse fluxo automaticamente.

Isso amarra Shell + Python + SSH/Netmiko + Ansible + versionamento — exatamente a progressão da ementa.

---

## Sugestão de ritmo (se for autoestudo paralelo à disciplina)

| Semana | Foco |
|---|---|
| 1–2 | Fase 0 + Fase 1 (lógica, Python e Shell básicos) |
| 3–4 | Fase 2 (automação com Shell + SSH) |
| 5–7 | Fase 3 (Python + Netmiko/Paramiko, o bloco mais denso) |
| 8–9 | Fase 4 (Ansible/Terraform + cultura DevOps) |
| 10 | Projeto final integrador + revisão |

## Ferramentas para praticar sem precisar de hardware real
- **Cisco Packet Tracer** ou **GNS3/EVE-NG** para simular dispositivos de rede
- **VS Code** com extensões de Python e YAML
- **Git/GitHub** para versionar os scripts desde o início (bom hábito DevOps)
