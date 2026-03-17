import winreg


def get_default_browser():
    """
    Retorna 'chrome', 'edge' ou 'unknown' com base nas configurações
    de associação de protocolo HTTP do usuário no Registro do Windows.
    """
    try:
        # O caminho no registro que define a escolha do usuário para o protocolo HTTP
        path = r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
            prog_id, _ = winreg.QueryValueEx(key, "ProgId")

        prog_id = prog_id.lower()

        if "chrome" in prog_id:
            return "chrome"
        elif "edge" in prog_id:
            return "edge"
        else:
            return f"unknown ({prog_id})"

    except Exception as e:
        print(f"Erro ao identificar navegador padrão: {e}")
        return "error"
