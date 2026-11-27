$body = @{
    start_date = "01/10/2026"
    end_date   = "07/10/2026"
    filiais = @("02")
    book_type = "entrada"
    tasks = @{
      open_book = $false
      update_book = $true
      close_book = $false
      save_spreadsheet = $false
      save_pdf = $false
    }
    save_path = "C:\Users\lu9887091\Downloads"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/automation/tax-books/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"