# Certificate of Land — Phase 1 Implementation Plan
## Scope: Single Plot → Owned Path Only

---

# 1. FOLDER STRUCTURE

```
tests/regression/land_certificate/
├── __init__.py
├── validation/
│   ├── __init__.py
│   └── test_land_required_fields.py      ← 1 test (LAND_VAL_001)
├── positive/
│   ├── __init__.py
│   └── test_land_positive.py             ← 3 tests (parametrized)
├── negative/
│   ├── __init__.py
│   └── test_land_negative.py             ← 5 tests (parametrized)
└── boundary/
    ├── __init__.py
    └── test_land_boundary.py             ← 3 tests (parametrized)
```

---

# 2. FILES TO CREATE (9)

| # | File |
|---|------|
| 1 | `tests/regression/land_certificate/__init__.py` |
| 2 | `tests/regression/land_certificate/validation/__init__.py` |
| 3 | `tests/regression/land_certificate/validation/test_land_required_fields.py` |
| 4 | `tests/regression/land_certificate/positive/__init__.py` |
| 5 | `tests/regression/land_certificate/positive/test_land_positive.py` |
| 6 | `tests/regression/land_certificate/negative/__init__.py` |
| 7 | `tests/regression/land_certificate/negative/test_land_negative.py` |
| 8 | `tests/regression/land_certificate/boundary/__init__.py` |
| 9 | `tests/regression/land_certificate/boundary/test_land_boundary.py` |

---

# 3. FILES TO EXTEND (3)

| # | File | Change |
|---|------|--------|
| 1 | `pages/land_certificate_page.py` | 6 additive methods at bottom |
| 2 | `conftest.py` | `land_ready_page` fixture at bottom |
| 3 | `pytest.ini` | `land_certificate` marker |

---

# 4. NEW PAGE METHODS (ADD to `land_certificate_page.py`)

| # | Method | Purpose | Implementation |
|---|--------|---------|----------------|
| 1 | `click_next()` | Click Next without filling | `get_by_role("button", name="Next").click()` |
| 2 | `select_plot_type(type_name)` | Select Single/Multiple radio | `get_by_role("radio", name=type_name).click()` + wait |
| 3 | `select_land_type(type_name)` | Select Owned/Leased radio | `get_by_role("radio", name=type_name).click()` + wait |
| 4 | `fill_land_area(value)` | Fill/clear land area field | `locator("#land_area_0").fill(value)` |
| 5 | `fill_document_date(date)` | Fill land document date directly | `locator("#land_title_date0").fill(date)` — NOT readonly |
| 6 | `fill_partial_owned_details(data, skip_fields)` | Fill all Owned fields except skipped + click Next | See logic below |

### `fill_partial_owned_details` Logic:

```
1. select_plot_type("Single") + wait 2000ms
2. select_land_type("Owned") + wait 1000ms
3. Area Unit: select_option(label=...) — always set (cannot blank)
4. Land Area: .fill() — clear with .fill("") if skipped
5. Situated In (specify): .fill() — clear if skipped
6. Situated At: .fill() — clear if skipped
7. Land Owned By: .fill() — clear if skipped
8. Land Title Document: select_option(label=...) — always set
9. IF title == "Sale Deed": Sale Deed Favor select_option
10. Registration Details: .fill()
11. Executed By: .fill()
12. Registration Office: .fill()
13. Document Date: .fill() directly (NOT readonly)
14. Click Next
```

**Existing `fill_land_details(data)` is NOT modified — READ-ONLY.**

---

# 5. FIXTURE REQUIRED

| Fixture | Scope | Depends On | Logic |
|---------|-------|-----------|-------|
| `land_ready_page` | function | `school_details_ready_page` | Click "Certificate of Land" tab → wait 3000ms → verify `#land_area_0` or radio visible → return page |

**Same tab-click pattern** as NOC and Trust fixtures (proven approach).

---

# 6. EXCEL SHEETS REQUIRED

### In `test_data/negative/Validation_Data.xlsx`:

#### Sheet: `Land_Positive` (3 rows)

| scenario_id | execute | description | area_unit | land_area | situated_in | situated_at | land_owned_by | land_title_document | sale_deed_favor | registration_details | executed_by | registration_office | document_date | expected_result | priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LAND_POS_001 | Yes | Valid Owned - Conveyance Deed | Square Meter | 5000 | Survey No(s) | Civil Lines, Jaipur | Shiksha Trust | Conveyance Deed | | REG-2020-001 | Mr. Sharma | Sub-Registrar Office, Jaipur | 15/03/2020 | Navigates to Upload Documents | High |
| LAND_POS_002 | Yes | Valid Owned - Sale Deed, favor=School | Square Foot | 10000 | Survey No(s) | Main Road, Ajmer | Education Trust | Sale Deed | School | REG-2019-001 | Mr. Gupta | Registrar Office, Ajmer | 20/06/2019 | Navigates with Sale Deed favor | High |
| LAND_POS_003 | Yes | Valid Owned - Sale Deed, favor=Trust | Square Yard | 8000 | Survey No(s) | Park Street, Mumbai | National Society | Sale Deed | Trust/Society/Company | REG-2018-001 | Ms. Patel | District Registrar, Mumbai | 10/01/2018 | Navigates with alternate favor | Medium |

#### Sheet: `Land_Negative` (5 rows)

| scenario_id | execute | description | field_name | field_value | expected_error | priority |
|---|---|---|---|---|---|---|
| LAND_FMT_001 | Yes | Land Area blank | land_area | | Please enter a valid land area | High |
| LAND_FMT_002 | Yes | Situated In specify blank | situate_speci | | Please specify where it is situated | High |
| LAND_FMT_003 | Yes | Land Area with alphabets | land_area | abcdef | Please enter a valid land area | Medium |
| LAND_FMT_004 | Yes | Land Area with negative value | land_area | -500 | Please enter a valid land area | Medium |
| LAND_FMT_005 | Yes | Area Unit not selected | area_unit | SKIP | Area unit is required | Medium |

#### Sheet: `Land_Boundary` (3 rows)

| scenario_id | execute | description | field_name | field_value | expected_outcome | expected_message | priority |
|---|---|---|---|---|---|---|---|
| LAND_BND_001 | Yes | Land Area - 1 digit | land_area | 1 | ACCEPT | Min value accepted | Medium |
| LAND_BND_002 | Yes | Land Area - large number | land_area | 999999999 | ACCEPT | Large value accepted | Medium |
| LAND_BND_003 | Yes | Document Date - valid past date | document_date | 15/03/2020 | ACCEPT | Date accepted via .fill() | Medium |

---

# 7. IMPLEMENTATION SEQUENCE

| Phase | Task | Depends On | Effort |
|-------|------|-----------|--------|
| 1.1 | Create folder structure + `__init__.py` | None | 5 min |
| 1.2 | Add methods to `land_certificate_page.py` | None | 45 min |
| 1.3 | Add `land_ready_page` fixture to `conftest.py` | None | 20 min |
| 1.4 | Register `land_certificate` marker in `pytest.ini` | None | 2 min |
| 1.5 | Create Excel sheets | None | 30 min |
| 1.6 | Implement Positive tests (validates fixture works) | 1.1–1.5 | 30 min |
| 1.7 | Implement Boundary tests | 1.1–1.5 | 20 min |
| 1.8 | Implement Negative tests | 1.1–1.5 | 30 min |
| 1.9 | Implement Validation test (@first_run) | 1.1–1.5 | 20 min |
| 1.10 | Run all + debug | 1.6–1.9 | 45 min |
| **Total** | | | **~4 hours** |

---

# 8. ESTIMATED EFFORT

| Task | Effort |
|------|--------|
| Framework additions (folders, methods, fixture, marker) | 1.5 hours |
| Excel data | 30 min |
| Test implementation (4 files) | 1.5 hours |
| Execution + debugging | 45 min |
| **Total** | **~4 hours** |

---

# 9. E2E COMPATIBILITY VERIFICATION

| Check | Guaranteed |
|-------|-----------|
| `test_preliminary_form_main.py` unchanged | ✅ |
| `fill_land_details(data)` unchanged | ✅ |
| Existing locators unchanged | ✅ |
| Existing fixtures unchanged | ✅ |
| Existing Excel data unchanged | ✅ |
| E2E execution identical | ✅ |

---

# 10. RISKS AND MITIGATIONS

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| 1 | Only 2 validation messages confirmed — other blank fields may navigate | Medium | If form navigates with blank field, classify as app behavior (same as Trust) |
| 2 | Area Unit dropdown disabled placeholder — blank test may fail | Medium | LAND_FMT_005 may need to be classified as non-testable after first save |
| 3 | Sale Deed conditional — favor field only appears dynamically | Low | E2E pattern already handles this — proven |
| 4 | `#land_title_date0` date format expected by app unknown | Low | `.fill("15/03/2020")` confirmed working in diagnostic |
| 5 | Dynamic form load after radio selection — timing | Low | 2000ms wait proven sufficient in E2E |

---

# FINAL SUMMARY

| Metric | Value |
|--------|-------|
| **Total tests** | 12 |
| **Total files to create** | 9 |
| **Total files to extend** | 3 |
| **New page methods** | 6 |
| **New fixture** | 1 (`land_ready_page`) |
| **Excel sheets** | 3 |
| **Estimated effort** | ~4 hours |
| **E2E impact** | Zero |

## Reused Components:

| Component | From |
|-----------|------|
| Folder structure pattern | School/Address/NOC/Trust |
| `fill_partial_*` architecture | All modules |
| Tab-click fixture pattern | NOC, Trust |
| `select_option()` for dropdowns | All modules |
| `.fill()` for text + date | Address, Trust |
| Screenshot on failure | All modules |
| Allure hierarchy | All modules |
| `@first_run` ordering | School, Address, NOC |
| Diagnostic on failure | Address, NOC, Trust |

## Expected Execution Outcome:

```
12 tests collected
- LAND_VAL_001: PASS (validation messages confirmed)
- LAND_POS_001–003: PASS (valid data navigates)
- LAND_FMT_001–002: PASS (confirmed validation messages)
- LAND_FMT_003–004: TBD (alphabets/negative — behavior unconfirmed)
- LAND_FMT_005: May fail (dropdown persistence issue)
- LAND_BND_001–003: PASS (within acceptable ranges)
```

---

**STATUS:** Implementation plan complete. Ready for phased execution.
