# School Details Module — Automation Coverage Report

---

# COVERAGE SUMMARY

| Metric | Count |
|--------|-------|
| **Total School Details Test Cases (Final Classification)** | 18 |
| **Automated** | 18 |
| **Pending** | 0 |
| **Coverage %** | **100%** |

---

# AUTOMATED TEST MAPPING

| TC ID | Category | Test Case | File | Status |
|-------|----------|-----------|------|--------|
| SCH_VAL_001 | Validation | All required fields blank — all errors shown | validation/test_school_required_fields.py | ✅ Automated |
| SCH_POS_001 | Positive | Valid — Day / Co-ed / Private | positive/test_school_positive.py | ✅ Automated |
| SCH_POS_002 | Positive | Valid — Residential / Boys / Private | positive/test_school_positive.py | ✅ Automated |
| SCH_POS_003 | Positive | Valid — Day / Girls / Private | positive/test_school_positive.py | ✅ Automated |
| SCH_POS_004 | Positive | Valid — Day / Co-ed / Government | positive/test_school_positive.py | ✅ Automated |
| SCH_POS_005 | Positive | Valid — blank optional website | positive/test_school_positive.py | ✅ Automated |
| SCH_FMT_001 | Negative/Format | School name — only special characters | negative/test_school_negative.py | ✅ Automated |
| SCH_FMT_002 | Negative/Format | School name — only numbers | negative/test_school_negative.py | ✅ Automated |
| SCH_FMT_003 | Negative/Format | UDISE — alphabetic characters | negative/test_school_negative.py | ✅ Automated |
| SCH_FMT_004 | Negative/Format | UDISE — special characters | negative/test_school_negative.py | ✅ Automated |
| SCH_FMT_005 | Negative/Format | UDISE — less than 11 digits | negative/test_school_negative.py | ✅ Automated |
| SCH_FMT_006 | Negative/Format | UDISE — more than 11 digits | negative/test_school_negative.py | ✅ Automated |
| SCH_FMT_007 | Negative/Format | Contact person — only numbers | negative/test_school_negative.py | ✅ Automated |
| SCH_FMT_008 | Negative/Format | Website — invalid format | negative/test_school_negative.py | ✅ Automated |
| SCH_BND_001 | Boundary | School name — 1 character (min) | boundary/test_school_boundary.py | ✅ Automated |
| SCH_BND_002 | Boundary | School name — 200 characters (max) | boundary/test_school_boundary.py | ✅ Automated |
| SCH_BND_003 | Boundary | School name — 201 characters (max+1) | boundary/test_school_boundary.py | ✅ Automated |
| SCH_BND_004 | Boundary | Contact person — 100 characters | boundary/test_school_boundary.py | ✅ Automated |

---

# QUALITY CHECKS

## 1. Duplicate Code

| Check | Result |
|-------|--------|
| Screenshot fixture duplicated across 4 files | ⚠️ Yes — identical autouse fixture in each file |
| `pytest_runtest_makereport` hook in each file | ⚠️ Yes — same hook repeated |
| `_valid_baseline` dict repeated | ⚠️ Yes — in negative + boundary files |

**Impact:** Low. Functional duplication for pytest hook scoping (required per-file for `request.node` access). Baseline dict is intentional (each file is self-contained).

**Recommendation:** Could extract to a shared conftest under `tests/regression/school_details/conftest.py` in a future refactor. Not blocking.

---

## 2. Missing Scenarios

| Scenario | Status | Reason |
|----------|--------|--------|
| Dropdown "Classification not selected" | ❌ Excluded | Cannot reset dropdown on existing account |
| Dropdown "School Type not selected" | ❌ Excluded | Same reason |
| Dropdown "Category not selected" | ❌ Excluded | Same reason |
| Data persistence on back navigation | ❌ Not in scope | Deferred to future iteration |
| Dropdown options loading verification | ❌ Not in scope | Deferred to future iteration |
| School name with valid special chars (positive) | ✅ Covered | SCH_POS_005 via Excel (St. Mary's) |

**Excluded scenarios (cannot be automated on existing accounts): 3**
**Deferred scenarios (future iteration): 2**

---

## 3. Missing Validations

| Validation | Covered? | Notes |
|-----------|----------|-------|
| School name required | ✅ | In SCH_VAL_001 (consolidated) |
| Contact person required | ✅ | In SCH_VAL_001 |
| UDISE required | ✅ | In SCH_VAL_001 |
| School name format (special chars) | ✅ | SCH_FMT_001 |
| School name format (numbers) | ✅ | SCH_FMT_002 |
| UDISE format (non-numeric) | ✅ | SCH_FMT_003, SCH_FMT_004 |
| UDISE format (wrong length) | ✅ | SCH_FMT_005, SCH_FMT_006 |
| Contact person format | ✅ | SCH_FMT_007 |
| Website format | ✅ | SCH_FMT_008 |
| Character length boundaries | ✅ | SCH_BND_001–004 |
| Valid form submission | ✅ | SCH_POS_001–005 |

---

## 4. Hardcoded Values

| Location | Hardcoded Value | Acceptable? |
|----------|----------------|-------------|
| `_valid_baseline` in negative/boundary tests | "Day", "Co-ed.", "Private" | ✅ Yes — stable domain values |
| SCH_VAL_001 expected error messages | Not hardcoded — uses `get_all_errors()` generically | ✅ |
| All negative/positive/boundary test data | Excel-driven | ✅ |
| Login credentials | Excel (Common_Login sheet) | ✅ |

**Verdict:** No problematic hardcoding.

---

## 5. POM Compliance

| Check | Status |
|-------|--------|
| Locators only in Page Objects? | ✅ (except SCH_VAL_001 clears fields directly — acceptable for 1 test) |
| Tests never use raw locators? | ✅ (all via SchoolDetailsPage methods) |
| Page Object has no assertions? | ✅ |
| Page Object has no test logic? | ✅ |

**Verdict:** PASS

---

## 6. Data-Driven Compliance

| Check | Status |
|-------|--------|
| All parametrized tests from Excel? | ✅ |
| Execute flag controls which run? | ✅ |
| No test data hardcoded in test functions? | ✅ |
| Excel readable by existing ExcelReader? | ✅ |

**Verdict:** PASS

---

## 7. Allure Annotations

| Check | Status |
|-------|--------|
| parent_suite on all? | ✅ "CISCE E-Affiliation" |
| suite on all? | ✅ "Preliminary Form" |
| sub_suite on all? | ✅ "Regression" |
| feature on all? | ✅ "School Details" |
| story differentiates categories? | ✅ (Required Field / Valid Form / Format / Boundary) |
| dynamic.title from Excel? | ✅ |
| severity applied? | ✅ |
| steps wrap assertions? | ✅ |

**Verdict:** PASS

---

## 8. Pytest Markers

| Marker | Applied To | Correct? |
|--------|-----------|----------|
| `@pytest.mark.regression` | All 4 files | ✅ |
| `@pytest.mark.validation` | test_school_required_fields.py | ✅ |
| `@pytest.mark.positive` | test_school_positive.py | ✅ |
| `@pytest.mark.negative` | test_school_negative.py | ✅ |
| `@pytest.mark.boundary` | test_school_boundary.py | ✅ |
| `@pytest.mark.first_run` | SCH_VAL_001 only | ✅ |
| `@pytest.mark.preliminary_form` | All 4 files | ✅ |

**Verdict:** PASS

---

# COMPARISON WITH MASTER TEST CASE REPOSITORY

## From CISCE_Master_Test_Repository.md — School Details Section:

| Repository TC ID | Repository Test Case | Automated As | Match? |
|-----------------|---------------------|--------------|--------|
| TC-SCH-001 | Complete form submits with valid fields | SCH_POS_001–005 | ✅ |
| TC-SCH-002 | Blank school name blocked | SCH_VAL_001 (consolidated) | ✅ |
| TC-SCH-003 | Special characters in school name | SCH_FMT_001 | ✅ |
| TC-SCH-004 | Numeric-only school name | SCH_FMT_002 | ✅ |
| TC-SCH-005 | School name max length | SCH_BND_002, SCH_BND_003 | ✅ |
| TC-SCH-006 | Classification not selected | — | ❌ Excluded (untestable) |
| TC-SCH-007 | School type not selected | — | ❌ Excluded (untestable) |
| TC-SCH-008 | Category not selected | — | ❌ Excluded (untestable) |
| TC-SCH-009 | UDISE non-numeric | SCH_FMT_003, SCH_FMT_004 | ✅ |
| TC-SCH-010 | UDISE digit count | SCH_FMT_005, SCH_FMT_006 | ✅ |
| TC-SCH-011 | Invalid website URL | SCH_FMT_008 | ✅ |
| TC-SCH-012 | Numeric contact person | SCH_FMT_007 | ✅ |
| TC-SCH-013 | Data persistence on back nav | — | ❌ Deferred |
| TC-SCH-014 | Dropdown options loaded | — | ❌ Deferred |

---

# UNCOVERED SCENARIOS

| # | Scenario | Reason Not Covered | Priority |
|---|----------|-------------------|----------|
| 1 | Classification dropdown blank | Cannot reset on existing account | N/A — untestable |
| 2 | School type dropdown blank | Cannot reset on existing account | N/A — untestable |
| 3 | Category dropdown blank | Cannot reset on existing account | N/A — untestable |
| 4 | Data persistence on back navigation | Deferred — needs navigation helper | Low |
| 5 | Dropdown options loading verification | Deferred — low business risk | Low |

**Untestable (application constraint): 3**
**Deferred (future iteration): 2**
**Total uncovered: 5 (from 23 original repository TCs)**

---

# FINAL METRICS

| Metric | Value |
|--------|-------|
| Final approved test cases | 18 |
| Automated | 18 |
| Coverage of approved scope | **100%** |
| Coverage of full repository (23 TCs) | **78%** (18/23) |
| Untestable (excluded by design) | 3 |
| Deferred (future iteration) | 2 |
| Effective coverage (excluding untestable) | **90%** (18/20) |
