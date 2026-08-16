# SupportPulse Terminal Setup Script
# Автоматическая настройка окружения для проекта SupportPulse

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SupportPulse Terminal Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 1. Проверка Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Install Python 3.11+" -ForegroundColor Red
    exit 1
}
Write-Host "  Python found: $pythonVersion" -ForegroundColor Green

# 2. Создание виртуального окружения
Write-Host "[2/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "  .venv already exists, skipping." -ForegroundColor Gray
} else {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create .venv" -ForegroundColor Red
        exit 1
    }
    Write-Host "  Virtual environment created." -ForegroundColor Green
}

# 3. Активация виртуального окружения
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
Write-Host "  Virtual environment activated." -ForegroundColor Green

# 4. Установка зависимостей
Write-Host "[4/6] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "  Dependencies installed." -ForegroundColor Green
} else {
    Write-Host "  requirements.txt not found, skipping." -ForegroundColor Gray
}

# 5. Создание .env если не существует
Write-Host "[5/6] Checking .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "  Created .env from .env.example" -ForegroundColor Green
    } else {
        "# ProxyAPI key`nPROXYAPI_API_KEY=YOUR_KEY" | Out-File -FilePath ".env" -Encoding utf8
        Write-Host "  Created empty .env. Set PROXYAPI_API_KEY in .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "  .env already exists." -ForegroundColor Gray
}

# 6. Создание необходимых папок
Write-Host "[6/6] Checking data/ and logs/ directories..." -ForegroundColor Yellow
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
    Write-Host "  Created data/ directory" -ForegroundColor Green
}
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "  Created logs/ directory" -ForegroundColor Green
}

# Итог
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Set ProxyAPI key in .env" -ForegroundColor Gray
Write-Host "  2. Run: uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host "  3. Swagger: http://127.0.0.1:8000/docs`n" -ForegroundColor Gray