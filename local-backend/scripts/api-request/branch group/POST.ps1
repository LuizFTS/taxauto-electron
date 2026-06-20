$body = @{
    codigo = "5"
    nome = "E"
    analista = "PATRICIA"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/branch-group" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"