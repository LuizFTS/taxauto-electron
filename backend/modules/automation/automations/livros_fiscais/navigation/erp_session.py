import pygetwindow as gw
import win32gui
import win32con

class ERPSession:

    def _focar_e_maximizar(self, titulo_janela):
        # 1. Busca todas as janelas que contenham o título
        janelas = gw.getWindowsWithTitle(titulo_janela)
        
        if not janelas:
            print(f"Nenhuma janela com o título '{titulo_janela}' encontrada.")
            return

        print(f"Encontradas {len(janelas)} janelas. Focando na primeira...")
        
        # 2. Seleciona a primeira (ou você pode iterar se quiser uma específica)
        janela = janelas[0] 
        hwnd = janela._hWnd # Pega o Handle da janela para usar com win32gui

        try:
            # 3. Forçar a restauração caso esteja minimizada
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            
            # 4. Trazer para o topo (Hack para ignorar restrição do Windows)
            win32gui.SetVariantPart(hwnd) # Remove o "ghosting"
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(hwnd)
            
            # 5. Maximizar na tela principal
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            
            print(f"Janela '{janela.title}' movida para tela principal e focada.")
            
        except Exception as e:
            print(f"Erro ao tentar focar janela: {e}")

    def open(self):
        self._focar_e_maximizar("Portal Casa do Adubo")

    def close(self):
        pass