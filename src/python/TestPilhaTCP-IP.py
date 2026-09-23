import platform
import socket
import subprocess
import sys


class TCPIPStackDiagnoser:

    def __init__(self, target_host="8.8.8.8", target_domain="google.com"):
        self.target_host = target_host
        self.target_domain = target_domain
        self.os_type = platform.system().lower()

    def _exec_cmd(self, cmd):
        try:
            res = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3
            )
            return res.returncode == 0
        except Exception:
            return False

    def test_layer1_2_interface(self):
        """Camada 1/2: Valida se há interface de rede física/loopback ativa."""
        print("[1/5] Testando Camada 1/2 (Interface & Loopback)...")

        # Teste de Loopback (Valida se o driver TCP/IP do SO está carregado)
        loopback_ip = "127.0.0.1"
        param = "-n" if self.os_type == "windows" else "-c"
        cmd = ["ping", param, "1", loopback_ip]

        if self._exec_cmd(cmd):
            print("  └─ [OK] Pilha TCP/IP local e Loopback (127.0.0.1) ativos.")
            return True
        else:
            print(
                "  └─ [FALHA] Falha na pilha local TCP/IP ou na interface de loopback."
            )
            return False

    def test_layer3_gateway_internet(self):
        """Camada 3 (Rede): Valida roteamento e conectividade ICMP/IP externa."""
        print("[2/5] Testando Camada 3 (Rede / Roteamento IP)...")

        param = "-n" if self.os_type == "windows" else "-c"
        cmd = ["ping", param, "2", self.target_host]

        if self._exec_cmd(cmd):
            print(
                f"  └─ [OK] Conectividade de Camada 3 estabelecida com {self.target_host}."
            )
            return True
        else:
            print(
                f"  └─ [FALHA] Sem alcance de Camada 3 para {self.target_host}. Verifique Gateway/Roteamento."
            )
            return False

    def test_layer4_transport(self, port=53):
        """Camada 4 (Transporte): Valida socket TCP/UDP e handshake na porta de transporte."""
        print(
            f"[3/5] Testando Camada 4 (Transporte / Handshake TCP na porta {port})..."
        )

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)

        try:
            result = sock.connect_ex((self.target_host, port))
            sock.close()

            if result == 0:
                print(
                    f"  └─ [OK] Socket TCP aberto com sucesso em {self.target_host}:{port}."
                )
                return True
            else:
                print(
                    f"  └─ [FALHA] Falha no handshake TCP com {self.target_host}:{port} (Código erro: {result})."
                )
                return False
        except Exception as e:
            print(f"  └─ [FALHA] Erro de transporte: {e}")
            return False

    def test_dns_resolution(self):
        """Camada 7 (DNS / Resolução de Nomes)."""
        print(
            f"[4/5] Testando Resolução DNS (Aplicação) para {self.target_domain}..."
        )

        try:
            ip_resolved = socket.gethostbyname(self.target_domain)
            print(
                f"  └─ [OK] Nome {self.target_domain} resolvido para {ip_resolved}."
            )
            return True
        except socket.gaierror:
            print(
                f"  └─ [FALHA] Não foi possível resolver o domínio {self.target_domain}. Falha no DNS."
            )
            return False

    def test_layer7_application(self):
        """Camada 7 (Aplicação HTTP/HTTPS)."""
        print("[5/5] Testando Camada 7 (Aplicação HTTP/HTTPS)...")

        try:
            import urllib.request

            req = urllib.request.Request(
                f"https://{self.target_domain}",
                headers={"User-Agent": "TCPIP-Diagnoser/1.0"},
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    print(
                        "  └─ [OK] Requisição HTTP/HTTPS concluída com status 200 OK."
                    )
                    return True
                else:
                    print(
                        f"  └─ [AVISO] Resposta da aplicação com código HTTP {response.status}."
                    )
                    return True
        except Exception as e:
            print(f"  └─ [FALHA] Falha na Camada de Aplicação (HTTP): {e}")
            return False

    def run_diagnostics(self):
        print(f"=== INICIANDO DIAGNÓSTICO DA PILHA TCP/IP ===")
        print(
            f"Alvos de Teste: IP {self.target_host} | Domínio: {self.target_domain}\n"
        )

        # Abordagem isolada para identificar o ponto exato da falha
        l1_2 = self.test_layer1_2_interface()
        if not l1_2:
            print(
                "\n[DIAGNÓSTICO FINAL] Falha detectada na camada local (Drivers/Interface)."
            )
            return

        l3 = self.test_layer3_gateway_internet()
        if not l3:
            print(
                "\n[DIAGNÓSTICO FINAL] Falha detectada na Camada 3 (Roteamento/IP/Gateway)."
            )
            return

        l4 = self.test_layer4_transport()
        if not l4:
            print(
                "\n[DIAGNÓSTICO FINAL] Falha detectada na Camada 4 (Bloqueio de Porta TCP/Firewall)."
            )
            return

        dns = self.test_dns_resolution()
        if not dns:
            print(
                "\n[DIAGNÓSTICO FINAL] Falha detectada no Serviço de DNS (Servidor DNS inacessível ou incorreto)."
            )
            return

        l7 = self.test_layer7_application()
        if not l7:
            print(
                "\n[DIAGNÓSTICO FINAL] Falha detectada na Camada 7 (Protocolo de Aplicação/Proxy/WAF)."
            )
            return

        print(
            "\n[DIAGNÓSTICO FINAL] A pilha TCP/IP está 100% operacional e sem falhas encontradas."
        )


if __name__ == "__main__":
    diagnoser = TCPIPStackDiagnoser()
    diagnoser.run_diagnostics()