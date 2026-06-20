import logging
import subprocess
import time
from time import sleep

import nazm as a
import nazm.capture as c

logger = logging.getLogger(__name__)


class ERPSession:
    def __init__(self, titulo="Portal Casa do Adubo"):
        self.titulo = titulo
        self.hwnd = None

    def _execute_ps(self, script: str):
        """Helper para executar PowerShell e capturar saída."""
        return subprocess.run(
            ["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True
        )

    def get_window(self, timeout=10):
        """Busca o HWND com lógica de retry (importante para Apps Java)."""
        start_time = time.time()
        ps_script = f"""
        $win = Get-Process | Where-Object {{ $_.MainWindowTitle -like "*{self.titulo}*" }} | Select-Object -First 1
        if ($win) {{ $win.MainWindowHandle }}
        """

        while (time.time() - start_time) < timeout:
            result = self._execute_ps(ps_script)
            handle = result.stdout.strip()
            if handle and handle != "0":
                return handle
            time.sleep(1)
        return None

    def open(self):
        """Inicializa a sessão encontrando a janela."""
        logger.info(f"[ERP] Abrindo janela: {self.titulo}...")
        self.hwnd = self.get_window()
        if self.hwnd:
            self.focus()

            sleep(1.5)
            self._identify_homepage()

            return True
        logger.error("[ERP] Erro: Janela não encontrada.")
        return False

    def focus(self):
        """Foca na janela usando o HWND salvo."""
        if not self.hwnd:
            # Tenta re-capturar se o hwnd sumiu
            if not self.open():
                return

        ps_script = f"""
        $code = @'
            [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
            [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
            [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hAfter, int x, int y, int cx, int cy, uint f);
'@
        if (-not ([Ref].Assembly.GetType("Win32.Win32Utils"))) {{
            Add-Type -MemberDefinition $code -Name "Win32Utils" -Namespace "Win32"
        }}
        
        $h = [IntPtr]{self.hwnd}
        [Win32.Win32Utils]::ShowWindow($h, 9)
        [Win32.Win32Utils]::SetWindowPos($h, [IntPtr]::Zero, 0, 0, 0, 0, 0x0041)
        [Win32.Win32Utils]::ShowWindow($h, 3)
        [Win32.Win32Utils]::SetForegroundWindow($h)
        """
        self._execute_ps(ps_script)

    def close(self):
        """Opcional: Fecha o processo do ERP se necessário."""
        if self.hwnd:
            self._execute_ps(
                f"Stop-Process -Id (Get-Process | Where-Object {{ $_.MainWindowHandle -eq {self.hwnd} }}).Id -Force"
            )
            self.hwnd = None

    def _identify_homepage(self):
        t = c.load_templates()

        result = a.wait_for(t.erp_home)

        # result is a tupple (bool, int,int)
        if result[0]:
            logger.info("[ERP] Página inicial identificada.")
            return True
        else:
            logger.error("[ERP] Erro ao identificar página inicial.")
            raise Exception("Erro ao identificar página inicial.")
