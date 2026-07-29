# Certificate of Land — Optimized Implementation Plan
## Based on Approved 35-Test Optimized Regression Matrix

---

# SCOPE

Implement the optimized regression suite (35 tests) for the Certificate of Land module covering:
- Single Plot → Owned (18 tests)
- Single Plot → Leased (8 tests)
- Multiple Plot (9 tests)

---

# CURRENT STATE (What Already Exists)

| Item | Status |
|------|--------|
| `tests/regression/land_certificate/` folder structure | ✅ Created |
| `tests/regression/land_certificate/__init__.py` (all 5) | ✅ Created |
| `pages/land_certificate_page.py` — E2E method `fill_land_details()` | ✅ Exists (READ-ONLY) |
| `pages/land_certificate_page.py` — Regression methods (Owned path) | ✅ Exists (6 methods) |
| `conftest.py` — `land_ready_page` fixture | ✅ Exists |
| `pytest.ini` — `land_certificate` marker | ✅ Exists |
| Excel sheets: `Land_Positive`, `Land_Negative`, `Land_Boundary` | ✅ Exists (old 12-test data) |
| Old test files (12-test Phase 1) | ⚠️ Will be REPLACED |

---

# PHASE 1 — FRAMEWORK SETUP

## Objective: Add page methods for Leased and Multiple paths

### Files to Extend:

| # | File | Change |
|---|------|--------|
| 1 | `pages/land_certificate_page.py` | Add 3 new methods (Leased + Multiple) |

### New Page Methods Required:

| # | Method | Purpose | Implementation |
|---|--------|---------|----------------|
| 1 | `fill_partial_leased_details(data, skip_fields)` | Fill Single→Leased path fields + click Next | Select Single + Leased, fill lease fields, handle Renewal conditional, click Next |
| 2 | `fill_multiple_plot_details(data, skip_fields)` | Fill Multiple path fields + click Next | Select Multiple, fill plots/number fields, handle Contiguous→Boundary→Explanation chain, click Next |
| 3 | `select_renewal_clause(option)` | Select Renewal Yes/No radio + wait | `locator("#renewal_yes"/"#renewal_no").click()` + wait 1000ms |

### Existing Methods Reused (NO modification):

| Method | Used By |
|--------|---------|
| `click_next()` | All tests |
| `select_plot_type(type_name)` | Leased, Multiple, UI tests |
| `select_land_type(type_name)` | Leased tests |
| `fill_land_area(value)` | Boundary tests |
| `fill_document_date(date_value)` | Boundary, Negative tests |
| `fill_partial_owned_details(data, skip_fields)` | Positive, Negative, Boundary (Owned) |

### Fixture — Already Exists:

`land_ready_page` (conftest.py) — no change needed.

### Diagnostics Required BEFORE Implementation:

| # | Diagnostic | For Phase |
|---|-----------|-----------|
| 1 | Leased path: Confirm all field IDs and readonly status | Phase 4 |
| 2 | Leased path: Confirm lease date fields are readonly | Phase 4 |
| 3 | Leased path: Confirm Renewal radio locators (`#renewal_yes`/`#renewal_no` or different) | Phase 4 |
| 4 | Multiple path: Confirm Contiguous radio locators | Phase 5 |
| 5 | Multiple path: Confirm Boundary Wall radio + Explanation textarea locators | Phase 5 |
| 6 | Multiple path: Confirm validation messages for blank fields | Phase 5 |

### Estimated Effort: 1.5 hours
### Risk: Low (additive only — existing methods untouched)
### Reused: Existing `select_plot_type()`, `select_land_type()`, `ValidationHelper.set_readonly_date()` pattern

---

# PHASE 2 — EXCEL TEST DATA

## Objective: Replace old 12-test Excel data with optimized 35-test data

### Files to Modify:

| # | File | Change |
|---|------|--------|
| 1 | `test_data/negative/Validation_Data.xlsx` | Replace `Land_Positive`, `Land_Negative`, `Land_Boundary` sheets. Add `Land_UI` sheet. |

### Excel Sheets Required:

#### Sheet: `Land_Positive` (9 rows)

| scenario_id | execute | scenario_description | flow | plot_type | land_type | area_unit | land_area | situated_in | situated_at | land_owned_by | land_title_document | sale_deed_favor | registration_details | executed_by | registration_office | document_date | renewal_clause | renewal_duration | no_of_plots | plot_number | contiguous | boundary_wall | explanation | expected_result | priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Rows:** LAND_POS_001 through LAND_POS_009

#### Sheet: `Land_Negative` (11 rows)

| scenario_id | execute | scenario_description | flow | field_name | field_value | expected_error | priority | remarks |
|---|---|---|---|---|---|---|---|---|

**Rows:** LAND_NEG_001 through LAND_NEG_011

#### Sheet: `Land_Boundary` (7 rows)

| scenario_id | execute | scenario_description | flow | field_name | field_value | expected_outcome | expected_message | priority |
|---|---|---|---|---|---|---|---|---|

**Rows:** LAND_BND_001 through LAND_BND_007

#### Sheet: `Land_UI` (5 rows — optional, may be hardcoded in test)

| scenario_id | execute | scenario_description | action | expected_visible | expected_hidden | priority |
|---|---|---|---|---|---|---|

**Rows:** LAND_UI_001 through LAND_UI_005

### Estimated Effort: 45 minutes
### Risk: Low (data entry only)
### Reused: Existing `ExcelReader` utility, existing sheet pattern

---

# PHASE 3 — SINGLE PLOT → OWNED (18 tests)

## Objective: Implement all Owned path tests

### Tests:

| Category | Tests | IDs |
|----------|-------|-----|
| Validation | 1 | LAND_VAL_001 |
| Positive | 5 | LAND_POS_001–005 |
| Negative | 6 | LAND_NEG_001–006 |
| Boundary | 4 | LAND_BND_001–004 |
| Dynamic UI | 2 | LAND_UI_001, LAND_UI_002 |

### Files to Create/Replace:

| # | File | Purpose |
|---|------|---------|
| 1 | `tests/regression/land_certificate/validation/test_land_validation.py` | LAND_VAL_001 (@first_run) |
| 2 | `tests/regression/land_certificate/positive/test_land_positive.py` | LAND_POS_001–005 (parametrized) |
| 3 | `tests/regression/land_certificate/negative/test_land_negative.py` | LAND_NEG_001–006 (parametrized) |
| 4 | `tests/regression/land_certificate/boundary/test_land_boundary.py` | LAND_BND_001–004 (parametrized) |
| 5 | `tests/regression/land_certificate/ui/test_land_ui_owned.py` | LAND_UI_001, LAND_UI_002 |

### New Folder:

| Folder | Purpose |
|--------|---------|
| `tests/regression/land_certificate/ui/` | Dynamic UI behaviour tests |
| `tests/regression/land_certificate/ui/__init__.py` | Package init |

### Existing Test Files to REPLACE (not modify):

The old Phase 1 test files (validation, positive, negative, boundary) will be **replaced entirely** with the new optimized versions. The old files had 12 tests; new files have 18 tests for the Owned path.

### Key Patterns Reused:

| Pattern | From |
|---------|------|
| `fill_partial_owned_details(data, skip_fields)` | Existing method |
| `@first_run` marker for validation test | NOC/Trust pattern |
| Parametrized negative with diagnostic on failure | Trust Details pattern |
| `ValidationHelper.assert_error_present()` | All modules |
| `ScreenshotUtil.take_screenshot()` on failure | All modules |
| Allure hierarchy (`parent_suite / suite / sub_suite`) | All modules |
| Navigate-back-after-positive pattern | NOC positive pattern |

### Estimated Effort: 3 hours
### Risk: Low (all locators proven, all methods exist)
### Expected Outcome: 18 tests PASS (High confidence — Owned path is fully diagnostic-confirmed)

---

# PHASE 4 — SINGLE PLOT → LEASED (8 tests)

## Objective: Implement Leased path tests

### Prerequisite: Leased Path Diagnostic

Before implementation, run a diagnostic to confirm:
- All leased field IDs and types
- Lease date fields readonly status
- Renewal clause radio locators
- Duration of Renewal field ID
- Validation messages for blank leased fields

### Tests:

| Category | Tests | IDs |
|----------|-------|-----|
| Validation | 1 | LAND_VAL_002 |
| Positive | 2 | LAND_POS_006, LAND_POS_007 |
| Negative | 3 | LAND_NEG_007, LAND_NEG_008, LAND_NEG_009 |
| Boundary | 1 | LAND_BND_005 |
| Dynamic UI | 1 | LAND_UI_003 |

### Files to Extend:

| # | File | Change |
|---|------|--------|
| 1 | `tests/regression/land_certificate/validation/test_land_validation.py` | Add LAND_VAL_002 |
| 2 | `tests/regression/land_certificate/positive/test_land_positive.py` | POS_006–007 added via Excel (parametrized) |
| 3 | `tests/regression/land_certificate/negative/test_land_negative.py` | NEG_007–009 added via Excel (parametrized) |
| 4 | `tests/regression/land_certificate/boundary/test_land_boundary.py` | BND_005 added via Excel (parametrized) |

### Files to Create:

| # | File | Purpose |
|---|------|---------|
| 1 | `tests/regression/land_certificate/ui/test_land_ui_leased.py` | LAND_UI_003 |

### New Page Methods (from Phase 1 framework):

| Method | Purpose |
|--------|---------|
| `fill_partial_leased_details(data, skip_fields)` | Already planned in Phase 1 |
| `select_renewal_clause(option)` | Already planned in Phase 1 |

### Estimated Effort: 3.5 hours (includes diagnostic)
### Risk: Medium (locators not fully confirmed — diagnostic required first)
### Expected Outcome: 8 tests — outcome depends on diagnostic findings

---

# PHASE 5 — MULTIPLE PLOT (9 tests)

## Objective: Implement Multiple Plot path tests

### Prerequisite: Multiple Path Diagnostic

Before implementation, run a diagnostic to confirm:
- `#no_of_plots` and `#plot_number_school_building` field behaviour
- Contiguous radio locators (may be `#renewal_yes`/`#renewal_no` with name=`plotTypeyes`)
- Boundary Wall radio locators (appear dynamically)
- Explanation textarea locator (appears dynamically)
- Validation messages for blank multiple fields

### Tests:

| Category | Tests | IDs |
|----------|-------|-----|
| Validation | 1 | LAND_VAL_003 |
| Positive | 2 | LAND_POS_008, LAND_POS_009 |
| Negative | 2 | LAND_NEG_010, LAND_NEG_011 |
| Boundary | 2 | LAND_BND_006, LAND_BND_007 |
| Dynamic UI | 2 | LAND_UI_004, LAND_UI_005 |

### Files to Extend:

| # | File | Change |
|---|------|--------|
| 1 | `tests/regression/land_certificate/validation/test_land_validation.py` | Add LAND_VAL_003 |
| 2 | `tests/regression/land_certificate/positive/test_land_positive.py` | POS_008–009 via Excel |
| 3 | `tests/regression/land_certificate/negative/test_land_negative.py` | NEG_010–011 via Excel |
| 4 | `tests/regression/land_certificate/boundary/test_land_boundary.py` | BND_006–007 via Excel |

### Files to Create:

| # | File | Purpose |
|---|------|---------|
| 1 | `tests/regression/land_certificate/ui/test_land_ui_multiple.py` | LAND_UI_004, LAND_UI_005 |

### New Page Method (from Phase 1 framework):

| Method | Purpose |
|--------|---------|
| `fill_multiple_plot_details(data, skip_fields)` | Already planned in Phase 1 |

### Estimated Effort: 3.5 hours (includes diagnostic)
### Risk: Medium-High (locators partially unknown, nested conditionals complex)
### Expected Outcome: 9 tests — outcome depends on diagnostic findings

---

# PHASE 6 — COVERAGE VERIFICATION

## Objective: Run full 35-test suite and verify coverage

### Actions:

| # | Action | Command |
|---|--------|---------|
| 1 | Collect all tests | `python -m pytest tests/regression/land_certificate/ --collect-only -q` |
| 2 | Run sanity subset (12 tests) | `python -m pytest tests/regression/land_certificate/ -m "land_certificate and (validation or positive)" --headed` |
| 3 | Run full regression (35 tests) | `python -m pytest tests/regression/land_certificate/ -v --headed` |
| 4 | Verify E2E unaffected | `python -m pytest tests/test_preliminary_form_main.py --collect-only -q` |
| 5 | Generate Excel report | Automatic via conftest hooks |
| 6 | Verify markers registered | `python -m pytest --markers` |

### Expected Results:

| Metric | Target |
|--------|--------|
| Tests collected | 35 |
| Owned tests PASS | 18/18 (all confirmed by diagnostic) |
| Leased tests | Depends on diagnostic findings |
| Multiple tests | Depends on diagnostic findings |
| E2E test collected | 1 (unchanged) |
| Execution time | ~30 minutes |

### Estimated Effort: 1 hour (run + fix any issues)
### Risk: Low (verification only)

---

# PHASE 7 — ALLURE VERIFICATION

## Objective: Verify Allure report hierarchy and metadata

### Actions:

| # | Action | Verification |
|---|--------|-------------|
| 1 | Run with Allure | `python -m pytest tests/regression/land_certificate/ --alluredir=allure-results` |
| 2 | Generate report | `allure generate allure-results --clean -o allure-report` |
| 3 | Open report | `allure open allure-report --port 9090` |
| 4 | Verify hierarchy | Parent Suite: "CISCE E-Affiliation" → Suite: "Certificate of Land" → Sub-suites: Validation/Positive/Negative/Boundary/UI |
| 5 | Verify screenshots | Failure screenshots attached to failed tests |
| 6 | Verify severity | Critical/Normal mapped correctly |
| 7 | Verify tags | regression, land_certificate, validation/positive/negative/boundary |

### Estimated Effort: 30 minutes
### Risk: Low

---

# GRAND SUMMARY

## Files to Create (New)

| # | File | Purpose |
|---|------|---------|
| 1 | `tests/regression/land_certificate/ui/__init__.py` | Package init |
| 2 | `tests/regression/land_certificate/ui/test_land_ui_owned.py` | LAND_UI_001, UI_002 |
| 3 | `tests/regression/land_certificate/ui/test_land_ui_leased.py` | LAND_UI_003 |
| 4 | `tests/regression/land_certificate/ui/test_land_ui_multiple.py` | LAND_UI_004, UI_005 |

**Total new files: 4**

## Files to Replace (Existing — full rewrite with new optimized content)

| # | File | Old Tests | New Tests |
|---|------|-----------|-----------|
| 1 | `tests/regression/land_certificate/validation/test_land_required_fields.py` → rename to `test_land_validation.py` | 1 | 3 (VAL_001–003) |
| 2 | `tests/regression/land_certificate/positive/test_land_positive.py` | 3 | 9 (POS_001–009) |
| 3 | `tests/regression/land_certificate/negative/test_land_negative.py` | 5 | 11 (NEG_001–011) |
| 4 | `tests/regression/land_certificate/boundary/test_land_boundary.py` | 3 | 7 (BND_001–007) |

**Total replaced files: 4**

## Files to Extend (Additive only)

| # | File | Change |
|---|------|--------|
| 1 | `pages/land_certificate_page.py` | Add 3 new methods (Leased + Multiple) |
| 2 | `test_data/negative/Validation_Data.xlsx` | Replace 3 sheets + add 1 sheet |

**Total extended files: 2**

## Files NEVER Modified

| File | Status |
|------|--------|
| `tests/test_preliminary_form_main.py` | 🔒 LOCKED |
| `pages/land_certificate_page.py` → `fill_land_details()` | 🔒 LOCKED |
| `conftest.py` | ✅ No change needed (fixture exists) |
| `pytest.ini` | ✅ No change needed (marker exists) |
| All other page objects | 🔒 LOCKED |
| All other test files | 🔒 LOCKED |

---

## New Fixtures: 0 (land_ready_page already exists)

## New Page Methods: 3

| # | Method | Flow |
|---|--------|------|
| 1 | `fill_partial_leased_details(data, skip_fields)` | Single→Leased |
| 2 | `fill_multiple_plot_details(data, skip_fields)` | Multiple |
| 3 | `select_renewal_clause(option)` | Leased (Renewal radio) |

## Existing Methods Reused: 6

| Method | Reused By |
|--------|-----------|
| `click_next()` | All 35 tests |
| `select_plot_type()` | All 35 tests |
| `select_land_type()` | Owned + Leased tests |
| `fill_land_area()` | Boundary tests |
| `fill_document_date()` | Boundary + Negative tests |
| `fill_partial_owned_details()` | Owned Positive + Negative + Boundary |

---

## Coverage Summary

| Coverage | Tests | IDs |
|----------|-------|-----|
| Full Regression | 35 | R01–R35 |
| Sanity Subset | 12 | S01–S12 |
| Owned Path | 18 | VAL_001, POS_001–005, NEG_001–006, BND_001–004, UI_001–002 |
| Leased Path | 8 | VAL_002, POS_006–007, NEG_007–009, BND_005, UI_003 |
| Multiple Path | 9 | VAL_003, POS_008–009, NEG_010–011, BND_006–007, UI_004–005 |

---

## Expected Execution Time

| Suite | Tests | Time |
|-------|-------|------|
| Sanity (build verification) | 12 | ~6 min |
| Full Regression (pre-deployment) | 35 | ~30 min |
| Owned-only (Phase 3 validation) | 18 | ~15 min |

---

## Estimated Total Effort

| Phase | Effort |
|-------|--------|
| Phase 1 — Framework setup | 1.5 hrs |
| Phase 2 — Excel test data | 45 min |
| Phase 3 — Owned (18 tests) | 3 hrs |
| Phase 4 — Leased (8 tests) | 3.5 hrs |
| Phase 5 — Multiple (9 tests) | 3.5 hrs |
| Phase 6 — Coverage verification | 1 hr |
| Phase 7 — Allure verification | 30 min |
| **TOTAL** | **~14 hours** |

---

## Risk Summary

| Phase | Risk | Mitigation |
|-------|------|-----------|
| 3 (Owned) | Low | All locators confirmed, methods exist |
| 4 (Leased) | Medium | Run diagnostic first; locators partially known |
| 5 (Multiple) | Medium-High | Run diagnostic first; nested conditionals complex |
| 1–2, 6–7 | Low | Framework/data/verification only |

---

## Reused Components

| Component | From Module |
|-----------|-------------|
| `fill_partial_*()` pattern | School, Address, NOC, Trust |
| Tab-click fixture (`land_ready_page`) | NOC, Trust |
| `@first_run` marker for validation | School, NOC |
| Parametrized negative with diagnostic-on-failure | Trust |
| `ValidationHelper.set_readonly_date()` | NOC, Trust |
| `ValidationHelper.get_all_errors()` + `assert_error_present()` | All modules |
| `ScreenshotUtil.take_screenshot()` | All modules |
| `ExcelReader.get_sheet_data()` | All modules |
| Allure hierarchy pattern | All modules |
| Navigate-back-after-positive | NOC, Trust |

---

## E2E Backward Compatibility: ✅ CONFIRMED

| Check | Guaranteed |
|-------|-----------|
| `test_preliminary_form_main.py` untouched | ✅ |
| `fill_land_details(data)` method unchanged | ✅ |
| Existing locators used by E2E unchanged | ✅ |
| Existing fixtures unchanged | ✅ |
| Existing Excel data (Master/School sheets) unchanged | ✅ |
| E2E execution flow identical | ✅ |
| `conftest.py` hooks unchanged | ✅ |
| All other module tests unchanged | ✅ |

---

**STATUS:** Optimized Implementation Plan complete. Ready for phased execution starting Phase 1.
