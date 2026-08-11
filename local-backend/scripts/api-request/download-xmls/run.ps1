$body = @{
    start_date = "12/06/2026"
    end_date = "27/07/2026"
    filiais = @("45")
    save_path = "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (6)"
    login = "DEFIS_AUX20"
    password = "lfT#1020304050"
    tipo_documento = 1
    tipo_operacao = 2
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/automation/download-xmls/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"