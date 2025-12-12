# -----------------------------------------
# Playwright + Pytest + Arduino Automation Setup Script
# Windows PowerShell version
# -----------------------------------------

Write-Host "=== Starting environment setup ==="

# 1. Create virtual environment
Write-Host "[1/6] Creating Python virtual environment..."
python -m venv test_venv

# 2. Activate environment
Write-Host "[2/6] Activating virtual environment..."
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
. test_venv\Scripts\Activate.ps1

# 3. Upgrade pip
Write-Host "[3/6] Upgrading pip..."
pip install --upgrade pip

# 4. Install dependencies
Write-Host "[4/6] Installing required Python packages..."
pip install -Ur requirements.txt
pip install pytest pytest-asyncio pytest-playwright playwright

# 5. Install Playwright browsers
Write-Host "[5/6] Installing Playwright browsers..."
playwright install

# 6. Verify installation
Write-Host "[6/6] Verifying installation..."
pytest --version
playwright --version

Write-Host "===================================="
Write-Host "Setup Completed Successfully!"
Write-Host "To start testing, run:"
Write-Host "    .\.venv\Scripts\Activate.ps1"
Write-Host "    pytest -vv"
Write-Host "===================================="
