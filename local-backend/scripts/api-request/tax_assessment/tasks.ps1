$body = @{
    date = "01/10/2026"
    filiais = @("02", "06", "09")
    save_path = "C:\Users\lu9887091\Downloads"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/automation/tax-reports/assessment" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"