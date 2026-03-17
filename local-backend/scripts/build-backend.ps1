Write-Host "Building backend..."

cd $PSScriptRoot/..

# ativa venv
.\.venv\Scripts\Activate.ps1

# garante dependencias
pip install -r requirements.txt

# limpa builds anteriores
if (Test-Path dist) { Remove-Item dist -Recurse -Force }
if (Test-Path build) { Remove-Item build -Recurse -Force }

# build com pyinstaller
pyinstaller `
  --onefile `
  --name backend `
  --distpath dist `
  --noconfirm `
  main.py

Write-Host "Backend build concluído"