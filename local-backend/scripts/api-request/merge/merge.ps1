$body = @{
    paths = @(
        "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (4)\AUDITAR_CANCELADAS\01.csv",
        "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (4)\AUDITAR_CANCELADAS\02.csv"
    )
    output_path = "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (4)\AUDITAR_CANCELADAS"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/utilities/merge-excel-files/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"