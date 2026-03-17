$body = @{
    start_date = "01/03/2026"
    end_date   = "10/03/2026"
    filiais = @("20")
    book_type = "entrada"
    save_path = "C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (4)"
    tasks = @{
      open_book = $false
      update_book = $false
      close_book = $false
      save_spreadsheet = $false
      save_pdf = $true
    }
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/livros-fiscais/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"