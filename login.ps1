# Definimos o User-Agent globalmente para a sessão parecer um navegador real
$ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"

# 1. Iniciar a sessão e capturar o ViewState inicial
$urlLogin = "http://100.126.64.15:8080/adged/login.xhtml"
$resInicial = Invoke-WebRequest -Uri $urlLogin -SessionVariable "sessaoAdged" -UserAgent $ua

# Extrair o ViewState dinâmico da página de login
$vsLogin = ($resInicial.InputFields | Where-Object { $_.name -eq "javax.faces.ViewState" }).value

# 2. Realizar o Login
$bodyLogin = @{
    "formLogin" = "formLogin"
    "formLogin:usuario" = "DEFIS_AUX20"
    "formLogin:senha" = "lfT#1020304050"
    "javax.faces.ViewState" = $vsLogin
    "formLogin:btnLogar" = "" # Certifique-se que este é o nome real do botão
}

# Faz o POST de login
# O parâmetro -PassThru permite que a gente veja se o login redirecionou (sucesso)
$resLogin = Invoke-WebRequest -Uri $urlLogin `
                  -Method "POST" `
                  -Body $bodyLogin `
                  -WebSession $sessaoAdged `
                  -UserAgent $ua

# 3. Acessar a página de relatório para pegar o NOVO ViewState
$urlRelatorio = "http://100.126.64.15:8080/adged/relatorio.xhtml"
$paginaRelatorio = Invoke-WebRequest -Uri $urlRelatorio `
                                     -Method "GET" `
                                     -WebSession $sessaoAdged `
                                     -UserAgent $ua

$vsRelatorio = ($paginaRelatorio.InputFields | Where-Object { $_.name -eq "javax.faces.ViewState" }).value

# 4. Montagem dos Headers e Body para o Download
$headersDownload = @{
    "Origin"="http://100.126.64.15:8080"
    "Referer"=$urlRelatorio
}

# Usamos o operador -join para manter o Body limpo e sem espaços extras acidentais
$bodyParts = @(
    "formCadastro=formCadastro",
    "formCadastro%3AbtnGerarRelatorio=",
    "formCadastro%3AdtPeriodoInicio_input=20%2F03%2F2026",
    "formCadastro%3AdtPeriodoFinal_input=20%2F03%2F2026",
    "formCadastro%3Arelatorio=STATUS_NFE",
    "formCadastro%3Aj_idt83=0",
    "formCadastro%3Astatus=2", "formCadastro%3Astatus=3", "formCadastro%3Astatus=4", "formCadastro%3Astatus=5",
    "formCadastro%3AtpDoc=XLSX",
    "formCadastro%3ArelatorioTable%3Atable%3Aj_idt104%3Afilter=",
    "formCadastro%3ArelatorioTable%3Atable_selection=20",
    "formCadastro%3ArelatorioTable%3Atable_scrollState=0%2C0",
    "javax.faces.ViewState=$([System.Web.HttpUtility]::UrlEncode($vsRelatorio))"
)
$bodyDownload = $bodyParts -join "&"

# 5. Executamos o download final
Invoke-WebRequest -UseBasicParsing -Uri $urlRelatorio `
    -Method "POST" `
    -WebSession $sessaoAdged `
    -Headers $headersDownload `
    -ContentType "application/x-www-form-urlencoded" `
    -Body $bodyDownload `
    -UserAgent $ua `
    -OutFile "C:\Users\lu9887091\Downloads\relatorio.xls"

Write-Host "Processo finalizado!" -ForegroundColor Cyan