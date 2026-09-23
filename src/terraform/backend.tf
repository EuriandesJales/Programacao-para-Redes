# backend.tf
#
# Configuração de backend remoto para o Terraform state.
# Usar backend remoto (em vez de state local) é praticamente obrigatório
# em qualquer time, porque:
#   - Evita conflitos quando mais de uma pessoa/pipeline roda terraform apply
#   - Guarda o state de forma durável (não fica só na máquina de alguém)
#   - O DynamoDB garante state locking: evita dois applies simultâneos
#     corromperem o state
#
# Pré-requisitos (crie uma vez, fora do Terraform ou em um projeto "bootstrap"):
#   - Bucket S3 com versionamento habilitado
#   - Tabela DynamoDB com chave de partição "LockID" (tipo String)

terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket         = "minha-empresa-terraform-state"
    key            = "projetos/minha-api/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      ManagedBy   = "terraform"
      Environment = var.environment
      Project     = var.project_name
    }
  }
}

# --- variables.tf (mesmo arquivo, por simplicidade) ---

variable "aws_region" {
  description = "Região AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente de deploy (dev, staging, production)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "environment deve ser: dev, staging ou production."
  }
}

variable "project_name" {
  description = "Nome do projeto, usado em tags e nomes de recursos"
  type        = string
}

# --- Exemplo de uso com múltiplos ambientes ---
#
# Rode assim para cada ambiente, usando workspaces ou diretórios separados:
#
#   terraform workspace new production
#   terraform workspace select production
#   terraform apply -var="environment=production" -var="project_name=minha-api"
#
# Ou, se preferir diretórios separados (mais explícito, evita erro humano):
#   environments/
#     dev/main.tf        (com sua própria key no backend, ex: "projetos/minha-api/dev/terraform.tfstate")
#     production/main.tf (key: "projetos/minha-api/production/terraform.tfstate")
