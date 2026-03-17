Write-Host "Starting FastAPI server..."

& ".\.venv\Scripts\Activate.ps1"

uvicorn backend.main:app --reload