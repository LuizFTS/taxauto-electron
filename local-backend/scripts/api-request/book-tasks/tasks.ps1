$body = @{
    start_date = "15/10/2024"
    end_date   = "15/10/2024"
    filiais = @("02")
    book_type = "entrada"
    tasks = @{
      open_book = $false
      update_book = $false
      close_book = $false
      save_spreadsheet = $true
      save_pdf = $false
    }
    save_path = "C:\Users\lu9887091\Downloads"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/automation/tax-reports/run" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"