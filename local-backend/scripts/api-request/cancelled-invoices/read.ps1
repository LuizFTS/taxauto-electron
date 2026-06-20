Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/taxdata/cancelled-invoices/report?report_name=relatorio_auditoria_20260325_132654.xlsx" `
    -Method Get `
    -ContentType "application/json"