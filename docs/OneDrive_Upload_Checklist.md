# OneDrive Upload Checklist
## CISCE Preliminary Form Automation Project

---

# FILES/FOLDERS TO UPLOAD ✅

| # | Path | Type | Mandatory | Purpose |
|---|------|------|-----------|---------|
| 1 | `tests/` | Folder | ✅ Yes | All test files (E2E, regression, sanity) |
| 2 | `pages/` | Folder | ✅ Yes | Page Object Models |
| 3 | `utils/` | Folder | ✅ Yes | Utilities (ExcelReader, ValidationHelper, ScreenshotUtil, ReportGenerator) |
| 4 | `test_data/` | Folder | ✅ Yes | Excel test data (Validation_Data.xlsx, Data_Schools.xlsx) |
| 5 | `docs/` | Folder | ✅ Yes | All documentation and reports |
| 6 | `reports/` | Folder | Optional | Generated HTML/Excel reports |
| 7 | `allure-report/` | Folder | Optional | Generated Allure report (viewable) |
| 8 | `screenshots/` | Folder | Optional | Failure screenshots |
| 9 | `conftest.py` | File | ✅ Yes | Fixtures + pytest hooks |
| 10 | `pytest.ini` | File | ✅ Yes | Pytest configuration + markers |
| 11 | `requirements.txt` | File | ✅ Yes | Python dependencies |
| 12 | `README.md` | File | ✅ Yes | Project overview |
| 13 | `COMMANDS.md` | File | Optional | Execution commands reference |
| 14 | `run_tests.bat` | File | Optional | Windows batch runner |
| 15 | `run_tests.ps1` | File | Optional | PowerShell runner |

---

# FILES/FOLDERS NOT TO UPLOAD ❌

| # | Path | Reason |
|---|------|--------|
| 1 | `__pycache__/` | Python bytecode cache — auto-generated |
| 2 | `.pytest_cache/` | Pytest internal cache |
| 3 | `venv/` | Virtual environment (large, reproducible from requirements.txt) |
| 4 | `.git/` | Git repository data (use git remote instead) |
| 5 | `allure-results/` | Raw allure data — use `allure-report/` instead |
| 6 | `test-results/` | Playwright trace files (large) |
| 7 | `traces/` | Playwright trace artifacts |
| 8 | `recordings/` | Video recordings (large files) |
| 9 | `videos/` | Video artifacts |
| 10 | `Preliminary_Form_Recording/` | Recording artifacts |
| 11 | `diagnostics/` | Temporary diagnostic scripts (development only) |
| 12 | `allure-single-report/` | Old single-run reports |
| 13 | `allure-single-report - regression/` | Old reports |
| 14 | `allure-single-report - School_Details(Regression)/` | Old reports |
| 15 | `Scripts/` | Virtual env scripts |
| 16 | `generate_excel_report.py` | Duplicate of utils/report_generator.py |
| 17 | `CISCE_Allure_Report.zip` | Old archived report |
| 18 | `tests/debug_*.py` | Development debug scripts (11 files) |
| 19 | `fixtures/` | Empty/unused folder |
| 20 | `config/` | Unused config folder |
| 21 | `logs/` | Runtime logs |

---

# UPLOAD SIZE ESTIMATE

| Component | Approximate Size |
|-----------|-----------------|
| Tests + Pages + Utils | ~500 KB |
| Test Data (Excel) | ~200 KB |
| Documentation | ~300 KB |
| Allure Report (HTML) | ~5 MB |
| Screenshots | ~2-10 MB |
| Reports (HTML/Excel) | ~1 MB |
| **Total (without venv/recordings)** | **~8-15 MB** |

---

# QUICK COMMAND TO VERIFY BEFORE UPLOAD

```bash
python -m pytest tests/ --collect-only -q
# Expected: 152 tests collected
```
