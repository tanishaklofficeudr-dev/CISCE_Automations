@echo off
REM ============================================================
REM CISCE Preliminary Form Automation - Test Runner with Allure
REM ============================================================
REM This script:
REM 1. Preserves previous allure history for trend analysis
REM 2. Runs pytest with allure results collection
REM 3. Generates allure report with full history
REM 4. Opens report on a FIXED port (9090)
REM ============================================================

echo.
echo ============================================================
echo   CISCE Preliminary Form Automation - Test Execution
echo ============================================================
echo.

REM --- Step 1: Preserve history from previous report ---
echo [1/5] Preserving test history for trend analysis...
if exist allure-report\history (
    if not exist allure-results\history mkdir allure-results\history
    xcopy /E /Y /Q allure-report\history allure-results\history\ >nul 2>&1
    echo       History preserved successfully.
) else (
    echo       No previous history found (first run).
)

REM --- Step 2: Clean old allure results (keep history) ---
echo [2/5] Cleaning previous results...
for %%f in (allure-results\*.json) do del "%%f" >nul 2>&1
for %%f in (allure-results\*.txt) do del "%%f" >nul 2>&1
for %%f in (allure-results\*.attach) do del "%%f" >nul 2>&1
echo       Done.

REM --- Step 3: Run tests ---
echo [3/5] Running tests...
echo.
python -m pytest tests/test_preliminary_form_main.py --headed
echo.

REM --- Step 4: Generate allure report ---
echo [4/5] Generating Allure report with trend history...
allure generate allure-results --clean -o allure-report
echo       Report generated at: allure-report\

REM --- Step 5: Serve on fixed port 9090 ---
echo [5/5] Opening Allure report on port 9090...
echo.
echo ============================================================
echo   Allure Report: http://localhost:9090
echo   Press Ctrl+C to stop the server
echo ============================================================
echo.
allure open allure-report --port 9090
