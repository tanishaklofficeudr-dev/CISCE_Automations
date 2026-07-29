# School Details Module — Automation Design Document

---

# 1. REUSABLE METHODS (Already Exist — No Change)

## Page Object: pages/school_details_page.py

| Method | What It Does | Reuse For |
|--------|--------------|-----------|
| `fill_school_details(data)` | Fills all fields (name, classification, type, contact, website, UDISE, category) + clicks Next | TC-SCH-001 (positive complete submission) |

## Utility: utils/excel_reader.py

| Method | Reuse For |
|--------|-----------|
| `ExcelReader(file_path)` | Loading Validation_Data.xlsx for negative scenarios |
| `get_sheet_data(sheet_name)` | Reading "School_Negative" sheet |

## Utility: utils/screenshot_util.py

| Method | Reuse For |
|--------|-----------|
| `ScreenshotUtil.take_screenshot(page, name)` | Evidence capture on assertion failure |

## Utility: utils/logger.py

| Method | Reuse For |
|--------|-----------|
| `setup_logger()` | Logging test execution in regression tests |

## Fixtures (conftest.py)

| Fixture | Reuse For |
|---------|-----------|
| `page` | Base Playwright page for all tests |
| `browser_context_args` | Video recording during regression runs |

---

# 2. MISSING METHODS (Need to ADD to school_details_page.py)

| Method Name | Purpose | Used By Test Cases |
|-------------|---------|-------------------|
| `click_next()` | Click Next button WITHOUT filling any field | TC-SCH-002 through TC-SCH-008 (blank/mandatory tests) |
| `fill_school_name(name)` | Fill ONLY the school name field | TC-SCH-003, TC-SCH-004, TC-SCH-005 |
| `select_classification(value)` | Select ONLY classification dropdown | TC-SCH-006 |
| `select_school_type(value)` | Select ONLY school type dropdown | TC-SCH-007 |
| `select_category(value)` | Select ONLY category dropdown | TC-SCH-008 |
| `fill_udise(value)` | Fill ONLY UDISE field | TC-SCH-009, TC-SCH-010 |
| `fill_contact_person(value)` | Fill ONLY contact person | TC-SCH-012 |
| `fill_website(value)` | Fill ONLY website | TC-SCH-011 |
| `get_validation_errors()` | Return list of all visible validation error texts | All negative tests |
| `get_field_error(field_name)` | Return error message for a specific field | Individual field tests |
| `is_on_school_details_page()` | Verify current page is School Details (URL or heading check) | Navigation assertions |
| `fill_all_except(data, skip_field)` | Fill all fields EXCEPT one specified field | Mandatory field tests |

**CRITICAL RULE:** These methods are ADDED to the existing file. The existing `fill_school_details(data)` is NEVER modified.

---

# 3. MISSING FIXTURES (Need to ADD to conftest.py)

| Fixture Name | Scope | Purpose | Dependencies |
|--------------|-------|---------|--------------|
| `school_details_ready_page` | function | Returns a page already navigated to School Details (logged in + clicked Next on Get Started) | `page`, Common_Login data, login_page.py, registration_page.py |

**How it works:**
1. Reads Common_Login from Validation_Data.xlsx
2. Navigates to registration URL
3. Registers (handles duplicate gracefully)
4. Logs in
5. Waits for dashboard
6. Clicks Next on Get Started page
7. Returns page on School Details form

**Why needed:** Without this, every negative test would repeat 4 steps (register + login + dashboard + Next) — wasting ~30 seconds per test.

---

# 4. REQUIRED EXCEL DATA

## File: test_data/negative/Validation_Data.xlsx
## Sheet: School_Negative

| scenario_id | execute | scenario_description | field_name | field_value | other_fields_valid | expected_error | scenario_type | priority |
|---|---|---|---|---|---|---|---|---|
| SCH_NEG_01 | Yes | Blank school name - Next blocked | school_name | (empty) | Yes | School name is required | Negative | High |
| SCH_NEG_02 | Yes | Special characters only in school name | school_name | @#$%^&*() | Yes | Invalid school name | Negative | Medium |
| SCH_NEG_03 | Yes | Numbers only in school name | school_name | 123456789 | Yes | Invalid school name | Negative | Medium |
| SCH_NEG_04 | Yes | Classification not selected | school_classification | (not selected) | Yes | Classification is required | Negative | High |
| SCH_NEG_05 | Yes | School type not selected | school_type | (not selected) | Yes | School type is required | Negative | High |
| SCH_NEG_06 | Yes | Category not selected | school_category | (not selected) | Yes | Category is required | Negative | High |
| SCH_NEG_07 | Yes | UDISE with alphabets | udise_number | abcdefghij | Yes | Invalid UDISE number | Negative | Medium |
| SCH_NEG_08 | Yes | UDISE with special chars | udise_number | 123@#$456 | Yes | Invalid UDISE number | Negative | Medium |
| SCH_NEG_09 | Yes | Numeric-only contact person | contact_person | 123456 | Yes | Invalid contact name | Negative | Low |
| SCH_NEG_10 | Yes | Invalid website format | website | notavalidurl | Yes | Invalid URL format | Negative | Low |
| SCH_BND_01 | Yes | School name maximum length | school_name | (200+ char string) | Yes | Field limit exceeded | Boundary | Medium |
| SCH_BND_02 | Yes | School name minimum (1 char) | school_name | A | Yes | (may pass or require minimum) | Boundary | Low |
| SCH_BND_03 | Yes | UDISE fewer digits than required | udise_number | 12345 | Yes | Must be N digits | Boundary | Medium |
| SCH_BND_04 | Yes | UDISE more digits than required | udise_number | 123456789012345 | Yes | Must be N digits | Boundary | Medium |

---

# 5. TEST FILE NAMES

| File | Purpose | Test Count |
|------|---------|-----------|
| tests/test_school_details_validation.py | All School Details negative + boundary tests | 14 |

**Internal test functions:**

| Function | Marker | Scenarios |
|----------|--------|-----------|
| `test_school_details_complete_submission` | @smoke, @sanity, @regression | TC-SCH-001 (positive, uses existing `fill_school_details`) |
| `test_school_mandatory_field_validation` | @regression, @negative | TC-SCH-002, SCH-004 to SCH-008 (parametrized from Excel) |
| `test_school_name_invalid_input` | @regression, @negative | TC-SCH-003, TC-SCH-004 (parametrized) |
| `test_school_field_boundary` | @regression, @boundary | TC-SCH-005, TC-SCH-010 (parametrized) |
| `test_school_udise_invalid` | @regression, @negative | TC-SCH-009 (parametrized) |
| `test_school_optional_field_validation` | @regression, @negative | TC-SCH-011, TC-SCH-012 |
| `test_school_data_persistence_back_nav` | @regression | TC-SCH-013 |
| `test_school_dropdown_options_loaded` | @regression | TC-SCH-014 |

---

# 6. EXECUTION STRATEGY

## Test Execution Flow

```
┌────────────────────────────────────────────────────┐
│ school_details_ready_page fixture                   │
│ (Login → Dashboard → Click Next → School Details)  │
└───────────────────────┬────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
    ┌───────▼───────┐     ┌────────▼────────┐
    │ POSITIVE TEST │     │ NEGATIVE TESTS  │
    │ (1 test)      │     │ (parametrized)  │
    │               │     │                 │
    │ fill_school_  │     │ For each row:   │
    │ details(data) │     │ 1. fill_all_    │
    │               │     │    except(skip) │
    │ Assert: page  │     │ 2. click_next() │
    │ navigated     │     │ 3. Assert error │
    └───────────────┘     │    matches      │
                          │    expected     │
                          └─────────────────┘
```

## Execution Commands

```powershell
# Run ALL School Details tests
pytest tests/test_school_details_validation.py -v --alluredir=allure-results

# Run ONLY negative School tests
pytest tests/test_school_details_validation.py -m negative -v

# Run ONLY boundary School tests
pytest tests/test_school_details_validation.py -m boundary -v

# Run School as part of full regression
pytest tests/ -m regression -v --alluredir=allure-results
```

## Parametrization Strategy

```
Validation_Data.xlsx → "School_Negative" sheet
    → Filter: execute == "Yes"
    → Filter: scenario_type == "Negative" (for negative marker)
    → Filter: scenario_type == "Boundary" (for boundary marker)
    → Each row becomes one pytest parametrized test case
    → Test ID = scenario_id (SCH_NEG_01, SCH_BND_01 etc.)
```

## Fixture Dependency Chain

```
page (pytest-playwright)
  └── school_details_ready_page (conftest.py)
        ├── Reads: Common_Login from Validation_Data.xlsx
        ├── Uses: RegistrationPage.register_school()
        ├── Uses: LoginPage.login()
        ├── Waits: page.wait_for_url(**/dashboard)
        └── Clicks: Next button
              └── Returns: page on School Details form
```

---

# 7. RISK ANALYSIS

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| `fill_all_except()` logic breaks for new fields added to form | Low | Medium | Method should dynamically read field list from data keys |
| `get_validation_errors()` locator changes if UI redesigned | Medium | High | Use generic CSS pattern for error classes (e.g., `.invalid-feedback`, `.error-message`) |
| Pre-authentication fixture fails if password changes | High | Critical | Store credentials in config/ or environment variable, not hardcoded |
| `page.pause()` in login blocks automated regression | High | Critical | Create alternative login method that uses stored/encrypted password for regression |
| Some mandatory fields may not show error immediately (client-side vs server-side) | Medium | Medium | Add wait after click_next() before checking errors |
| School Details form fields may change between releases | Low | Medium | Data-driven approach isolates changes to Excel, not test code |
| Dropdown options loaded asynchronously | Medium | Low | Add `wait_for_timeout(1000)` before checking options |
| `click_next()` may trigger page navigation even with errors (server-side validation) | Low | High | Assert URL didn't change OR assert error text appeared |

## Critical Risk: page.pause() in Login

The existing `login_page.py` uses `page.pause()` for manual password entry. This is acceptable for E2E (where a human supervises) but **blocks fully automated regression execution.**

**Recommended resolution for regression (without modifying existing login method):**

Add a NEW method to login_page.py:
```
login_automated(data)  ← New method, fills password from data["password"]
```

The fixture `school_details_ready_page` would use `login_automated()` instead of `login()`.
The E2E script continues using `login()` with `page.pause()` — unchanged.

---

# 8. ALLURE REPORTING STRUCTURE

```
Epic: CISCE Preliminary Affiliation Form
  └── Feature: School Details Validation
        ├── Story: Mandatory Field Validation
        │     ├── TC-SCH-002: Blank school name blocked
        │     ├── TC-SCH-006: Classification not selected blocked
        │     ├── TC-SCH-007: School type not selected blocked
        │     └── TC-SCH-008: Category not selected blocked
        │
        ├── Story: Input Quality Validation
        │     ├── TC-SCH-003: Special characters rejected
        │     ├── TC-SCH-004: Numeric-only name rejected
        │     ├── TC-SCH-009: UDISE non-numeric rejected
        │     ├── TC-SCH-011: Invalid website URL
        │     └── TC-SCH-012: Numeric contact person
        │
        ├── Story: Boundary Testing
        │     ├── TC-SCH-005: School name max length
        │     └── TC-SCH-010: UDISE digit count
        │
        └── Story: Data Integrity
              ├── TC-SCH-013: Data persistence on back nav
              └── TC-SCH-014: Dropdown options loaded
```

---

# 9. DEFINITION OF DONE

| Criteria | Measurement |
|----------|-------------|
| All 14 tests passing | `pytest tests/test_school_details_validation.py` → 14 passed |
| Zero impact on E2E | `pytest tests/test_preliminary_form_main.py` → still passes |
| Allure report shows School Details stories | Behaviors tab shows all 4 stories |
| Excel data drives all scenarios | No hardcoded values in test file |
| Screenshots on failure | Every failed test has screenshot attached |
| Markers applied correctly | `-m negative` runs only negative, `-m boundary` runs only boundary |
| Parametrized IDs visible | Test output shows SCH_NEG_01, SCH_BND_01 etc. |

---

# 10. ESTIMATED EFFORT

| Task | Effort |
|------|--------|
| Add new methods to school_details_page.py | 2 hours |
| Create school_details_ready_page fixture | 1 hour |
| Create School_Negative sheet in Validation_Data.xlsx | 1 hour |
| Create tests/test_school_details_validation.py | 3 hours |
| Test execution + debugging | 2 hours |
| **Total** | **~1.5 days** |
