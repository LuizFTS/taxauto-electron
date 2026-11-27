$body = @{
    start_date = "01/10/2026"
    end_date = "10/10/2026"
    filiais = @("02")
    save_path = "C:\Users\lu9887091\AppData\Local\Temp"
    login = "DEFIS_AUX20"
    password = "lfT#1020304050"
    tipo_documento = 30
    tipo_operacao = 1
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/automation/download-xmls/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"