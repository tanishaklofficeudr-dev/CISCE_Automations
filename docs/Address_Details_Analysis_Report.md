# Address Details Module — Automation Design Analysis
## Pre-Implementation Report

---

# 1. FIELD CLASSIFICATION TABLE

| # | Field Name | Locator | Input Type | Mandatory | Dependency | Existing Method |
|---|-----------|---------|-----------|-----------|------------|-----------------|
| 1 | Address Line | `#address_1` | Textbox | Yes (assumed *) | None | `fill_address_details()` |
| 2 | Country | `get_by_role("textbox", name="India")` → `get_by_role("option", name=...)` | Searchable Autocomplete (Select2) | Yes | None — loads all countries | `fill_address_details()` |
| 3 | State | `#select2-state-container` → `get_by_role("option", name=...)` | Dependent Searchable Dropdown (Select2) | Yes | **Depends on Country** | `fill_address_details()` |
| 4 | District | `get_by_role("textbox", name="Select")` → `get_by_role("option", name=...)` | Dependent Searchable Dropdown (Select2) | Yes | **Depends on State** | `fill_address_details()` |
| 5 | City | `get_by_role("textbox", name="Select")` → `get_by_role("option", name=...)` | Dependent Searchable Dropdown (Select2) | Yes | **Depends on District** | `fill_address_details()` |
| 6 | ZIP/PIN Code | `#zip` | Textbox (numeric) | Yes | None | `fill_address_details()` |
| 7 | Locality Type | `#locality` | Standard Dropdown (`<select>`) | Yes | None | `fill_address_details()` |

---

# 2. DROPDOWN DEPENDENCY CHAIN

```
Country (Select2 Autocomplete)
    ↓ loads
State (Select2 Dependent)
    ↓ loads
District (Select2 Dependent)
    ↓ loads
City (Select2 Dependent)
```

### Dependency Behaviour Analysis:

| Question | Answer (Based on Code) |
|----------|----------------------|
| Does selecting Country load State? | **Yes** — State dropdown is separate and selected after Country |
| Does selecting State load District? | **Yes** — District uses same `get_by_role("textbox", name="Select")` pattern |
| Does selecting District load City? | **Yes** — City uses same pattern, selected after District |
| Can values be cleared? | **Unknown** — Select2 may have a clear button, but code doesn't use it |
| Are values retained after save? | **Likely Yes** — same SPA behavior as School Details |
| Can the dropdown return to blank? | **Unlikely** — Select2 retains selection; no "Select" reset available |
| Does automation need waits after selection? | **Yes** — cascading load requires network fetch between each selection |

### Critical Observation:

The locator `get_by_role("textbox", name="Select")` is used for BOTH District and City. This is ambiguous — it relies on the first matching "Select" textbox being District, and after District is filled, the next "Select" becomes City. This is **fragile** and order-dependent.

---

# 3. VALIDATION RULES (Inferred)

| Field | Validation Rule | Type |
|-------|----------------|------|
| Address Line | Mandatory — cannot be blank | Required |
| Address Line | Maximum character limit (unknown) | Boundary |
| Country | Must be selected | Required |
| State | Must be selected (loads after Country) | Required |
| District | Must be selected (loads after State) | Required |
| City | Must be selected (loads after District) | Required |
| ZIP/PIN Code | Mandatory — cannot be blank | Required |
| ZIP/PIN Code | Must be exactly 6 digits | Format |
| ZIP/PIN Code | Must be numeric only | Format |
| Locality Type | Must be selected | Required |

---

# 4. EXISTING REUSABLE METHODS

| Method | What It Does | Reuse For |
|--------|--------------|-----------|
| `fill_address_details(data)` | Fills all 7 fields + clicks Next | E2E positive path |

**Only ONE method exists.** No individual field methods, no click_next(), no partial fill.

---

# 5. MISSING METHODS TO ADD

| Method | Purpose | Complexity |
|--------|---------|-----------|
| `click_next()` | Click Next without filling | Simple |
| `fill_partial_details(data, skip_fields)` | Fill all except specified fields + click Next | Medium |
| `fill_address_line(value)` | Fill only address field (for boundary testing) | Simple |
| `fill_zip(value)` | Fill only ZIP field (for format/boundary testing) | Simple |
| `select_country(country)` | Select only country (for cascade testing) | Simple |

### Constraints for `fill_partial_details()`:

The cascading dropdowns create a challenge:
- **Cannot skip Country** without breaking State/District/City
- **Cannot skip State** without breaking District/City
- **Cannot skip District** without breaking City
- **Can skip** Address Line, ZIP, Locality independently

Therefore `skip_fields` logic must:
- If Country is skipped → also skip State, District, City (entire cascade)
- If State is skipped → also skip District, City
- If District is skipped → also skip City
- Address, ZIP, Locality can be skipped independently

---

# 6. TEST CLASSIFICATION (Following School Details Pattern)

## Validation (Required Field) — 1 test

| TC ID | Test Case | Condition |
|-------|-----------|-----------|
| ADDR_VAL_001 | All mandatory fields blank — verify all errors shown | First visit only |

**Same constraint as School Details:** Only testable before first save. Dropdowns retain values after save.

## Positive — 3-4 tests

| TC ID | Test Case |
|-------|-----------|
| ADDR_POS_001 | Valid complete address with all fields |
| ADDR_POS_002 | Valid address with different country/state/district/city combination |
| ADDR_POS_003 | Valid address with different locality type |

## Negative (Format) — 4-5 tests

| TC ID | Test Case | Field | Value |
|-------|-----------|-------|-------|
| ADDR_FMT_001 | PIN code with alphabets | zip_pin | `abcdef` |
| ADDR_FMT_002 | PIN code with special characters | zip_pin | `12@#56` |
| ADDR_FMT_003 | PIN code less than 6 digits | zip_pin | `12345` |
| ADDR_FMT_004 | PIN code more than 6 digits | zip_pin | `1234567` |
| ADDR_FMT_005 | Address line blank (cleared) | address_line_1 | (empty) |

## Boundary — 2-3 tests

| TC ID | Test Case | Field | Value |
|-------|-----------|-------|-------|
| ADDR_BND_001 | Address line — 1 character (min) | address_line_1 | `A` |
| ADDR_BND_002 | Address line — 500 characters (max) | address_line_1 | 500 chars |
| ADDR_BND_003 | PIN code — exactly 6 digits | zip_pin | `123456` |

---

# 7. NON-AUTOMATABLE SCENARIOS

| Scenario | Reason |
|----------|--------|
| Country dropdown blank | Select2 retains selection after first save — cannot reset |
| State dropdown blank | Cascade dependency — cannot reset without Country reset |
| District dropdown blank | Same cascade issue |
| City dropdown blank | Same cascade issue |
| Locality dropdown blank | Standard `<select>` may not have a blank/reset option |

**Same lesson from School Details:** Dropdown-blank tests are only possible on first visit.

---

# 8. AUTOMATION CHALLENGES

| Challenge | Severity | Mitigation |
|-----------|----------|-----------|
| **Ambiguous locator** for District/City: both use `get_by_role("textbox", name="Select")` | HIGH | Execution order matters — must fill District first, then City appears |
| **Cascading waits**: State loads after Country, District after State, City after District | MEDIUM | Add explicit `wait_for_timeout` between each cascade step |
| **Select2 component**: Not a standard `<select>` — requires click-then-option pattern | MEDIUM | Already handled in existing code |
| **Data persistence**: After first save, all fields pre-filled | MEDIUM | Clear text fields before testing; cannot reset dropdowns |
| **PIN code behavior**: May have input mask like UDISE (needs verification) | MEDIUM | Run diagnostic first before assuming `.fill()` works |
| **SPA navigation**: URL doesn't change between steps | LOW | Use `#TabNOCDetails` or similar to detect navigation |

---

# 9. RISKS

| Risk | Impact | Likelihood |
|------|--------|-----------|
| PIN code has same issue as UDISE (accepts in DOM but validates differently) | Test failures | Medium |
| District/City locator `name="Select"` matches wrong element if page state changes | Flaky tests | High |
| Cascading dropdown timeout — slow network causes option not to appear | Flaky tests | Medium |
| First-visit validation test fails on accounts that already saved data | False failure | High (same as School Details) |

---

# 10. FIXTURE REQUIREMENT

| Fixture | Purpose | How It Works |
|---------|---------|-------------|
| `address_ready_page` | Pre-authenticated page on Address Details step | Login → School Details tab → fill school details → click Next → arrives at Address Details |

**Depends on:** School Details being filled first (form is sequential).

**Implementation:** Reuse `school_details_ready_page` + fill school details with valid data + click Next.

---

# 11. ESTIMATED IMPLEMENTATION EFFORT

| Task | Effort |
|------|--------|
| Add methods to address_details_page.py (click_next, fill_partial, fill_zip) | 1 hour |
| Create address_ready_page fixture | 1 hour |
| Create Address Excel sheets (Positive, Negative, Boundary) | 1 hour |
| Create tests/regression/address_details/ structure + 4 test files | 3 hours |
| Diagnostic verification for PIN code field | 30 min |
| Testing + debugging | 2 hours |
| **Total** | **~1.5 days** |

---

# 12. FOLDER STRUCTURE (Proposed)

```
tests/regression/address_details/
├── validation/
│   └── test_address_required_fields.py    ← 1 test (ADDR_VAL_001)
├── positive/
│   └── test_address_positive.py           ← 3 tests
├── negative/
│   └── test_address_negative.py           ← 5 tests (PIN format + blank address)
└── boundary/
    └── test_address_boundary.py           ← 3 tests
```

**Total: ~12 tests**

---

# 13. KEY DIFFERENCES FROM SCHOOL DETAILS

| Aspect | School Details | Address Details |
|--------|---------------|-----------------|
| Dropdown type | Standard `<select>` | Select2 searchable autocomplete |
| Field dependencies | None | Cascading chain (Country → State → District → City) |
| Skip logic | Any field can be skipped independently | Skipping Country cascades to State/District/City |
| Ambiguous locators | None | District + City share `name="Select"` locator |
| Waits required | Minimal | Between every cascade step |
| Fields testable for blank | school_name, contact_person, udise | address_line, zip (text only) |
| Dropdown blank tests | Not possible (persisted) | Not possible (persisted + cascade) |

---

**STATUS:** Analysis complete. Awaiting approval before implementation.
