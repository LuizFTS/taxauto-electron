$body = @{
    codigo = "9"
    nome   = "venda nova do imigrante"
    uf = "ES"
    cnpj = "28138113000258"
    ie = "080501044"
    company_id = 1
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/branches" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"