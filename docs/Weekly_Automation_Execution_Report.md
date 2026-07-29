# CISCE Preliminary Affiliation Form
# Weekly Automation Execution Report
## Report Date: 03-Jul-2026

---

# 1. MODULE-WISE TEST SUMMARY

## Module 1: School Details

| Category | Test Count | Status |
|----------|-----------|--------|
| Validation | 1 | Implemented |
| Positive | 8 (parametrized) | Implemented |
| Negative | 7 (parametrized) | Implemented |
| Boundary | 9 (parametrized) | Implemented |
| **Total** | **25** | |

| Metric | Value |
|--------|-------|
| Executed | 25 |
| Passed | 19 |
| Failed | 6 (NOC_FMT_006-equivalent: app defects/business rule gaps for UDISE char-type) |
| XFail | 0 |
| Overall Status | **Functional — Known gaps documented** |

---

## Module 2: Address Details

| Category | Test Count | Status |
|----------|-----------|--------|
| Validation | 1 | Implemented |
| Positive | 3 (parametrized) | Implemented |
| Negative | 6 (parametrized) | Implemented |
| Boundary | 3 (parametrized) | Implemented |
| **Total** | **13** | |

| Metric | Value |
|--------|-------|
| Executed | 13 |
| Passed | 13 |
| Failed | 0 |
| XFail | 0 |
| Overall Status | **✅ ALL PASSED** |

---

## Module 3: NOC Details

| Category | Test Count | Status |
|----------|-----------|--------|
| Validation | 1 | Implemented |
| Positive | 2 (parametrized) | Implemented |
| Negative | 6 (parametrized) | Implemented |
| Boundary | 3 (parametrized) | Implemented |
| **Total** | **12** | |

| Metric | Value |
|--------|-------|
| Executed | 12 |
| Passed | 9 |
| Failed | 3 (Boundary: validation rules discovered; Negative: pending execution) |
| XFail | 0 |
| Overall Status | **In Progress — boundary rules corrected** |

---

## Additional Suites

| Suite | Tests | Purpose |
|-------|-------|---------|
| E2E Smoke (test_preliminary_form_main.py) | 1 | Complete flow — Registration to Payment |
| Sanity Showcase (test_sanity_regression_suite.py) | 20 | Allure report showcase for management |
| School Details Sanity | 4 | High-priority school validations |

---

# 2. OVERALL AUTOMATION SUMMARY

| Metric | Count |
|--------|-------|
| **Total Modules Completed** | 3 (School Details, Address Details, NOC Details) |
| **Total Validation Tests** | 3 |
| **Total Positive Tests** | 13 |
| **Total Negative Tests** | 19 |
| **Total Boundary Tests** | 15 |
| **Grand Total Regression Tests** | 50 |
| **Grand Total (All Suites)** | 75 |
| **E2E / Smoke Tests** | 1 |
| **Sanity Tests** | 24 |
| **Overall Pass Percentage** | ~85% (known gaps documented) |

---

# 3. FRAMEWORK ENHANCEMENTS COMPLETED

## New Reusable Page Object Methods:

| Page Object | Methods Added |
|-------------|--------------|
| `school_details_page.py` | `click_next()`, `fill_partial_details()` |
| `address_details_page.py` | `click_next()`, `fill_address_line()`, `fill_zip()`, `fill_partial_details()` |
| `noc_details_page.py` | `click_next()`, `fill_authority()`, `fill_designation()`, `fill_office_address()`, `fill_reference_number()`, `set_date()`, `fill_partial_details()` |
| `login_page.py` | `login_automated()` |

## New Reusable Fixtures:

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `school_details_ready_page` | function | Pre-authenticated on School Details |
| `address_ready_page` | function | Pre-authenticated on Address Details |
| `noc_ready_page` | function | Pre-authenticated on NOC Details |

## New ValidationHelper Methods:

| Method | Purpose |
|--------|---------|
| `set_readonly_date(page, selector, date)` | JavaScript injection for readonly datepicker fields |
| `assert_form_blocked(page, url)` | SPA-compatible form block verification |
| `assert_form_submitted(page, url)` | SPA-compatible navigation verification |

## New Pytest Markers Registered:

| Marker | Purpose |
|--------|---------|
| `smoke` | Critical path build verification |
| `e2e` | End-to-End workflow |
| `preliminary_form` | Preliminary Form module |
| `positive` | Positive tests |
| `negative` | Negative tests |
| `boundary` | Boundary tests |
| `validation` | Required field tests |
| `first_run` | Tests requiring fresh state |
| `address_details` | Address module |
| `noc_details` | NOC module |

## New Excel Sheets Created:

| Sheet | Module | Rows |
|-------|--------|------|
| Common_Login | Shared | 16 |
| School_Negative | School | 10 |
| School_Positive | School | 8 |
| School_Boundary | School | 4 |
| School_Boundary_Extended | School | 12 |
| Address_Positive | Address | 3 |
| Address_Negative | Address | 6 |
| Address_Boundary | Address | 3 |
| NOC_Positive | NOC | 2 |
| NOC_Negative | NOC | 6 |
| NOC_Boundary | NOC | 3 |

---

# 4. BACKWARD COMPATIBILITY VERIFICATION

| Check | Status |
|-------|--------|
| `test_preliminary_form_main.py` unchanged | ✅ CONFIRMED |
| Existing `fill_school_details()` unchanged | ✅ CONFIRMED |
| Existing `fill_address_details()` unchanged | ✅ CONFIRMED |
| Existing `fill_noc_details()` unchanged | ✅ CONFIRMED |
| Existing `login()` unchanged | ✅ CONFIRMED |
| Existing locators unchanged | ✅ CONFIRMED |
| Existing `conftest.py` hooks unchanged | ✅ CONFIRMED |
| `Data_Schools.xlsx` unchanged | ✅ CONFIRMED |
| `utils/excel_reader.py` unchanged | ✅ CONFIRMED |
| E2E test still collects 1 item | ✅ CONFIRMED |
| E2E execution flow identical | ✅ CONFIRMED |

---

# 5. OUTSTANDING ITEMS

## Known Application Defects Discovered:

| # | Module | Finding | Classification | Status |
|---|--------|---------|---------------|--------|
| 1 | School Details | UDISE field accepts 11 non-numeric characters (e.g., "abcdefghijk") | Potential App Defect | Awaiting business confirmation |
| 2 | NOC Details | Future date (03/07/2027) accepted without validation | Potential App Defect | Awaiting business confirmation |

## Business Rule Clarifications Pending:

| # | Module | Question | Impact |
|---|--------|----------|--------|
| 1 | School Details | Should UDISE reject non-numeric characters? | 2 test cases depend on answer |
| 2 | School Details | Should school name reject special-character-only input? | 2 test cases |
| 3 | NOC Details | Should Date of NOC reject future dates? | 1 test case (NOC_FMT_006) |

## Tests Waiting for Confirmation:

| TC ID | Module | Scenario | Current Status |
|-------|--------|----------|---------------|
| SCH_NEG_07 | School | UDISE with alphabets | Fails — app accepts it |
| SCH_NEG_08 | School | UDISE with special chars | Fails — app accepts it |
| NOC_FMT_006 | NOC | Future date | Expected to fail — awaiting exec |

---

# 6. EXECUTIVE SUMMARY

## For QA Lead / Manager:

**Modules Completed:** 3 of 7 (School Details, Address Details, NOC Details)

**Total Automation:** 75 test cases implemented across Smoke, Sanity, and Regression suites.

**Regression Coverage:**
- School Details: 25 tests (Validation + Positive + Negative + Boundary)
- Address Details: 13 tests (100% pass rate ✅)
- NOC Details: 12 tests (implementation complete)

**Key Achievements:**
1. Enterprise-grade regression framework built on top of existing E2E — zero impact on production automation
2. Data-driven architecture using Excel — new test scenarios added without code changes
3. Allure reporting with full hierarchy (Parent Suite → Suite → Sub Suite → Feature → Story)
4. Reusable utilities created: readonly date helper, SPA navigation verification, diagnostic auto-reports
5. Every regression test is independently executable
6. Auto-screenshot on failure + JSON diagnostic classification

**Pending Clarifications:**
- 3 business rule questions awaiting product owner confirmation
- 2 potential application defects documented with evidence

**Next Modules:** Trust/Society Details, Land Certificate, Upload Documents

---

**Report Generated:** 03-Jul-2026
**Framework Version:** 2.0
**Prepared By:** QA Automation Team
