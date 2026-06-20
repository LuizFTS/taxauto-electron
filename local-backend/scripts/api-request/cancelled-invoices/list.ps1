Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/taxdata/cancelled-invoices/reports" `
    -Method Get `
    -ContentType "application/json"