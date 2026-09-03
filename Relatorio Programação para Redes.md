## Glossario bash script

```Bash

# Declaração de variaveis
Nome="Euriandes"
local PORTA=20 # var local restrita para funções
readonly COSTANTE=1 # Imutável uma tupal

# Coleções
declare -a LISTA=("item1" "Item2" "Item3")
Lista+=("Item4") # Operação de adição em uma lista
echo "${LISTA[0]}" # sintaxe de acesso a uma lista
echo "${LISTA[@]}"  # mostra todos os elementos a lista
echo "${#LISTA[]}"  # retorna o tamanho do array

# Array Assosiativos (Dicionario)
declare -A DICIONARIO
DICIONARIO=( ["IP"]="192.168.0.1" ["PORTA"]="20")
DICIONARIO["USER"]="euriandes" #atribuição
echo "${DICIONARIO[ip]}"

```