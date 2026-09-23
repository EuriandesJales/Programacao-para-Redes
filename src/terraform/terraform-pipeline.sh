#!/usr/bin/env bash
#
# terraform-pipeline.sh
#
# Wrapper de segurança para rodar Terraform em CI/CD ou localmente.
# Padroniza o fluxo fmt -> validate -> plan -> apply, com proteções
# comuns no dia a dia:
#   - Nunca aplica sem antes gerar e revisar um plano salvo em arquivo
#   - Exige confirmação explícita para "apply" em produção
#   - Falha rápido (set -euo pipefail) se qualquer comando der erro
#   - Suporta múltiplos ambientes via workspace
#
# Uso:
#   ./terraform-pipeline.sh plan production
#   ./terraform-pipeline.sh apply production
#   ./terraform-pipeline.sh destroy dev
#
# Em pipelines de CI, normalmente você roda "plan" no pull request
# e "apply" só depois de aprovação (merge na branch principal).

set -euo pipefail

ACTION="${1:-}"
ENVIRONMENT="${2:-}"
PLAN_FILE="tfplan-${ENVIRONMENT}.out"

if [[ -z "$ACTION" || -z "$ENVIRONMENT" ]]; then
  echo "Uso: $0 <plan|apply|destroy> <ambiente>"
  echo "Exemplo: $0 plan production"
  exit 1
fi

log() {
  echo "[terraform-pipeline] $1"
}

select_workspace() {
  log "Selecionando workspace: $ENVIRONMENT"
  terraform workspace select "$ENVIRONMENT" 2>/dev/null || terraform workspace new "$ENVIRONMENT"
}

run_fmt_and_validate() {
  log "Verificando formatação (terraform fmt -check)..."
  if ! terraform fmt -check -recursive; then
    log "❌ Código fora do padrão de formatação. Rode 'terraform fmt -recursive' e commite."
    exit 1
  fi

  log "Validando configuração (terraform validate)..."
  terraform validate
}

run_plan() {
  log "Gerando plano para o ambiente '$ENVIRONMENT'..."
  terraform plan \
    -var="environment=${ENVIRONMENT}" \
    -out="$PLAN_FILE"
  log "✅ Plano salvo em $PLAN_FILE. Revise antes de aplicar."
}

run_apply() {
  if [[ ! -f "$PLAN_FILE" ]]; then
    log "❌ Nenhum plano encontrado ($PLAN_FILE). Rode '$0 plan $ENVIRONMENT' primeiro."
    exit 1
  fi

  if [[ "$ENVIRONMENT" == "production" ]]; then
    log "⚠️  Você está prestes a aplicar mudanças em PRODUÇÃO."
    read -r -p "Digite 'aplicar' para confirmar: " confirmacao
    if [[ "$confirmacao" != "aplicar" ]]; then
      log "Cancelado pelo usuário."
      exit 1
    fi
  fi

  log "Aplicando plano salvo ($PLAN_FILE)..."
  terraform apply "$PLAN_FILE"
  rm -f "$PLAN_FILE"
  log "✅ Apply concluído com sucesso."
}

run_destroy() {
  log "⚠️  Você está prestes a DESTRUIR recursos no ambiente '$ENVIRONMENT'."
  read -r -p "Digite o nome do ambiente novamente para confirmar ('$ENVIRONMENT'): " confirmacao
  if [[ "$confirmacao" != "$ENVIRONMENT" ]]; then
    log "Cancelado pelo usuário."
    exit 1
  fi

  terraform destroy -var="environment=${ENVIRONMENT}"
  log "Recursos destruídos."
}

select_workspace
run_fmt_and_validate

case "$ACTION" in
  plan)
    run_plan
    ;;
  apply)
    run_apply
    ;;
  destroy)
    run_destroy
    ;;
  *)
    log "Ação inválida: $ACTION. Use plan, apply ou destroy."
    exit 1
    ;;
esac
