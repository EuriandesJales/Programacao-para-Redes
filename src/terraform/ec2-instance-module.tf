# main.tf
#
# Módulo reutilizável para provisionar uma instância EC2 dentro de uma
# VPC, com Security Group dedicado. Esse é um dos padrões mais comuns
# do dia a dia: em vez de repetir o mesmo bloco de recursos em cada
# projeto, você cria um módulo e reusa com variáveis diferentes.
#
# Estrutura de pastas sugerida:
#   modules/
#     ec2-instance/
#       main.tf        <- este arquivo
#       variables.tf
#       outputs.tf
#   environments/
#     production/
#       main.tf         <- chama o módulo (veja exemplo de uso no final)

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_security_group" "instance_sg" {
  name        = "${var.name}-sg"
  description = "Security group para ${var.name}"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.allowed_ports
    content {
      description = "Permitir porta ${ingress.value}"
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = var.allowed_cidr_blocks
    }
  }

  egress {
    description = "Permitir todo tráfego de saída"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-sg"
  }
}

resource "aws_instance" "this" {
  ami                    = var.ami_id != "" ? var.ami_id : data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.instance_sg.id]
  key_name               = var.key_name

  root_block_device {
    volume_size = var.root_volume_size
    volume_type = "gp3"
    encrypted   = true
  }

  user_data = var.user_data

  tags = {
    Name = var.name
  }

  lifecycle {
    create_before_destroy = true
  }
}

# --- variables.tf (mesmo arquivo, por simplicidade) ---

variable "name" {
  description = "Nome base para os recursos criados"
  type        = string
}

variable "vpc_id" {
  description = "ID da VPC onde os recursos serão criados"
  type        = string
}

variable "subnet_id" {
  description = "ID da subnet onde a instância será criada"
  type        = string
}

variable "instance_type" {
  description = "Tipo da instância EC2"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI customizada (deixe vazio para usar Amazon Linux mais recente)"
  type        = string
  default     = ""
}

variable "key_name" {
  description = "Nome do key pair SSH para acesso à instância"
  type        = string
}

variable "allowed_ports" {
  description = "Lista de portas TCP liberadas no security group"
  type        = list(number)
  default     = [22, 443]
}

variable "allowed_cidr_blocks" {
  description = "CIDRs permitidos a acessar as portas liberadas"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "root_volume_size" {
  description = "Tamanho do disco raiz em GB"
  type        = number
  default     = 20
}

variable "user_data" {
  description = "Script de inicialização (cloud-init) da instância"
  type        = string
  default     = ""
}

# --- outputs.tf (mesmo arquivo, por simplicidade) ---

output "instance_id" {
  description = "ID da instância EC2 criada"
  value       = aws_instance.this.id
}

output "public_ip" {
  description = "IP público da instância"
  value       = aws_instance.this.public_ip
}

output "security_group_id" {
  description = "ID do security group criado"
  value       = aws_security_group.instance_sg.id
}

# --- Exemplo de uso do módulo (em environments/production/main.tf) ---
#
# module "api_server" {
#   source        = "../../modules/ec2-instance"
#   name          = "minha-api-producao"
#   vpc_id        = "vpc-0123456789abcdef0"
#   subnet_id     = "subnet-0123456789abcdef0"
#   instance_type = "t3.medium"
#   key_name      = "minha-chave-ssh"
#   allowed_ports = [22, 80, 443]
# }
#
# output "api_public_ip" {
#   value = module.api_server.public_ip
# }
