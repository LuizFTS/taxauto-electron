$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
$session.Cookies.Add((New-Object System.Net.Cookie("JSESSIONID", "c4c1c38d4b6964bdd7ebc81d996d", "/", "100.126.64.15")))
$result = Invoke-WebRequest -UseBasicParsing -Uri "http://100.126.64.15:8080/adged/relatorio.xhtml" `
-Method "POST" `
-WebSession $session `
-Headers @{
"Accept"="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
  "Accept-Encoding"="gzip, deflate"
  "Accept-Language"="pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
  "Cache-Control"="max-age=0"
  "Origin"="http://100.126.64.15:8080"
  "Referer"="http://100.126.64.15:8080/adged/relatorio.xhtml"
  "Upgrade-Insecure-Requests"="1"
} `
-ContentType "application/x-www-form-urlencoded" `
-Body "formCadastro=formCadastro&formCadastro%3AbtnGerarRelatorio=&formCadastro%3AdtPeriodoInicio_input=20%2F03%2F2026&formCadastro%3AdtPeriodoFinal_input=20%2F03%2F2026&formCadastro%3Arelatorio=STATUS_NFE&formCadastro%3Aj_idt83=0&formCadastro%3Astatus=2&formCadastro%3Astatus=3&formCadastro%3Astatus=4&formCadastro%3Astatus=5&formCadastro%3AtpDoc=XLSX&formCadastro%3ArelatorioTable%3Atable%3Aj_idt104%3Afilter=&formCadastro%3ArelatorioTable%3Atable_selection=20&formCadastro%3ArelatorioTable%3Atable_scrollState=0%2C0&javax.faces.ViewState=-9205125149222468615%3A8512612224583933490" `
-OutFile "C:\Users\lu9887091\Downloads\relatorio.xls"