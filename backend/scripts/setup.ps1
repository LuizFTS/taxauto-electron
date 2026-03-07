Write-Host "===================================="
Write-Host "Python Project Setup"
Write-Host "===================================="

# Check Python
Write-Host "Checking Python installation..."

$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Host "Python is not installed or not in PATH."
    exit 1
}

Write-Host "Python found."

# Create virtual environment
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
} else {
    Write-Host "Virtual environment already exists."
}

# Activate venv
Write-Host "Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Install dev tools explicitly
Write-Host "Installing dev tools..."
pip install ruff black

Write-Host ""
Write-Host "Setup complete."
Write-Host "Activate the environment with:"
Write-Host ".\.venv\Scripts\Activate.ps1"