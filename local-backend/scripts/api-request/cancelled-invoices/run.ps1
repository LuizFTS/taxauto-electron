$body = @{
    start_date = "01/03/2026"
    end_date = "24/03/2026"
    filiais = @("06")
    save_path = "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (4)\PORTALGED"
    login = "DEFIS_AUX19"
    password = "230422"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/automation/cancelled-invoices/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"