# Certificate of Land Module — Complete Analysis Report

---

# 1. MODULE OVERVIEW

The Certificate of Land page is the most complex form in the Preliminary Affiliation workflow. It contains:
- Multiple radio groups controlling conditional flows
- Dynamic form sections that appear/disappear based on selections
- Nested conditional logic (up to 3 levels deep)
- Different field sets depending on Owned vs Leased
- Multiple plot support

---

# 2. DECISION TREE — ALL CONDITIONAL FLOWS

```
┌─────────────────────────────────────────────────────────────┐
│ Are the Plots?                                               │
├──────────────────┬──────────────────────────────────────────┤
│ ○ Single         │ ○ Multiple                               │
└────────┬─────────┴──────────────────┬───────────────────────┘
         │                             │
    ┌────▼────┐                   ┌────▼────────────────────┐
    │ Owner's │                   │ Number of Plots          │
    │ Details │                   │ On which plot building   │
    │ (Plot 1)│                   │ Are plots contiguous?    │
    └────┬────┘                   └────┬────────────────────┘
         │                             │
    ┌────▼────────────┐           ┌────▼────┐
    │ ○ Owned         │           │ ○ Yes   │ → (no extra fields)
    │ ○ Leased        │           │ ○ No    │ → Single boundary?
    └──┬──────────┬───┘           └────┬────┘
       │          │                    │
  ┌────▼───┐  ┌──▼───────┐       ┌────▼────┐
  │ OWNED  │  │ LEASED   │       │ ○ Yes   │ → (no extra fields)
  │ FIELDS │  │ FIELDS   │       │ ○ No    │ → Explanation textarea
  └────┬───┘  └──┬───────┘       └─────────┘
       │          │
  ┌────▼────────────────┐
  │ Land Title Document │
  │ = "Sale Deed"?      │
  ├─────────┬───────────┤
  │ YES     │ NO        │
  │ ↓       │           │
  │ Sale    │           │
  │ Deed    │           │
  │ Favor   │           │
  └─────────┴───────────┘

  LEASED → Renewal clause?
  ├── Yes → Duration of Renewal
  └── No  → (no extra fields)
```

---

# 3. FIELD CLASSIFICATION — OWNED PATH (Currently Automated in E2E)

| # | Field | Locator (from E2E) | Type | Mandatory | Dynamic | Condition |
|---|-------|-------------------|------|-----------|---------|-----------|
| 1 | Plot Type | `get_by_role("radio", name=data["plot_type"])` | Radio (Single/Multiple) | Yes | No | Always visible |
| 2 | Type of Land | `get_by_role("radio", name=data["Type_of_Land"])` | Radio (Owned/Leased) | Yes | Yes | After plot type selected |
| 3 | Area Unit | `#land_unit_0` | Standard `<select>` | Yes | Yes | After Owned/Leased selected |
| 4 | Land Area | `input[id^="land_area"]` nth(0) | Textbox (numeric) | Yes | Yes | After Owned/Leased |
| 5 | Situated In | `input[id^="situate_speci"]` nth(0) | Textbox | Yes | Yes | After Owned/Leased |
| 6 | Situated At | `input[id^="situated_at"]` nth(0) | Textbox | Yes | Yes | After Owned/Leased |
| 7 | Land Owned By | `input[id^="owned_by"]` nth(0) | Textbox | Yes | Yes | Only if Owned |
| 8 | Land Title Document | `select[id^='land_title_doc']` first | Standard `<select>` | Yes | Yes | Only if Owned |
| 9 | Sale Deed Favor | `select[id^='sale_deed_favor_whom']` first | Standard `<select>` | Yes | Yes | Only if Title = "Sale Deed" |
| 10 | Registration Details | `input[id^="land_title"]` nth(0) | Textbox | Yes | Yes | Only if Owned |
| 11 | Executed By (Seller) | `input[id^="executed_by"]` nth(0) | Textbox | Yes | Yes | Only if Owned |
| 12 | Registration Office | `input[id^="regid_ofc_details"]` nth(0) | Textbox | Yes | Yes | Only if Owned |
| 13 | Land Document Date | `get_by_role("textbox", name="Select a date")` last | Date field | Yes | Yes | Only if Owned |

---

# 4. FIELD CLASSIFICATION — LEASED PATH (NOT in E2E)

| # | Field | Expected Locator Pattern | Type | Mandatory | Condition |
|---|-------|-------------------------|------|-----------|-----------|
| 1 | Area Unit | `#land_unit_0` | `<select>` | Yes | Leased selected |
| 2 | Land Area | `input[id^="land_area"]` | Textbox (numeric) | Yes | Leased |
| 3 | Name of Lessee | Unknown | Textbox | Yes | Leased |
| 4 | Name of Lessor | Unknown | Textbox | Yes | Leased |
| 5 | Date of Lease Deed | Unknown | Date (likely readonly) | Yes | Leased |
| 6 | Duration of Lease Deed | Unknown | Textbox/Number | Yes | Leased |
| 7 | Date of Registration | Unknown | Date (likely readonly) | Yes | Leased |
| 8 | Details of Registration Office | Unknown | Textbox | Yes | Leased |
| 9 | Renewal clause? | Unknown | Radio (Yes/No) | Yes | Leased |
| 10 | Duration of Renewal | Unknown | Textbox/Number | Conditional | Only if Renewal = Yes |

---

# 5. FIELD CLASSIFICATION — MULTIPLE PLOTS PATH (NOT in E2E)

| # | Field | Type | Mandatory | Condition |
|---|-------|------|-----------|-----------|
| 1 | Number of plots | Number input | Yes | Multiple selected |
| 2 | On which plot school building | Number/Textbox | Yes | Multiple |
| 3 | Are plots contiguous? | Radio (Yes/No) | Yes | Multiple |
| 4 | Single boundary/wall? | Radio (Yes/No) | Conditional | Only if contiguous = No |
| 5 | Explanation textarea | Textarea | Conditional | Only if boundary = No |

---

# 6. E2E COVERAGE ANALYSIS

| Flow | Automated in E2E? | Notes |
|------|-------------------|-------|
| Single → Owned → Non-Sale-Deed | ✅ Yes | Partial — always fills same path |
| Single → Owned → Sale Deed | ✅ Yes (conditional) | `if data["land_title_document"] == "Sale Deed"` |
| Single → Leased | ❌ No | Entire leased path not automated |
| Multiple → Contiguous=Yes | ❌ No | Not automated |
| Multiple → Contiguous=No → Boundary=Yes | ❌ No | Not automated |
| Multiple → Contiguous=No → Boundary=No | ❌ No | Not automated |

---

# 7. AUTOMATION CHALLENGES

| # | Challenge | Severity | Description |
|---|-----------|----------|-------------|
| 1 | Dynamic form rendering | HIGH | Radio selections load entire form sections dynamically — requires waits |
| 2 | Nested conditionals (3 levels) | HIGH | Plot type → Land type → Title type / Renewal |
| 3 | nth(0) locators | MEDIUM | Multiple plots = multiple indexed elements — fragile |
| 4 | Date field (Land Document Date) | MEDIUM | E2E uses `.fill()` on `get_by_role("textbox", name="Select a date")` — may be readonly like NOC/Trust |
| 5 | Leased path completely untested | HIGH | No existing E2E coverage — all locators unknown |
| 6 | Multiple plots path untested | HIGH | No existing E2E coverage |
| 7 | Area Unit dropdown behavior | MEDIUM | Previously had issues — hardcoded "Square Meter" |
| 8 | Form state persistence | MEDIUM | Same as Trust — fields may retain values |

---

# 8. CRITICAL OBSERVATIONS FROM E2E CODE

1. **Date field uses `.fill()`** — unlike NOC/Trust which are readonly:
```python
self.page.get_by_role("textbox", name="Select a date").last.fill(data["land_document_date"])
```
This suggests the Land Document Date may NOT be readonly (or the E2E bypasses it differently). **Needs diagnostic.**

2. **Area Unit is hardcoded:**
```python
self.page.locator("#land_unit_0").select_option("Square Meter")
```
Not data-driven — always selects "Square Meter."

3. **All field locators use `nth(0)`** — designed for single plot. Multiple plots would need `nth(1)`, `nth(2)` etc.

4. **Sale Deed conditional is clean** — `if data["land_title_document"] == "Sale Deed"` pattern proven.

---

# 9. POTENTIAL VALIDATION RULES

| Field | Possible Validation |
|-------|-------------------|
| Land Area | Must be positive number |
| Area Unit | Must be selected |
| All text fields | Mandatory (cannot blank) |
| Land Document Date | Must be valid past date |
| Number of plots | Must be positive integer (Multiple path) |
| Duration fields | Must be positive number |
| Explanation | Required if contiguous=No AND boundary=No |

---

# 10. POTENTIAL BUSINESS RULES

| Rule | Applies To |
|------|-----------|
| Land document date cannot be future | Owned path |
| Lease deed date cannot be future | Leased path |
| Lease duration must be positive | Leased path |
| Renewal duration only if renewal = Yes | Leased path |
| Explanation only if both contiguous=No AND boundary=No | Multiple path |

---

# 11. REUSABLE EXISTING METHODS

| Method/Pattern | Reuse For |
|----------------|-----------|
| `ValidationHelper.set_readonly_date()` | Date fields (if readonly) |
| `select_option(label/value)` | Area Unit, Land Title Doc, Sale Deed Favor |
| `get_by_role("radio", name=...)` | All radio selections |
| `fill_partial_details()` pattern | Owned path field filling |
| `.fill()` | Text fields |
| `wait_for_timeout()` | Dynamic form load waits |
| `wait_for(state="visible")` | Wait for conditional fields |

---

# 12. RECOMMENDED APPROACH

## Phase 1: Automate ONLY the Owned path (matches E2E)
- Same fields already have locators
- Validated by existing E2E
- Lower risk

## Phase 2: Automate Leased path (requires diagnostics)
- All locators unknown
- Needs full field discovery
- Higher risk

## Phase 3: Automate Multiple plots (most complex)
- Nested conditionals
- Dynamic field counts
- Highest risk

---

# 13. DIAGNOSTICS REQUIRED BEFORE IMPLEMENTATION

| # | Diagnostic | Priority | Reason |
|---|-----------|----------|--------|
| 1 | Is Land Document Date readonly or fillable? | HIGH | E2E uses .fill() but pattern differs from NOC/Trust |
| 2 | What happens when form fields are cleared (persistence behavior)? | HIGH | Same issue as Trust Details |
| 3 | Area Unit dropdown — what are the actual options and values? | MEDIUM | Currently hardcoded |
| 4 | Land Title Document — what are all options? | MEDIUM | Only "Sale Deed" conditional tested |
| 5 | Leased path — what are the field locators? | HIGH (Phase 2) | Zero E2E coverage |
| 6 | Multiple plots — what are the field locators? | HIGH (Phase 3) | Zero E2E coverage |
| 7 | Validation messages — what appears when fields blank? | MEDIUM | Capture exact messages |

---

# 14. ESTIMATED TEST CATEGORIES (Owned Path Only — Phase 1)

| Category | Tests | Scope |
|----------|-------|-------|
| Validation | 1 | All owned fields blank |
| Positive | 2–3 | Valid owned (non-sale-deed), valid owned (sale deed) |
| Negative | 4–6 | Blank fields, invalid area, future date |
| Boundary | 2–3 | Area min/max, text field lengths |
| **Total Phase 1** | **9–13** | |

## Future Phases:
- Phase 2 (Leased): +8–10 tests
- Phase 3 (Multiple): +5–7 tests
- **Grand Total Potential:** 22–30 tests

---

# 15. NON-AUTOMATABLE SCENARIOS (Same Patterns)

| Scenario | Reason |
|----------|--------|
| Area Unit blank after save | Dropdown retains selection |
| Land Title Document blank | Dropdown retains selection |
| Sale Deed Favor blank | Only appears conditionally — testing requires specific path |
| Calendar UI date restrictions | JS injection bypasses |

---

**STATUS:** Analysis complete. Diagnostics required before implementation — especially Date field behavior and persistence.
