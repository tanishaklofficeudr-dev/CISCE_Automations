# Address Details Module — Implementation Plan

---

# FILES TO CREATE

| # | File | Purpose |
|---|------|---------|
| 1 | `tests/regression/address_details/__init__.py` | Package marker |
| 2 | `tests/regression/address_details/validation/__init__.py` | Package marker |
| 3 | `tests/regression/address_details/validation/test_address_required_fields.py` | 1 test (ADDR_VAL_001) |
| 4 | `tests/regression/address_details/positive/__init__.py` | Package marker |
| 5 | `tests/regression/address_details/positive/test_address_positive.py` | 3 tests (ADDR_POS_001–003) |
| 6 | `tests/regression/address_details/negative/__init__.py` | Package marker |
| 7 | `tests/regression/address_details/negative/test_address_negative.py` | 6 tests (ADDR_FMT_001–006) |
| 8 | `tests/regression/address_details/boundary/__init__.py` | Package marker |
| 9 | `tests/regression/address_details/boundary/test_address_boundary.py` | 3 tests (ADDR_BND_001–003) |

---

# FILES TO EXTEND

| # | File | What to Add | What NOT to Touch |
|---|------|-------------|-------------------|
| 1 | `pages/address_details_page.py` | `click_next()`, `fill_zip(value)`, `fill_address_line(value)`, `fill_partial_details(data, skip_fields)` | Existing `fill_address_details(data)` |
| 2 | `conftest.py` | `address_ready_page` fixture (at bottom) | All existing fixtures and hooks |
| 3 | `test_data/negative/Validation_Data.xlsx` | Add 3 sheets: `Address_Positive`, `Address_Negative`, `Address_Boundary` | All existing sheets |

---

# NEW PAGE OBJECT METHODS

## pages/address_details_page.py — Methods to ADD:

| # | Method | Signature | Purpose |
|---|--------|-----------|---------|
| 1 | `click_next()` | `def click_next(self)` | Click Next without filling — for validation test |
| 2 | `fill_zip(value)` | `def fill_zip(self, value)` | Clear ZIP and fill with given value — for format/boundary tests |
| 3 | `fill_address_line(value)` | `def fill_address_line(self, value)` | Clear address and fill with given value — for boundary tests |
| 4 | `fill_partial_details(data, skip_fields)` | `def fill_partial_details(self, data, skip_fields=None)` | Fill all fields except skipped ones + click Next |

### `fill_partial_details` Cascade Rules:

```
skip_fields logic:
- If "country" in skip_fields → also skip state, district, city (entire cascade breaks)
- If "state" in skip_fields → also skip district, city
- If "district" in skip_fields → also skip city
- "address_line_1", "zip_pin", "locality_type" → can be skipped independently

For text fields in skip_fields:
- address_line_1 → clear with .fill("")
- zip_pin → clear with .fill("")

For dropdowns in skip_fields:
- Leave unchanged (retain saved value)

Waits:
- wait_for_timeout(1000) after each cascade selection (Country → State → District → City)
```

---

# NEW FIXTURE

## conftest.py — Add at bottom:

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `address_ready_page` | function | Pre-authenticated page on Address Details step |

### Fixture Flow:
```
1. Use school_details_ready_page fixture (gets to School Details)
2. Fill School Details with valid baseline data using fill_partial_details()
3. Wait for navigation to Address Details
4. Verify on Address Details (check for #address_1 or Address heading)
5. Return page
```

**Dependency:** `school_details_ready_page` → fill school → arrives at Address Details

---

# EXCEL SHEETS TO ADD

## In: `test_data/negative/Validation_Data.xlsx`

### Sheet: `Address_Positive`

| Column | Type |
|--------|------|
| scenario_id | String |
| execute | String |
| scenario_description | String |
| address_line_1 | String |
| country | String |
| state | String |
| district | String |
| city | String |
| zip_pin | String |
| locality_type | String |
| expected_result | String |
| priority | String |

**Rows: 3** (ADDR_POS_001–003)

### Sheet: `Address_Negative`

| Column | Type |
|--------|------|
| scenario_id | String |
| execute | String |
| scenario_description | String |
| field_name | String |
| field_value | String |
| expected_error | String |
| scenario_type | String |
| priority | String |

**Rows: 6** (ADDR_FMT_001–006)

### Sheet: `Address_Boundary`

| Column | Type |
|--------|------|
| scenario_id | String |
| execute | String |
| scenario_description | String |
| field_name | String |
| field_value | String |
| expected_outcome | String |
| expected_message | String |
| priority | String |

**Rows: 3** (ADDR_BND_001–003)

---

# UTILITIES

No new utility files required. Reuse:
- `utils/validation_helper.py` — `assert_form_blocked()`, `assert_form_submitted()`, `assert_error_present()`, `get_all_errors()`
- `utils/screenshot_util.py` — failure screenshots
- `utils/excel_reader.py` — data loading

### Validation Helper Update Needed:

The `assert_form_submitted()` currently checks for `#TabAddressDetails`. For Address Details module, it should detect navigation to **NOC Details**. Options:
- A) Make `assert_form_submitted()` accept a `next_step_locator` parameter
- B) Check for `#TabNOCDetails` in the Address tests directly
- **Recommended: Option A** — add optional parameter to make it reusable across all modules

---

# FOLDER STRUCTURE (After Implementation)

```
tests/regression/address_details/
├── __init__.py
├── validation/
│   ├── __init__.py
│   └── test_address_required_fields.py    ← 1 test
├── positive/
│   ├── __init__.py
│   └── test_address_positive.py           ← 3 tests
├── negative/
│   ├── __init__.py
│   └── test_address_negative.py           ← 6 tests
└── boundary/
    ├── __init__.py
    └── test_address_boundary.py           ← 3 tests
```

---

# IMPLEMENTATION PHASES

| Phase | Task | Depends On | Effort |
|-------|------|-----------|--------|
| 1 | Create folder structure + `__init__.py` files | None | 5 min |
| 2 | Add methods to `pages/address_details_page.py` | None | 1 hour |
| 3 | Update `ValidationHelper.assert_form_submitted()` — add `next_step_locator` param | None | 30 min |
| 4 | Add `address_ready_page` fixture to `conftest.py` | Phase 2 | 30 min |
| 5 | Add Excel sheets (`Address_Positive`, `Address_Negative`, `Address_Boundary`) | None | 30 min |
| 6 | Implement `test_address_required_fields.py` (Validation) | Phases 2–5 | 30 min |
| 7 | Implement `test_address_positive.py` (Positive) | Phases 2–5 | 1 hour |
| 8 | Implement `test_address_negative.py` (Negative/Format) | Phases 2–5 | 1 hour |
| 9 | Implement `test_address_boundary.py` (Boundary) | Phases 2–5 | 30 min |
| 10 | Run all + debug | Phases 6–9 | 1 hour |
| **Total** | | | **~6.5 hours (~1 day)** |

---

# IMPLEMENTATION ORDER (Safest)

```
Phase 1 (Folders) → Phase 2 (Page Methods) → Phase 3 (Validation Helper)
     ↓
Phase 4 (Fixture) → Phase 5 (Excel Data)
     ↓
Phase 7 (Positive tests FIRST — safest, confirms fixture works)
     ↓
Phase 9 (Boundary — uses same fill approach)
     ↓
Phase 8 (Negative — PIN format tests)
     ↓
Phase 6 (Validation — first-run test last)
     ↓
Phase 10 (Run all + debug)
```

---

# RISK ASSESSMENT

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|-----------|-----------|
| 1 | Cascading dropdown timeout — option doesn't load in time | Medium | Medium | Add `wait_for_timeout(1000)` between each cascade step |
| 2 | District/City locator ambiguity (`name="Select"`) | Medium | Low | Always fill in sequence; never skip District without City |
| 3 | PIN format tests fail (same as UDISE issue) | Medium | Medium | If 6-char non-numeric passes validation, document as app gap — but manual testing confirms it works |
| 4 | `address_ready_page` fixture fails because School Details submission fails | High | Low | Depends on School Details fixture working; tested previously |
| 5 | SPA detection — wrong `next_step_locator` for NOC | Low | Low | Verify actual tab ID via DOM inspection |
| 6 | First-visit validation test fails on existing account | Medium | High | Mark as `@pytest.mark.first_run` |

---

# E2E IMPACT VERIFICATION

| Check | Impact |
|-------|--------|
| `test_preliminary_form_main.py` modified? | **NO** |
| `fill_address_details(data)` modified? | **NO** |
| `Data_Schools.xlsx` modified? | **NO** |
| `conftest.py` existing hooks modified? | **NO** |
| Existing fixtures modified? | **NO** |
| `ValidationHelper` methods removed? | **NO** (only parameter added) |

---

# VALID BASELINE DATA (For Negative/Boundary Tests)

```python
_valid_baseline = {
    "address_line_1": "123 Test Street, Diagnostic Lane",
    "country": "India",
    "state": "Rajasthan",
    "district": "(first available)",  # Dynamic — select first option
    "city": "(first available)",      # Dynamic — select first option
    "zip_pin": "302001",
    "locality_type": "Urban",
}
```

**Note:** District and City must use dynamic selection (`page.get_by_role("option").first.click()`) because available options depend on State selection.

---

**STATUS:** Implementation plan complete. Ready for phased implementation.
