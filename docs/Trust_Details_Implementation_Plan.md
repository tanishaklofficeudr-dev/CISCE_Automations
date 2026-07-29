# Trust/Society/Company Details — Implementation Plan
## Phased Execution Strategy

---

# PHASE 1: Framework Preparation

### Files Created:

| # | File | Purpose |
|---|------|---------|
| 1 | `tests/regression/trust_details/__init__.py` | Package marker |
| 2 | `tests/regression/trust_details/validation/__init__.py` | Package marker |
| 3 | `tests/regression/trust_details/positive/__init__.py` | Package marker |
| 4 | `tests/regression/trust_details/negative/__init__.py` | Package marker |
| 5 | `tests/regression/trust_details/boundary/__init__.py` | Package marker |

### Files Extended:

| # | File | What to Add |
|---|------|-------------|
| 1 | `pages/trust_details_page.py` | 6 additive methods |
| 2 | `conftest.py` | `trust_ready_page` fixture at bottom |
| 3 | `pytest.ini` | `trust_details` marker |

### New Page Object Methods (ADD to `trust_details_page.py`):

| # | Method | Purpose | Reuses |
|---|--------|---------|--------|
| 1 | `click_next()` | Click Next without filling | Same as other modules |
| 2 | `fill_name(value)` | Fill/clear trust name (textarea) | `.fill()` |
| 3 | `fill_registration_number(value)` | Fill/clear reg number | `.fill()` |
| 4 | `set_establishment_date(date)` | Set est date via JS | `ValidationHelper.set_readonly_date()` |
| 5 | `set_registration_date(date)` | Set reg date via JS | `ValidationHelper.set_readonly_date()` |
| 6 | `fill_partial_details(data, skip_fields)` | Fill all except skipped + click Next | Proven pattern |

**Methods NOT needed (already exists):**
- `fill_trust_details(data)` — exists in E2E, stays READ-ONLY

### `fill_partial_details` Logic:
```
- ownership_type: select_option(value) — cannot blank (disabled placeholder)
- owner_name (textarea): .fill() — clear with .fill("")
- establishment_date: set_readonly_date() — clear with ""
- registration_date: set_readonly_date() — clear with ""
- registration_no: .fill() — clear with .fill("")
- Wait 500ms after ownership selection (onchange handler)
- Always set ownership to valid value (cannot blank)
```

### New Fixture (`trust_ready_page`):

```
Logic:
1. Use school_details_ready_page
2. Click "Trust /Society /Company" tab directly (confirmed in diagnostic)
3. Wait 3000ms (page has 2s dynamic load)
4. Verify #ownership_type visible
5. Return page
```

### Marker Registration (`pytest.ini`):
```ini
trust_details: Trust/Society/Company Details module tests
```

### Risk Level: LOW
### Effort: 1 hour

---

# PHASE 2: Excel Data

### Files Extended:

| File | Sheets Added |
|------|-------------|
| `test_data/negative/Validation_Data.xlsx` | `Trust_Positive`, `Trust_Negative`, `Trust_Boundary` |

### Sheet: `Trust_Positive` (2 rows)

| Columns | Description |
|---------|-------------|
| scenario_id, execute, scenario_description, ownership_type, trust_name, establishment_date, registration_date, registration_number, expected_result, priority | |

| scenario_id | ownership_type | trust_name | est_date | reg_date | reg_number |
|---|---|---|---|---|---|
| TRUST_POS_001 | Trust | Shiksha Education Trust | 05/03/2018 | 10/04/2019 | TRUST-REG-2019-001 |
| TRUST_POS_002 | Society | National Education Society | 15/06/2015 | 20/08/2016 | SOC-REG-2016-002 |

### Sheet: `Trust_Negative` (6 rows)

| scenario_id | field_name | field_value | expected_error |
|---|---|---|---|
| TRUST_FMT_001 | owner_name | (empty) | Ownership name is required. |
| TRUST_FMT_002 | registration_no | (empty) | Registration number is required. |
| TRUST_FMT_003 | establishment_date | (empty) | Date of Establishment is required. |
| TRUST_FMT_004 | registration_date | (empty) | Date of Registration is required. |
| TRUST_FMT_005 | establishment_date | FUTURE | Should reject future date |
| TRUST_FMT_006 | registration_date | BEFORE_EST | Should enforce chronological order |

### Sheet: `Trust_Boundary` (3 rows)

| scenario_id | field_name | field_value | expected_outcome |
|---|---|---|---|
| TRUST_BND_001 | owner_name | A | ACCEPT |
| TRUST_BND_002 | owner_name | (300 chars) | ACCEPT |
| TRUST_BND_003 | registration_no | (50 chars) | ACCEPT |

### Risk Level: NONE
### Effort: 30 minutes

---

# PHASE 3: Validation Test

### Files Created:

| File | Tests |
|------|-------|
| `tests/regression/trust_details/validation/test_trust_required_fields.py` | 1 test (TRUST_VAL_001) |

### Approach:
- Uses `trust_ready_page` fixture
- Clears: name, reg number, both dates via `set_readonly_date("", "")`
- Clicks Next
- Asserts errors visible
- Hardcoded (no Excel) — same as School/Address/NOC

### Markers: `@regression`, `@trust_details`, `@validation`, `@first_run`
### Risk Level: LOW
### Effort: 30 minutes

---

# PHASE 4: Positive Tests

### Files Created:

| File | Tests |
|------|-------|
| `tests/regression/trust_details/positive/test_trust_positive.py` | 2 tests (parametrized) |

### Approach:
- Reads from `Trust_Positive` sheet
- Fills all fields with valid data
- Uses `select_option(label=...)` for ownership
- Uses `set_readonly_date()` for both dates
- Verifies navigation to "Certificate of Land"
- Navigates back via tab click

### Markers: `@regression`, `@trust_details`, `@positive`
### Risk Level: LOW
### Effort: 30 minutes

---

# PHASE 5: Boundary Tests

### Files Created:

| File | Tests |
|------|-------|
| `tests/regression/trust_details/boundary/test_trust_boundary.py` | 3 tests (parametrized) |

### Approach:
- Fills ALL mandatory fields with valid data FIRST (lesson from NOC boundary)
- Overwrites target field with boundary value
- Clicks Next
- Checks ACCEPT/REJECT

### Markers: `@regression`, `@trust_details`, `@boundary`
### Risk Level: LOW
### Effort: 30 minutes

---

# PHASE 6: Negative Tests

### Files Created:

| File | Tests |
|------|-------|
| `tests/regression/trust_details/negative/test_trust_negative.py` | 6 tests (parametrized) |

### Special Handling:
- TRUST_FMT_005 (`FUTURE`): Generates future date dynamically, submits, checks result. If accepted — fails with diagnostic report classifying as "Business Rule Pending Confirmation"
- TRUST_FMT_006 (`BEFORE_EST`): Sets est=2022, reg=2019, submits, checks result. Same approach.
- Both tests NOT marked `@xfail` — run normally, generate evidence on failure

### Markers: `@regression`, `@trust_details`, `@negative`
### Risk Level: MEDIUM (2 tests expected to fail per diagnostic findings)
### Effort: 45 minutes

---

# PHASE 7: Coverage Verification

### Commands:
```powershell
python -m pytest tests/regression/trust_details/ --collect-only -q
python -m pytest tests/regression/trust_details/ -v --headed --alluredir=allure-results
python -m pytest tests/test_preliminary_form_main.py --collect-only -q
```

### Expected:
- 12 tests collected
- 10 passed + 2 failed (TRUST_FMT_005, TRUST_FMT_006 — business rule pending)
- E2E: 1 test collected (unchanged)

### Effort: 1 hour

---

# PHASE 8: Allure Verification

### Expected Hierarchy:
```
CISCE E-Affiliation
└── Trust Details
    ├── Validation → Required Field Validation
    ├── Positive → Valid Form Submission
    ├── Negative → Negative Scenarios
    └── Boundary → Boundary Value Scenarios
```

### Effort: 15 minutes

---

# SUMMARY

## 1. Files to Create (9):

| # | File |
|---|------|
| 1 | `tests/regression/trust_details/__init__.py` |
| 2 | `tests/regression/trust_details/validation/__init__.py` |
| 3 | `tests/regression/trust_details/validation/test_trust_required_fields.py` |
| 4 | `tests/regression/trust_details/positive/__init__.py` |
| 5 | `tests/regression/trust_details/positive/test_trust_positive.py` |
| 6 | `tests/regression/trust_details/negative/__init__.py` |
| 7 | `tests/regression/trust_details/negative/test_trust_negative.py` |
| 8 | `tests/regression/trust_details/boundary/__init__.py` |
| 9 | `tests/regression/trust_details/boundary/test_trust_boundary.py` |

## 2. Files to Extend (3):

| # | File | Change |
|---|------|--------|
| 1 | `pages/trust_details_page.py` | 6 methods added at bottom |
| 2 | `conftest.py` | `trust_ready_page` fixture added at bottom |
| 3 | `pytest.ini` | `trust_details` marker registered |

## 3. New Page Methods (6):

| Method | Purpose |
|--------|---------|
| `click_next()` | Click Next without filling |
| `fill_name(value)` | Fill/clear textarea |
| `fill_registration_number(value)` | Fill/clear reg number |
| `set_establishment_date(date)` | JS date injection |
| `set_registration_date(date)` | JS date injection |
| `fill_partial_details(data, skip_fields)` | Fill all except skipped |

## 4. New Fixture (1):

| Fixture | Approach |
|---------|----------|
| `trust_ready_page` | `school_details_ready_page` → click Trust tab → wait → return page |

## 5. Excel Sheets (3):

| Sheet | Rows |
|-------|------|
| Trust_Positive | 2 |
| Trust_Negative | 6 |
| Trust_Boundary | 3 |

## 6. Estimated Effort:

| Phase | Effort |
|-------|--------|
| Phase 1 (Framework) | 1 hour |
| Phase 2 (Excel) | 30 min |
| Phase 3 (Validation) | 30 min |
| Phase 4 (Positive) | 30 min |
| Phase 5 (Boundary) | 30 min |
| Phase 6 (Negative) | 45 min |
| Phase 7 (Coverage) | 1 hour |
| Phase 8 (Allure) | 15 min |
| **Total** | **~5 hours** |

## 7. Backward Compatibility:

| Check | Guaranteed |
|-------|-----------|
| `test_preliminary_form_main.py` unchanged | ✅ |
| `fill_trust_details(data)` unchanged | ✅ |
| Existing locators unchanged | ✅ |
| Existing fixtures unchanged | ✅ |
| Existing Excel data unchanged | ✅ |
| E2E execution identical | ✅ |

## 8. Files Completely Untouched:

| File |
|------|
| `test_preliminary_form_main.py` |
| `pages/registration_page.py` |
| `pages/login_page.py` |
| `pages/school_details_page.py` |
| `pages/address_details_page.py` |
| `pages/noc_details_page.py` |
| `pages/land_certificate_page.py` |
| `pages/upload_documents_page.py` |
| `utils/excel_reader.py` |
| `utils/validation_helper.py` |
| `utils/screenshot_util.py` |
| `utils/report_generator.py` |
| `test_data/Data_Schools.xlsx` |

---

**STATUS:** Implementation plan complete. Ready for phased execution.
