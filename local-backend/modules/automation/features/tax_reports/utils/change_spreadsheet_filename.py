import glob
import os
import time


def resolve_unique_filepath(directory, base_name):
    """Garante que não sobrescreva se o arquivo já existir."""
    filename = f"{base_name}.csv"
    path = os.path.join(directory, filename)
    counter = 1
    while os.path.exists(path):
        counter += 1
        path = os.path.join(directory, f"{base_name}_{counter}.csv")
    return path


def wait_for_file_ready(filepath, timeout=15):
    """Espera o arquivo existir e não estar mais sendo escrito (tamanho estável)."""
    start_time = time.time()
    last_size = -1

    while time.time() - start_time < timeout:
        if os.path.exists(filepath):
            current_size = os.path.getsize(filepath)
            if current_size > 0 and current_size == last_size:
                return True  # Arquivo existe e parou de crescer
            last_size = current_size
        time.sleep(1)
    return False


def rename_with_retry(latest_file, new_file_path, retries=5, delay=1):
    # Primeiro: Esperamos o arquivo de ORIGEM ficar pronto
    if not wait_for_file_ready(latest_file):
        print(f"[ERROR] O arquivo original {latest_file} não ficou pronto a tempo.")
        return None

    for i in range(retries):
        try:
            os.rename(latest_file, new_file_path)
            print(f"[SUCCESS] {os.path.basename(latest_file)} -> {os.path.basename(new_file_path)}")
            return new_file_path
        except OSError as e:
            if getattr(e, "winerror", None) == 32:  # Arquivo em uso
                print(f"[RETRY {i+1}/{retries}] Bloqueado, tentando em {delay}s...")
                time.sleep(delay)
            else:
                raise e
    return None


def change_spreadsheet_filename(directory_path: str, base_name: str) -> str | None:
    # 1. Busca arquivos CSV
    files = glob.glob(os.path.join(directory_path, "*.csv"))

    # Filtro importante: Ignorar arquivos que já foram renomeados (que terminam com _SAIDA.csv)
    # para não pegar o arquivo da filial anterior por erro de timestamp
    pending_files = [f for f in files if "EMISSAO" in os.path.basename(f)]

    if not pending_files:
        print(f"[ERROR] Nenhum download pendente encontrado em: {directory_path}")
        return None

    # 2. Pega o mais recente dos pendentes
    latest_file = max(pending_files, key=os.path.getmtime)

    # 3. Resolve nome único (evita sobrescrever 1_SAIDA.csv se ele já existir)
    new_file_path = resolve_unique_filepath(directory_path, base_name)

    # 4. Tenta renomear
    return rename_with_retry(latest_file, new_file_path)
