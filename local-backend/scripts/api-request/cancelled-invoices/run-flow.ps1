$body = @{
    start_date = "01/06/2026"
    end_date = "10/06/2026"
    filiais = @("02", "06", "09", "12")
    save_path = "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (6)"
    login = "DEFIS_AUX19"
    password = "230422"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/automation/cancelled-invoices-flow/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"