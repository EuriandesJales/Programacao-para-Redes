import csv
import os
import shutil
from datetime import datetime
from pathlib import Path


def backup_configuracoes(caminho_csv: str, diretorio_destino: str) -> None:
    """Realiza o backup dos arquivos de configuracao listados em um CSV.

    :param caminho_csv: Caminho para o arquivo CSV contendo os softwares e
      caminhos.
    :param diretorio_destino: Diretorio onde os backups serao armazenados.
    """
    csv_path = Path(caminho_csv).resolve()
    destino_path = Path(diretorio_destino).resolve()

    # Valida existencia do CSV
    if not csv_path.is_file():
        print(f"[ERRO] O arquivo CSV '{csv_path}' nao foi encontrado.")
        return

    # Garante a existencia do diretorio de destino
    try:
        destino_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(
            f"[ERRO] Falha ao criar diretorio de destino '{destino_path}': {e}"
        )
        return

    # Abertura e parsing do CSV
    try:
        with open(csv_path, mode="r", encoding="utf-8") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)

            for linha in leitor:
                # Ignora linhas vazias ou malformatadas
                if not linha or len(linha) < 2:
                    continue

                software = linha[0].strip()
                caminho_origem_str = linha[1].strip()

                # Ignora cabecalho caso exista
                if software.lower() == "software" or caminho_origem_str.lower() in [
                    "caminho",
                    "path",
                ]:
                    continue

                # Notificacao do inicio da operacao
                print(f"Salvando arquivo de configuracao do {software}...")

                # Expande til (~) se houver e resolve o caminho
                origem_path = Path(caminho_origem_str).expanduser().resolve()

                # Checa se o arquivo/diretorio de origem realmente existe
                if not origem_path.exists():
                    print(
                        f"  └─ [AVISO] Origem nao encontrada para {software}: '{origem_path}'"
                    )
                    continue

                # Define o destino (ex: destino/zsh/.zshrc ou destino/zsh_config)
                # Mantem o nome do arquivo original dentro de uma pasta dedicada ao software
                pasta_destino_software = destino_path / software.lower()
                pasta_destino_software.mkdir(parents=True, exist_ok=True)

                try:
                    if origem_path.is_file():
                        shutil.copy2(
                            origem_path,
                            pasta_destino_software / origem_path.name,
                        )
                    elif origem_path.is_dir():
                        destino_dir = pasta_destino_software / origem_path.name
                        shutil.copytree(
                            origem_path, destino_dir, dirs_exist_ok=True
                        )

                    print(f"  └─ [SUCESSO] Backup concluido.")

                except (PermissionError, OSError) as err:
                    print(
                        f"  └─ [ERRO] Falha ao copiar configuracao do {software}: {err}"
                    )

    except Exception as err_file:
        print(f"[ERRO] Falha na leitura do arquivo CSV: {err_file}")


# Exemplo de uso pratico
if __name__ == "__main__":
    # Exemplo de chamada da funcao
    CSV_INPUT = "apps.csv"
    DEST_DIR = f"./backups_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    backup_configuracoes(caminho_csv=CSV_INPUT, diretorio_destino=DEST_DIR)