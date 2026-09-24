
# Glossário: Git, Estrutura de Pastas e Padrões de Branch



# Operações Git

## 2. Configuração inicial

```bash
git config --global user.name "Seu Nome" #config user name
git config --global user.email "seu@email.com" #config email user
git config --global init.defaultBranch main # branch padrão
```

---

## 3. Criar / clonar repositório

```bash
git init                          # cria repositório novo na pasta atual
git clone <url>                   # copia um repositório remoto para sua máquina
git clone <url> pasta-destino     # clona em uma pasta com nome específico
```

---

## 4. Ciclo básico do dia a dia

```bash
git status                # mostra o que mudou, o que está staged, branch atual
git add arquivo.txt        # adiciona um arquivo específico ao staging
git add .                  # adiciona tudo que mudou na pasta atual
git add -p                 # adiciona interativamente, pedaço por pedaço (útil pra commits limpos)
git commit -m "mensagem"   # cria um commit com a mensagem
git commit -am "mensagem"  # add + commit em um passo (só para arquivos já rastreados)
```

---

## 5. Histórico e inspeção

```bash
git log                        # histórico de commits
git log --oneline              # histórico compacto (uma linha por commit)
git log --oneline --graph --all  # histórico visual com branches
git show <hash>                 # detalhes de um commit específico
git diff                        # diferenças não staged
git diff --staged               # diferenças já no staging
git blame arquivo.txt            # quem alterou cada linha e quando
```

---

## 6. Branches

```bash
git branch                       # lista branches locais
git branch -a                    # lista todas (locais + remotas)
git branch nome-da-branch        # cria uma branch nova (sem mudar para ela)
git checkout nome-da-branch      # muda para uma branch
git checkout -b nome-da-branch   # cria E muda para a branch (atalho mais usado)
git switch nome-da-branch        # forma moderna de trocar de branch (substitui checkout)
git switch -c nome-da-branch     # forma moderna de criar + trocar

git branch -d nome-da-branch     # deleta branch local (só se já foi mesclada)
git branch -D nome-da-branch     # força deleção (mesmo sem merge)
git push origin --delete nome    # deleta branch remota
```

---

## 7. Merge e Rebase (juntar branches)

```bash
git checkout main
git merge feature/login          # traz as mudanças de feature/login para main
```

- **Merge:** preserva o histórico como aconteceu, cria um "commit de merge" quando há divergência. Mais seguro, mas o histórico fica com mais ramificações visuais.
- **Rebase:** reescreve o histórico, aplicando seus commits "por cima" da branch de destino, como se você tivesse começado a trabalhar dali. Histórico mais limpo, mas reescreve commits (cuidado se já foi compartilhado com outras pessoas).

```bash
git checkout feature/login
git rebase main                  # reaplica commits de feature/login em cima de main
```

**Regra prática:** nunca dar rebase em branch compartilhada que outras pessoas já usam — só em branches locais/próprias antes de compartilhar.

---

## 8. Trabalhando com o remoto

```bash
git remote -v                   # lista remotos configurados
git remote add origin <url>      # associa um remoto chamado "origin"

git fetch                        # baixa mudanças do remoto SEM aplicar no seu código
git pull                         # fetch + merge (baixa e já aplica)
git pull --rebase                # fetch + rebase (baixa e reaplica seus commits por cima)

git push                         # envia commits locais para o remoto
git push -u origin nome-branch   # primeiro push de uma branch nova (define upstream)
git push --force                 # força sobrescrever o remoto (perigoso — evite em branch compartilhada)
git push --force-with-lease      # versão mais segura do force (verifica se ninguém mais alterou antes)
```

---

## 9. Desfazendo coisas

|Situação|Comando|
|---|---|
|Descartar mudanças não commitadas em um arquivo|`git checkout -- arquivo.txt` ou `git restore arquivo.txt`|
|Tirar arquivo do staging (sem perder a mudança)|`git reset arquivo.txt` ou `git restore --staged arquivo.txt`|
|Desfazer o último commit, mantendo as mudanças|`git reset --soft HEAD~1`|
|Desfazer o último commit e as mudanças também|`git reset --hard HEAD~1`|
|Criar um commit que desfaz outro (sem apagar histórico)|`git revert <hash>`|
|Editar mensagem do último commit|`git commit --amend`|

**Regra prática:** `revert` é seguro para histórico já compartilhado/pushed. `reset --hard` é destrutivo — use só em commits locais que ninguém mais viu.

---

## 10. Guardando trabalho temporariamente (stash)

```bash
git stash                    # guarda mudanças não commitadas de lado
git stash list                # lista os stashes guardados
git stash pop                 # traz de volta o último stash e remove da lista
git stash apply               # traz de volta mas mantém na lista
git stash drop                # descarta um stash
```

Útil quando você precisa trocar de branch rapidamente sem commitar algo pela metade.

---

## 11. Resolvendo conflitos

Quando um merge/rebase não consegue combinar automaticamente, o Git marca o conflito no arquivo:

```
<<<<<<< HEAD
sua versão
=======
versão da outra branch
>>>>>>> feature/login
```

Passos:

1. Editar o arquivo, decidir o que fica, remover os marcadores (`<<<<<<<`, `=======`, `>>>>>>>`).
2. `git add arquivo.txt` (marca como resolvido).
3. `git commit` (se for merge) ou `git rebase --continue` (se for rebase).

---

## 12. Tags (marcar versões)

```bash
git tag v1.0.0                        # cria tag simples
git tag -a v1.0.0 -m "Versão 1.0.0"    # tag anotada (com mensagem, recomendado)
git push origin v1.0.0                 # envia tag específica
git push origin --tags                 # envia todas as tags
```

---

## 13. .gitignore

Arquivo que lista o que o Git deve ignorar (não versionar nem subir para nuvem):

```
# dependências
node_modules/
venv/
__pycache__/

# builds
dist/
build/

# segredos e configs locais
.env
*.log

# arquivos de IDE/SO
.vscode/
.idea/
.DS_Store
```

---

## PARTE 2 — Padrões de Estrutura de Pastas

## Estrutura genérica (a maioria das linguagens)

```
meu-projeto/
├── src/                  # código-fonte principal
├── tests/                # testes automatizados
├── docs/                 # documentação
├── scripts/              # scripts auxiliares (build, deploy, migração)
├── .github/
│   └── workflows/        # pipelines de CI/CD (GitHub Actions)
├── .gitignore
├── README.md
├── LICENSE
└── (arquivo de dependências: package.json, requirements.txt, go.mod, etc.)
```

## Projeto Python

```
meu-projeto/
├── src/
│   └── meu_pacote/
│       ├── __init__.py
│       ├── main.py
│       └── modulo.py
├── tests/
│   └── test_modulo.py
├── requirements.txt      # ou pyproject.toml (padrão mais moderno)
├── .venv/                # ambiente virtual (vai no .gitignore)
├── README.md
└── .gitignore
```

## Projeto Node.js / JavaScript

```
meu-projeto/
├── src/
│   ├── index.js
│   ├── components/
│   ├── services/
│   └── utils/
├── tests/
├── node_modules/         # (no .gitignore, nunca commitado)
├── public/               # arquivos estáticos (se for frontend)
├── package.json
├── package-lock.json
├── .env.example          # modelo de variáveis de ambiente (sem valores reais)
└── .gitignore
```

## Aplicação Web (front + back separados)

```
meu-projeto/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/
│   ├── tests/
│   └── requirements.txt (ou package.json)
├── docker-compose.yml
└── README.md
```

## Estrutura em camadas (backend, arquitetura em N-camadas)

```
src/
├── controllers/    # recebe requisições, chama a lógica
├── services/       # regra de negócio
├── repositories/   # acesso a dados/banco
├── models/         # entidades/estrutura de dados
├── routes/         # definição de endpoints
├── middlewares/     # interceptadores (auth, log, etc.)
└── config/          # configurações (banco, variáveis de ambiente)
```

## Monorepo (múltiplos projetos relacionados em um repositório)

```
monorepo/
├── packages/
│   ├── app-web/
│   ├── app-mobile/
│   └── shared-lib/
├── package.json           # configuração raiz (ex: workspaces do npm/yarn)
└── turbo.json / lerna.json (ferramentas de orquestração de monorepo)
```

### Convenções úteis de nomeação de pastas/arquivos

- `snake_case` (nomes_assim) → comum em Python
- `kebab-case` (nomes-assim) → comum em pastas, URLs, projetos JS/config
- `camelCase` (nomesAssim) → comum em variáveis/arquivos JS
- `PascalCase` (NomesAssim) → comum em componentes React/classes

---

## PARTE 3 — Padrões de Nomes de Branch

## Convenção mais usada: `tipo/descricao-curta`

|Prefixo|Uso|Exemplo|
|---|---|---|
|`feature/`|nova funcionalidade|`feature/login-com-google`|
|`fix/`|correção de bug|`fix/erro-calculo-frete`|
|`hotfix/`|correção urgente direto em produção|`hotfix/falha-pagamento`|
|`bugfix/`|alternativa a `fix/`, mesmo sentido|`bugfix/token-expirado`|
|`chore/`|tarefas de manutenção (configs, dependências, etc.)|`chore/atualizar-dependencias`|
|`refactor/`|refatoração sem mudar comportamento|`refactor/servico-usuario`|
|`docs/`|mudanças só de documentação|`docs/atualizar-readme`|
|`test/`|adicionar ou ajustar testes|`test/cobertura-checkout`|
|`release/`|preparação de uma versão/release|`release/v2.1.0`|
|`experiment/`|testes exploratórios, protótipos|`experiment/nova-arquitetura`|

**Regras gerais de nome:**

- Sempre em minúsculas.
- Palavras separadas por hífen (`-`), nunca espaço.
- Descrição curta e objetiva (3-5 palavras no máximo).
- Se usar ticket/issue de sistema de gestão (Jira, Linear, GitHub Issues), incluir o número: `feature/PROJ-123-login-google`

## Branches principais (permanentes) — modelos comuns

### Git Flow (mais formal, usado em projetos com ciclo de release definido)

```
main / master     → código em produção, sempre estável
develop           → integração das próximas features
feature/*         → branches de features individuais, saem de develop e voltam pra develop
release/*         → preparação de uma versão antes de ir pra main
hotfix/*          → correção urgente, sai de main e volta pra main E develop
```

### Trunk-Based Development / GitHub Flow (mais simples, usado com CI/CD forte)

```
main              → única branch de longa duração, sempre "deployável"
feature/*         → branches curtas, viram Pull Request e voltam pra main rapidamente
```

**Qual escolher?**

- Times pequenos, deploy contínuo → **Trunk-Based / GitHub Flow** (mais simples, menos branches vivas).
- Produtos com versões formais, releases espaçadas, múltiplos ambientes → **Git Flow**.

---

## Tabela-resumo rápida (cola de referência)

|Preciso de...|Comando/Padrão|
|---|---|
|Começar a versionar uma pasta|`git init`|
|Copiar um repositório existente|`git clone <url>`|
|Ver o que mudou|`git status` / `git diff`|
|Preparar mudanças|`git add .`|
|Salvar um snapshot|`git commit -m "mensagem"`|
|Criar e mudar de branch|`git switch -c feature/nome`|
|Enviar pro remoto|`git push -u origin feature/nome`|
|Trazer mudanças do remoto|`git pull`|
|Juntar branches|`git merge` (preserva histórico) ou `git rebase` (reescreve)|
|Desfazer commit local (mantendo mudanças)|`git reset --soft HEAD~1`|
|Desfazer commit já compartilhado|`git revert <hash>`|
|Guardar trabalho temporário|`git stash`|
|Nome de branch de feature|`feature/nome-curto-da-tarefa`|
|Nome de branch de correção urgente|`hotfix/nome-do-problema`|

---

**Dica final:** o fluxo mais comum no dia a dia de times pequenos/médios é: `git switch -c feature/algo` → trabalhar e commitar → `git push -u origin feature/algo` → abrir Pull Request → merge para `main` → deletar a branch. Fixando esse ciclo, 90% do uso prático de Git no trabalho já está coberto.

---
# Shell Script com Bash
## Glossário: Lógica de Programação → Bash Script

Este glossário conecta conceitos de lógica de programação (que você já domina) com a sintaxe equivalente em Bash. A ideia é servir de "dicionário de tradução" para você começar a escrever scripts rapidamente.

---

## 1. Variáveis

**Lógica:** um espaço nomeado que guarda um valor.

```bash
nome="João"          # atribuição de valor  
idade=30
echo "$nome tem $idade anos"
```

- Não existe tipagem declarada (tudo é string por padrão, mas números são tratados como tais em contextos aritméticos).
- Para usar o valor, prefixe com `$`: `$nome` ou `${nome}` (a segunda forma evita =ambiguidade quando colado a outro texto: `${nome}s`).
- Variáveis de ambiente (globais do sistema): `$HOME`, `$PATH`, `$USER`.

---

## 2. Entrada e saída (I/O)

**Lógica:** ler dado do usuário / imprimir na tela.

```bash
echo "Digite seu nome:"
read nome
echo "Olá, $nome"
```

- `echo` = print
- `read` = input
- `printf` = print formatado (tipo `printf` do C), mais previsível que `echo`.

---

## 3. Condicionais (if/else)

**Lógica:** `if (condição) { } else { }`

```bash
if [ "$idade" -ge 18 ]; then
    echo "Maior de idade"
elif [ "$idade" -ge 13 ]; then
    echo "Adolescente"
else
    echo "Criança"
fi
```

Pontos-chave:

- `[ ]` é na verdade um comando (`test`). Precisa de espaços dentro dos colchetes.
- `[[ ]]` é uma versão mais moderna e segura (suporta `&&`, `||`, regex `=~`), prefira ela para strings.
- Bloco sempre fecha com `fi` (if invertido), assim como `do...done` e `case...esac`.

### Operadores de comparação

| Lógica      | Números (`[ ]`) | Strings (`[[ ]]`)       |
| ----------- | --------------- | ----------------------- |
| igual       | `-eq`           | `==`                    |
| diferente   | `-ne`           | `!=`                    |
| maior       | `-gt`           | `>` (dentro de `[[ ]]`) |
| menor       | `-lt`           | `<`                     |
| maior/igual | `-ge`           | —                       |
| menor/igual | `-le`           | —                       |
| E lógico    | `&&`            | `&&`                    |
| OU lógico   | `\|`            | `\|`                    |
| NÃO lógico  | `!`             | `!`                     |

### Testes de arquivo (muito usados em scripts)

```bash
[ -f "$arquivo" ]   # é um arquivo comum?
[ -d "$pasta" ]     # é um diretório?
[ -e "$caminho" ]   # existe?
[ -x "$arquivo" ]   # é executável?
```

---

## 4. Laços de repetição (loops)

### `for` — quando você sabe a coleção/intervalo

```bash
for i in 1 2 3 4 5; do
    echo "Número: $i"
done

for i in {1..10}; do echo "$i"; done      # range
for i in $(seq 1 2 10); do echo "$i"; done # range com passo (1,3,5...)

for arquivo in *.txt; do
    echo "Processando $arquivo"
done
```

C-like, se preferir:

```bash
for ((i=0; i<10; i++)); do
    echo "$i"
done
```

### `while` — enquanto condição for verdadeira

```bash
contador=0
while [ "$contador" -lt 5 ]; do
    echo "Contador: $contador"
    contador=$((contador + 1))
done
```

### `until` — o inverso do while (roda até a condição ser verdadeira)

```bash
until [ "$contador" -ge 5 ]; do
    contador=$((contador + 1))
done
```

### `break` e `continue`

Funcionam exatamente como você espera: `break` sai do loop, `continue` pula para a próxima iteração.

---

## 5. Estrutura de múltipla escolha (switch/case)

**Lógica:** `switch (x) { case 1: ... }`

```bash
case "$opcao" in
    1)
        echo "Opção 1"
        ;;
    2|3)
        echo "Opção 2 ou 3"
        ;;
    *)
        echo "Opção inválida"
        ;;
esac
```

- `;;` é o equivalente ao `break` do switch.
- `*` é o `default`.
- Aceita padrões (glob), ex: `*.txt)` casa qualquer coisa terminando em `.txt`.

---

## 6. Funções

**Lógica:** bloco reutilizável de código, com parâmetros e retorno.

```bash
saudacao() {
    local nome=$1        # $1 = primeiro argumento (local = variável local à função)
    echo "Olá, $nome!"
}

saudacao "Maria"
```

Pontos importantes:

- Não existe `function nome(params)` com parênteses de parâmetros — os "parâmetros" são acessados como `$1`, `$2`, `$3`... dentro da função, igual aos argumentos de linha de comando.
- `$#` = quantidade de argumentos recebidos.
- `$@` = todos os argumentos.
- **"Retorno":** funções em Bash não retornam valores como em outras linguagens — `return` só devolve um código numérico (0-255), usado tipicamente para indicar sucesso/erro. Para "retornar" um valor de verdade, use `echo` dentro da função e capture com `$(...)`:

```bash
dobro() {
    echo $(( $1 * 2 ))
}

resultado=$(dobro 5)
echo "$resultado"   # 10
```

---

## 7. Arrays (vetores/listas)

**Lógica:** estrutura indexada que guarda vários valores.

```bash
frutas=("maçã" "banana" "uva")

echo "${frutas[0]}"        # primeiro elemento
echo "${frutas[@]}"        # todos os elementos
echo "${#frutas[@]}"       # tamanho do array

frutas+=("manga")          # adicionar elemento

for fruta in "${frutas[@]}"; do
    echo "$fruta"
done
```

Arrays associativos (equivalente a dicionário/hash map):

```bash
declare -A idades
idades["João"]=30
idades["Maria"]=25

echo "${idades["João"]}"

for chave in "${!idades[@]}"; do
    echo "$chave -> ${idades[$chave]}"
done
```

---

## 8. Operações aritméticas

**Lógica:** cálculos matemáticos.

```bash
a=5
b=3

soma=$((a + b))
echo $((a * b))
echo $((a / b))     # divisão inteira: dá 1
echo $((a % b))     # resto (módulo): dá 2

# Incremento
a=$((a + 1))
((a++))             # equivalente, dentro de contexto aritmético
```

- Bash só trabalha com **inteiros** nativamente. Para float, use `bc` ou `awk`:

```bash
echo "5 / 3" | bc -l
```

---

## 9. Comparação e "verdade" no Bash (importante!)

Diferente de outras linguagens, em Bash:

- **Código de saída `0` = sucesso/verdadeiro**
- **Qualquer código diferente de `0` = falha/falso**

Isso é o oposto do `true/false` booleano que você está acostumado. Todo comando, ao terminar, retorna esse código em `$?`.

```bash
ls /pasta/existente
echo $?    # 0 = deu certo

ls /pasta/inexistente
echo $?    # diferente de 0 = deu erro
```

Isso é o que permite:

```bash
comando1 && comando2   # roda comando2 SE comando1 teve sucesso (AND lógico)
comando1 || comando2   # roda comando2 SE comando1 falhou (OR lógico)
```

---

## 10. Strings — manipulação comum

```bash
texto="Olá Mundo"

echo "${#texto}"            # tamanho da string: 9
echo "${texto:0:3}"         # substring (do índice 0, 3 caracteres): "Olá"
echo "${texto/Mundo/Bash}"  # substituição: "Olá Bash"
echo "${texto^^}"           # maiúsculas
echo "${texto,,}"           # minúsculas

# Concatenação: é só colar
saudacao="Olá"
nome="Ana"
mensagem="$saudacao, $nome!"
```

Comparação de strings sempre com `[[ ]]` e `==`/`!=` (não use `-eq` para strings).

---

## 11. Tratamento de erros

**Lógica:** try/catch equivalente.

Bash não tem try/catch nativo, mas você simula com checagem de código de saída:

```bash
if ! comando_arriscado; then
    echo "Erro ao executar comando" >&2
    exit 1
fi
```

Boas práticas de robustez no início do script:

```bash
#!/bin/bash
set -e          # aborta o script se qualquer comando falhar
set -u          # erro se usar variável não definida
set -o pipefail # erro se qualquer parte de um pipe falhar
```

`trap` funciona como um "finally" ou tratador de sinal:

```bash
trap 'echo "Script interrompido"; exit 1' SIGINT
```

---

## 12. Escopo e ambiente

- Variáveis são **globais por padrão** dentro do script.
- Dentro de funções, use `local nome=valor` para escopo local (evita efeitos colaterais).
- `export VAR=valor` torna a variável visível para subprocessos (herança de escopo para processos filhos).

---

## 13. Argumentos de linha de comando (parâmetros do "main")

```bash
#!/bin/bash
# uso: ./script.sh arg1 arg2

echo "Nome do script: $0"
echo "Primeiro argumento: $1"
echo "Segundo argumento: $2"
echo "Todos os argumentos: $@"
echo "Quantidade de argumentos: $#"
```

---

## 14. Pipes e redirecionamento (composição de funções)

**Lógica:** encadear a saída de uma função como entrada de outra.

```bash
comando1 | comando2      # saída de comando1 vira entrada de comando2 (pipe)

comando > arquivo.txt    # redireciona saída (sobrescreve)
comando >> arquivo.txt   # redireciona saída (acrescenta)
comando < arquivo.txt    # usa arquivo como entrada
comando 2> erros.txt     # redireciona só os erros (stderr)
comando &> tudo.txt      # redireciona saída + erros
```

---

## 15. Execução em segundo plano / concorrência básica

```bash
comando_demorado &   # roda em background
wait                 # espera todos os processos em background terminarem
```

---

## Tabela-resumo rápida (cola de referência)

|Conceito de lógica|Bash|
|---|---|
|Variável|`var=valor` / `$var`|
|If/else|`if [[ ]]; then ... else ... fi`|
|Switch/case|`case ... in ... esac`|
|For|`for x in lista; do ... done`|
|While|`while [[ ]]; do ... done`|
|Função|`nome() { ... }`|
|Array|`arr=(a b c)` / `${arr[i]}`|
|Dicionário|`declare -A map`|
|Booleano (sucesso/falha)|código de saída `$?` (0 = true)|
|AND / OR|`&&` / `\|`|
|Try/catch|checar `$?` ou `set -e` + `trap`|
|Retorno de valor|`echo` + `$(...)` (captura)|
|Comentário|`# isso é um comentário`|

---
# Python Glossário: Lógica de Programação

Mesma ideia do glossário de Bash: um "dicionário de tradução" entre lógica de programação e a sintaxe do Python. Boa notícia — Python é a linguagem que mais se parece com pseudocódigo, então essa tradução costuma ser bem direta.

---

## 1. Variáveis

**Lógica:** um espaço nomeado que guarda um valor.

```python
nome = "João"
idade = 30
print(nome, idade)
```

- Não precisa declarar tipo (tipagem dinâmica) — mas cada valor tem um tipo internamente (`str`, `int`, `float`, `bool`, `list`, `dict`, etc).
- Descobrir o tipo: `type(idade)` → `<class 'int'>`.
- Conversão de tipo: `int("10")`, `str(10)`, `float("3.14")`.

---

## 2. Entrada e saída (I/O)

```python
nome = input("Digite seu nome: ")
print(f"Olá, {nome}")       # f-string: forma moderna de formatar texto
```

- `print()` = saída
- `input()` = entrada (sempre retorna **string** — se quiser número, converta: `idade = int(input("Idade: "))`)

---

## 3. Condicionais (if/elif/else)

```python
if idade >= 18:
    print("Maior de idade")
elif idade >= 13:
    print("Adolescente")
else:
    print("Criança")
```

Pontos-chave:

- **Sem chaves `{}`** — o bloco é definido por indentação (geralmente 4 espaços). Isso é obrigatório, não estético.
- Sempre termina a linha da condição com `:`.
- `elif` = "else if".

### Operadores de comparação e lógicos

|Lógica|Python|
|---|---|
|igual|`==`|
|diferente|`!=`|
|maior|`>`|
|menor|`<`|
|maior/igual|`>=`|
|menor/igual|`<=`|
|E lógico|`and`|
|OU lógico|`or`|
|NÃO lógico|`not`|
|pertence a|`in`|

```python
if idade >= 18 and idade < 65:
    print("Adulto")

if nome in ["João", "Maria"]:
    print("Nome conhecido")
```

---

## 4. Laços de repetição (loops)

### `for` — quando você itera sobre uma coleção/intervalo

```python
for i in range(5):          # 0,1,2,3,4
    print(i)

for i in range(1, 11, 2):   # de 1 a 10, passo 2 → 1,3,5,7,9
    print(i)

frutas = ["maçã", "banana", "uva"]
for fruta in frutas:
    print(fruta)

for i, fruta in enumerate(frutas):   # com índice
    print(i, fruta)
```

### `while` — enquanto condição for verdadeira

```python
contador = 0
while contador < 5:
    print(contador)
    contador += 1
```

### `break` e `continue`

Idênticos ao conceito geral: `break` sai do loop, `continue` pula para a próxima iteração.

### List comprehension (atalho muito usado em Python para "loop + condição + criação de lista")

```python
pares = [x for x in range(10) if x % 2 == 0]
# equivale a:
pares = []
for x in range(10):
    if x % 2 == 0:
        pares.append(x)
```

---

## 5. Estrutura de múltipla escolha (switch/case)

Python (a partir da versão 3.10) tem `match/case`:

```python
match opcao:
    case 1:
        print("Opção 1")
    case 2 | 3:
        print("Opção 2 ou 3")
    case _:
        print("Opção inválida")
```

- `_` é o `default`.
- Em versões antigas (<3.10), o padrão era simular com `if/elif` encadeado, ou usar um dicionário de funções.

---

## 6. Funções

```python
def saudacao(nome):
    return f"Olá, {nome}!"

resultado = saudacao("Maria")
print(resultado)
```

Pontos importantes:

- `def nome(parâmetros):` + corpo indentado.
- `return` devolve **qualquer tipo de valor** (diferente do Bash, que só devolve código numérico).
- Parâmetros com valor padrão: `def saudacao(nome="visitante"):`
- Argumentos nomeados: `saudacao(nome="Ana")`
- Número variável de argumentos: `def soma(*args): return sum(args)`
- Funções são "cidadãs de primeira classe" — podem ser passadas como variáveis:

```python
def dobro(x):
    return x * 2

operacao = dobro
print(operacao(5))   # 10
```

---

## 7. Estruturas de dados (listas, tuplas, dicionários, conjuntos)

### Lista (array/vetor — mutável, ordenada)

```python
frutas = ["maçã", "banana", "uva"]
frutas.append("manga")
frutas[0]              # "maçã"
frutas[-1]             # último elemento: "manga"
len(frutas)            # tamanho: 4
frutas[1:3]            # fatiamento (slice): ["banana", "uva"]
```

### Tupla (como lista, mas imutável)

```python
coordenada = (10, 20)
x, y = coordenada       # desempacotamento
```

### Dicionário (mapa/hash map chave-valor)

```python
idades = {"João": 30, "Maria": 25}
idades["Pedro"] = 40          # adicionar
print(idades["João"])         # acessar
for chave, valor in idades.items():
    print(chave, valor)
```

### Conjunto (set — coleção sem duplicatas)

```python
numeros = {1, 2, 3, 3, 2}     # vira {1, 2, 3}
numeros.add(4)
```

---

## 8. Operações aritméticas

```python
a, b = 5, 3

print(a + b)     # soma
print(a - b)     # subtração
print(a * b)     # multiplicação
print(a / b)     # divisão real: 1.666...
print(a // b)    # divisão inteira: 1
print(a % b)     # módulo (resto): 2
print(a ** b)    # potência: 125

a += 1           # incremento (não existe a++ em Python!)
```

Python já trabalha nativamente com float — sem precisar de ferramentas externas como no Bash.

---

## 9. Booleanos e "verdade" em Python

Diferente do Bash, Python tem um tipo booleano de verdade: `True` e `False` (com maiúscula inicial).

```python
ativo = True
if ativo:
    print("Está ativo")
```

Valores considerados "falsy" (equivalem a `False` em contexto booleano): `0`, `0.0`, `""` (string vazia), `[]`, `{}`, `None`. Todo o resto é "truthy".

```python
lista = []
if not lista:
    print("Lista vazia")
```

---

## 10. Strings — manipulação comum

```python
texto = "Olá Mundo"

len(texto)                  # tamanho: 9
texto[0:3]                  # fatiamento: "Olá"
texto.replace("Mundo", "Python")   # substituição
texto.upper()                # maiúsculas
texto.lower()                # minúsculas
texto.split(" ")             # divide em lista: ["Olá", "Mundo"]
" ".join(["Olá", "Mundo"])   # junta lista em string
texto.strip()                 # remove espaços nas pontas

# Concatenação e formatação
nome = "Ana"
mensagem = f"Olá, {nome}!"    # f-string (recomendado)
mensagem2 = "Olá, " + nome + "!"
```

---

## 11. Tratamento de erros (try/except)

```python
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Erro: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
else:
    print("Deu tudo certo")        # roda se NÃO houve erro
finally:
    print("Sempre executa")        # roda sempre, com ou sem erro
```

- `raise Exception("mensagem")` — lançar um erro manualmente.
- Isso é conceitualmente idêntico ao try/catch de outras linguagens.

---

## 12. Escopo

```python
x = 10   # escopo global

def funcao():
    y = 5           # escopo local — só existe dentro da função
    print(x)         # pode LER variável global
    # mas para MODIFICAR a global, precisa declarar:

def outra_funcao():
    global x
    x = 20
```

---

## 13. Argumentos de linha de comando

```python
import sys

print(sys.argv)        # lista de argumentos, sys.argv[0] é o nome do script
print(sys.argv[1])     # primeiro argumento
```

Para scripts mais robustos, usa-se o módulo `argparse`.

---

## 14. Classes e Orientação a Objetos

```python
class Pessoa:
    def __init__(self, nome, idade):   # construtor
        self.nome = nome
        self.idade = idade

    def saudacao(self):                # método
        return f"Olá, meu nome é {self.nome}"

p = Pessoa("Ana", 25)
print(p.saudacao())
```

- `self` = referência ao próprio objeto (equivalente ao `this` de outras linguagens).
- `__init__` = construtor.
- Herança: `class Aluno(Pessoa):`

---

## 15. Módulos e organização de código

```python
# arquivo utilitarios.py
def somar(a, b):
    return a + b
```

```python
# outro arquivo
import utilitarios
print(utilitarios.somar(2, 3))

# ou
from utilitarios import somar
print(somar(2, 3))
```

```python
if __name__ == "__main__":
    # só roda se o arquivo for executado diretamente,
    # não quando importado por outro módulo
    main()
```

---

## 16. Concorrência básica / execução assíncrona (visão geral)

```python
import threading

def tarefa():
    print("Rodando em paralelo")

t = threading.Thread(target=tarefa)
t.start()
t.join()   # espera terminar
```

Para I/O assíncrono moderno, Python usa `async`/`await` (mais avançado, mas vale saber que existe):

```python
import asyncio

async def tarefa():
    await asyncio.sleep(1)
    print("Concluído")

asyncio.run(tarefa())
```

---

## Tabela-resumo rápida (cola de referência)

|Conceito de lógica|Python|
|---|---|
|Variável|`var = valor`|
|If/else|`if x: ... elif y: ... else: ...`|
|Switch/case|`match x: case 1: ...`|
|For|`for x in colecao: ...`|
|While|`while condicao: ...`|
|Função|`def nome(params): return valor`|
|Lista/array|`[1, 2, 3]`|
|Tupla (imutável)|`(1, 2, 3)`|
|Dicionário/mapa|`{"chave": "valor"}`|
|Conjunto|`{1, 2, 3}`|
|Booleano|`True` / `False`|
|AND / OR / NOT|`and` / `or` / `not`|
|Try/catch|`try: ... except Exception as e: ...`|
|Classe|`class Nome: def __init__(self): ...`|
|Comentário|`# isso é um comentário`|
|Bloco de código|indentação (sem chaves)|

---
# Principais bibliotecas para automação de Redes com python


## Automate the Boring Stuff (3ª ed.) — Bibliotecas por capítulo com foco em DevOps

Segue um resumo prático de cada biblioteca, sempre puxando para cenários de automação de infraestrutura, pipelines e operações.

### Cap. 11-12 — Arquivos e CLI: `os`, `shutil`, `send2trash`, `argparse`

Base de qualquer script de automação: manipular caminhos, copiar/mover/apagar arquivos e construir interfaces de linha de comando.

python

```python
import os, shutil, argparse

parser = argparse.ArgumentParser(description="Rotaciona logs antigos")
parser.add_argument("--dias", type=int, default=7)
args = parser.parse_args()

for raiz, _, arquivos in os.walk("/var/log/app"):
    for f in arquivos:
        caminho = os.path.join(raiz, f)
        if os.path.getmtime(caminho) < time.time() - args.dias * 86400:
            shutil.move(caminho, "/var/log/app/archive/")
```

**DevOps:** scripts de limpeza de logs, rotação de artefatos de build, organização de diretórios de deploy. `argparse` é a base de qualquer ferramenta CLI interna (wrappers de `kubectl`, `terraform`, etc). `send2trash` evita `rm -rf` acidental em scripts que rodam em máquinas de desenvolvedores.

### Cap. 13 — Web Scraping: Requests, Beautiful Soup, Selenium, Playwright

Requests + BeautifulSoup baixam e interpretam HTML estático; Selenium/Playwright controlam um navegador real quando há JavaScript.

python

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://status.meuservico.com")
soup = BeautifulSoup(r.text, "html.parser")
status = soup.select_one(".status-indicator").text
```

**DevOps:** checagem de status pages de terceiros, scraping de changelogs/release notes para alertas de upgrade, testes de smoke em dashboards internos que exigem login/JS (Playwright é hoje preferido a Selenium por ser mais rápido e estável em CI). Também útil para validar que uma página de status/health-check está no ar após deploy.

### Cap. 14 — Planilhas Excel: OpenPyXL

Lê e escreve arquivos `.xlsx` sem precisar do Excel instalado.

python

```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.append(["Serviço", "Uptime %", "Incidentes"])
ws.append(["API Gateway", 99.95, 2])
wb.save("relatorio_sla.xlsx")
```

**DevOps:** geração automática de relatórios de SLA/uptime para stakeholders não técnicos, exportar métricas do Prometheus/Grafana para planilhas de auditoria.

### Cap. 15 — Google Sheets: EZSheets

Abstrai a API do Google Sheets sem exigir lidar diretamente com OAuth de forma manual.

python

```python
import ezsheets
ss = ezsheets.Spreadsheet('id_da_planilha')
sheet = ss[0]
sheet.appendRow(['2026-09-23', 'deploy-prod', 'sucesso'])
```

**DevOps:** dashboards colaborativos de deploys/incidentes, registro de mudanças (change log) compartilhado com o time sem precisar de um sistema dedicado.

### Cap. 16 — SQLite: `sqlite3`

Banco relacional embutido, zero configuração de servidor.

python

```python
import sqlite3
conn = sqlite3.connect("metrics.db")
conn.execute("CREATE TABLE IF NOT EXISTS deploys (ts TEXT, servico TEXT, status TEXT)")
conn.execute("INSERT INTO deploys VALUES (?, ?, ?)", ("2026-09-23", "auth-svc", "ok"))
conn.commit()
```

**DevOps:** cache local de estado em scripts de automação (ex.: quais hosts já foram atualizados), histórico leve de execuções de jobs sem precisar subir Postgres/MySQL, ótimo para ferramentas CLI internas que precisam de persistência simples.

### Cap. 17 — PDF e Word: PyPDF, PDFMiner, python-docx

Extração/manipulação de PDFs e geração de documentos Word.

python

```python
from pypdf import PdfReader
texto = "".join(p.extract_text() for p in PdfReader("laudo.pdf").pages)
```

**DevOps:** extrair dados de relatórios de auditoria/compliance em PDF, gerar automaticamente documentação de runbooks ou postmortems em Word a partir de templates.

### Cap. 18 — CSV/JSON/XML: `csv`, `json`, `xml`

Formatos onipresentes em configuração e troca de dados.

python

```python
import json
with open("inventario.json") as f:
    hosts = json.load(f)
for h in hosts:
    print(h["nome"], h["ip"])
```

**DevOps:** parsing de manifests Kubernetes exportados como JSON, leitura de inventários do Ansible, processamento de exports de métricas em CSV, transformação de configs XML legados (ex.: Jenkins, Maven).

### Cap. 19 — Tempo e agendamento: `time`, `datetime`, `sched`

Controle de tempo, timestamps e agendamento simples de tarefas dentro do próprio processo Python (sem cron externo).

python

```python
import sched, time
s = sched.scheduler(time.time, time.sleep)
def healthcheck():
    print("checando serviços...")
    s.enter(300, 1, healthcheck)
s.enter(0, 1, healthcheck)
s.run()
```

**DevOps:** scripts de monitoramento em loop, cálculo de janelas de manutenção, geração de timestamps padronizados (UTC) para logs.

### Cap. 20 — Email e notificações: `smtplib`, `imapclient`, ntfy.sh

Envio/leitura de email e push notifications simples via HTTP (ntfy.sh não exige app nem conta).

python

```python
import requests
requests.post("https://ntfy.sh/meu-canal-alertas", data="Deploy falhou em prod!".encode())
```

**DevOps:** alertas de pipeline (build quebrado, deploy falho, certificado expirando) direto no celular via ntfy, sem precisar integrar Slack/PagerDuty para scripts simples; `smtplib` para relatórios automáticos por email.

### Cap. 21 — Gráficos e imagens: Pillow, Matplotlib, pyperclipimg

Manipulação de imagens e geração de gráficos.

python

```python
import matplotlib.pyplot as plt
plt.plot(dias, uso_cpu)
plt.title("Uso de CPU - últimos 30 dias")
plt.savefig("cpu_report.png")
```

**DevOps:** gerar gráficos de métricas (CPU, latência, custo de cloud) para relatórios automatizados, redimensionar/anotar screenshots de dashboards para documentação de incidentes.

### Cap. 22 — OCR: PyTesseract

Extrai texto de imagens.

python

```python
import pytesseract
from PIL import Image
texto = pytesseract.image_to_string(Image.open("screenshot_erro.png"))
```

**DevOps:** extrair mensagens de erro de screenshots enviados por usuários/suporte, processar logs que só existem como imagem (ex.: consoles legados, VMs sem acesso a texto).

### Cap. 23 — Controle de teclado e mouse: PyAutoGUI, PyScreeze

Automação de GUI — clicar, digitar, reconhecer elementos na tela.

python

```python
import pyautogui
pyautogui.click(pyautogui.locateCenterOnScreen("botao_deploy.png"))
```

**DevOps:** automatizar interações com ferramentas legadas sem API (consoles de VMware, sistemas internos antigos), últimos casos onde não há alternativa via CLI/API — usar com cautela, é frágil e deve ser último recurso.

### Cap. 24 — Texto-para-fala e voz: pyttsx3, gTTS, Whisper

Síntese de voz e transcrição de áudio.

python

```python
import pyttsx3
engine = pyttsx3.init()
engine.say("Alerta: disco cheio no servidor de produção")
engine.runAndWait()
```

**DevOps:** alertas sonoros em salas de operação (NOC), transcrição automática (Whisper) de reuniões de postmortem/incident review para gerar atas e buscar termos-chave depois.
# Glossário: Ansible para DevOps

é uma ferramenta que faz abstração de SO, ela permite que você escreva qual é o estado final que as maquinas da rede devem estra, e ela vai fazer os passos necessarios para chegar a o estado indicado.

ela opera por conexão ssh fazendo uso de chaves publicas compartilhadas com o computador administrador que deve ter a privada, para fazer ssh sem autenticação por senha facilitando a automação de processos, originalmente pensada em desenvolvimento no linux, mas com algumas modificações no sistema windowns consegue operar também neste sistema.

o controle opera via acervo de hostnames e mac address que torna possivel fazer conexão ssh alguns, seu arquivo de oconfiguração usa ymal, vamos ver um pouco da sintaxe de código desta ferramenta.

Referência prática das principais operações do Ansible — da estrutura básica aos comandos do dia a dia de um administrador/DevOps.

---

## 1. Conceitos fundamentais

|Termo|O que é|
|---|---|
|Control node|A máquina onde o Ansible é instalado e executado (não precisa de agente nas máquinas remotas)|
|Managed node (host)|As máquinas que o Ansible gerencia/configura|
|Inventory|Arquivo que lista os hosts gerenciados, organizados em grupos|
|Playbook|Arquivo YAML que descreve o estado desejado (uma sequência de tarefas)|
|Task|Uma ação individual dentro de um playbook (ex: instalar um pacote)|
|Module|A unidade que executa a ação de fato (ex: `apt`, `copy`, `service`)|
|Role|Forma organizada e reutilizável de agrupar tasks, variáveis, templates e handlers|
|Play|Um bloco dentro do playbook que mapeia um grupo de hosts a um conjunto de tasks|
|Handler|Task especial que só roda quando "notificada" por outra task (ex: reiniciar um serviço)|
|Fact|Informação coletada automaticamente sobre o host (IP, SO, memória, etc.)|
|Idempotência|Rodar o mesmo playbook várias vezes produz sempre o mesmo resultado, sem efeitos colaterais|
|Ad-hoc command|Comando único, sem playbook, para uma ação rápida e pontual|

**Fluxo mental:** `inventory` (quem) → `playbook` (o quê, em ordem) → `tasks/modules` (como) → `handlers` (reação a mudanças)

---

## 2. Instalação e configuração

```bash
pip install ansible                # instalação via pip
# ou
sudo apt install ansible           # Debian/Ubuntu
sudo dnf install ansible           # RHEL/Fedora
sudo pacman -S ansible  # Arch 

ansible --version                  # verificar versão e localizar arquivos de config
```

Arquivo de configuração principal: `ansible.cfg` (procurado na pasta atual, depois em `~/.ansible.cfg`, depois em `/etc/ansible/ansible.cfg`).

```ini
[defaults]
inventory = ./inventory/hosts.ini
remote_user = deploy
private_key_file = ~/.ssh/id_rsa
host_key_checking = False
```

---

## 3. Inventário (inventory)

### Formato INI

```ini
[web]
web1.exemplo.com
web2.exemplo.com ansible_host=192.168.1.10

[banco]
db1.exemplo.com

[producao:children]
web
banco

[web:vars]
ansible_user=deploy
ambiente=producao
```

### Formato YAML (alternativa mais estruturada)

```yaml
all:
  children:
    web:
      hosts:
        web1.exemplo.com:
        web2.exemplo.com:
      vars:
        ambiente: producao
    banco:
      hosts:
        db1.exemplo.com:
```

### Comandos úteis de inventário

```bash
ansible-inventory --list                 # mostra inventário processado em JSON
ansible-inventory --graph                # mostra hierarquia de grupos em árvore
ansible all --list-hosts                 # lista todos os hosts do inventário
```

- **Inventário dinâmico:** em vez de arquivo estático, um script/plugin busca hosts de uma fonte externa (AWS EC2, Azure, GCP, etc.) — muito usado em cloud, onde IPs mudam constantemente.

---

## 4. Comandos Ad-Hoc (ações rápidas sem playbook)

```bash
ansible all -m ping                              # testa conectividade
ansible web -m command -a "uptime"               # roda um comando remoto
ansible web -m shell -a "df -h | grep sda"       # comando com pipe/redirecionamento (precisa do shell)
ansible web -m apt -a "name=nginx state=present" --become   # instala pacote
ansible web -m service -a "name=nginx state=restarted" --become
ansible web -m copy -a "src=arquivo.conf dest=/etc/app/arquivo.conf" --become
ansible all -m setup                             # coleta e mostra os "facts" do host
```

`-m` = módulo | `-a` = argumentos do módulo | `--become` = executa como root (sudo) | `-i` = especifica um inventário diferente do padrão

---

## 5. Estrutura de um Playbook

```yaml
---
- name: Configurar servidores web
  hosts: web
  become: true
  vars:
    pacote_web: nginx

  tasks:
    - name: Instalar o Nginx
      apt:
        name: "{{ pacote_web }}"
        state: present
        update_cache: true

    - name: Copiar arquivo de configuração
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Reiniciar Nginx

    - name: Garantir que o Nginx está ativo
      service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Reiniciar Nginx
      service:
        name: nginx
        state: restarted
```

### Rodando o playbook

```bash
ansible-playbook site.yml                        # executa o playbook
ansible-playbook site.yml --check                # dry-run (simula, sem aplicar mudanças)
ansible-playbook site.yml --diff                 # mostra as diferenças que seriam aplicadas
ansible-playbook site.yml -i inventory/prod.ini  # especifica inventário
ansible-playbook site.yml --limit web1           # roda só num host específico
ansible-playbook site.yml -e "versao=1.2.3"      # passa variável extra via linha de comando
ansible-playbook site.yml -v / -vv / -vvv        # aumenta o nível de detalhe do log (verbose)
ansible-playbook site.yml --tags "deploy"        # roda só tasks marcadas com essa tag
ansible-playbook site.yml --skip-tags "debug"    # pula tasks com essa tag
ansible-playbook site.yml --syntax-check         # só valida a sintaxe, sem executar
ansible-playbook site.yml --step                 # confirma task por task antes de rodar
ansible-playbook site.yml --start-at-task="Nome" # retoma a partir de uma task específica
```

---

## 6. Módulos mais usados no dia a dia

|Categoria|Módulo|Exemplo de uso|
|---|---|---|
|Pacotes|`apt`, `yum`, `dnf`, `package`|instalar/remover pacotes (`package` é agnóstico de SO)|
|Serviços|`service`, `systemd`|iniciar, parar, reiniciar, habilitar no boot|
|Arquivos|`copy`, `template`, `file`, `lineinfile`, `blockinfile`|copiar arquivos, gerar a partir de template, criar diretórios, editar linhas|
|Usuários/grupos|`user`, `group`|criar/gerenciar contas do sistema|
|Execução de comando|`command`, `shell`, `raw`|rodar comandos (evite `shell`/`command` quando existir módulo específico)|
|Rede/download|`get_url`, `uri`|baixar arquivos, chamar APIs REST|
|Git|`git`|clonar/atualizar repositórios|
|Docker|`docker_container`, `docker_image`|gerenciar containers e imagens|
|Cloud|`amazon.aws.ec2_instance`, `azure.azcollection.*`, `google.cloud.*`|provisionar recursos em nuvem|
|Diversos|`debug`, `pause`, `wait_for`, `cron`, `mount`|imprimir valores, pausar execução, esperar porta abrir, agendar tarefas|

**Boa prática:** sempre prefira um módulo específico (`apt`, `copy`, `service`) a `shell`/`command`, porque módulos são idempotentes — rodar de novo não muda nada se já está no estado desejado. `shell`/`command` não têm essa garantia por padrão.

---

## 7. Variáveis

### Onde declarar (ordem de precedência, do menor para o maior peso, resumida)

```
defaults da role  →  inventory (vars de grupo/host)  →  vars da play  →  vars da task  →  extra vars (-e na linha de comando)
```

```yaml
# Direto no playbook
vars:
  porta: 8080

# Em arquivo separado
vars_files:
  - vars/producao.yml
```

```ini
# No inventário
[web:vars]
ambiente=producao
```

```bash
# Via linha de comando (maior precedência)
ansible-playbook site.yml -e "ambiente=homologacao"
```

### Usando variáveis (Jinja2)

```yaml
- name: Exibir variável
  debug:
    msg: "Ambiente atual: {{ ambiente }}"
```

### Registrar saída de uma task em variável

```yaml
- name: Verificar versão instalada
  command: nginx -v
  register: resultado

- name: Mostrar resultado
  debug:
    var: resultado.stdout
```

---

## 8. Facts (informações coletadas automaticamente)

```yaml
- name: Mostrar sistema operacional
  debug:
    msg: "{{ ansible_facts['os_family'] }} - {{ ansible_facts['distribution'] }}"
```

```bash
ansible web -m setup                          # ver todos os facts disponíveis
ansible web -m setup -a "filter=ansible_eth*"  # filtrar por padrão
```

Facts comuns: `ansible_hostname`, `ansible_os_family`, `ansible_distribution`, `ansible_default_ipv4.address`, `ansible_memtotal_mb`.

---

## 9. Condicionais, loops e handlers

### Condicional (`when`)

```yaml
- name: Instalar pacote só no Debian/Ubuntu
  apt:
    name: nginx
    state: present
  when: ansible_facts['os_family'] == "Debian"
```

### Loop

```yaml
- name: Instalar múltiplos pacotes
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - git
    - curl
```

```yaml
- name: Criar múltiplos usuários
  user:
    name: "{{ item.nome }}"
    groups: "{{ item.grupo }}"
  loop:
    - { nome: "ana", grupo: "devs" }
    - { nome: "bruno", grupo: "ops" }
```

### Handlers (executados só quando notificados, e só uma vez mesmo se notificado várias vezes)

```yaml
tasks:
  - name: Atualizar configuração
    template:
      src: app.conf.j2
      dest: /etc/app/app.conf
    notify: Reiniciar aplicação

handlers:
  - name: Reiniciar aplicação
    service:
      name: app
      state: restarted
```

---

## 10. Templates (Jinja2)

Arquivo `templates/nginx.conf.j2`:

```nginx
server {
    listen {{ porta }};
    server_name {{ ansible_facts['hostname'] }};

    {% if ambiente == "producao" %}
    access_log /var/log/nginx/access.log;
    {% endif %}

    {% for rota in rotas %}
    location {{ rota.caminho }} {
        proxy_pass {{ rota.destino }};
    }
    {% endfor %}
}
```

```yaml
- name: Gerar configuração a partir de template
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/conf.d/app.conf
  notify: Reiniciar Nginx
```

- `template` processa Jinja2 (variáveis, `if`, `for`) — use para arquivos que mudam conforme o host/ambiente.
- `copy` apenas copia o arquivo como está — use para arquivos estáticos.

---

## 11. Roles (organização e reutilização)

### Estrutura padrão de uma role

```
roles/
└── nginx/
    ├── tasks/
    │   └── main.yml          # tasks principais
    ├── handlers/
    │   └── main.yml          # handlers da role
    ├── templates/
    │   └── nginx.conf.j2
    ├── files/
    │   └── arquivo-estatico.txt
    ├── vars/
    │   └── main.yml          # variáveis fixas (alta precedência)
    ├── defaults/
    │   └── main.yml          # variáveis padrão (baixa precedência, sobrescrevíveis)
    └── meta/
        └── main.yml          # metadados e dependências de outras roles
```

### Criando uma role com scaffold automático

```bash
ansible-galaxy init roles/nginx
```

### Usando a role no playbook

```yaml
---
- name: Configurar servidores
  hosts: web
  become: true
  roles:
    - nginx
    - { role: firewall, vars: { porta_liberada: 443 } }
```

---

## 12. Ansible Galaxy (compartilhar e reutilizar código)

```bash
ansible-galaxy install geerlingguy.nginx          # instala uma role da comunidade
ansible-galaxy collection install community.docker  # instala uma collection
ansible-galaxy list                                # lista roles instaladas
ansible-galaxy init minha-role                     # cria esqueleto de uma role nova
```

Arquivo `requirements.yml` para versionar dependências do projeto:

```yaml
roles:
  - name: geerlingguy.nginx
    version: "3.1.0"
collections:
  - name: community.docker
    version: ">=3.0.0"
```

```bash
ansible-galaxy install -r requirements.yml
```

---

## 13. Ansible Vault (segredos e dados sensíveis)

```bash
ansible-vault create secrets.yml            # cria arquivo já criptografado
ansible-vault edit secrets.yml               # edita um arquivo criptografado
ansible-vault view secrets.yml                # visualiza sem editar
ansible-vault encrypt vars/producao.yml       # criptografa um arquivo existente
ansible-vault decrypt vars/producao.yml       # descriptografa
ansible-vault rekey secrets.yml               # troca a senha de criptografia

ansible-playbook site.yml --ask-vault-pass    # pede a senha na hora de rodar
ansible-playbook site.yml --vault-password-file ~/.vault_pass.txt  # lê senha de um arquivo
```

Criptografar só uma variável específica dentro de um arquivo normal:

```bash
ansible-vault encrypt_string 'senha-super-secreta' --name 'db_senha'
```

**Boa prática:** nunca commitar senhas em texto puro; sempre usar Vault para variáveis sensíveis (senhas de banco, chaves de API, tokens).

---

## 14. Tags

```yaml
tasks:
  - name: Instalar pacotes
    apt:
      name: nginx
      state: present
    tags:
      - instalacao

  - name: Configurar aplicação
    template:
      src: app.conf.j2
      dest: /etc/app/app.conf
    tags:
      - configuracao
      - deploy
```

```bash
ansible-playbook site.yml --tags "configuracao"       # roda só essas tasks
ansible-playbook site.yml --skip-tags "instalacao"    # pula essas tasks
ansible-playbook site.yml --list-tags                  # lista todas as tags do playbook
```

---

## 15. Estrutura de projeto recomendada (múltiplos ambientes)

```
projeto-ansible/
├── ansible.cfg
├── inventory/
│   ├── producao/
│   │   ├── hosts.ini
│   │   └── group_vars/
│   │       └── all.yml
│   └── homologacao/
│       ├── hosts.ini
│       └── group_vars/
│           └── all.yml
├── group_vars/
│   └── all.yml               # variáveis globais para todos os grupos
├── host_vars/
│   └── web1.exemplo.com.yml  # variáveis específicas de um host
├── roles/
│   ├── nginx/
│   ├── banco-dados/
│   └── firewall/
├── site.yml                  # playbook principal, referencia as roles
├── requirements.yml
└── secrets.yml (criptografado com vault)
```

```bash
ansible-playbook -i inventory/producao site.yml
ansible-playbook -i inventory/homologacao site.yml
```

---

## 16. Depuração e boas práticas de troubleshooting

```bash
ansible-playbook site.yml --check --diff     # simula e mostra o que mudaria, sem aplicar
ansible-playbook site.yml -vvv                # log bem detalhado (útil para debugar conexão/módulos)
ansible-doc apt                                # documentação de um módulo direto no terminal
ansible-doc -l                                 # lista todos os módulos disponíveis
ansible-lint site.yml                          # analisa o playbook em busca de más práticas (ferramenta externa)
```

```yaml
- name: Debug de variável
  debug:
    var: minha_variavel

- name: Debug de mensagem customizada
  debug:
    msg: "Valor atual: {{ minha_variavel }}"

- name: Pausar execução manualmente
  pause:
    seconds: 10
```

---

## 17. Estratégias de execução (performance)

```yaml
- hosts: web
  strategy: free          # cada host avança nas tasks no seu próprio ritmo (padrão é "linear": espera todos)
  serial: 2                 # aplica em lotes de 2 hosts por vez (deploy gradual/rolling)
  forks: 10                 # quantidade de hosts processados em paralelo (padrão do ansible.cfg é 5)
```

- `serial` é essencial em deploys de produção para rolling updates (evitar derrubar todos os servidores ao mesmo tempo).
- `forks` no `ansible.cfg` controla o paralelismo global.

---

## Tabela-resumo rápida (cola de referência)

|Preciso de...|Comando/conceito|
|---|---|
|Testar se os hosts respondem|`ansible all -m ping`|
|Rodar comando rápido em vários hosts|`ansible web -m shell -a "comando"`|
|Rodar um playbook|`ansible-playbook site.yml`|
|Simular sem aplicar|`ansible-playbook site.yml --check --diff`|
|Rodar só em um host/grupo|`ansible-playbook site.yml --limit web1`|
|Rodar só tasks específicas|`ansible-playbook site.yml --tags "deploy"`|
|Ver documentação de um módulo|`ansible-doc nome_do_modulo`|
|Criar segredo criptografado|`ansible-vault create secrets.yml`|
|Rodar playbook com vault|`ansible-playbook site.yml --ask-vault-pass`|
|Criar estrutura de role|`ansible-galaxy init roles/nome`|
|Instalar role/collection da comunidade|`ansible-galaxy install nome` / `collection install`|
|Ver todos os facts de um host|`ansible host -m setup`|
|Fazer deploy gradual (rolling)|`serial: N` no playbook|
|Reiniciar serviço só se algo mudou|`notify:` + bloco `handlers:`|

---

**Dica final:** o ciclo mais comum de um DevOps no dia a dia é: escrever/ajustar roles em `roles/`, versionar segredos com `ansible-vault`, testar com `--check --diff` antes de aplicar de verdade, e rodar com `--limit` num host de teste antes de liberar para o `all` ou usar `serial` para rollout gradual em produção. Dominando isso, a maior parte do uso prático de Ansible em operação já está coberta.

# Glossário: Terraform — Infraestrutura como Código

Referência técnica sobre o que é o Terraform, por que ele é usado, seus principais conceitos e as operações e estrutura de arquivos do dia a dia.

---

## 1. O que é e por que é usado

**Terraform** é uma ferramenta de **IaC (Infrastructure as Code — Infraestrutura como Código)**, criada pela HashiCorp. Em vez de criar servidores, redes, bancos de dados e outros recursos clicando em painéis (AWS Console, Azure Portal, etc.), você **descreve o estado desejado da infraestrutura em arquivos de texto** (linguagem própria, HCL), e o Terraform se encarrega de criar, alterar ou destruir os recursos reais para que correspondam a essa descrição.

### Por que usar Terraform (e não clicar direto no console)

|Problema sem IaC|Solução com Terraform|
|---|---|
|Infra criada manualmente não é rastreável|Código versionado no Git → histórico, revisão, rollback|
|Difícil replicar ambiente (dev, homolog, produção)|Mesmo código, variáveis diferentes → ambientes idênticos|
|Mudanças manuais geram "drift" (divergência) sem controle|`terraform plan` mostra exatamente o que vai mudar antes de aplicar|
|Multi-cloud exige aprender várias interfaces distintas|Mesma linguagem (HCL) para AWS, Azure, GCP, Kubernetes, etc.|
|Documentação da infraestrutura fica desatualizada|O próprio código É a documentação, sempre atual|

### Diferença importante: Terraform x Ansible

- **Terraform** é **declarativo e focado em provisionamento**: ele cria/gerencia o ciclo de vida de recursos de infraestrutura (VMs, redes, bancos, buckets) e mantém um "estado" de tudo que gerencia.
- **Ansible** é mais focado em **configuração** dentro dos servidores já existentes (instalar pacotes, subir serviços). É comum usar os dois juntos: Terraform cria a VM, Ansible a configura por dentro.

---

## 2. Conceitos fundamentais

|Termo|O que é|
|---|---|
|IaC|Prática de descrever infraestrutura como código, versionável e reproduzível|
|HCL (HashiCorp Configuration Language)|A linguagem de configuração usada nos arquivos `.tf`|
|Provider|Plugin que conecta o Terraform a uma plataforma (AWS, Azure, GCP, Kubernetes, Docker, GitHub...)|
|Resource|Um componente de infraestrutura gerenciado (uma VM, uma rede, um bucket, um banco de dados)|
|Data source|Consulta de informação **já existente** (não gerenciada pelo Terraform), usada como referência|
|State (estado)|Arquivo (`terraform.tfstate`) que guarda o mapeamento entre o código e os recursos reais criados|
|Backend|Onde o state é armazenado (local, S3, Terraform Cloud, Azure Blob, etc.)|
|Plan|Simulação do que vai ser criado/alterado/destruído, sem aplicar de fato|
|Apply|Execução real das mudanças planejadas|
|Module|Conjunto reutilizável de arquivos `.tf`, como uma "função" de infraestrutura|
|Variable (input)|Parâmetro configurável, evita hardcode de valores no código|
|Output|Valor exposto após o `apply` (ex: IP público de uma VM criada)|
|Workspace|Mecanismo para gerenciar múltiplos estados isolados a partir do mesmo código|
|Drift|Divergência entre o que está no código e o que realmente existe na infraestrutura|
|Provisioner|Mecanismo (menos recomendado hoje) para rodar scripts dentro do recurso recém-criado|
|Lock (state locking)|Trava que impede duas execuções simultâneas de mexerem no mesmo state ao mesmo tempo|

**Fluxo mental:** escrever código (`.tf`) → `terraform init` (baixa providers) → `terraform plan` (simula) → `terraform apply` (aplica) → estado é salvo/atualizado no `state`

---

## 3. Instalação e primeiros passos

```bash
# instalação (exemplo Linux via gerenciador de pacotes da HashiCorp, ou binário direto)
terraform version              # verifica versão instalada

mkdir meu-projeto && cd meu-projeto
touch main.tf
```

Estrutura mínima de um arquivo `main.tf`:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "servidor_web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "servidor-web"
  }
}
```

---

## 4. Principais operações (workflow)

```bash
terraform init          # baixa os providers/módulos necessários; roda 1x por projeto (ou quando providers/backend mudam)
terraform validate      # valida a sintaxe dos arquivos .tf, sem consultar a cloud
terraform fmt           # formata o código no padrão oficial (indentação, espaçamento)
terraform plan          # mostra o que SERIA criado/alterado/destruído (não aplica nada)
terraform apply         # aplica as mudanças de fato (pede confirmação, a menos que use -auto-approve)
terraform destroy       # destrói todos os recursos gerenciados por aquele state
terraform show          # mostra o state atual de forma legível
terraform state list    # lista todos os recursos rastreados no state
terraform output        # mostra os valores de output definidos
```

### Variações úteis

```bash
terraform plan -out=plano.tfplan          # salva o plano em arquivo, para aplicar depois exatamente esse plano
terraform apply plano.tfplan               # aplica um plano salvo anteriormente (mais seguro em pipelines de CI/CD)
terraform apply -auto-approve              # aplica sem pedir confirmação (uso comum em automação/CI)
terraform destroy -target=aws_instance.servidor_web   # destrói só um recurso específico
terraform apply -target=aws_instance.servidor_web     # aplica só um recurso específico
terraform apply -var="ambiente=producao"   # passa uma variável pela linha de comando
terraform apply -var-file="producao.tfvars"  # usa um arquivo de variáveis específico
```

**Regra prática de segurança:** sempre rode `terraform plan` antes de `apply` e leia a saída com atenção — ela usa `+` (criar), `-` (destruir) e `~` (modificar) para indicar o que vai acontecer. Um `-/+` (destruir e recriar) em produção merece atenção redobrada.

---

## 5. Providers

Providers são os plugins que traduzem o HCL em chamadas de API de cada plataforma.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = "us-east-1"
}
```

Exemplos comuns de providers: `hashicorp/aws`, `hashicorp/azurerm`, `hashicorp/google`, `hashicorp/kubernetes`, `hashicorp/helm`, `hashicorp/docker`, `cloudflare/cloudflare`, `hashicorp/github`.

Múltiplos providers da mesma plataforma (ex: multi-região) usam `alias`:

```hcl
provider "aws" {
  alias  = "oregon"
  region = "us-west-2"
}

resource "aws_instance" "servidor_oregon" {
  provider = aws.oregon
  # ...
}
```

---

## 6. Resources (o coração do Terraform)

```hcl
resource "<tipo_do_recurso>" "<nome_local>" {
  argumento1 = "valor"
  argumento2 = "valor"
}
```

```hcl
resource "aws_s3_bucket" "dados" {
  bucket = "meu-bucket-exemplo-2026"
}

resource "aws_security_group" "web_sg" {
  name = "permitir-http"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

- `tipo_do_recurso` é definido pelo provider (ex: `aws_instance`, `azurerm_virtual_machine`).
- `nome_local` é um apelido usado só dentro do código Terraform, para referenciar o recurso em outros lugares.

### Referenciando um recurso a partir de outro (dependência implícita)

```hcl
resource "aws_instance" "servidor" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.web_sg.id]
}
```

O Terraform detecta automaticamente que `servidor` depende de `web_sg` e cria na ordem correta.

### Dependência explícita (quando não há referência direta)

```hcl
resource "aws_instance" "servidor" {
  # ...
  depends_on = [aws_s3_bucket.dados]
}
```

---

## 7. Data Sources (consultar o que já existe)

Diferente de `resource` (que cria/gerencia algo), `data` apenas **lê** informação já existente, sem controlá-la.

```hcl
data "aws_ami" "ubuntu_mais_recente" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-*"]
  }
}

resource "aws_instance" "servidor" {
  ami           = data.aws_ami.ubuntu_mais_recente.id
  instance_type = "t2.micro"
}
```

---

## 8. Variáveis (input variables)

Arquivo `variables.tf`:

```hcl
variable "ambiente" {
  description = "Ambiente de deploy (dev, homolog, producao)"
  type        = string
  default     = "dev"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "tags_padrao" {
  type = map(string)
  default = {
    projeto = "meu-app"
  }
}
```

Usando a variável no código:

```hcl
resource "aws_instance" "servidor" {
  instance_type = var.instance_type
  tags          = var.tags_padrao
}
```

### Formas de passar valores para as variáveis (ordem de precedência, do menor para o maior)

```
default no bloco variable  →  arquivo terraform.tfvars (carregado automaticamente)  →  arquivo *.auto.tfvars  →  -var-file na linha de comando  →  -var na linha de comando  →  variável de ambiente TF_VAR_nome
```

Arquivo `terraform.tfvars`:

```hcl
ambiente      = "producao"
instance_type = "t3.medium"
```

Variável de ambiente:

```bash
export TF_VAR_instance_type="t3.large"
```

---

## 9. Outputs (valores de saída)

Arquivo `outputs.tf`:

```hcl
output "ip_publico" {
  description = "IP público do servidor criado"
  value       = aws_instance.servidor.public_ip
}

output "endpoint_banco" {
  value     = aws_db_instance.principal.endpoint
  sensitive = true    # esconde o valor no output padrão do terminal
}
```

```bash
terraform output                    # mostra todos os outputs
terraform output ip_publico          # mostra um output específico
terraform output -json               # em formato JSON (útil para consumir em scripts/CI)
```

---

## 10. State (o arquivo mais crítico do Terraform)

O `terraform.tfstate` guarda o mapeamento entre o código e os recursos reais — é como o Terraform "sabe" o que já existe.

```bash
terraform state list                          # lista recursos no state
terraform state show aws_instance.servidor    # detalhes de um recurso específico no state
terraform state mv aws_instance.antigo aws_instance.novo   # renomeia um recurso no state (sem recriar na cloud)
terraform state rm aws_instance.servidor       # remove do state SEM destruir o recurso real (ele "some" do controle do Terraform)
terraform import aws_instance.servidor i-0123456789   # traz um recurso já existente na cloud PARA dentro do state
```

**Cuidados importantes:**

- **Nunca edite o `.tfstate` manualmente.**
- **Nunca versione o `.tfstate` no Git** em texto puro — ele pode conter dados sensíveis (senhas, chaves) e gera conflitos entre pessoas do time.
- Em equipe, use sempre um **backend remoto** com **locking** (trava), para duas pessoas não aplicarem mudanças ao mesmo tempo.

### Backend remoto (exemplo com AWS S3 + DynamoDB para lock)

```hcl
terraform {
  backend "s3" {
    bucket         = "meu-bucket-terraform-state"
    key            = "projetos/app/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

Outras opções comuns de backend: Terraform Cloud/HCP Terraform, Azure Blob Storage, Google Cloud Storage.

---

## 11. Modules (reutilização de código)

Um módulo é uma pasta com arquivos `.tf` que pode ser reutilizada e parametrizada, como uma "função" de infraestrutura.

### Estrutura de um módulo

```
modulos/
└── servidor-web/
    ├── main.tf          # resources do módulo
    ├── variables.tf      # inputs que o módulo aceita
    ├── outputs.tf        # valores que o módulo expõe
    └── README.md
```

`modulos/servidor-web/main.tf`:

```hcl
resource "aws_instance" "este" {
  ami           = var.ami
  instance_type = var.tipo_instancia
  tags          = { Name = var.nome }
}
```

### Usando o módulo no projeto principal

```hcl
module "web1" {
  source         = "./modulos/servidor-web"
  ami            = "ami-0c55b159cbfafe1f0"
  tipo_instancia = "t2.micro"
  nome           = "web1"
}

module "web2" {
  source         = "./modulos/servidor-web"
  ami            = "ami-0c55b159cbfafe1f0"
  tipo_instancia = "t2.small"
  nome           = "web2"
}
```

- `source` pode ser um caminho local, um repositório Git, ou o **Terraform Registry** (`source = "terraform-aws-modules/vpc/aws"`), que tem módulos prontos e mantidos pela comunidade para praticamente qualquer caso de uso comum.

```bash
terraform get           # baixa/atualiza módulos referenciados (também roda dentro do init)
```

---

## 12. Meta-argumentos: `count` e `for_each`

Usados para criar múltiplas instâncias de um mesmo recurso sem repetir código.

### `count` (baseado em índice numérico)

```hcl
resource "aws_instance" "servidor" {
  count         = 3
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  tags = {
    Name = "servidor-${count.index}"
  }
}
```

### `for_each` (baseado em um mapa ou conjunto — mais seguro para evitar recriação acidental)

```hcl
variable "servidores" {
  type = map(string)
  default = {
    web = "t2.micro"
    api = "t2.small"
  }
}

resource "aws_instance" "servidor" {
  for_each      = var.servidores
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = each.value
  tags = {
    Name = each.key
  }
}
```

**Regra prática:** prefira `for_each` a `count` quando os itens têm identidade própria (nomes), porque remover um item do meio de uma lista com `count` pode fazer o Terraform recriar todos os recursos seguintes — com `for_each` isso não acontece.

---

## 13. Expressões condicionais e funções

```hcl
# Condicional (ternário)
instance_type = var.ambiente == "producao" ? "t3.large" : "t2.micro"

# Funções embutidas comuns
locals {
  nome_completo = "${var.projeto}-${var.ambiente}"
  lista_upper   = [for s in var.lista, upper(s)]
}
```

Funções úteis: `length()`, `join()`, `split()`, `lookup()`, `merge()`, `concat()`, `file()`, `templatefile()`, `coalesce()`.

### `locals` (valores computados/reutilizados dentro do código, não são inputs externos)

```hcl
locals {
  ambiente_tag = upper(var.ambiente)
}

resource "aws_instance" "servidor" {
  tags = {
    Ambiente = local.ambiente_tag
  }
}
```

---

## 14. Workspaces (múltiplos estados a partir do mesmo código)

```bash
terraform workspace list          # lista workspaces existentes
terraform workspace new homolog    # cria e muda para um novo workspace
terraform workspace select prod    # muda para um workspace existente
terraform workspace show           # mostra o workspace atual
```

```hcl
resource "aws_instance" "servidor" {
  tags = {
    Ambiente = terraform.workspace
  }
}
```

**Observação prática:** workspaces são úteis para variações pequenas do mesmo ambiente, mas para ambientes muito diferentes (dev/homolog/produção com configurações bem distintas), a prática mais comum no mercado é usar **pastas separadas por ambiente** com seus próprios arquivos `.tfvars` e backends, em vez de depender só de workspaces.

---

## 15. Estrutura de projeto recomendada

```
projeto-terraform/
├── ambientes/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── producao/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── backend.tf
├── modulos/
│   ├── vpc/
│   ├── servidor-web/
│   └── banco-dados/
├── .gitignore              # ignora .terraform/, *.tfstate, *.tfvars com segredo
└── README.md
```

`.gitignore` típico:

```
.terraform/
*.tfstate
*.tfstate.backup
*.tfvars
!example.tfvars
.terraform.lock.hcl
```

(Obs: algumas equipes optam por versionar o `.terraform.lock.hcl` para travar versões de provider — nesse caso ele **não** entra no `.gitignore`.)

---

## 16. Segurança e boas práticas

- **Nunca** coloque senhas/chaves diretamente no código `.tf` — use variáveis marcadas como `sensitive`, um cofre de segredos (Vault, AWS Secrets Manager) ou variáveis de ambiente.
- Use `terraform plan` sempre antes de `apply`, principalmente em produção.
- Use backend remoto com **lock** em qualquer projeto com mais de uma pessoa.
- Fixe as versões de provider (`required_providers` com `version`) para evitar quebras inesperadas.
- Separe ambientes fisicamente (pastas/backends diferentes) para reduzir o risco de aplicar em produção por engano.
- Rode `terraform fmt` e `terraform validate` no CI antes de qualquer `plan`/`apply`.
- Considere ferramentas complementares: `tflint` (lint), `checkov`/`tfsec` (segurança), `terraform-docs` (documentação automática de módulos).

```hcl
variable "senha_banco" {
  type      = string
  sensitive = true
}
```

---

## Tabela-resumo rápida (cola de referência)

| Preciso de...                                | Comando/conceito                                                     |
| -------------------------------------------- | -------------------------------------------------------------------- |
| Iniciar um projeto / baixar providers        | `terraform init`                                                     |
| Ver o que vai mudar antes de aplicar         | `terraform plan`                                                     |
| Aplicar as mudanças                          | `terraform apply`                                                    |
| Destruir tudo que o Terraform gerencia       | `terraform destroy`                                                  |
| Formatar o código                            | `terraform fmt`                                                      |
| Validar sintaxe                              | `terraform validate`                                                 |
| Ver recursos no state                        | `terraform state list`                                               |
| Trazer recurso já existente para o Terraform | `terraform import`                                                   |
| Ver valores de saída                         | `terraform output`                                                   |
| Criar recurso do tipo X                      | `resource "tipo" "nome" { ... }`                                     |
| Consultar algo já existente (sem gerenciar)  | `data "tipo" "nome" { ... }`                                         |
| Parametrizar valores                         | `variable "nome" { ... }` + `var.nome`                               |
| Reutilizar bloco de infraestrutura           | `module "nome" { source = "./caminho" }`                             |
| Criar N recursos iguais                      | `count = N` ou `for_each = mapa`                                     |
| Guardar o state em equipe, com trava         | `backend "s3" { ... }` (ou Terraform Cloud, Azure Blob, etc.)        |
| Separar ambientes com o mesmo código         | `terraform workspace` (uso pontual) ou pastas separadas (mais comum) |

---

**Dica final:** o ciclo mais comum no dia a dia é: escrever/ajustar o código em módulos reutilizáveis, rodar `terraform fmt` + `terraform validate`, revisar com `terraform plan` (ou integrar isso no Pull Request via CI), e só então `terraform apply` — de preferência com backend remoto e lock ativado. Dominando `init → plan → apply → state → module`, a maior parte do uso prático do Terraform em operação já está coberta.


# Glossário: Netmiko — Automação de Redes com Python

Referência técnica sobre o que é o Netmiko, por que é usado, seus principais conceitos e as operações e estrutura de código mais comuns em automação de rede (roteadores, switches, firewalls).

---

## 1. O que é e por que é usado

**Netmiko** é uma biblioteca Python multi-vendor (multi-fabricante) que simplifica conexões **SSH/Telnet/Serial com equipamentos de rede** (roteadores, switches, firewalls) para enviar comandos e coletar/alterar configurações via linha de comando (CLI).

Ela é construída **em cima do Paramiko** (biblioteca SSH genérica de Python), mas resolve problemas específicos de dispositivos de rede que o Paramiko puro não trata bem:

|Problema com SSH "cru" (Paramiko puro) em equipamento de rede|Solução do Netmiko|
|---|---|
|Cada fabricante (Cisco, Juniper, Huawei, Arista...) tem prompts, modos e comandos diferentes|Uma classe por `device_type`, com o comportamento específico já tratado|
|A saída do comando vem "suja" (eco do comando, paginação, prompt no final)|Netmiko detecta o prompt automaticamente, desabilita paginação e limpa a saída|
|Entrar em modo de configuração exige sequência de comandos (`configure terminal`, depois cada linha, depois `end`)|`send_config_set()` faz isso automaticamente|
|Equipamentos legados usam Telnet ou até console serial, não só SSH|Netmiko suporta os três: SSH, Telnet e Serial, com a mesma interface|
|Timeout/erro de autenticação exige tratamento específico|Exceções próprias (`NetmikoTimeoutException`, `NetmikoAuthenticationException`)|

### Por que usar Netmiko (contexto de automação de rede)

- É a ferramenta mais usada para automação **baseada em CLI** (em vez de API) em ambientes de rede tradicionais, muito comuns em datacenters e provedores de internet.
- Funciona onde não há API estruturada (NETCONF/RESTCONF) disponível — muitos equipamentos legados só têm CLI via SSH.
- É a base de ferramentas maiores como **Nornir** (orquestrador de automação de rede) e é frequentemente combinada com **TextFSM** ou **Genie parsers** para transformar saída de texto em dados estruturados (JSON/dicionário).

---

## 2. Conceitos fundamentais

|Termo|O que é|
|---|---|
|`ConnectHandler`|Função de entrada da biblioteca — recebe os dados do dispositivo e retorna um objeto de conexão|
|`device_type`|String que identifica o fabricante/SO do equipamento (ex: `cisco_ios`, `juniper_junos`)|
|Enable mode (modo privilegiado)|Nível de acesso elevado em equipamentos Cisco-like, exige senha extra (`secret`)|
|Config mode (modo de configuração)|Estado onde comandos alteram a configuração do equipamento, em vez de apenas consultá-la|
|Prompt|O texto que o equipamento mostra esperando comando (ex: `router#`) — o Netmiko usa isso para saber quando um comando terminou|
|Paging (paginação)|Comportamento padrão de CLIs de mostrar a saída "página por página" — o Netmiko desabilita isso automaticamente|
|Session log|Registro bruto de tudo que trafegou na sessão SSH, útil para depuração|
|TextFSM / Genie parser|Ferramentas usadas junto ao Netmiko para transformar saída de texto (ex: `show ip route`) em dados estruturados|
|Netmiko Exceptions|Classes de erro específicas para timeout, falha de autenticação, etc.|

**Fluxo mental:** definir dicionário do dispositivo → `ConnectHandler(**dispositivo)` (conecta) → `send_command()` / `send_config_set()` (executa) → tratar/parsear saída → `disconnect()` (encerra)

---

## 3. Instalação

```bash
pip install netmiko
```

Dependências que o Netmiko já traz junto: Paramiko (SSH), scp (transferência de arquivo), pyserial (conexão serial), textfsm (opcional, para parsing estruturado).

---

## 4. Conectando a um dispositivo

### Estrutura básica (dicionário + ConnectHandler)

```python
from netmiko import ConnectHandler

dispositivo = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "minha_senha",
    "secret": "senha_enable",   # senha do modo privilegiado, se houver
    "port": 22,                  # opcional, padrão 22
}

conexao = ConnectHandler(**dispositivo)
print(conexao.find_prompt())     # mostra o prompt atual, confirma que conectou
conexao.disconnect()             # sempre feche a conexão ao terminar
```

### Usando `with` (fecha a conexão automaticamente, boa prática)

```python
from netmiko import ConnectHandler

dispositivo = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "minha_senha",
}

with ConnectHandler(**dispositivo) as conexao:
    saida = conexao.send_command("show version")
    print(saida)
# conexão já foi fechada automaticamente aqui
```

### Principais parâmetros do dicionário de conexão

|Parâmetro|Uso|
|---|---|
|`device_type`|Obrigatório — define qual "driver" o Netmiko usa (ver seção 5)|
|`host` / `ip`|Endereço do equipamento|
|`username` / `password`|Credenciais de login|
|`secret`|Senha do modo enable (privilegiado), se diferente da senha de login|
|`port`|Porta SSH/Telnet (padrão 22 para SSH, 23 para Telnet)|
|`timeout`|Tempo máximo de espera por resposta|
|`session_log`|Caminho de arquivo para gravar tudo que trafegou na sessão (debug)|
|`use_keys` / `key_file`|Autenticação via chave SSH em vez de senha|
|`fast_cli`|Acelera conexões em massa reduzindo delays internos (usar com cautela)|
|`global_delay_factor`|Multiplica os tempos de espera internos — aumente em links lentos/VPN|

---

## 5. `device_type` (o "driver" de cada fabricante)

O `device_type` é o que diz ao Netmiko como aquele fabricante específico se comporta (prompts, comandos de paginação, sintaxe de config).

Exemplos comuns:

|Fabricante/SO|`device_type`|
|---|---|
|Cisco IOS / IOS-XE|`cisco_ios`|
|Cisco IOS-XR|`cisco_xr`|
|Cisco NX-OS|`cisco_nxos`|
|Cisco ASA|`cisco_asa`|
|Juniper Junos|`juniper_junos`|
|Arista EOS|`arista_eos`|
|HP/Aruba ProCurve|`hp_procurve`|
|Huawei|`huawei`|
|Palo Alto PAN-OS|`paloalto_panos`|
|Fortinet FortiOS|`fortinet`|
|Linux (host genérico via SSH)|`linux`|
|Genérico (fallback)|`terminal_server` / `generic_termserver`|

```bash
# ver a lista completa e atualizada de device_types suportados
python -c "from netmiko import platforms; print(platforms)"
```

**Boa prática:** sempre confira o `device_type` correto na documentação/lista atual do Netmiko, pois novas plataformas são adicionadas com frequência e nomes específicos podem variar (ex: `cisco_ios` vs `cisco_ios_telnet`).

### Autodetecção de dispositivo (quando não se sabe o `device_type`)

```python
from netmiko import SSHDetect, ConnectHandler

dispositivo = {
    "device_type": "autodetect",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "minha_senha",
}

detector = SSHDetect(**dispositivo)
tipo_detectado = detector.autodetect()
print(tipo_detectado)  # ex: 'cisco_ios'

dispositivo["device_type"] = tipo_detectado
conexao = ConnectHandler(**dispositivo)
```

---

## 6. Enviando comandos de consulta (modo `show`)

```python
saida = conexao.send_command("show ip interface brief")
print(saida)
```

- Netmiko detecta o prompt final automaticamente e retorna só a saída "limpa" (sem eco do comando, sem o prompt no fim).
- Desabilita paginação automaticamente (não precisa se preocupar com `--More--`).

### Parâmetros úteis de `send_command`

```python
saida = conexao.send_command(
    "show running-config",
    read_timeout=30,          # tempo máximo de espera pela resposta completa
    expect_string=r"#",        # string específica que indica fim da resposta
    strip_prompt=True,          # remove o prompt do final (padrão)
    strip_command=True,         # remove o eco do comando enviado (padrão)
)
```

### `send_command_timing` (baseado em tempo, não em detecção de prompt)

```python
saida = conexao.send_command_timing("show version")
```

Usado quando o dispositivo tem comportamento de prompt não padrão, ou quando um comando interativo pede confirmação (`[y/n]`) no meio da execução.

---

## 7. Enviando comandos de configuração (modo `config`)

```python
comandos = [
    "interface GigabitEthernet0/1",
    "description Conectado-ao-Switch-Core",
    "no shutdown",
]

saida = conexao.send_config_set(comandos)
print(saida)
```

- `send_config_set()` entra automaticamente em `configure terminal`, envia cada linha, e sai do modo de configuração ao final.
- Aceita lista de strings (mais comum) ou um único comando.

### A partir de um arquivo de configuração

```python
saida = conexao.send_config_from_file("configuracoes/interface_gi01.txt")
```

### Entrando/saindo do modo privilegiado (enable) manualmente

```python
conexao.enable()             # entra em modo privilegiado (usa a senha 'secret')
conexao.exit_enable_mode()   # sai do modo privilegiado
conexao.check_enable_mode()  # retorna True/False se já está em modo enable
```

---

## 8. Salvando a configuração

Cada fabricante tem sua própria forma de "gravar" a configuração em execução como configuração permanente:

```python
# Cisco IOS
conexao.save_config()               # atalho equivalente a enviar 'write memory' / 'copy run start'
```

Para fabricantes sem um método padrão embutido, envia-se o comando manualmente:

```python
conexao.send_command("write memory")
```

---

## 9. Tratamento de erros (exceções específicas)

```python
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

try:
    conexao = ConnectHandler(**dispositivo)
except NetmikoTimeoutException:
    print("Não foi possível conectar: timeout (dispositivo inacessível)")
except NetmikoAuthenticationException:
    print("Falha de autenticação: usuário/senha incorretos")
```

- `NetmikoTimeoutException` — dispositivo inacessível ou porta fechada.
- `NetmikoAuthenticationException` — usuário/senha inválidos.
- Boa prática: sempre envolver a conexão em `try/except` quando o script roda contra múltiplos dispositivos, para que uma falha em um não interrompa os demais.

---

## 10. Parsing estruturado da saída (TextFSM e Genie)

Por padrão, `send_command` retorna **texto puro**. Para transformar isso em dados estruturados (listas/dicionários), usa-se um parser.

### TextFSM (via `use_textfsm=True`)

```python
saida = conexao.send_command("show ip interface brief", use_textfsm=True)
# saida agora é uma lista de dicionários, ex:
# [{'interface': 'GigabitEthernet0/1', 'ip_address': '192.168.1.1', 'status': 'up', ...}, ...]
```

Requer que o pacote `ntc-templates` (templates TextFSM da comunidade) esteja instalado e configurado via variável de ambiente `NET_TEXTFSM`.

### Genie (parsers oficiais da Cisco, via `use_genie=True`)

```python
saida = conexao.send_command("show ip interface brief", use_genie=True)
```

Requer os pacotes `genie` e `pyats` instalados; funciona muito bem especificamente para saídas Cisco.

**Regra prática:** sem parser, você recebe texto para tratar manualmente (regex, split); com TextFSM/Genie, você recebe dados prontos para usar em lógica de programação (loops, condicionais, comparações) sem parsing manual.

---

## 11. Automatizando múltiplos dispositivos

### Sequencial simples (loop)

```python
from netmiko import ConnectHandler

dispositivos = [
    {"device_type": "cisco_ios", "host": "192.168.1.1", "username": "admin", "password": "senha"},
    {"device_type": "cisco_ios", "host": "192.168.1.2", "username": "admin", "password": "senha"},
]

for dispositivo in dispositivos:
    with ConnectHandler(**dispositivo) as conexao:
        saida = conexao.send_command("show version")
        print(f"--- {dispositivo['host']} ---")
        print(saida)
```

### Em paralelo (threading — Netmiko não é assíncrono nativamente, mas suporta multithreading)

```python
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler

def coletar_versao(dispositivo):
    with ConnectHandler(**dispositivo) as conexao:
        return dispositivo["host"], conexao.send_command("show version")

with ThreadPoolExecutor(max_workers=10) as executor:
    resultados = executor.map(coletar_versao, dispositivos)

for host, saida in resultados:
    print(host, saida)
```

**Observação:** para orquestração mais robusta em escala (inventário, grupos, execução paralela nativa, plugins), a ferramenta mais usada junto/acima do Netmiko é o **Nornir**, que usa o Netmiko como um dos seus "plugins de conexão".

---

## 12. Transferência de arquivos (SCP)

```python
from netmiko import ConnectHandler, file_transfer

conexao = ConnectHandler(**dispositivo)

resultado = file_transfer(
    conexao,
    source_file="novo_firmware.bin",
    dest_file="novo_firmware.bin",
    file_system="flash:",
    direction="put",     # 'put' envia do computador pro equipamento, 'get' faz o inverso
)
print(resultado)
```

Usado tipicamente para upload de imagens de sistema operacional (upgrade de firmware) ou backup/restauração de configuração completa.

---

## 13. Estrutura de projeto recomendada

```
automacao-rede/
├── inventario/
│   └── dispositivos.yaml        # lista de equipamentos e credenciais (não versionar senha em texto puro!)
├── scripts/
│   ├── coletar_versao.py
│   ├── configurar_interface.py
│   └── backup_configuracao.py
├── templates_config/
│   └── interface_padrao.j2      # templates Jinja2 para gerar configuração dinâmica
├── backups/
│   └── (arquivos de configuração salvos, por data/host)
├── utils/
│   └── conexao.py               # função reutilizável para criar conexões a partir do inventário
├── requirements.txt              # netmiko, textfsm, pyyaml, etc.
└── .env / vault (segredos, nunca em texto puro no repositório)
```

Exemplo de `inventario/dispositivos.yaml`:

```yaml
dispositivos:
  - nome: switch-core-01
    device_type: cisco_ios
    host: 192.168.1.1
  - nome: switch-acesso-01
    device_type: cisco_ios
    host: 192.168.1.2
```

Exemplo de `utils/conexao.py` (carregando credenciais de variável de ambiente, não hardcoded):

```python
import os
import yaml
from netmiko import ConnectHandler

def carregar_inventario(caminho="inventario/dispositivos.yaml"):
    with open(caminho) as arquivo:
        return yaml.safe_load(arquivo)["dispositivos"]

def conectar(dispositivo):
    return ConnectHandler(
        device_type=dispositivo["device_type"],
        host=dispositivo["host"],
        username=os.environ["NET_USUARIO"],
        password=os.environ["NET_SENHA"],
        secret=os.environ.get("NET_ENABLE_SENHA", ""),
    )
```

---

## 14. Gerando configuração dinâmica com Jinja2 (comum junto ao Netmiko)

```python
from jinja2 import Template

template = Template("""
interface {{ interface }}
 description {{ descricao }}
 ip address {{ ip }} {{ mascara }}
 no shutdown
""")

config_gerada = template.render(
    interface="GigabitEthernet0/1",
    descricao="Link-Uplink",
    ip="10.0.0.1",
    mascara="255.255.255.0",
)

comandos = config_gerada.strip().splitlines()
conexao.send_config_set(comandos)
```

Esse padrão (dados em YAML + template Jinja2 + Netmiko para aplicar) é a base de praticamente toda automação de configuração de rede em Python, e é o mesmo princípio usado por ferramentas maiores como Ansible (módulos `ios_config`, etc., usam Netmiko por baixo dos panos em vários casos).

---

## 15. Boas práticas e segurança

- **Nunca** deixe usuário/senha direto no código-fonte — use variáveis de ambiente, arquivos `.env` (fora do Git) ou um cofre de segredos.
- Sempre feche a conexão (`disconnect()` ou use `with`), especialmente em loops com muitos dispositivos — conexões deixadas abertas consomem sessões no equipamento.
- Use `try/except` com as exceções específicas do Netmiko ao rodar contra múltiplos equipamentos, para que um dispositivo fora do ar não pare o script inteiro.
- Prefira `send_config_set()` a montar strings de comando manualmente — reduz erro de sintaxe e de sequência de modos.
- Ative `session_log` durante o desenvolvimento/depuração para ver exatamente o que foi trocado na sessão SSH.
- Para escala (dezenas/centenas de dispositivos), migre de loops simples para **Nornir** ou paralelismo com `ThreadPoolExecutor`.
- Combine com TextFSM/Genie sempre que for **processar** a saída (comparar, gerar relatório) em vez de só exibir texto — parsear manualmente com regex é mais frágil e trabalhoso.

---

## Tabela-resumo rápida (cola de referência)

| Preciso de...                                   | Código/conceito                                                     |
| ----------------------------------------------- | ------------------------------------------------------------------- |
| Conectar a um dispositivo                       | `ConnectHandler(**dispositivo)`                                     |
| Descobrir automaticamente o tipo de dispositivo | `SSHDetect(**dispositivo).autodetect()`                             |
| Rodar um comando de consulta (`show`)           | `conexao.send_command("comando")`                                   |
| Rodar comando com timing/interação (`[y/n]`)    | `conexao.send_command_timing("comando")`                            |
| Enviar comandos de configuração                 | `conexao.send_config_set([lista_de_comandos])`                      |
| Enviar configuração a partir de arquivo         | `conexao.send_config_from_file("caminho.txt")`                      |
| Entrar em modo privilegiado (enable)            | `conexao.enable()`                                                  |
| Salvar configuração em memória permanente       | `conexao.save_config()`                                             |
| Obter dados estruturados (não texto puro)       | `send_command(..., use_textfsm=True)` ou `use_genie=True`           |
| Tratar erro de timeout/autenticação             | `except NetmikoTimeoutException` / `NetmikoAuthenticationException` |
| Automatizar vários dispositivos em paralelo     | `ThreadPoolExecutor` (ou migrar para Nornir)                        |
| Transferir arquivo (firmware/config) via SCP    | `file_transfer(conexao, ...)`                                       |
| Fechar a conexão corretamente                   | `conexao.disconnect()` ou bloco `with`                              |

---

**Dica final:** o ciclo mais comum de quem faz automação de rede no dia a dia é: definir o inventário (YAML/CSV com host + `device_type`), conectar via `ConnectHandler` dentro de um `with`, usar `send_command(..., use_textfsm=True)` para coletar dados estruturados de auditoria, e `send_config_set()` (muitas vezes gerado a partir de um template Jinja2) para aplicar mudanças em lote. Dominando esse ciclo — conectar → coletar/parsear → configurar → desconectar — cobre a maior parte do uso prático do Netmiko em operação.