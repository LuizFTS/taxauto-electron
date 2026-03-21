import subprocess


def aguardar_e_maximizar_jnlp(titulo_janela, timeout_segundos=30):
    ps_script = f"""
    $code = @'
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
'@
    if (-not ([Ref].Assembly.GetType("Win32.Win32Utils"))) {{
        Add-Type -MemberDefinition $code -Name "Win32Utils" -Namespace "Win32"
    }}

    # Busca a janela (Get-Process filtra automaticamente o que é visível/relevante)
    $window = Get-Process | Where-Object {{ $_.MainWindowTitle -like "*{titulo_janela}*" }} | Select-Object -First 1

    if ($window) {{
        $hwnd = $window.MainWindowHandle
        
        # 1. Traz a janela para o "estado normal" (caso esteja minimizada)
        [Win32.Win32Utils]::ShowWindow($hwnd, 9)
        
        # 2. MOVE A JANELA PARA O MONITOR PRINCIPAL (Coordenada 0,0)
        # Isso é o que resolve o problema de ela maximizar na tela errada.
        # Flags: 0x0040 (SHOWWINDOW) + 0x0001 (NOSIZE)
        [Win32.Win32Utils]::SetWindowPos($hwnd, [IntPtr]::Zero, 0, 0, 0, 0, 0x0041)
        
        # 3. Agora sim, maximiza. Como ela foi movida para 0,0, 
        # o Windows é obrigado a maximizá-la no Monitor Principal.
        [Win32.Win32Utils]::ShowWindow($hwnd, 3)
        
        # 4. Dá o foco final
        [Win32.Win32Utils]::SetForegroundWindow($hwnd)
        
        Write-Host "Janela movida para o monitor principal e maximizada."
    }} else {{
        Write-Error "Janela não encontrada."
    }}
    """

    subprocess.run(["powershell", "-Command", ps_script])


def capturar_e_preparar_janela(titulo_janela):
    # Script que retorna o Handle (HWND) da janela encontrada
    ps_script = f"""
    $window = Get-Process | Where-Object {{ $_.MainWindowTitle -like "*{titulo_janela}*" }} | Select-Object -First 1
    if ($window) {{
        $hwnd = $window.MainWindowHandle
        # Retorna apenas o número do Handle para o Python
        Write-Host $hwnd
    }}
    """
    result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)

    handle = result.stdout.strip()
    return handle if handle else None


def focar_por_handle(hwnd):
    if not hwnd:
        return

    ps_script = f"""
    $code = @'
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
'@
    $type = Add-Type -MemberDefinition $code -Name "Win32Utils" -Namespace "Win32" -PassThru
    $hwndInt = [IntPtr]{hwnd}

    [Win32.Win32Utils]::ShowWindow($hwndInt, 9)
    [Win32.Win32Utils]::SetWindowPos($hwndInt, [IntPtr]::Zero, 0, 0, 0, 0, 0x0041)
    [Win32.Win32Utils]::ShowWindow($hwndInt, 3)
    [Win32.Win32Utils]::SetForegroundWindow($hwndInt)
    """
    subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
