$body = @{
    codigo = "002"
    nome   = "casal"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/companies" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"