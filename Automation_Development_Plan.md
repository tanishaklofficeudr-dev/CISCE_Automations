# CISCE Preliminary Affiliation Portal
# Automation Development Plan
## Regression & Sanity Suite Expansion

---

# SECTION 1: LOCKED COMPONENTS (DO NOT MODIFY)

| # | Component | File Path | Lock Reason |
|---|-----------|-----------|-------------|
| 1 | E2E Test Script | tests/test_preliminary_form_main.py | Baseline implementation, verified, parametrized |
| 2 | Registration Page Object | pages/registration_page.py | Working E2E dependency |
| 3 | Login Page Object | pages/login_page.py | Working E2E dependency |
| 4 | School Details Page Object | pages/school_details_page.py | Working E2E dependency |
| 5 | Address Details Page Object | pages/address_details_page.py | Working E2E dependency |
| 6 | NOC Details Page Object | pages/noc_details_page.py | Working E2E dependency |
| 7 | Trust Details Page Object | pages/trust_details_page.py | Working E2E dependency |
| 8 | Land Certificate Page Object | pages/land_certificate_page.py | Working E2E dependency |
| 9 | Upload Documents Page Object | pages/upload_documents_page.py | Working E2E dependency |
| 10 | Excel Reader | utils/excel_reader.py | Data contract for E2E |
| 11 | Logger | utils/logger.py | Used across all tests |
| 12 | Screenshot Utility | utils/screenshot_util.py | Used across all tests |
| 13 | Report Generator | utils/report_generator.py | Auto-report infrastructure |
| 14 | conftest.py (existing hooks) | conftest.py | Report + Allure + video hooks |
| 15 | pytest.ini | pytest.ini | Global test configuration |
| 16 | Excel Data (existing sheets) | test_data/Data_Schools.xlsx | E2E data contract |
| 17 | Sanity Regression Suite | tests/test_sanity_regression_suite.py | Allure showcase suite |

---

# SECTION 2: EXISTING REUSABLE COMPONENTS

## Page Object Methods Available for Reuse

| Page Object | Method | What It Does | Reuse For |
|-------------|--------|--------------|-----------|
| registration_page.py | `register_school(data)` | Full registration flow | Positive registration tests |
| login_page.py | `login(data)` | Full login flow | Pre-authentication in regression |
| school_details_page.py | `fill_school_details(data)` | Fill all school fields + click Next | Positive form tests |
| address_details_page.py | `fill_address_details(data)` | Fill address with cascading dropdowns | Positive address tests |
| noc_details_page.py | `fill_noc_details(data)` | Fill NOC with date picker | Positive NOC tests |
| trust_details_page.py | `fill_trust_details(data)` | Fill trust with JS date injection | Positive trust tests |
| land_certificate_page.py | `fill_land_details(data)` | Fill land with conditional logic | Positive land tests |
| upload_documents_page.py | `upload_documents(data)` | Upload all docs + payment | Positive upload + payment tests |
| excel_reader.py | `get_sheet_data(sheet)` | Read any Excel sheet | Loading negative/boundary data |
| excel_reader.py | `get_row_by_school_id(sheet, id)` | Get specific school data | Fetching per-school test data |
| excel_reader.py | `get_school_ids_to_execute()` | Get active school IDs | Controlled execution |
| screenshot_util.py | `take_screenshot(page, name)` | Capture evidence | Failure evidence in regression |

## Fixtures Available for Reuse

| Fixture | Scope | Source | Reuse For |
|---------|-------|--------|-----------|
| `page` | function | pytest-playwright | Every browser test |
| `browser_context_args` | session | conftest.py | Video recording for all tests |

## Utilities Available for Reuse

| Utility | Purpose | Reuse For |
|---------|---------|-----------|
| ExcelReader | Load test data from any sheet | Loading negative/boundary data files |
| ScreenshotUtil | Capture screenshots | Evidence in regression tests |
| setup_logger() | Console logging | Logging in all new test scripts |
| ExcelReportGenerator | Generate .xlsx reports | Already auto-triggered for all tests |

---

# SECTION 3: COMPONENTS TO BE EXTENDED (ADDITIONS ONLY)

## 3.1 New Page Object Methods (ADD to existing files)

### pages/registration_page.py — New Methods to Add

| Method | Purpose | Used By |
|--------|---------|---------|
| `navigate_to_registration()` | Only navigate without filling | Regression tests needing page access |
| `fill_mobile_only(mobile)` | Fill only mobile field | Negative email tests |
| `fill_email_only(email)` | Fill only email field | Negative mobile tests |
| `click_register()` | Only click Register without fill | Blank field tests |
| `get_validation_error_text()` | Return visible error message text | Assertion in negative tests |
| `is_success_popup_visible()` | Boolean check for popup | Validation assertions |

### pages/login_page.py — New Methods to Add

| Method | Purpose | Used By |
|--------|---------|---------|
| `navigate_to_login()` | Only navigate to login page | Direct login page tests |
| `fill_mobile(mobile)` | Fill only mobile without submitting | Partial form tests |
| `click_login_button()` | Only click Login without filling | Blank field tests |
| `get_error_message()` | Return login error text | Negative login assertions |
| `is_error_displayed()` | Boolean check for error | Quick validation |

### pages/school_details_page.py — New Methods to Add

| Method | Purpose | Used By |
|--------|---------|---------|
| `click_next()` | Only click Next without filling | Blank form submission test |
| `fill_school_name(name)` | Fill only school name | Individual field tests |
| `select_classification(value)` | Select only classification | Individual dropdown tests |
| `get_validation_errors()` | Return list of all visible errors | Multi-field validation |
| `is_on_school_details_page()` | Verify current page | Navigation assertions |

### pages/address_details_page.py — New Methods to Add

| Method | Purpose | Used By |
|--------|---------|---------|
| `click_next()` | Only click Next without filling | Blank form test |
| `fill_pin_code(pin)` | Fill only PIN field | PIN boundary tests |
| `select_country(country)` | Select only country | Cascading tests |
| `get_state_options()` | Return available states | Cascading validation |
| `get_validation_errors()` | Return visible errors | Mandatory field tests |

### pages/noc_details_page.py — New Methods to Add

| Method | Purpose | Used By |
|--------|---------|---------|
| `click_next()` | Only click Next | Blank form test |
| `open_date_picker()` | Only open date picker | Date navigation tests |
| `select_future_date()` | Select a date in the future | Business rule test |
| `get_validation_errors()` | Return visible errors | Mandatory field tests |

### pages/trust_details_page.py — New Methods to Add

| Method | Purpose | Used By |
|--------|---------|---------|
| `click_next()` | Only click Next | Blank form test |
| `set_establishment_date(date)` | Set only est. date | Date logic tests |
| `set_registration_date(date)` | Set only reg. date | Date logic tests |
| `get_validation_errors()` | Return visible errors | Mandatory field tests |

### pages/land_certificate_page.py — New Methods to Add

| Method | Purpose | Used By |
|--------|---------|---------|
| `click_next()` | Only click Next | Blank form test |
| `fill_land_area(value)` | Fill only area field | Boundary tests |
| `select_plot_type(type)` | Select only plot type | Conditional form tests |
| `is_dynamic_form_visible()` | Check if owner details appeared | Conditional rendering test |
| `get_validation_errors()` | Return visible errors | Mandatory field tests |

### pages/upload_documents_page.py — New Methods to Add

| Method | Purpose | Used By |
|--------|---------|---------|
| `click_proceed_to_payment()` | Only click Proceed | Missing upload tests |
| `upload_single_document(doc_type, file)` | Upload one specific doc | Individual upload tests |
| `get_upload_errors()` | Return upload error messages | Missing doc tests |
| `is_proceed_button_enabled()` | Check button state | Checkbox dependency tests |

---

## 3.2 New Fixtures to Add (in conftest.py)

| Fixture | Scope | Purpose | Dependency |
|---------|-------|---------|------------|
| `logged_in_page` | function | Return page already on dashboard after login | login_page.py + valid data |
| `school_details_ready_page` | function | Return page on School Details step | logged_in_page + Next click |
| `address_ready_page` | function | Return page on Address Details step | school_details filled |
| `noc_ready_page` | function | Return page on NOC Details step | address filled |
| `trust_ready_page` | function | Return page on Trust Details step | NOC filled |
| `land_ready_page` | function | Return page on Land Certificate step | trust filled |
| `upload_ready_page` | function | Return page on Upload Documents step | land filled |
| `validation_data` | session | Load Validation_Data.xlsx | ExcelReader |
| `boundary_data` | session | Load boundary test data | ExcelReader |

---

## 3.3 New Utility Classes to Create

### utils/validation_helper.py (NEW FILE)

| Method | Purpose |
|--------|---------|
| `assert_validation_error_visible(page, expected_text)` | Assert error msg appears |
| `assert_no_navigation(page, current_url)` | Assert page didn't change |
| `assert_field_has_error(page, field_locator)` | Assert field shows error state |
| `get_all_visible_errors(page)` | Return list of all error messages |
| `assert_field_value(page, locator, expected)` | Assert field contains value |
| `assert_dropdown_has_options(page, locator)` | Assert dropdown is populated |

### utils/navigation_helper.py (NEW FILE)

| Method | Purpose |
|--------|---------|
| `login_and_reach_dashboard(page, login_data)` | Automate login + reach dashboard |
| `navigate_to_step(page, step_number)` | Navigate to specific form step |
| `get_current_step_name(page)` | Return current active step name |
| `go_back_one_step(page)` | Click back button |
| `is_on_page(page, url_pattern)` | Boolean URL check |

### utils/test_data_helper.py (NEW FILE)

| Method | Purpose |
|--------|---------|
| `get_negative_data(field_name)` | Return invalid values for a field |
| `get_boundary_data(field_name)` | Return min/max values for a field |
| `get_valid_login_credentials()` | Return working login data for fixtures |

---

## 3.4 New Excel Data Files

### test_data/Validation_Data.xlsx (NEW FILE)

| Sheet Name | Purpose | Sample Columns |
|------------|---------|----------------|
| Login_Negative | Invalid login combinations | scenario, mobile, password, expected_error |
| Registration_Negative | Invalid registration data | scenario, mobile, email, expected_error |
| School_Negative | Invalid school details | scenario, field_name, value, expected_error |
| Address_Negative | Invalid address data | scenario, field_name, value, expected_error |
| NOC_Negative | Invalid NOC data | scenario, field_name, value, expected_error |
| Trust_Negative | Invalid trust data | scenario, field_name, value, expected_error |
| Land_Negative | Invalid land data | scenario, field_name, value, expected_error |
| Upload_Negative | Invalid upload scenarios | scenario, file_type, file_path, expected_error |
| Boundary_Data | All boundary values | module, field, min_value, max_value, over_max |

---

# SECTION 4: NEW TEST SCRIPTS REQUIRED

| # | Script | Module | Test Count | Priority |
|---|--------|--------|-----------|----------|
| 1 | tests/test_registration_validation.py | Registration | 11 | P1 |
| 2 | tests/test_login_validation.py | Authentication | 8 | P1 |
| 3 | tests/test_school_details_validation.py | School Details | 12 | P2 |
| 4 | tests/test_address_validation.py | Address Details | 10 | P2 |
| 5 | tests/test_noc_validation.py | NOC Details | 6 | P2 |
| 6 | tests/test_trust_validation.py | Trust Details | 6 | P2 |
| 7 | tests/test_land_validation.py | Land Certificate | 8 | P3 |
| 8 | tests/test_upload_validation.py | Upload Documents | 8 | P3 |
| 9 | tests/test_payment_validation.py | Payment | 6 | P3 |
| 10 | tests/test_workflow_validation.py | Cross-Cutting | 5 | P4 |

---

# SECTION 5: MODULE-WISE TEST CASE BREAKDOWN

---

## MODULE 1: REGISTRATION

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **13** |
| Positive | 5 |
| Negative | 5 |
| Boundary | 3 |
| Smoke | 1 |
| Sanity | 4 |
| Regression | 13 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-REG-001 | Register with valid mobile and email | Positive | Yes | Yes | Yes |
| TC-REG-002 | Registration page loads correctly | Positive | No | Yes | Yes |
| TC-REG-003 | Duplicate mobile registration rejected | Negative | No | Yes | Yes |
| TC-REG-004 | Blank mobile field blocked | Negative | No | No | Yes |
| TC-REG-005 | Invalid mobile format rejected | Negative | No | No | Yes |
| TC-REG-006 | Mobile less than 10 digits rejected | Boundary | No | No | Yes |
| TC-REG-007 | Mobile more than 10 digits rejected | Boundary | No | No | Yes |
| TC-REG-008 | Blank email field blocked | Negative | No | No | Yes |
| TC-REG-009 | Invalid email format rejected | Negative | No | No | Yes |
| TC-REG-010 | Email max length handling | Boundary | No | No | Yes |
| TC-REG-011 | Country code validation | Positive | No | No | Yes |
| TC-REG-012 | Success popup content verification | Positive | No | Yes | Yes |
| TC-REG-013 | Post-registration page state | Positive | No | No | Yes |

---

## MODULE 2: AUTHENTICATION

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **10** |
| Positive | 4 |
| Negative | 6 |
| Boundary | 0 |
| Smoke | 1 |
| Sanity | 5 |
| Regression | 10 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-AUTH-001 | Login with valid credentials | Positive | Yes | Yes | Yes |
| TC-AUTH-002 | Login page navigation works | Positive | No | Yes | Yes |
| TC-AUTH-003 | Invalid mobile login rejected | Negative | No | Yes | Yes |
| TC-AUTH-004 | Invalid password login rejected | Negative | No | Yes | Yes |
| TC-AUTH-005 | Blank mobile login blocked | Negative | No | No | Yes |
| TC-AUTH-006 | Blank password login blocked | Negative | No | No | Yes |
| TC-AUTH-007 | Multiple failed attempts handling | Negative | No | No | Yes |
| TC-AUTH-008 | Session persists on refresh | Positive | No | No | Yes |
| TC-AUTH-009 | Logout terminates session | Positive | No | Yes | Yes |
| TC-AUTH-010 | Unauthorized route access blocked | Negative | No | No | Yes |

---

## MODULE 3: NAVIGATION / DASHBOARD

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **4** |
| Positive | 4 |
| Negative | 0 |
| Boundary | 0 |
| Smoke | 2 |
| Sanity | 2 |
| Regression | 4 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-NAV-001 | Dashboard loads after login | Positive | Yes | Yes | Yes |
| TC-NAV-002 | Next button navigates to School Details | Positive | Yes | Yes | Yes |
| TC-NAV-003 | Step progress indicator updates | Positive | No | No | Yes |
| TC-NAV-004 | Get Started page instructions correct | Positive | No | No | Yes |

---

## MODULE 4: SCHOOL DETAILS

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **14** |
| Positive | 4 |
| Negative | 8 |
| Boundary | 2 |
| Smoke | 1 |
| Sanity | 3 |
| Regression | 14 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-SCH-001 | Complete form submits successfully | Positive | Yes | Yes | Yes |
| TC-SCH-002 | Blank school name blocked | Negative | No | Yes | Yes |
| TC-SCH-003 | Special characters in school name | Negative | No | No | Yes |
| TC-SCH-004 | Numeric-only school name rejected | Negative | No | No | Yes |
| TC-SCH-005 | School name max length enforcement | Boundary | No | No | Yes |
| TC-SCH-006 | Classification not selected blocked | Negative | No | Yes | Yes |
| TC-SCH-007 | School type not selected blocked | Negative | No | No | Yes |
| TC-SCH-008 | Category not selected blocked | Negative | No | No | Yes |
| TC-SCH-009 | UDISE non-numeric rejected | Negative | No | No | Yes |
| TC-SCH-010 | UDISE digit count enforcement | Boundary | No | No | Yes |
| TC-SCH-011 | Invalid website URL handling | Negative | No | No | Yes |
| TC-SCH-012 | Numeric-only contact person rejected | Negative | No | No | Yes |
| TC-SCH-013 | Data retained on back navigation | Positive | No | No | Yes |
| TC-SCH-014 | Dropdown options load correctly | Positive | No | No | Yes |

---

## MODULE 5: ADDRESS DETAILS

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **12** |
| Positive | 4 |
| Negative | 5 |
| Boundary | 3 |
| Smoke | 1 |
| Sanity | 4 |
| Regression | 12 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-ADDR-001 | Complete address submits successfully | Positive | Yes | Yes | Yes |
| TC-ADDR-002 | Blank address line blocked | Negative | No | Yes | Yes |
| TC-ADDR-003 | State cascading loads per country | Positive | No | Yes | Yes |
| TC-ADDR-004 | District cascading loads per state | Positive | No | Yes | Yes |
| TC-ADDR-005 | City cascading loads per district | Positive | No | No | Yes |
| TC-ADDR-006 | Non-numeric PIN rejected | Negative | No | No | Yes |
| TC-ADDR-007 | PIN less than 6 digits rejected | Boundary | No | No | Yes |
| TC-ADDR-008 | PIN more than 6 digits rejected | Boundary | No | No | Yes |
| TC-ADDR-009 | Country not selected blocked | Negative | No | No | Yes |
| TC-ADDR-010 | State not selected blocked | Negative | No | No | Yes |
| TC-ADDR-011 | Address max length handling | Boundary | No | No | Yes |
| TC-ADDR-012 | Locality not selected blocked | Negative | No | No | Yes |

---

## MODULE 6: NOC DETAILS

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **8** |
| Positive | 2 |
| Negative | 6 |
| Boundary | 0 |
| Smoke | 1 |
| Sanity | 2 |
| Regression | 8 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-NOC-001 | Complete NOC form submits successfully | Positive | Yes | Yes | Yes |
| TC-NOC-002 | Blank authority blocked | Negative | No | Yes | Yes |
| TC-NOC-003 | Blank designation blocked | Negative | No | No | Yes |
| TC-NOC-004 | Blank office address blocked | Negative | No | No | Yes |
| TC-NOC-005 | Future NOC date rejected (business rule) | Negative | No | No | Yes |
| TC-NOC-006 | Blank reference number blocked | Negative | No | No | Yes |
| TC-NOC-007 | Date picker back navigation works | Positive | No | No | Yes |
| TC-NOC-008 | No date selected blocked | Negative | No | No | Yes |

---

## MODULE 7: TRUST / SOCIETY DETAILS

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **8** |
| Positive | 2 |
| Negative | 6 |
| Boundary | 0 |
| Smoke | 1 |
| Sanity | 3 |
| Regression | 8 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-TRUST-001 | Complete trust form submits successfully | Positive | Yes | Yes | Yes |
| TC-TRUST-002 | Ownership type not selected blocked | Negative | No | Yes | Yes |
| TC-TRUST-003 | Blank trust name blocked | Negative | No | No | Yes |
| TC-TRUST-004 | Future establishment date rejected | Negative | No | Yes | Yes |
| TC-TRUST-005 | Registration before establishment rejected | Negative | No | No | Yes |
| TC-TRUST-006 | Blank registration number blocked | Negative | No | No | Yes |
| TC-TRUST-007 | Dynamic form loading verified | Positive | No | No | Yes |
| TC-TRUST-008 | Blank establishment date blocked | Negative | No | No | Yes |

---

## MODULE 8: LAND CERTIFICATE

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **10** |
| Positive | 4 |
| Negative | 6 |
| Boundary | 0 |
| Smoke | 1 |
| Sanity | 3 |
| Regression | 10 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-LAND-001 | Complete land form submits successfully | Positive | Yes | Yes | Yes |
| TC-LAND-002 | Plot type triggers dynamic form | Positive | No | Yes | Yes |
| TC-LAND-003 | Owned vs Leased shows correct fields | Positive | No | Yes | Yes |
| TC-LAND-004 | Zero land area rejected | Negative | No | No | Yes |
| TC-LAND-005 | Negative land area rejected | Negative | No | No | Yes |
| TC-LAND-006 | Non-numeric land area rejected | Negative | No | No | Yes |
| TC-LAND-007 | Sale Deed conditional fields work | Positive | No | No | Yes |
| TC-LAND-008 | Area unit not selected blocked | Negative | No | No | Yes |
| TC-LAND-009 | Future document date rejected | Negative | No | No | Yes |
| TC-LAND-010 | All blank fields shows all errors | Negative | No | No | Yes |

---

## MODULE 9: UPLOAD DOCUMENTS

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **10** |
| Positive | 3 |
| Negative | 5 |
| Boundary | 2 |
| Smoke | 1 |
| Sanity | 3 |
| Regression | 10 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-DOC-001 | All documents upload and proceed | Positive | Yes | Yes | Yes |
| TC-DOC-002 | NOC document missing blocked | Negative | No | Yes | Yes |
| TC-DOC-003 | Invalid file type rejected | Negative | No | Yes | Yes |
| TC-DOC-004 | File size exceeds limit rejected | Boundary | No | No | Yes |
| TC-DOC-005 | Affiliation type not selected blocked | Negative | No | No | Yes |
| TC-DOC-006 | Checkboxes unchecked blocked | Negative | No | No | Yes |
| TC-DOC-007 | File replacement works | Positive | No | No | Yes |
| TC-DOC-008 | Comments max length handling | Boundary | No | No | Yes |
| TC-DOC-009 | Valid image formats accepted | Positive | No | No | Yes |
| TC-DOC-010 | All documents missing shows errors | Negative | No | No | Yes |

---

## MODULE 10: PAYMENT

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **10** |
| Positive | 6 |
| Negative | 4 |
| Boundary | 0 |
| Smoke | 3 |
| Sanity | 5 |
| Regression | 10 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-PAY-001 | Complete payment via ICICI succeeds | Positive | Yes | Yes | Yes |
| TC-PAY-002 | Payment URL redirect correct | Positive | No | Yes | Yes |
| TC-PAY-003 | ICICI gateway selection works | Positive | No | Yes | Yes |
| TC-PAY-004 | HDFC gateway selection works | Positive | No | No | Yes |
| TC-PAY-005 | No gateway selected blocked | Negative | No | Yes | Yes |
| TC-PAY-006 | Payment timeout handled | Negative | No | No | Yes |
| TC-PAY-007 | Payment cancellation handled | Negative | No | No | Yes |
| TC-PAY-008 | Transaction success message shown | Positive | Yes | Yes | Yes |
| TC-PAY-009 | Post-payment redirect to homepage | Positive | Yes | Yes | Yes |
| TC-PAY-010 | Correct payment amount displayed | Negative | No | No | Yes |

---

## MODULE 11: CROSS-CUTTING / WORKFLOW

| Metric | Count |
|--------|-------|
| **Total Test Cases** | **7** |
| Positive | 5 |
| Negative | 2 |
| Boundary | 0 |
| Smoke | 1 |
| Sanity | 1 |
| Regression | 7 |

| TC ID | Test Case | Scenario Type | Smoke | Sanity | Regression |
|-------|-----------|---------------|-------|--------|------------|
| TC-WF-001 | Complete E2E flow succeeds | Positive | Yes | Yes | Yes |
| TC-WF-002 | Multi-school execution works | Positive | No | No | Yes |
| TC-WF-003 | Screenshot captured on failure | Positive | No | No | Yes |
| TC-WF-004 | Error logging on failure | Positive | No | No | Yes |
| TC-WF-005 | Back navigation between steps | Positive | No | No | Yes |
| TC-WF-006 | Session timeout handling | Negative | No | No | Yes |
| TC-WF-007 | Browser refresh data persistence | Negative | No | No | Yes |

---

# SECTION 6: CONSOLIDATED SUMMARY

## Test Case Totals

| Metric | Count |
|--------|-------|
| **Total Unique Test Cases** | **97** |
| Total Positive | 43 |
| Total Negative | 47 |
| Total Boundary | 7 |
| Total Smoke | 14 |
| Total Sanity | 35 |
| Total Regression | 97 |

## Automation Coverage (Current vs Target)

| State | Count | Percentage |
|-------|-------|------------|
| Currently Fully Covered | 33 | 34% |
| Currently Partially Covered | 5 | 5% |
| Currently Not Covered | 59 | 61% |
| **Target After Implementation** | **97** | **100%** |

---

# SECTION 7: DEVELOPMENT ROADMAP — IMPLEMENTATION ORDER

## Sprint 1 (Days 1-3): Foundation + Authentication

| # | Task | Deliverable | Effort |
|---|------|-------------|--------|
| 1 | Create utils/validation_helper.py | Reusable assertion utilities | 0.5 day |
| 2 | Create utils/navigation_helper.py | Reusable navigation utilities | 0.5 day |
| 3 | Create test_data/Validation_Data.xlsx | Negative + boundary data for all modules | 0.5 day |
| 4 | Add new fixtures to conftest.py | logged_in_page, validation_data, boundary_data | 0.5 day |
| 5 | Create tests/test_registration_validation.py | 11 negative/boundary registration tests | 0.5 day |
| 6 | Create tests/test_login_validation.py | 8 negative login tests | 0.5 day |

**Sprint 1 Output:** 19 new automated tests + 3 reusable utility files

---

## Sprint 2 (Days 4-6): Form Validation — Core Modules

| # | Task | Deliverable | Effort |
|---|------|-------------|--------|
| 7 | Add new methods to school_details_page.py | click_next(), get_validation_errors() | 0.5 day |
| 8 | Create tests/test_school_details_validation.py | 12 school validation tests | 1 day |
| 9 | Add new methods to address_details_page.py | click_next(), fill_pin_code() | 0.5 day |
| 10 | Create tests/test_address_validation.py | 10 address validation tests | 1 day |

**Sprint 2 Output:** 22 new automated tests

---

## Sprint 3 (Days 7-9): Form Validation — Remaining Modules

| # | Task | Deliverable | Effort |
|---|------|-------------|--------|
| 11 | Add new methods to noc_details_page.py | click_next(), select_future_date() | 0.5 day |
| 12 | Create tests/test_noc_validation.py | 6 NOC validation tests | 0.5 day |
| 13 | Add new methods to trust_details_page.py | click_next(), set dates individually | 0.5 day |
| 14 | Create tests/test_trust_validation.py | 6 trust validation tests | 0.5 day |
| 15 | Add new methods to land_certificate_page.py | click_next(), fill_land_area() | 0.5 day |
| 16 | Create tests/test_land_validation.py | 8 land validation tests | 0.5 day |

**Sprint 3 Output:** 20 new automated tests

---

## Sprint 4 (Days 10-11): Upload + Payment + Workflow

| # | Task | Deliverable | Effort |
|---|------|-------------|--------|
| 17 | Add new methods to upload_documents_page.py | click_proceed(), get_upload_errors() | 0.5 day |
| 18 | Create tests/test_upload_validation.py | 8 upload validation tests | 0.5 day |
| 19 | Create tests/test_payment_validation.py | 6 payment tests | 0.5 day |
| 20 | Create tests/test_workflow_validation.py | 5 workflow tests | 0.5 day |

**Sprint 4 Output:** 19 new automated tests

---

## Implementation Priority Order

| Priority | Module | Reason | Test Count |
|----------|--------|--------|-----------|
| P1 | Registration | Entry point, most negative scenarios | 13 |
| P1 | Authentication | Security critical, high risk | 10 |
| P2 | School Details | Most form fields, highest regression value | 14 |
| P2 | Address Details | Cascading logic, complex interactions | 12 |
| P3 | NOC Details | Business rules (date logic) | 8 |
| P3 | Trust Details | Business rules (date relationships) | 8 |
| P4 | Land Certificate | Conditional rendering, dynamic forms | 10 |
| P4 | Upload Documents | File handling, mandatory uploads | 10 |
| P5 | Payment | External gateway, limited control | 10 |
| P5 | Workflow | Cross-cutting, depends on other modules | 7 |

---

# SECTION 8: EXECUTION COMMANDS (POST-IMPLEMENTATION)

```
# Run ALL regression (97 tests)
python -m pytest tests/ -m regression -v --alluredir=allure-results

# Run ONLY smoke (14 tests)
python -m pytest tests/ -m smoke -v --alluredir=allure-results

# Run ONLY sanity (35 tests)
python -m pytest tests/ -m sanity -v --alluredir=allure-results

# Run specific module
python -m pytest tests/test_school_details_validation.py -v --alluredir=allure-results

# Run E2E (unchanged)
python -m pytest tests/test_preliminary_form_main.py --headed -v --alluredir=allure-results

# Run negative tests only
python -m pytest tests/ -k "negative or invalid or blank" -v --alluredir=allure-results
```

---

# SECTION 9: RISK ASSESSMENT

| Risk | Mitigation |
|------|-----------|
| New methods break existing Page Objects | Add-only approach; never modify existing method signatures |
| New fixtures conflict with existing | Use unique fixture names; add at bottom of conftest |
| Negative tests interfere with E2E data | Use separate Validation_Data.xlsx; never modify Data_Schools.xlsx |
| Regression suite execution time too long | Use pre-authenticated fixtures to skip login for most tests |
| Password manual entry blocks regression | Create API-based login fixture OR store encrypted credentials |

---

# SECTION 10: SUCCESS CRITERIA

| Milestone | Criteria | Target |
|-----------|----------|--------|
| Sprint 1 Complete | 19 tests passing, utilities reusable | Day 3 |
| Sprint 2 Complete | 41 cumulative tests passing | Day 6 |
| Sprint 3 Complete | 61 cumulative tests passing | Day 9 |
| Sprint 4 Complete | 80 cumulative tests passing | Day 11 |
| Full Coverage | 97 tests, all suites runnable independently | Day 11 |
| Quality Gate | Zero impact on existing E2E script | Always |

---

**Document Status:** FINAL
**Prepared By:** Senior QA Automation Architect
**Date:** 01-Jul-2026
**Framework Version:** 1.0
**Next Action:** Approve plan → Begin Sprint 1 implementation
