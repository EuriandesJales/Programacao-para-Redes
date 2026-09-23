import hashlib
from urllib.parse import urlparse
import dns.resolver
import requests

""" Ferramenta de busca de domínios de phishing """

# Dicionário simples de substituição de homóglifos/caracteres visualmente similares
HOMOGLYPHS = {"a": ["4", "à"], "e": ["3"], "i": ["1", "l"], "o": ["0"], "s": ["5"]}


def calcular_hash_favicon(url_favicon: str) -> str | None:
    """Baixa o favicon e calcula o hash SHA-256 do arquivo."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Defensive-Brand-Protection-Bot/1.0)"
    }
    try:
        response = requests.get(url_favicon, headers=headers, timeout=5)
        if response.status_code == 200:
            return hashlib.sha256(response.content).hexdigest()
    except requests.RequestException:
        return None
    return None


def gerar_variacoes_dominios(dominio_base: str) -> set[str]:
    """Gera variações básicas do domínio para auditoria."""
    variacoes = set()
    nome, tld = dominio_base.split(".")[0], ".".join(dominio_base.split(".")[1:])

    # 1. Adição de sufixos comuns em phishing
    sufixos = ["login", "portal", "suporte", "secure"]
    for suf in sufixos:
        variacoes.add(f"{nome}-{suf}.{tld}")
        variacoes.add(f"{nome}{suf}.{tld}")

    # 2. Substituição por caracteres similares (Typosquatting)
    for i, char in enumerate(nome):
        if char in HOMOGLYPHS:
            for sub in HOMOGLYPHS[char]:
                novo_nome = nome[:i] + sub + nome[i + 1 :]
                variacoes.add(f"{novo_nome}.{tld}")

    return variacoes


def verificar_dominios(dominio_alvo: str, hash_favicon_referencia: str):
    """Resolve os domínios gerados e compara o favicon se estiverem ativos."""
    candidatos = gerar_variacoes_dominios(dominio_alvo)
    print(
        f"[*] Analisando {len(candidatos)} variações para o domínio: {dominio_alvo}\n"
    )

    for dominio in candidatos:
        # Checa se o domínio possui registro DNS ativo
        try:
            dns.resolver.resolve(dominio, "A")
            print(f"[!] Domínio ATIVO encontrado no DNS: {dominio}")

            # Tenta baixar o favicon
            url_favicon = f"http://{dominio}/favicon.ico"
            hash_encontrado = calcular_hash_favicon(url_favicon)

            if hash_encontrado:
                if hash_encontrado == hash_favicon_referencia:
                    print(
                        f"  └── [ALERTA CRÍTICO] Favicon IDÊNTICO detectado em http://{dominio}!"
                    )
                else:
                    print(
                        f"  └── Favicon presente, mas com hash diferente ({hash_encontrado[:10]}...)"
                    )
            else:
                print("  └── Não foi possível obter o favicon via HTTP.")

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
            # Domínio não registrado ou sem apontamento A
            continue


if __name__ == "__main__":
    # Exemplo de Execução:
    # 1. Domínio da empresa
    DOMINIO_EMPRESA = "exemplo.com.br"

    # 2. Hash SHA-256 pré-calculado do favicon legítimo
    # Exemplo de como gerar o hash no Linux: curl -s http://exemplo.com.br/favicon.ico | sha256sum
    HASH_REFERENCIA = (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )

    verificar_dominios(DOMINIO_EMPRESA, HASH_REFERENCIA)