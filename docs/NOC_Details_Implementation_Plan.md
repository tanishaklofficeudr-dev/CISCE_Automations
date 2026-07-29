# NOC Details Module — Implementation Plan
## Phased Execution Strategy

---

# PHASE 1: Framework Preparation

## Objective: Create folder structure, add Page Object methods, create fixture, register markers.

### Files Created:

| # | File | Purpose |
|---|------|---------|
| 1 | `tests/regression/noc_details/__init__.py` | Package marker |
| 2 | `tests/regression/noc_details/validation/__init__.py` | Package marker |
| 3 | `tests/regression/noc_details/positive/__init__.py` | Package marker |
| 4 | `tests/regression/noc_details/negative/__init__.py` | Package marker |
| 5 | `tests/regression/noc_details/boundary/__init__.py` | Package marker |

### Files Extended:

| # | File | What to Add |
|---|------|-------------|
| 1 | `pages/noc_details_page.py` | 7 additive methods (see below) |
| 2 | `conftest.py` | `noc_ready_page` fixture at bottom |
| 3 | `pytest.ini` | `noc_details` marker (if not present) |

### New Page Object Methods (ADD to `noc_details_page.py`):

| # | Method | Purpose |
|---|--------|---------|
| 1 | `click_next()` | Click Next without filling |
| 2 | `fill_authority(value)` | Fill/clear NOC authority |
| 3 | `fill_designation(value)` | Fill/clear designation |
| 4 | `fill_office_address(value)` | Fill/clear office address |
| 5 | `fill_reference_number(value)` | Fill/clear reference number |
| 6 | `set_date(date_value)` | Wrapper for `ValidationHelper.set_readonly_date()` |
| 7 | `fill_partial_details(data, skip_fields)` | Fill all except specified + click Next |

### `fill_partial_details` Logic:
```
Text fields in skip_fields → clear with .fill("")
Date in skip_fields → clear with set_readonly_date("", "")
Country/State → always select valid values (cannot blank)
Country selection → wait 1000ms before State
```

### New Fixture (`noc_ready_page`):
```
Logic:
1. Use school_details_ready_page
2. Click "NOC Details" tab directly (confirmed working in diagnostic)
3. Wait 3000ms
4. Verify #noc_authority visible
5. Return page
```

### Marker Registration (`pytest.ini`):
```ini
noc_details: NOC Details module tests
```

### Files Left Untouched:
- `test_preliminary_form_main.py`
- `fill_noc_details()`
- All existing locators
- All existing fixtures
- `utils/excel_reader.py`
- `utils/validation_helper.py` (already has `set_readonly_date`)

### Risk Level: LOW
### Effort: 1.5 hours

---

# PHASE 2: Excel Data

## Objective: Create test data sheets in Validation_Data.xlsx

### Files Extended:

| File | Sheets Added |
|------|-------------|
| `test_data/negative/Validation_Data.xlsx` | `NOC_Positive`, `NOC_Negative`, `NOC_Boundary` |

### Sheet: `NOC_Positive` (2 rows)

| scenario_id | execute | description | noc_authority | designation | office_address | country_value | state_value | noc_reference_number | noc_date | expected_result | priority |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NOC_POS_001 | Yes | Valid NOC — India, Rajasthan, past date | District Education Officer | Director | Govt Office, Jaipur | 2 | 30 | NOC-REG-001 | 16/05/2025 | Form submits to Trust Details | High |
| NOC_POS_002 | Yes | Valid NOC — different state (Maharashtra) | State Education Board | Secretary | Board Office, Mumbai | 2 | 21 | NOC-REG-002 | 10/03/2025 | Form submits successfully | Medium |

### Sheet: `NOC_Negative` (6 rows)

| scenario_id | execute | description | field_name | field_value | expected_error | scenario_type | priority |
|---|---|---|---|---|---|---|---|
| NOC_FMT_001 | Yes | Authority blank | noc_authority | | Authority is required | Negative | High |
| NOC_FMT_002 | Yes | Designation blank | designation | | Designation is required | Negative | Medium |
| NOC_FMT_003 | Yes | Office address blank | office_address | | Office address is required | Negative | Medium |
| NOC_FMT_004 | Yes | Reference number blank | noc_reference_number | | Reference number is required | Negative | Medium |
| NOC_FMT_005 | Yes | Date cleared (empty) | noc_date | | Date is required | Negative | High |
| NOC_FMT_006 | Yes | Future date (xfail) | noc_date | FUTURE | Date cannot be future | Negative | Medium |

### Sheet: `NOC_Boundary` (3 rows)

| scenario_id | execute | description | field_name | field_value | expected_outcome | expected_message | priority |
|---|---|---|---|---|---|---|---|
| NOC_BND_001 | Yes | Authority 1 char | noc_authority | A | ACCEPT | Min char accepted | Medium |
| NOC_BND_002 | Yes | Office address 300 chars | office_address | (300 chars) | ACCEPT | Long address handling | Medium |
| NOC_BND_003 | Yes | Reference number 50 chars | noc_reference_number | (50 chars) | ACCEPT | Long reference handling | Low |

### Files Left Untouched:
- All existing Excel sheets (Common_Login, School_*, Address_*)
- `Data_Schools.xlsx`

### Risk Level: NONE
### Effort: 30 minutes

---

# PHASE 3: Validation Test Implementation

## Objective: Implement NOC_VAL_001

### Files Created:

| File | Tests |
|------|-------|
| `tests/regression/noc_details/validation/test_noc_required_fields.py` | 1 test |

### Markers:
- `@pytest.mark.regression`
- `@pytest.mark.noc_details`
- `@pytest.mark.validation`
- `@pytest.mark.first_run`

### Allure:
- Parent Suite: CISCE E-Affiliation
- Suite: NOC Details
- Sub Suite: Validation
- Feature: NOC Details
- Story: Required Field Validation

### Risk Level: LOW
### Effort: 30 minutes

---

# PHASE 4: Positive Test Implementation

## Objective: Implement NOC_POS_001, NOC_POS_002

### Files Created:

| File | Tests |
|------|-------|
| `tests/regression/noc_details/positive/test_noc_positive.py` | 2 tests (parametrized from Excel) |

### Markers:
- `@pytest.mark.regression`
- `@pytest.mark.noc_details`
- `@pytest.mark.positive`

### Allure:
- Sub Suite: Positive
- Story: Valid Form Submission

### Risk Level: LOW
### Effort: 30 minutes

---

# PHASE 5: Boundary Test Implementation

## Objective: Implement NOC_BND_001–003

### Files Created:

| File | Tests |
|------|-------|
| `tests/regression/noc_details/boundary/test_noc_boundary.py` | 3 tests (parametrized from Excel) |

### Markers:
- `@pytest.mark.regression`
- `@pytest.mark.noc_details`
- `@pytest.mark.boundary`

### Allure:
- Sub Suite: Boundary
- Story: Boundary Value Validation

### Risk Level: LOW
### Effort: 30 minutes

---

# PHASE 6: Negative Test Implementation

## Objective: Implement NOC_FMT_001–006

### Files Created:

| File | Tests |
|------|-------|
| `tests/regression/noc_details/negative/test_noc_negative.py` | 6 tests (parametrized from Excel) |

### Special handling:
- NOC_FMT_005 (empty date): Uses `ValidationHelper.set_readonly_date(page, selector, "")`
- NOC_FMT_006 (future date): Marked `@pytest.mark.xfail(reason="Potential app defect: future date accepted")`
- NOC_FMT_006 data: `field_value = "FUTURE"` → test generates future date dynamically

### Markers:
- `@pytest.mark.regression`
- `@pytest.mark.noc_details`
- `@pytest.mark.negative`

### Allure:
- Sub Suite: Negative
- Story: Negative Validation Scenarios

### Diagnostic on failure (same as Address module):
- Auto-captures screenshot
- Generates JSON diagnostic classifying root cause

### Risk Level: MEDIUM (NOC_FMT_006 expected to fail = xfail)
### Effort: 45 minutes

---

# PHASE 7: Coverage Verification

## Objective: Verify all 12 tests collect and execute correctly.

### Commands:
```powershell
# Collect all
python -m pytest tests/regression/noc_details/ --collect-only -q

# Run all
python -m pytest tests/regression/noc_details/ -v --headed --alluredir=allure-results

# Verify E2E unaffected
python -m pytest tests/test_preliminary_form_main.py --collect-only -q
```

### Expected Results:
- 12 tests collected
- 11 passed + 1 xfail (NOC_FMT_006)
- E2E: 1 test collected (unchanged)

### Risk Level: LOW
### Effort: 1 hour (run + debug)

---

# PHASE 8: Allure Verification

## Objective: Verify Allure report structure.

### Expected Allure Hierarchy:
```
CISCE E-Affiliation
└── NOC Details
    ├── Validation
    │   └── Required Field Validation
    │       └── NOC_VAL_001
    ├── Positive
    │   └── Valid Form Submission
    │       ├── NOC_POS_001
    │       └── NOC_POS_002
    ├── Negative
    │   └── Negative Validation Scenarios
    │       ├── NOC_FMT_001–005
    │       └── NOC_FMT_006 (xfail — Known Issue)
    └── Boundary
        └── Boundary Value Validation
            ├── NOC_BND_001–003
```

### Command:
```powershell
allure open allure-report --port 9090
```

### Risk Level: NONE
### Effort: 15 minutes

---

# SUMMARY: FILES

## Files to Create (9):

| # | File |
|---|------|
| 1 | `tests/regression/noc_details/__init__.py` |
| 2 | `tests/regression/noc_details/validation/__init__.py` |
| 3 | `tests/regression/noc_details/validation/test_noc_required_fields.py` |
| 4 | `tests/regression/noc_details/positive/__init__.py` |
| 5 | `tests/regression/noc_details/positive/test_noc_positive.py` |
| 6 | `tests/regression/noc_details/negative/__init__.py` |
| 7 | `tests/regression/noc_details/negative/test_noc_negative.py` |
| 8 | `tests/regression/noc_details/boundary/__init__.py` |
| 9 | `tests/regression/noc_details/boundary/test_noc_boundary.py` |

## Files to Extend (3):

| # | File | Change |
|---|------|--------|
| 1 | `pages/noc_details_page.py` | 7 methods added at bottom |
| 2 | `conftest.py` | `noc_ready_page` fixture added at bottom |
| 3 | `pytest.ini` | `noc_details` marker registered |

(Excel extension handled via script — not a code file change)

## Files NEVER to Modify:

| File | Reason |
|------|--------|
| `test_preliminary_form_main.py` | LOCKED E2E |
| `fill_noc_details()` in noc_details_page.py | LOCKED method |
| `conftest.py` existing hooks/fixtures | READ-ONLY |
| `utils/excel_reader.py` | READ-ONLY |
| `utils/validation_helper.py` | Already has `set_readonly_date()` |
| `utils/screenshot_util.py` | READ-ONLY |
| `utils/report_generator.py` | READ-ONLY |
| `test_data/Data_Schools.xlsx` | E2E data contract |
| All other Page Objects | Not part of this module |

---

# E2E BACKWARD COMPATIBILITY CONFIRMATION

| Check | Guaranteed |
|-------|-----------|
| `test_preliminary_form_main.py` unchanged | ✅ |
| `fill_noc_details(data)` unchanged | ✅ |
| Existing locators unchanged | ✅ |
| Existing fixtures unchanged | ✅ |
| Existing Excel data unchanged | ✅ |
| E2E collects same test count | ✅ |
| E2E execution flow identical | ✅ |

---

# TOTAL ESTIMATED EFFORT

| Phase | Effort |
|-------|--------|
| Phase 1 (Framework) | 1.5 hours |
| Phase 2 (Excel) | 30 min |
| Phase 3 (Validation) | 30 min |
| Phase 4 (Positive) | 30 min |
| Phase 5 (Boundary) | 30 min |
| Phase 6 (Negative) | 45 min |
| Phase 7 (Coverage) | 1 hour |
| Phase 8 (Allure) | 15 min |
| **Total** | **~5.5 hours (~0.75 day)** |

---

**STATUS:** Implementation plan complete. Ready for phased execution.
