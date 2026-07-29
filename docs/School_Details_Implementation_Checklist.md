# School Details Module — Implementation Checklist
## Approved Architecture — Step-by-Step Execution Plan

---

# IMPLEMENTATION SEQUENCE (Safest Order)

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7
   ↓          ↓          ↓          ↓          ↓          ↓          ↓
New Files   Extend     Excel      Fixtures   Markers    Allure     Tests
(utils)     (pages)    (data)     (conftest)  (ini)     (labels)   (run)
```

**Principle:** Build foundation first (utils, methods), then data, then fixtures, then test file last. At every phase, run E2E to verify zero breakage.

---

# PHASE 1: FILES TO CREATE

| # | File | Action | Purpose | Risk to E2E |
|---|------|--------|---------|-------------|
| 1.1 | `utils/validation_helper.py` | **Create New** | Generic validation error extraction utility | ZERO — new file, nothing depends on it |
| 1.2 | `test_data/negative/Validation_Data.xlsx` | **Create New** | Negative/boundary test data for School module | ZERO — new file in new folder |
| 1.3 | `tests/test_school_details_validation.py` | **Create New** (empty shell first) | Regression test file for School Details | ZERO — new file, E2E unaware |

### Checklist — Phase 1:
- [ ] Create `utils/validation_helper.py` with `get_all_validation_errors(page)` method
- [ ] Create `test_data/negative/Validation_Data.xlsx` with "Common_Login" sheet and "School_Negative" sheet
- [ ] Create empty `tests/test_school_details_validation.py` (imports only, no tests yet)
- [ ] **VERIFY:** Run `pytest tests/test_preliminary_form_main.py --collect-only` → Still collects E2E test
- [ ] **VERIFY:** Run `pytest tests/test_school_details_validation.py --collect-only` → 0 tests (empty shell)

---

# PHASE 2: FILES TO EXTEND

| # | File | Action | What to Add | What NOT to Touch |
|---|------|--------|-------------|-------------------|
| 2.1 | `pages/login_page.py` | **Extend Existing** | Add `login_automated(data)` method at bottom | Never modify `login(data)` |
| 2.2 | `pages/school_details_page.py` | **Extend Existing** | Add `click_next()` and `fill_partial_details(data, skip_fields)` at bottom | Never modify `fill_school_details(data)` |

### Checklist — Phase 2:
- [ ] Add `login_automated(data)` to end of `pages/login_page.py`
  - Fills mobile from data
  - Fills password from data["password"]
  - Clicks Login
  - NO page.pause()
- [ ] Add `click_next()` to end of `pages/school_details_page.py`
  - Only clicks `page.get_by_role("button", name="Next")`
  - No field filling
- [ ] Add `fill_partial_details(data, skip_fields)` to end of `pages/school_details_page.py`
  - Accepts data dict and list of field names to skip
  - Fills all fields except those in skip_fields
  - Clicks Next at the end
- [ ] **VERIFY:** Run `pytest tests/test_preliminary_form_main.py --collect-only` → Still collects E2E test
- [ ] **VERIFY:** Run `python -c "from pages.login_page import LoginPage; print('OK')"` → No import errors
- [ ] **VERIFY:** Run `python -c "from pages.school_details_page import SchoolDetailsPage; print('OK')"` → No import errors

---

# PHASE 3: EXCEL DATA STRUCTURE

## File: `test_data/negative/Validation_Data.xlsx`

### Sheet 1: "Common_Login"

| Column | Type | Required | Example |
|--------|------|----------|---------|
| scenario_id | String | Yes | COMMON_01 |
| mobile_number | String | Yes | 9876543210 |
| password | String | Yes | ValidPass123 |
| description | String | No | Default regression login |

**Rows:** 1 (single valid login credential for fixtures)

---

### Sheet 2: "School_Negative"

| Column | Type | Required | Example |
|--------|------|----------|---------|
| scenario_id | String | Yes | SCH_NEG_01 |
| execute | String | Yes | Yes |
| scenario_description | String | Yes | Blank school name |
| field_name | String | Yes | school_name |
| field_value | String | No | (empty for blank tests) |
| expected_error | String | Yes | School name is required |
| scenario_type | String | Yes | Negative |
| priority | String | Yes | High |

**Rows:** 14 (matching TC-SCH-001 through TC-SCH-014)

---

### Checklist — Phase 3:
- [ ] Create Validation_Data.xlsx in `test_data/negative/`
- [ ] Add "Common_Login" sheet with 1 row of valid credentials
- [ ] Add "School_Negative" sheet with 14 scenario rows
- [ ] Set `execute = Yes` for all 14 rows initially
- [ ] **VERIFY:** Run `python -c "from utils.excel_reader import ExcelReader; er = ExcelReader('test_data/negative/Validation_Data.xlsx'); print(len(er.get_sheet_data('School_Negative')), 'rows')"` → 14 rows
- [ ] **VERIFY:** E2E script unaffected (doesn't read this file)

---

# PHASE 4: FIXTURES

| # | File | Action | Fixture Name | Scope |
|---|------|--------|--------------|-------|
| 4.1 | `conftest.py` | **Extend Existing** (add at bottom) | `school_details_ready_page` | function |

### Fixture Logic:
```
Input: page (from pytest-playwright)
Steps:
  1. Read Common_Login data from Validation_Data.xlsx
  2. Navigate to registration URL
  3. Call RegistrationPage(page).register_school(data)
  4. Call LoginPage(page).login_automated(data)
  5. Wait for dashboard URL
  6. Click Next button
  7. Return page (now on School Details form)
Output: page positioned on School Details page
```

### Checklist — Phase 4:
- [ ] Add `school_details_ready_page` fixture at bottom of `conftest.py`
- [ ] Fixture uses `login_automated()` (NOT `login()` — no page.pause)
- [ ] Fixture reads credentials from `test_data/negative/Validation_Data.xlsx` "Common_Login" sheet
- [ ] **VERIFY:** Run `pytest tests/test_preliminary_form_main.py --collect-only` → E2E still works
- [ ] **VERIFY:** Existing hooks (pytest_sessionstart, pytest_runtest_makereport, pytest_sessionfinish) unaffected

---

# PHASE 5: PYTEST MARKERS

| # | File | Action | What to Add |
|---|------|--------|-------------|
| 5.1 | `pytest.ini` | **Extend Existing** | Add `negative` and `boundary` markers |

### Current pytest.ini markers:
```ini
markers =
    sanity: Sanity test cases
    regression: Regression test cases
```

### After extension:
```ini
markers =
    sanity: Sanity test cases
    regression: Regression test cases
    negative: Negative validation scenarios
    boundary: Boundary value scenarios
    smoke: Smoke test - critical path only
```

### Checklist — Phase 5:
- [ ] Add `negative`, `boundary`, `smoke` markers to pytest.ini
- [ ] **VERIFY:** Run `pytest --markers` → Shows all 5 markers
- [ ] **VERIFY:** Run `pytest tests/test_preliminary_form_main.py --collect-only` → No warnings about unknown markers

---

# PHASE 6: ALLURE LABELS

### Allure hierarchy for School Details tests:

| Label | Value |
|-------|-------|
| `@allure.epic` | "CISCE Preliminary Affiliation Form" |
| `@allure.feature` | "School Details Validation" |
| `@allure.story` (per test group) | "Mandatory Field Validation" / "Input Quality Validation" / "Boundary Testing" / "Data Integrity" |
| `@allure.severity` | CRITICAL for mandatory tests, NORMAL for input quality, MINOR for boundary |
| `allure.dynamic.title` | Scenario description from Excel |
| `allure.dynamic.description` | Full test context with field_name and expected_error |

### Checklist — Phase 6:
- [ ] All tests in file have `@allure.epic("CISCE Preliminary Affiliation Form")`
- [ ] All tests have `@allure.feature("School Details Validation")`
- [ ] Mandatory field tests have `@allure.story("Mandatory Field Validation")`
- [ ] Invalid input tests have `@allure.story("Input Quality Validation")`
- [ ] Boundary tests have `@allure.story("Boundary Testing")`
- [ ] Data persistence tests have `@allure.story("Data Integrity")`
- [ ] `allure.dynamic.title()` set from `scenario["scenario_description"]`
- [ ] Severity applied: CRITICAL for mandatory, NORMAL for input, MINOR for boundary

---

# PHASE 7: EXECUTION STRATEGY

### Test Functions in `tests/test_school_details_validation.py`:

| # | Function | Parametrized? | Data Source | Markers |
|---|----------|---------------|-------------|---------|
| 1 | `test_school_mandatory_field_blocked` | Yes (from Excel rows where field must be blank) | School_Negative where field_value is empty/SKIP | @regression, @negative, @sanity |
| 2 | `test_school_invalid_input_rejected` | Yes (from Excel rows with invalid values) | School_Negative where field_value has invalid data | @regression, @negative |
| 3 | `test_school_boundary_validation` | Yes (from Excel Boundary rows) | School_Negative where scenario_type=Boundary | @regression, @boundary |
| 4 | `test_school_data_persistence` | No | Uses valid data from Data_Schools.xlsx | @regression |
| 5 | `test_school_dropdown_options_loaded` | No | No data needed | @regression |

### Execution Commands:

| Purpose | Command |
|---------|---------|
| Run ALL School Details tests | `pytest tests/test_school_details_validation.py -v --alluredir=allure-results` |
| Run only negative | `pytest tests/test_school_details_validation.py -m negative -v` |
| Run only boundary | `pytest tests/test_school_details_validation.py -m boundary -v` |
| Run as part of full regression | `pytest tests/ -m regression -v --alluredir=allure-results` |
| Run E2E (unchanged) | `pytest tests/test_preliminary_form_main.py --headed -v --alluredir=allure-results` |
| Run everything | `pytest tests/ -v --alluredir=allure-results` |

### Checklist — Phase 7:
- [ ] Test file uses `@pytest.mark.parametrize` with Excel data
- [ ] Parametrize IDs use `scenario_id` (SCH_NEG_01 etc.)
- [ ] Tests filter by `execute == "Yes"` before parametrization
- [ ] All negative tests marked `@pytest.mark.negative`
- [ ] All boundary tests marked `@pytest.mark.boundary`
- [ ] All tests marked `@pytest.mark.regression`
- [ ] Mandatory field tests also marked `@pytest.mark.sanity`

---

# PHASE 8: VALIDATION STRATEGY

### How Each Test Validates:

| Test Type | Validation Approach |
|-----------|-------------------|
| Mandatory blank field | 1. Call `fill_partial_details(valid_data, skip_fields=[field])` 2. Capture current URL 3. Call `get_all_validation_errors(page)` 4. Assert `expected_error` in error list 5. Assert URL unchanged (no navigation) |
| Invalid input | 1. Fill all fields with valid data 2. Override target field with invalid value 3. Click Next 4. Assert error message matches expected |
| Boundary | 1. Fill target field with boundary value 2. Fill all others valid 3. Click Next 4. Assert appropriate behavior (error or acceptance) |
| Data persistence | 1. Fill all valid 2. Proceed to next page 3. Navigate back 4. Assert values retained |
| Dropdown loaded | 1. Wait for page load 2. Check each dropdown has >0 options |

### Assertion Utility — `get_all_validation_errors(page)`:

| Approach | CSS Pattern | Returns |
|----------|-------------|---------|
| Primary | `.invalid-feedback:visible`, `.error-message:visible` | List of strings |
| Fallback | `[class*="error"]:visible`, `[class*="invalid"]:visible` | List of strings |
| Last resort | All red-colored text elements | List of strings |

**Note:** Exact CSS selectors need to be confirmed during implementation by inspecting the actual DOM when validation errors appear.

### Checklist — Phase 8:
- [ ] Every test asserts `expected_error` from Excel matches actual error from page
- [ ] Every negative test asserts page URL did NOT change (form was blocked)
- [ ] Boundary tests that should PASS assert navigation occurred
- [ ] Boundary tests that should FAIL assert error message
- [ ] Screenshots captured on assertion failure (via existing conftest hook)
- [ ] Allure step annotations wrap assertion logic

---

# PHASE 9: EXPECTED FOLDER STRUCTURE (After Implementation)

```
CISCE_Preliminary_Form_Automation_Main/
│
├── conftest.py                              ← EXTENDED (fixture added at bottom)
├── pytest.ini                               ← EXTENDED (markers added)
│
├── pages/
│   ├── login_page.py                        ← EXTENDED (login_automated added)
│   ├── school_details_page.py               ← EXTENDED (2 methods added)
│   ├── registration_page.py                 ← DO NOT MODIFY
│   ├── address_details_page.py              ← DO NOT MODIFY
│   ├── noc_details_page.py                  ← DO NOT MODIFY
│   ├── trust_details_page.py                ← DO NOT MODIFY
│   ├── land_certificate_page.py             ← DO NOT MODIFY
│   └── upload_documents_page.py             ← DO NOT MODIFY
│
├── tests/
│   ├── test_preliminary_form_main.py        ← DO NOT MODIFY
│   ├── test_sanity_regression_suite.py      ← DO NOT MODIFY
│   └── test_school_details_validation.py    ← CREATE NEW
│
├── utils/
│   ├── __init__.py                          ← DO NOT MODIFY
│   ├── excel_reader.py                      ← DO NOT MODIFY
│   ├── logger.py                            ← DO NOT MODIFY
│   ├── screenshot_util.py                   ← DO NOT MODIFY
│   ├── report_generator.py                  ← DO NOT MODIFY
│   └── validation_helper.py                 ← CREATE NEW
│
├── test_data/
│   ├── Data_Schools.xlsx                    ← DO NOT MODIFY
│   ├── LandCertificate.pdf                  ← DO NOT MODIFY
│   └── negative/
│       └── Validation_Data.xlsx             ← CREATE NEW
│
├── fixtures/                                ← CREATED (Phase prev)
│   └── __init__.py
├── config/                                  ← CREATED (Phase prev)
├── logs/                                    ← CREATED (Phase prev)
└── docs/                                    ← CREATED (Phase prev)
    ├── School_Details_Automation_Design.md
    ├── School_Details_Implementation_Review.md
    └── School_Details_Implementation_Checklist.md (this file)
```

### File Status Summary:

| Action | Count |
|--------|-------|
| CREATE NEW | 3 files |
| EXTEND EXISTING | 4 files (conftest, pytest.ini, login_page, school_details_page) |
| DO NOT MODIFY | 12 files |
| **TOTAL FILES TOUCHED** | **7** |

---

# PHASE 10: EXPECTED ALLURE OUTPUT

### After running `pytest tests/test_school_details_validation.py -v --alluredir=allure-results`:

**Overview Dashboard:**
```
Total: 14 tests
Passed: 14 (or fewer if app has unexpected behavior)
Failed: 0
```

**Behaviors Tab:**
```
Epic: CISCE Preliminary Affiliation Form
└── Feature: School Details Validation
    ├── Story: Mandatory Field Validation (6 tests)
    │   ├── ✅ SCH_NEG_01 — Blank school name blocked
    │   ├── ✅ SCH_NEG_04 — Classification not selected blocked
    │   ├── ✅ SCH_NEG_05 — School type not selected blocked
    │   ├── ✅ SCH_NEG_06 — Category not selected blocked
    │   ├── ✅ SCH_NEG_07 — UDISE with alphabets rejected
    │   └── ✅ SCH_NEG_08 — UDISE with special chars rejected
    │
    ├── Story: Input Quality Validation (4 tests)
    │   ├── ✅ SCH_NEG_02 — Special characters only rejected
    │   ├── ✅ SCH_NEG_03 — Numbers only rejected
    │   ├── ✅ SCH_NEG_09 — Numeric contact person rejected
    │   └── ✅ SCH_NEG_10 — Invalid website format handled
    │
    ├── Story: Boundary Testing (4 tests)
    │   ├── ✅ SCH_BND_01 — School name max length
    │   ├── ✅ SCH_BND_02 — School name min length
    │   ├── ✅ SCH_BND_03 — UDISE fewer digits
    │   └── ✅ SCH_BND_04 — UDISE more digits
    │
    └── Story: Data Integrity (2 tests — if implemented)
        ├── ✅ Data persistence on back navigation
        └── ✅ Dropdown options loaded
```

**Trend Tab (after multiple runs):**
```
Run 1: 01-Jul-2026 15:30 — 14 passed
Run 2: 01-Jul-2026 16:00 — 14 passed
Run 3: 02-Jul-2026 10:00 — 13 passed, 1 failed (regression detected!)
```

**Each Test Detail:**
```
Test: SCH_NEG_01 — Blank school name blocked
Severity: CRITICAL
Tags: regression, negative, sanity
Steps:
  ✅ Navigate to School Details page (via fixture)
  ✅ Fill all fields except school_name
  ✅ Click Next
  ✅ Verify validation error: "School name is required"
  ✅ Verify page did not navigate
Duration: 2.3s
```

---

# SAFETY VERIFICATION CHECKLIST

Run after EVERY phase:

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | E2E still collects | `pytest tests/test_preliminary_form_main.py --collect-only` | 1 test collected |
| 2 | E2E imports clean | `python -c "import tests.test_preliminary_form_main"` | No errors |
| 3 | Page objects import | `python -c "from pages.school_details_page import SchoolDetailsPage"` | No errors |
| 4 | Login page imports | `python -c "from pages.login_page import LoginPage"` | No errors |
| 5 | Utils import | `python -c "from utils.validation_helper import get_all_validation_errors"` | No errors |
| 6 | Excel readable | `python -c "from utils.excel_reader import ExcelReader; ExcelReader('test_data/negative/Validation_Data.xlsx')"` | No errors |
| 7 | Conftest loads | `pytest --co -q 2>&1` | No conftest errors |
| 8 | No marker warnings | `pytest tests/ --collect-only 2>&1` | No "PytestUnknownMarkWarning" |

---

# IMPLEMENTATION ORDER (CHRONOLOGICAL)

| Step | Action | Risk | Verify After |
|------|--------|------|--------------|
| 1 | Create `utils/validation_helper.py` | None | Import check |
| 2 | Create `test_data/negative/Validation_Data.xlsx` | None | ExcelReader read check |
| 3 | Add `login_automated(data)` to `pages/login_page.py` | Low | Import check + E2E collect |
| 4 | Add `click_next()` to `pages/school_details_page.py` | Low | Import check + E2E collect |
| 5 | Add `fill_partial_details()` to `pages/school_details_page.py` | Low | Import check + E2E collect |
| 6 | Add markers to `pytest.ini` | None | Marker list check |
| 7 | Add `school_details_ready_page` fixture to `conftest.py` | Medium | E2E collect + conftest load |
| 8 | Create `tests/test_school_details_validation.py` with tests | Low | Collect + Run |
| 9 | Run full regression | — | All pass |
| 10 | Run E2E to confirm zero impact | — | E2E passes |
| 11 | Generate Allure report | — | Report shows School Details |

---

**STATUS:** READY FOR IMPLEMENTATION
**Approval:** Architecture approved, implementation checklist complete
**Next Step:** Begin Phase 1 — Create utility and data files
