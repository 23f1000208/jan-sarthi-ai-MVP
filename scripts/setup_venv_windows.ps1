# JAN-SARTHI AI Windows Setup Script
# Run from repository root: powershell -ExecutionPolicy Bypass -File .\scripts\setup_venv_windows.ps1

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "JAN-SARTHI AI: Environment Setup (Windows)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Python version
$pyVersion = python --version 2>&1
Write-Host "Detected Python: $pyVersion" -ForegroundColor Green

# 2. Create Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment in .venv..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host ".venv already exists, skipping creation." -ForegroundColor Green
}

# 3. Activate Virtual Environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# 4. Install Requirements
Write-Host "Installing project requirements..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. Copy Environment Template
if (-not (Test-Path ".env")) {
    Write-Host "Generating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
}

# 6. Generate Data
Write-Host "Generating baseline datasets..." -ForegroundColor Yellow
python scripts\generate_data.py

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Setup Complete! Run the dashboard using:" -ForegroundColor Green
Write-Host "streamlit run app/streamlit_app.py --server.port 8501" -ForegroundColor White
Write-Host "Or run the test suite:" -ForegroundColor Green
Write-Host "pytest -v" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Green
