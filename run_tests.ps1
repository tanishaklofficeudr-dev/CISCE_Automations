# ============================================================
# CISCE Preliminary Form Automation - Test Runner with Allure
# ============================================================
# This script:
# 1. Preserves previous allure history for trend analysis
# 2. Runs pytest with allure results collection
# 3. Generates allure report with full history (timestamps on x-axis)
# 4. Opens report on a FIXED port (9090)
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CISCE Preliminary Form Automation - Test Execution" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# --- Step 1: Preserve history from previous report ---
Write-Host "[1/5] Preserving test history for trend analysis..." -ForegroundColor Yellow
if (Test-Path "allure-report\history") {
    New-Item -ItemType Directory -Path "allure-results\history" -Force | Out-Null
    Copy-Item -Path "allure-report\history\*" -Destination "allure-results\history\" -Recurse -Force
    Write-Host "      History preserved successfully." -ForegroundColor Green
} else {
    Write-Host "      No previous history found (first run)." -ForegroundColor Gray
}

# --- Step 2: Clean old allure results (keep history folder) ---
Write-Host "[2/5] Cleaning previous results..." -ForegroundColor Yellow
Get-ChildItem -Path "allure-results" -File -ErrorAction SilentlyContinue | 
    Where-Object { $_.Extension -in ".json", ".txt", ".attach", ".png", ".log" } | 
    Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "      Done." -ForegroundColor Green

# --- Step 3: Run tests ---
Write-Host "[3/5] Running tests..." -ForegroundColor Yellow
Write-Host ""
python -m pytest tests/test_preliminary_form_main.py --headed
Write-Host ""

# --- Step 4: Generate allure report ---
Write-Host "[4/5] Generating Allure report with trend history..." -ForegroundColor Yellow
allure generate allure-results --clean -o allure-report
Write-Host "      Report generated at: allure-report\" -ForegroundColor Green

# --- Step 5: Serve on fixed port 9090 ---
Write-Host "[5/5] Opening Allure report on port 9090..." -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Allure Report: http://localhost:9090" -ForegroundColor Green
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
allure open allure-report --port 9090
