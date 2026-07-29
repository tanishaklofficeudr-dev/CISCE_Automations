# OneDrive Final Upload Checklist
## Exact Files & Folders to Upload for Manager Review

---

# 1. MANDATORY FOLDERS TO UPLOAD

| # | Folder | Contents | Why Required |
|---|--------|----------|-------------|
| 1 | `tests/` | All test files (E2E, regression, sanity, authentication) | Core automation code |
| 2 | `pages/` | 9 Page Object files | Automation framework |
| 3 | `utils/` | ExcelReader, ValidationHelper, ScreenshotUtil, ReportGenerator | Shared utilities |
| 4 | `test_data/` | Excel files (Validation_Data.xlsx, Data_Schools.xlsx, LandCertificate.pdf) | Test data |
| 5 | `allure-report/` | Generated Allure HTML report | Visual execution report |
| 6 | `reports/` | HTML + Excel execution reports | Execution evidence |
| 7 | `docs/` | All documentation and analysis reports | Project documentation |

---

# 2. MANDATORY FILES TO UPLOAD (Root Level)

| # | File | Purpose |
|---|------|---------|
| 1 | `conftest.py` | Fixtures, hooks, video recording, sanity markers, ordering |
| 2 | `pytest.ini` | Pytest configuration, markers, report settings |
| 3 | `requirements.txt` | Python dependencies |
| 4 | `README.md` | Project overview |
| 5 | `COMMANDS.md` | All execution commands reference |
| 6 | `Final_Master_Test_Case_Report.md` | Complete test inventory for manager |
| 7 | `Registration_Login_Test_Case_Catalog.md` | Authentication test cases |
| 8 | `Regression_and_Sanity_Test_Catalog.md` | Regression + sanity mapping |
| 9 | `run_tests.bat` | Windows batch runner |
| 10 | `run_tests.ps1` | PowerShell runner |

---

# 3. OPTIONAL FILES (Documentation — Include if Space Allows)

| # | File/Folder | Purpose |
|---|-------------|---------|
| 1 | `docs/Preliminary_Form_Automation_Completion_Report.md` | Overall project completion |
| 2 | `docs/Manager_Handover_Report.md` | Handover summary |
| 3 | `docs/Automation_Project_Statistics.md` | Project metrics |
| 4 | `docs/Regression_Test_Summary.md` | Module-wise regression counts |
| 5 | `docs/Complete_Test_Case_Inventory.md` | Every test ID listed |
| 6 | `docs/Sanity_Test_Summary.md` | Sanity suite details |
| 7 | `docs/Final_Production_Readiness_Report.md` | Production readiness |
| 8 | `docs/Upload_Documents_*` | Upload module documentation |
| 9 | `docs/Certificate_of_Land_*` | Land module documentation |
| 10 | `docs/Payment_Gateway_*` | Payment module documentation |
| 11 | `docs/OneDrive_Upload_Checklist.md` | This file |
| 12 | `docs/Project_Folder_Structure.md` | Directory tree guide |
| 13 | `screenshots/` | Failure screenshots (if any exist) |

---

# 4. FILES/FOLDERS NOT TO UPLOAD ❌

| # | Path | Reason |
|---|------|--------|
| 1 | `__pycache__/` | Auto-generated Python bytecode |
| 2 | `.pytest_cache/` | Pytest internal cache |
| 3 | `venv/` or `.venv/` | Virtual environment (large, reproducible) |
| 4 | `.git/` | Git repository data |
| 5 | `.idea/` or `.vscode/` | IDE settings |
| 6 | `allure-results/` | Raw JSON data (use `allure-report/` instead) |
| 7 | `test-results/` | Playwright trace files (large) |
| 8 | `traces/` | Trace artifacts |
| 9 | `recordings/` | Video recordings (large .webm files) |
| 10 | `videos/` | Video artifacts |
| 11 | `Preliminary_Form_Recording/` | Old recording folder |
| 12 | `diagnostics/` | Development-only scripts |
| 13 | `allure-single-report/` | Old report folders |
| 14 | `allure-single-report - regression/` | Old |
| 15 | `allure-single-report - School_Details(Regression)/` | Old |
| 16 | `Scripts/` | Virtual env scripts |
| 17 | `logs/` | Runtime logs |
| 18 | `fixtures/` | Empty/unused folder |
| 19 | `config/` | Unused |
| 20 | `generate_excel_report.py` | Duplicate of utils/ |
| 21 | `CISCE_Allure_Report.zip` | Old archive |
| 22 | `tests/debug_*.py` | 11 development debug scripts |
| 23 | `Automation_Development_Plan.md` | Old planning doc |
| 24 | `Framework_Architecture_Assessment.md` | Old planning doc |
| 25 | `CISCE_Master_Test_Repository.md` | Old deprecated doc |

---

# 5. RECOMMENDED FINAL FOLDER STRUCTURE

```
CISCE_Preliminary_Form_Automation_Main/
│
├── tests/
│   ├── test_preliminary_form_main.py          ← E2E
│   ├── test_sanity_regression_suite.py        ← Legacy suite
│   ├── sanity/                                ← Sanity module
│   └── regression/
│       ├── authentication/                    ← Registration + Login
│       │   ├── validation/
│       │   ├── positive/
│       │   ├── negative/
│       │   ├── boundary/
│       │   └── ui/
│       ├── school_details/
│       ├── address_details/
│       ├── noc_details/
│       ├── trust_details/
│       ├── land_certificate/
│       ├── upload_documents/
│       └── payment_gateway/
│
├── pages/
│   ├── registration_page.py
│   ├── login_page.py
│   ├── school_details_page.py
│   ├── address_details_page.py
│   ├── noc_details_page.py
│   ├── trust_details_page.py
│   ├── land_certificate_page.py
│   ├── upload_documents_page.py
│   └── payment_gateway_page.py
│
├── utils/
│   ├── excel_reader.py
│   ├── validation_helper.py
│   ├── screenshot_util.py
│   └── report_generator.py
│
├── test_data/
│   ├── Data_Schools.xlsx
│   ├── LandCertificate.pdf
│   └── negative/
│       └── Validation_Data.xlsx (29 sheets)
│
├── docs/
│   └── (25+ documentation files)
│
├── allure-report/
│   └── (Generated HTML report)
│
├── reports/
│   └── report.html + Excel reports
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
├── COMMANDS.md
├── run_tests.bat
├── run_tests.ps1
├── Final_Master_Test_Case_Report.md
├── Registration_Login_Test_Case_Catalog.md
├── Regression_and_Sanity_Test_Catalog.md
└── OneDrive_Final_Upload_Checklist.md
```

---

# 6. FINAL UPLOAD CHECKLIST

## Folders
- ☐ `tests/` (all subfolders included)
- ☐ `pages/` (9 page objects)
- ☐ `utils/` (4 utility files)
- ☐ `test_data/` (Excel + PDF)
- ☐ `allure-report/` (visual report)
- ☐ `reports/` (HTML + Excel reports)
- ☐ `docs/` (all documentation)

## Root Files
- ☐ `conftest.py`
- ☐ `pytest.ini`
- ☐ `requirements.txt`
- ☐ `README.md`
- ☐ `COMMANDS.md`
- ☐ `run_tests.bat`
- ☐ `run_tests.ps1`

## Key Reports (Root Level)
- ☐ `Final_Master_Test_Case_Report.md`
- ☐ `Registration_Login_Test_Case_Catalog.md`
- ☐ `Regression_and_Sanity_Test_Catalog.md`
- ☐ `OneDrive_Final_Upload_Checklist.md`

## Verification Before Upload
- ☐ Run: `python -m pytest tests/regression/ --collect-only -q` → Should show 155+ tests
- ☐ Run: `allure generate allure-results --clean -o allure-report` → Fresh report
- ☐ Verify `allure-report/index.html` opens in browser
- ☐ Verify `reports/report.html` exists

---

# 7. FINAL SUMMARY

| Metric | Count |
|--------|:-----:|
| Mandatory folders | 7 |
| Mandatory root files | 10 |
| Optional documentation files | 25+ (in `docs/`) |
| Files/folders excluded | 25 |
| Estimated upload size | ~15-20 MB |

## The Upload Package Covers:

| Area | Included? |
|------|:---------:|
| Source code (all tests) | ✅ |
| Regression automation (9 modules) | ✅ |
| Sanity suite (25 tests) | ✅ |
| E2E automation | ✅ |
| Allure visual report | ✅ |
| HTML + Excel reports | ✅ |
| Test statistics & inventory | ✅ |
| Authentication (Registration + Login) | ✅ |
| Payment Gateway automation | ✅ |
| Complete documentation | ✅ |
| Execution commands | ✅ |
| Dependencies (requirements.txt) | ✅ |

---

**Your manager will have everything needed to:**
1. Review the complete automation coverage
2. View the Allure report visually
3. Understand project statistics
4. See all test case IDs and their status
5. Run the automation independently (with Python + Playwright installed)

---

*Upload this entire folder to OneDrive and share the link with your manager.*
