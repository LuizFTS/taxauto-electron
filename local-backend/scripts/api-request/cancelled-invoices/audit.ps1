$body = @{
    book_path = "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (4)\AUDITAR_CANCELADAS\006_SAIDA.csv"
    portal_path = "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (4)\AUDITAR_CANCELADAS\06_01032026_25032026_CANCELADAS.xlsx"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/taxdata/cancelled-invoices/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"