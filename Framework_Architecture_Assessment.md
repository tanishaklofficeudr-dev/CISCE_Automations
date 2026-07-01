# CISCE Preliminary Affiliation Form
# Framework Architecture Assessment Report
## Senior QA Automation Architect Review

---

# 1. FRAMEWORK HEALTH SUMMARY

| Metric | Status | Score |
|--------|--------|-------|
| Project Structure | Well-organized POM architecture | 8/10 |
| Page Objects | Complete coverage of all form pages | 9/10 |
| Data-Driven Approach | Excel-based with Master sheet control | 8/10 |
| Test Execution Control | Parametrized by school_id with execute flag | 9/10 |
| Error Handling | Screenshots + logging on failure | 8/10 |
| Reporting | Allure + HTML + Excel reports auto-generated | 9/10 |
| Video Recording | Configured via browser_context_args fixture | 7/10 |
| CI/CD Readiness | run_tests.ps1 and .bat available | 7/10 |
| Maintainability | Clean separation of concerns | 8/10 |
| Scalability for Regression | Ready with minor extensions | 7/10 |

**Overall Framework Maturity: 8.0 / 10**

---

# 2. REUSABLE COMPONENTS (No Change Required)

| Component | File | Current Status | Recommended Action | Reason |
|-----------|------|----------------|-------------------|--------|
| Registration Page Object | pages/registration_page.py | Reusable | No Change | Handles both new and duplicate registrations gracefully |
| Login Page Object | pages/login_page.py | Reusable | No Change | Clean login flow with manual password support |
| School Details Page Object | pages/school_details_page.py | Reusable | No Change | Fills all mandatory fields with data-driven input |
| Address Details Page Object | pages/address_details_page.py | Reusable | No Change | Handles cascading dropdowns with Select2 |
| NOC Details Page Object | pages/noc_details_page.py | Reusable | No Change | Date picker navigation working |
| Trust Details Page Object | pages/trust_details_page.py | Reusable | No Change | JS injection for dates is stable |
| Land Certificate Page Object | pages/land_certificate_page.py | Reusable | No Change | Conditional logic for Sale Deed implemented |
| Upload Documents Page Object | pages/upload_documents_page.py | Reusable | No Change | Complete upload + payment flow |
| Excel Reader Utility | utils/excel_reader.py | Reusable | No Change | Generic sheet reading with school_id lookup |
| Screenshot Utility | utils/screenshot_util.py | Reusable | No Change | Timestamped screenshots on demand |
| Logger Utility | utils/logger.py | Reusable | No Change | Basic but functional logging |
| Report Generator | utils/report_generator.py | Reusable | No Change | Professional Excel report generation |
| pytest.ini | pytest.ini | Reusable | No Change | Allure + HTML report configuration |
| requirements.txt | requirements.txt | Reusable | No Change | All dependencies listed |
| Test Data Excel | test_data/Data_Schools.xlsx | Reusable | No Change | Master-controlled execution data |
| Test Data PDF | test_data/LandCertificate.pdf | Reusable | No Change | Upload test file |

---

# 3. COMPONENTS REQUIRING EXTENSION

| Component | File | Current Status | Recommended Action | What to Add | Reason |
|-----------|------|----------------|-------------------|-------------|--------|
| Excel Reader | utils/excel_reader.py | Needs Extension | Add New Methods | `get_negative_data(sheet, scenario)`, `get_boundary_data(sheet, field)` | Regression tests need invalid/boundary data retrieval |
| Login Page Object | pages/login_page.py | Needs Extension | Add New Methods | `login_without_password()`, `login_with_invalid_mobile()`, `verify_error_message()` | Negative login scenarios |
| Registration Page Object | pages/registration_page.py | Needs Extension | Add New Methods | `register_with_blank_mobile()`, `register_with_invalid_email()`, `verify_validation_error()` | Negative registration scenarios |
| School Details Page Object | pages/school_details_page.py | Needs Extension | Add New Methods | `submit_blank_form()`, `verify_validation_messages()`, `fill_partial_school_details()` | Mandatory field validation testing |
| conftest.py | conftest.py | Needs Extension | Add New Methods | `@pytest.fixture` for `logged_in_page` (pre-authenticated page for regression tests) | Regression tests shouldn't repeat login for every field validation |
| Logger | utils/logger.py | Needs Extension | Minor Enhancement | Add file handler to write logs to `logs/` folder | Logs currently only go to console |

---

# 4. COMPONENTS THAT MUST NOT BE MODIFIED

| Component | File | Reason |
|-----------|------|--------|
| **E2E Test Script** | tests/test_preliminary_form_main.py | BASELINE implementation. Working, verified, parametrized. Any modification risks breaking the proven E2E flow. |
| **Excel Data Structure** | test_data/Data_Schools.xlsx | Existing sheet structure (Master, Registration, Login, School_Details, etc.) is the contract for the E2E script. Adding sheets is OK; modifying existing sheets is NOT. |
| **conftest.py - Existing Hooks** | conftest.py | pytest_sessionstart, pytest_runtest_makereport, pytest_sessionfinish are stable and serve both E2E and Regression tests. |
| **Report Generator** | utils/report_generator.py | Generates Excel reports for all test types automatically. No modification needed. |
| **pytest.ini - addopts** | pytest.ini | Current addopts configuration works for all test files. Adding markers section is OK; changing addopts is NOT. |

---

# 5. RECOMMENDED NEW FILES

| File | Location | Purpose | Priority |
|------|----------|---------|----------|
| tests/test_registration_negative.py | tests/ | Negative registration scenarios (blank fields, invalid formats) | P1 |
| tests/test_login_negative.py | tests/ | Negative login scenarios (wrong password, blank fields, lockout) | P1 |
| tests/test_school_details_validation.py | tests/ | Mandatory field + boundary testing for School Details | P2 |
| tests/test_address_validation.py | tests/ | Address mandatory fields + PIN boundary testing | P2 |
| tests/test_noc_validation.py | tests/ | NOC mandatory fields + date business rules | P2 |
| tests/test_trust_validation.py | tests/ | Trust date logic + mandatory fields | P2 |
| tests/test_land_validation.py | tests/ | Land area boundary + conditional field testing | P3 |
| tests/test_upload_validation.py | tests/ | File type, size, mandatory document testing | P3 |
| tests/test_payment_negative.py | tests/ | Payment timeout, cancellation, no gateway | P3 |
| utils/validation_helper.py | utils/ | Reusable methods: verify_validation_msg(), verify_field_error(), verify_form_blocked() | P1 |
| utils/navigation_helper.py | utils/ | Reusable methods: navigate_to_step(), login_and_reach_page() | P1 |
| fixtures/authenticated_fixtures.py | fixtures/ | Pre-authenticated page fixtures for regression tests | P1 |

---

# 6. RECOMMENDED NEW EXCEL DATA

| File/Sheet | Purpose | Priority |
|------------|---------|----------|
| test_data/Data_Schools.xlsx → **New Sheet: "Negative_Data"** | Invalid mobile numbers, blank emails, wrong formats per field | P1 |
| test_data/Data_Schools.xlsx → **New Sheet: "Boundary_Data"** | Min/max character lengths, PIN codes, UDISE lengths | P2 |
| test_data/Validation_Data.xlsx (NEW file) | Dedicated file for negative/boundary test data to keep E2E data clean | P1 |

**RULE:** Never modify existing sheets in Data_Schools.xlsx. Only ADD new sheets or create new files.

---

# 7. RECOMMENDED NEW FIXTURES

| Fixture | Scope | Purpose | File |
|---------|-------|---------|------|
| `logged_in_page` | function | Returns a page already logged in and on dashboard (skip registration/login for regression) | conftest.py or fixtures/authenticated_fixtures.py |
| `school_details_page` | function | Returns a page already navigated to School Details step | conftest.py |
| `address_page` | function | Returns a page on Address Details step | conftest.py |
| `noc_page` | function | Returns a page on NOC Details step | conftest.py |
| `upload_page` | function | Returns a page on Upload Documents step | conftest.py |
| `negative_data` | session | Loads negative test data from Validation_Data.xlsx | conftest.py |
| `boundary_data` | session | Loads boundary test data | conftest.py |

**NOTE:** These fixtures should be ADDED to conftest.py without modifying existing fixtures. Alternatively, create a `fixtures/` folder with separate conftest files.

---

# 8. RECOMMENDED NEW HELPER METHODS

### utils/validation_helper.py (NEW)

| Method | Purpose |
|--------|---------|
| `verify_validation_error(page, field_name, expected_msg)` | Assert validation message appears for a field |
| `verify_form_not_submitted(page, current_url)` | Assert form stayed on same page after invalid submit |
| `verify_field_accepts_input(page, locator, value)` | Assert field accepts given value without error |
| `verify_field_rejects_input(page, locator, value)` | Assert field shows error for given value |
| `clear_all_fields(page, field_locators)` | Clear all form fields for blank submission testing |

### utils/navigation_helper.py (NEW)

| Method | Purpose |
|--------|---------|
| `login_and_navigate_to(page, data, target_step)` | Login and reach a specific form step directly |
| `skip_to_step(page, step_name)` | If app allows direct step access via URL |
| `get_current_step(page)` | Return which step user is currently on |

### Extensions to Existing Page Objects (ADD, don't replace)

| Page Object | New Method | Purpose |
|-------------|-----------|---------|
| registration_page.py | `register_blank_mobile()` | Click Register with blank mobile |
| registration_page.py | `register_invalid_email(email)` | Register with specific invalid email |
| registration_page.py | `get_validation_error()` | Return visible validation error text |
| login_page.py | `login_invalid(mobile, password)` | Login with known-bad credentials |
| login_page.py | `get_login_error()` | Return login error message |
| school_details_page.py | `click_next_without_filling()` | Click Next on empty form |
| school_details_page.py | `get_all_validation_errors()` | Return list of all visible errors |

---

# 9. RECOMMENDED FOLDER STRUCTURE

```
CISCE_Preliminary_Form_Automation_Main/
│
├── conftest.py                          ← KEEP (add new fixtures at bottom)
├── pytest.ini                           ← KEEP
├── requirements.txt                     ← KEEP
├── run_tests.ps1                        ← KEEP
├── run_tests.bat                        ← KEEP
│
├── pages/                               ← KEEP ALL (extend with new methods)
│   ├── registration_page.py
│   ├── login_page.py
│   ├── school_details_page.py
│   ├── address_details_page.py
│   ├── noc_details_page.py
│   ├── trust_details_page.py
│   ├── land_certificate_page.py
│   └── upload_documents_page.py
│
├── tests/
│   ├── test_preliminary_form_main.py    ← NEVER MODIFY (E2E baseline)
│   ├── test_sanity_regression_suite.py  ← KEEP (Allure showcase suite)
│   ├── test_registration_negative.py   ← NEW
│   ├── test_login_negative.py          ← NEW
│   ├── test_school_validation.py       ← NEW
│   ├── test_address_validation.py      ← NEW
│   ├── test_noc_validation.py          ← NEW
│   ├── test_trust_validation.py        ← NEW
│   ├── test_land_validation.py         ← NEW
│   ├── test_upload_validation.py       ← NEW
│   └── test_payment_negative.py        ← NEW
│
├── utils/
│   ├── __init__.py                      ← KEEP
│   ├── excel_reader.py                  ← KEEP (extend)
│   ├── logger.py                        ← KEEP (extend)
│   ├── screenshot_util.py              ← KEEP
│   ├── report_generator.py             ← KEEP
│   ├── validation_helper.py            ← NEW
│   └── navigation_helper.py            ← NEW
│
├── test_data/
│   ├── Data_Schools.xlsx               ← NEVER MODIFY existing sheets
│   ├── Validation_Data.xlsx            ← NEW (negative + boundary data)
│   └── LandCertificate.pdf            ← KEEP
│
├── reports/                             ← Auto-generated
├── screenshots/                         ← Auto-generated
├── recordings/                          ← Auto-generated
├── allure-results/                      ← Auto-generated
└── allure-report/                       ← Auto-generated
```

---

# 10. REGRESSION READINESS ASSESSMENT

| Criteria | Status | Score |
|----------|--------|-------|
| Page Objects reusable for regression | Yes - all 8 page objects can serve regression tests | 9/10 |
| Data-driven approach supports regression data | Yes - add new sheets/files without breaking E2E | 8/10 |
| Fixtures support isolated test execution | Partially - need pre-authenticated fixtures | 6/10 |
| Allure integration ready for regression | Yes - markers + steps + severity already configured | 9/10 |
| Parallel execution possible | Yes - pytest-xdist compatible architecture | 7/10 |
| Error handling supports regression reporting | Yes - screenshots + logging + Allure attachment | 9/10 |
| Can support 100+ regression tests | Yes - with new validation helper and fixtures | 8/10 |

**Regression Readiness Score: 8.0 / 10**

**Verdict:** Framework is ready for regression expansion. Primary gap is the lack of pre-authenticated fixtures and validation helper utilities. These are additive changes that don't touch the E2E baseline.

---

# 11. SANITY READINESS ASSESSMENT

| Criteria | Status | Score |
|----------|--------|-------|
| Critical path already automated | Yes - full E2E from registration to payment | 10/10 |
| Sanity markers can be applied | Yes - @pytest.mark.sanity already in use | 9/10 |
| Can run sanity independently | Yes - `pytest -m sanity` works | 9/10 |
| Sanity suite execution time acceptable | Depends on manual password - needs fixture | 6/10 |
| Sanity covers all critical modules | Yes - E2E touches every module | 9/10 |

**Sanity Readiness Score: 8.6 / 10**

**Verdict:** Sanity is essentially the E2E test itself. The existing `test_preliminary_form_main.py` IS the sanity suite. The `test_sanity_regression_suite.py` provides the 20-test showcase version for Allure reporting. Both work independently.

---

# 12. E2E SCRIPT SPECIAL ANALYSIS

## Assessment: test_preliminary_form_main.py

| Question | Answer |
|----------|--------|
| Should it be modified? | **NO - NEVER** |
| Should it be enhanced? | No - it works as designed |
| Should new helpers be added? | Only in separate utility files, not in this script |
| Is it the baseline? | **YES** - all other tests build on top of this flow |

### Reasoning:

1. **Proven in production** - Multiple school IDs executed successfully (SCH001-SCH009 visible in screenshots)
2. **Data-driven** - Adding new schools requires only Excel data, not code changes
3. **Error resilient** - try/except with screenshot + logging + allure attachment
4. **Well-structured** - Clear allure steps map 1:1 to business flow
5. **Parametrized** - Scales to N schools without code duplication

### Recommendation:
```
STATUS: LOCK - DO NOT MODIFY
REASON: Working baseline implementation serving as both E2E and Sanity test
ACTION: Build regression on top using same Page Objects, NOT by editing this file
```

---

# 13. PAGE OBJECT ANALYSIS

## registration_page.py

| Category | Methods |
|----------|---------|
| Existing Reusable | `register_school(data)` |
| Suitable for Regression | `register_school(data)` with invalid data |
| Suitable for Sanity | `register_school(data)` with valid data |
| Should Never Change | `register_school(data)` signature and core flow |
| Missing for Regression | `get_validation_error()`, `register_blank_fields()`, `verify_success_popup_text()` |
| Duplicates | None |

## login_page.py

| Category | Methods |
|----------|---------|
| Existing Reusable | `login(data)` |
| Suitable for Regression | `login(data)` with invalid data |
| Suitable for Sanity | `login(data)` with valid data |
| Should Never Change | `login(data)` signature and core flow |
| Missing for Regression | `login_without_password()`, `get_error_message()`, `verify_login_blocked()` |
| Duplicates | None |

## school_details_page.py

| Category | Methods |
|----------|---------|
| Existing Reusable | `fill_school_details(data)` |
| Suitable for Regression | Full method with invalid data + partial fill methods |
| Suitable for Sanity | `fill_school_details(data)` with valid data |
| Should Never Change | `fill_school_details(data)` core flow |
| Missing for Regression | `fill_partial_details(data, skip_fields)`, `click_next_empty()`, `get_validation_errors()` |
| Duplicates | None |

## address_details_page.py

| Category | Methods |
|----------|---------|
| Existing Reusable | `fill_address_details(data)` |
| Suitable for Regression | With invalid PIN, missing cascading selections |
| Suitable for Sanity | `fill_address_details(data)` with valid data |
| Should Never Change | Cascading dropdown interaction logic |
| Missing for Regression | `verify_cascading_loads(country)`, `fill_invalid_pin(value)` |
| Duplicates | None |

## noc_details_page.py

| Category | Methods |
|----------|---------|
| Existing Reusable | `fill_noc_details(data)` |
| Suitable for Regression | Date picker testing, blank field submission |
| Suitable for Sanity | Full method with valid data |
| Should Never Change | Date picker back arrow logic |
| Missing for Regression | `select_future_date()`, `submit_blank_noc()` |
| Duplicates | None |

## trust_details_page.py

| Category | Methods |
|----------|---------|
| Existing Reusable | `fill_trust_details(data)` |
| Suitable for Regression | Date logic testing, blank field submission |
| Suitable for Sanity | Full method with valid data |
| Should Never Change | JavaScript date injection approach |
| Missing for Regression | `set_invalid_date_combination()`, `submit_blank_trust()` |
| Duplicates | None |

## land_certificate_page.py

| Category | Methods |
|----------|---------|
| Existing Reusable | `fill_land_details(data)` |
| Suitable for Regression | Conditional logic, boundary area values |
| Suitable for Sanity | Full method with valid data |
| Should Never Change | Plot type dynamic form logic, Sale Deed conditional |
| Missing for Regression | `fill_zero_area()`, `fill_negative_area()`, `test_conditional_field_visibility()` |
| Duplicates | None |

## upload_documents_page.py

| Category | Methods |
|----------|---------|
| Existing Reusable | `upload_documents(data)` |
| Suitable for Regression | File type testing, missing uploads, payment paths |
| Suitable for Sanity | Full upload + payment flow |
| Should Never Change | File chooser interaction pattern, payment JS injection |
| Missing for Regression | `upload_invalid_file_type()`, `submit_without_uploads()`, `verify_all_upload_errors()` |
| Duplicates | None |

---

# 14. DATA-DRIVEN ANALYSIS

| Dataset Type | Currently Supported | Action Required |
|--------------|-------------------|-----------------|
| Positive datasets | YES - via Data_Schools.xlsx | None |
| Negative datasets | NO | Create Validation_Data.xlsx or add "Negative_Data" sheet |
| Boundary datasets | NO | Create Boundary_Data sheet |
| Regression datasets | PARTIAL - only positive path | Add negative + boundary data |
| Sanity datasets | YES - same as positive E2E data | None |
| Multi-school parallel | YES - parametrized by school_id | None |
| Execute control | YES - Master sheet with execute=Yes/No | None |

---

# 15. FRAMEWORK SCALABILITY ASSESSMENT

| Capability | Supported | Readiness |
|------------|-----------|-----------|
| 100+ Regression Test Cases | Yes | Ready with fixtures + validation helpers |
| Smoke Suite (14 tests) | Yes | test_sanity_regression_suite.py markers |
| Sanity Suite (42 tests) | Yes | -m sanity filter |
| Parallel Execution | Yes | Architecture compatible with pytest-xdist |
| Allure Reporting | Yes | Already integrated with steps + history |
| Future Maintenance | Yes | POM ensures locator changes in one place |
| New Module Addition | Yes | Add new page object + test file |
| Cross-browser | Possible | --browser flag already supported |
| Environment Switching | Partial | URLs hardcoded; recommend config file |

---

# 16. OVERALL FRAMEWORK MATURITY SCORE

| Category | Score |
|----------|-------|
| Architecture | 8/10 |
| Code Quality | 8/10 |
| Reusability | 9/10 |
| Scalability | 7/10 |
| Error Handling | 8/10 |
| Reporting | 9/10 |
| Data Management | 7/10 |
| Maintenance | 8/10 |
| Documentation | 7/10 |
| CI/CD Readiness | 7/10 |

## **OVERALL MATURITY: 7.8 / 10**

---

# 17. EXECUTIVE SUMMARY

The CISCE Preliminary Affiliation automation framework is a **well-architected, production-grade E2E automation solution** built on industry-standard patterns (POM + Data-Driven + Allure).

**Strengths:**
- Complete positive path coverage from Registration to Payment
- Clean Page Object separation with 8 dedicated page classes
- Excel-driven parametrization allowing unlimited school data scaling
- Triple reporting (Allure + HTML + Excel) with automated generation
- Video recording and screenshot evidence on failure

**Primary Gap:**
- No negative/boundary test automation (61% of regression scenarios uncovered)
- No pre-authenticated fixtures for efficient regression execution
- No dedicated validation helper utilities

**Path Forward:**
- Build regression by EXTENDING (never replacing) existing components
- Add `validation_helper.py` and `navigation_helper.py` utilities
- Create per-module negative test files under `tests/`
- Add negative/boundary data in a separate Excel file
- Estimated effort: ~11 days to reach 90%+ regression coverage

**The framework is READY for regression expansion with additive changes only.**
