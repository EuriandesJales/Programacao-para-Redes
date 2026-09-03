# Documentação para Automação de Redes: Guia Arquitetural e Prático

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Obsidian](https://img.shields.io/badge/Obsidian-483699?style=for-the-badge&logo=obsidian&logoColor=white)

## 1. Contexto Acadêmico e Objetivo
Este repositório contém o relatório estruturado para a disciplina de Redes de Computadores. O objetivo central é estabelecer uma fundação de **NetDevOps** (Network Development and Operations), diferenciando a teoria dos protocolos, a prática da automação e os desafios da operação em larga escala. 

## 2. Ambiente de Leitura e Execução: Obsidian Vault
A arquitetura deste documento foi desenhada para ser consumida e executada de forma iterativa através do **Obsidian**, tratando o relatório como um ambiente vivo, e não apenas um documento estático.

* **Abertura:** Abra o diretório raiz deste projeto como um *Vault* no Obsidian.
* **Execução Interativa:** Os blocos de código (`python`, `bash`) inseridos nas notas são executáveis nativamente. Certifique-se de ter um plugin de execução (como o *Execute Code*) habilitado.
* **Virtual Environment (venv):** A automação de redes exige o isolamento das dependências. Um ambiente `.venv` deve ser provisionado na raiz do projeto. Nas configurações do plugin de execução do Obsidian, aponte o interpretador Python para o binário do ambiente virtual (`/caminho/do/projeto/.venv/bin/python`). Isso garantirá que módulos como `netmiko` e `ansible-runner` operem corretamente dentro da interface do Obsidian.

## 3. Arquitetura Tecnológica
A automação moderna exige a composição de diferentes abstrações. Abaixo, a dissecação do papel arquitetural de cada tecnologia no stack.

### 3.1. Git (Single Source of Truth - SSOT)
* **Conceito:** Sistema de controle de versão distribuído, pilar da infraestrutura imutável.
* **Tradeoffs e Causa Raiz:** A operação tradicional de redes via CLI gera "Configuration Drift" (desvio de estado). O Git resolve a causa raiz deste problema atuando como a única fonte da verdade. O tradeoff é a resistência cultural inicial e o overhead operacional em alterações emergenciais.
* **Exemplo Compacto:**
  ```bash
  git init && git add config_router.yaml && git commit -m "feat: baseline config via OSPF"
  ```

### 3.2. Python & Netmiko (Orquestração e Integração Legada)
* **Conceito:** Python atua como a linguagem universal de *glue logic*. O `netmiko` é uma abstração de alto nível sobre SSH, resolvendo o complexo gerenciamento de prompts e estados de dispositivos (exec vs config mode).
* **Tradeoffs e Causa Raiz:** Equipamentos legados carecem de APIs programáticas (NETCONF/RESTCONF). O Netmiko mitiga isso utilizando *screen-scraping* (parsing de texto), uma abordagem intrinsecamente frágil a atualizações de firmware, mas obrigatória para manter retrocompatibilidade.
* **Exemplo Compacto:**
  ```python
  from netmiko import ConnectHandler

  device = {'device_type': 'cisco_ios', 'host': '10.0.0.1', 'username': 'admin', 'password': '123'}
  with ConnectHandler(**device) as net_connect:
      print(net_connect.send_command('show ip route'))
  ```

### 3.3. Ansible (Gerência de Configuração)
* **Conceito:** Ferramenta *agentless* que abstrai comandos em módulos YAML.
* **Tradeoffs e Causa Raiz:** O objetivo arquitetural não é "executar comandos", mas sim atingir a **idempotência** (garantir que múltiplas execuções resultem no mesmo estado final, sem refazer ações desnecessárias). O tradeoff é o desempenho (pode ser lento sem tunings como o *Mitogen*) e o mascaramento de falhas de baixo nível pelo motor de execução.
* **Exemplo Compacto:**
  ```yaml
  - name: OSPF Baseline
    hosts: core_routers
    tasks:
      - name: Garantir OSPF ID 10
        cisco.ios.ios_ospf_interfaces:
          config:
            - address_family: ipv4
              process_id: 10
          state: merged
  ```

### 3.4. Terraform (Infrastructure as Code - IaC)
* **Conceito:** Motor de provisionamento declarativo baseado em grafos de dependência e controle rigoroso de estado.
* **Tradeoffs e Causa Raiz:** Diferente do Ansible (que gerencia o SO do equipamento), o Terraform brilha no ciclo de vida de estruturas em nuvem ou SDNs (ex: AWS VPCs, Cisco ACI). O ponto de falha reside no `tfstate`: a dessincronização do arquivo de estado com a realidade física exige operações complexas de reconciliação (`terraform import` ou `taint`).
* **Exemplo Compacto:**
  ```hcl
  resource "aws_vpc" "net_core" {
    cidr_block = "10.0.0.0/16"
  }
  # init -> plan -> apply
  ```

### 3.5. Bash (Pipelines e Interações de Baixo Nível)
* **Conceito:** Linguagem nativa e onipresente em ambientes POSIX.
* **Tradeoffs e Causa Raiz:** Utilizado para *bootstrapping* rápido e testes de conectividade em CI/CD. Extremamente veloz, mas a ausência de tipos de dados avançados torna-o inadequado e propenso a bugs se usado para manipular JSONs ou regras de negócio complexas.
* **Exemplo Compacto:**
  ```bash
  # Validação assíncrona de conectividade de rede
  for ip in 192.168.1.{1..50}; do
    ping -c 1 -W 1 $ip >/dev/null && echo "$ip UP" &
  done; wait
  ```

## 4. Resumo das Decisões de Design
* **Git** gerencia as intenções.
* **Terraform** constrói a topologia (Cloud/SDN).
* **Ansible** configura o plano de controle e dados (OSPF, BGP).
* **Python/Netmiko** atua nas contingências e coletas complexas.
* **Bash** fornece o invólucro para validações rápidas ao nível do sistema operacional.

## 5. Licença
Este material é distribuído sob a Licença **MIT**. A adoção e integração deste código e documentação em ambientes acadêmicos ou comerciais é encorajada de forma totalmente permissiva, exigindo estritamente a preservação dos avisos de direitos autorais e citação do autor original na documentação de projetos derivados.
README.md
Exibindo README.md.