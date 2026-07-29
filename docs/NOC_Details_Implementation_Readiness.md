# NOC Details Module — Implementation Readiness Review
## Based on Completed Diagnostics

---

# CONFIRMED FIELD BEHAVIORS (From Diagnostics)

| Field | Method | Verified? |
|-------|--------|-----------|
| NOC Authority (`#noc_authority`) | `.fill()` | ✅ Standard textbox |
| Designation (`#noc_designation`) | `.fill()` | ✅ Standard textbox |
| Office Address (`#noc_office_address`) | `.fill()` | ✅ Standard textbox |
| Country (`#noc_country`) | `select_option(value="2")` | ✅ Standard `<select>` |
| State (`#noc_state`) | `select_option(value="30")` + 1s wait | ✅ Dependent `<select>`, AJAX loaded |
| NOC Reference Number | `.fill()` via `get_by_role("textbox", name="Select NOC Reference Number")` | ✅ Standard textbox |
| Date of NOC (`#noc_date`) | `ValidationHelper.set_readonly_date()` | ✅ Readonly, JS injection confirmed |

---

# 1. REQUIRED ADDITIVE PAGE OBJECT METHODS

| # | Method | Purpose |
|---|--------|---------|
| 1 | `click_next()` | Click Next without filling — for validation test |
| 2 | `fill_authority(value)` | Fill/clear authority field — for negative/boundary tests |
| 3 | `fill_designation(value)` | Fill/clear designation field |
| 4 | `fill_office_address(value)` | Fill/clear office address field |
| 5 | `fill_reference_number(value)` | Fill/clear reference number field |
| 6 | `set_date(page, date_value)` | Wrapper calling `ValidationHelper.set_readonly_date()` |
| 7 | `fill_partial_details(data, skip_fields)` | Fill all except specified + click Next |

**Total: 7 methods**

### `fill_partial_details` Logic:

```
For text fields in skip_fields → clear with .fill("")
For Country in skip_fields → leave unchanged (disabled "Select" — cannot reset)
For State in skip_fields → leave unchanged
For Date in skip_fields → set to "" via JS (clear date)
Country/State cascade: 1000ms wait after Country selection before State
```

---

# 2. REQUIRED FIXTURE

| Fixture | Scope | Depends On | Logic |
|---------|-------|-----------|-------|
| `noc_ready_page` | function | `address_ready_page` | Fill Address Details → arrives at NOC Details |

**Alternative:** Navigate directly via "NOC Details" tab click (confirmed working in diagnostic).

**Recommended:** Use tab click approach (faster, avoids cascading fixture chain):
```
school_details_ready_page → click "NOC Details" tab → wait → return page
```

---

# 3. REQUIRED EXCEL SHEETS

### In `test_data/negative/Validation_Data.xlsx`:

| Sheet | Rows | Columns |
|-------|------|---------|
| `NOC_Positive` | 2 | scenario_id, execute, description, noc_authority, designation, office_address, noc_reference_number, noc_date, expected_result, priority |
| `NOC_Negative` | 5–6 | scenario_id, execute, description, field_name, field_value, expected_error, scenario_type, priority |
| `NOC_Boundary` | 2–3 | scenario_id, execute, description, field_name, field_value, expected_outcome, expected_message, priority |

---

# 4. TEST INDEPENDENCE

| Test Category | Independent? | Reason |
|---------------|-------------|--------|
| NOC_VAL_001 (all blank) | First-visit only | Text fields can be cleared; dropdowns + date persist |
| NOC_POS_001–002 (valid) | ✅ Yes | Overwrites all fields with valid data |
| NOC_FMT_001–006 (format) | ✅ Yes | Overwrites target field only |
| NOC_BND_001–003 (boundary) | ✅ Yes | Overwrites target field only |

**9 of 10 tests are independently executable.** Only validation test needs first-visit consideration.

---

# 5. DATA PERSISTENCE IMPLICATIONS

| Field | Persists After Save | Can Clear | Can Overwrite |
|-------|--------------------:|-----------|--------------|
| Authority | Yes | ✅ `.fill("")` | ✅ `.fill("new value")` |
| Designation | Yes | ✅ `.fill("")` | ✅ `.fill("new value")` |
| Office Address | Yes | ✅ `.fill("")` | ✅ `.fill("new value")` |
| Country | Yes | ❌ "Select" is disabled | ✅ `select_option(value=...)` |
| State | Yes | ❌ "Select" is disabled | ✅ `select_option(value=...)` |
| Reference Number | Yes | ✅ `.fill("")` | ✅ `.fill("new value")` |
| Date | Yes | ✅ `set_readonly_date("", "")` | ✅ `set_readonly_date("", "16/05/2025")` |

---

# 6. VALIDATION STRATEGY (1 test)

| TC ID | Scenario | Method |
|-------|----------|--------|
| NOC_VAL_001 | All mandatory text fields cleared + date cleared → click Next | Clear authority, designation, address, reference, date via JS → click Next → assert errors |

**Note:** Country/State cannot be blanked — only text + date fields can be tested for mandatory validation.

---

# 7. POSITIVE STRATEGY (2 tests)

| TC ID | Scenario | Data |
|-------|----------|------|
| NOC_POS_001 | Valid complete NOC — all fields filled with valid data | Authority, Designation, Address, Country=India, State=Rajasthan, Ref=NOC-001, Date=16/05/2025 |
| NOC_POS_002 | Valid NOC with different state | Same but State=Maharashtra (value="21") |

---

# 8. BOUNDARY STRATEGY (2–3 tests)

| TC ID | Field | Value | Expected |
|-------|-------|-------|----------|
| NOC_BND_001 | noc_authority | "A" (1 char) | ACCEPT |
| NOC_BND_002 | noc_office_address | 300 chars | ACCEPT or truncate |
| NOC_BND_003 | noc_reference_number | 50 chars | ACCEPT or truncate |

---

# 9. NEGATIVE STRATEGY (5–6 tests)

| TC ID | Field | Value | Expected Error |
|-------|-------|-------|----------------|
| NOC_FMT_001 | noc_authority | "" (blank) | Authority is required |
| NOC_FMT_002 | designation | "" (blank) | Designation is required |
| NOC_FMT_003 | office_address | "" (blank) | Office address is required |
| NOC_FMT_004 | noc_reference_number | "" (blank) | Reference number is required |
| NOC_FMT_005 | noc_date | "" (cleared via JS) | Date is required |
| NOC_FMT_006 | noc_date | future date (via JS) | Date cannot be future (if validated) |

---

# 10. NON-AUTOMATABLE SCENARIOS

| Scenario | Reason |
|----------|--------|
| Country blank | "Select" option is disabled |
| State blank | "Select" option is disabled |
| Date selected from calendar UI (specific behavior) | Covered by E2E; regression uses JS |
| Calendar min/max date enforcement | Bypassed by JS — cannot test UI restrictions |

---

# 11. RISKS

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| 1 | Future date accepted (no validation) | Medium | If test fails, classify as app gap — don't remove test |
| 2 | JS-cleared date still saved server-side | Low | Diagnostic confirmed clearing works |
| 3 | State AJAX load slow | Low | 1000ms wait proven sufficient |
| 4 | NOC tab click doesn't work on fresh account | Medium | Fallback to sequential navigation |
| 5 | Exact validation messages unknown for blank fields | Medium | First run will capture; update Excel after |

---

# 12. ESTIMATED IMPLEMENTATION EFFORT

| Task | Effort |
|------|--------|
| Add 7 methods to `noc_details_page.py` | 1 hour |
| Create `noc_ready_page` fixture | 30 min |
| Create 3 Excel sheets (Positive, Negative, Boundary) | 30 min |
| Create folder structure + `__init__.py` | 5 min |
| Implement Positive tests | 30 min |
| Implement Negative tests | 45 min |
| Implement Boundary tests | 30 min |
| Implement Validation test | 30 min |
| Run + debug | 1 hour |
| **Total** | **~5.5 hours (~0.75 day)** |

---

# FINAL TEST COUNT

| Category | Tests |
|----------|-------|
| Validation | 1 |
| Positive | 2 |
| Negative | 5–6 |
| Boundary | 2–3 |
| **Total** | **10–12** |

---

# IMPLEMENTATION ORDER

```
1. Create folder structure
2. Add methods to noc_details_page.py
3. Create noc_ready_page fixture
4. Create Excel sheets
5. Implement Positive tests FIRST (validates fixture)
6. Implement Boundary tests
7. Implement Negative tests
8. Implement Validation test (first_run)
9. Run all + debug
```

---

**STATUS:** Implementation-ready. All diagnostics complete. No blockers.
