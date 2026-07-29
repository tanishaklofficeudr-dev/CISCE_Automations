# NOC Details Module — Automation Analysis Report

---

# 1. MODULE ANALYSIS

The NOC Details page captures information about the No Objection Certificate issued by the State/UT Education Department. The E2E automation fills all fields and clicks Next.

**Key observation from existing code:** Country and State dropdowns are HARDCODED to values `"2"` (India) and `"30"` (Rajasthan) rather than using data from Excel. Multiple commented-out approaches suggest instability in these dropdowns.

---

# 2. FIELD CLASSIFICATION TABLE

| # | Field Name | Locator | Input Type | Mandatory | Dependency | Data Source in E2E |
|---|-----------|---------|-----------|-----------|------------|-------------------|
| 1 | NOC Issuing Authority | `#noc_authority` | Textbox | Yes | None | `data["noc_issuing_authority"]` |
| 2 | Designation | `#noc_designation` | Textbox | Yes | None | `data["designation"]` |
| 3 | Office Address | `#noc_office_address` | Textbox | Yes | None | `data["office_address"]` |
| 4 | Country | `#noc_country` | Standard `<select>` Dropdown | Yes | None | **Hardcoded: value="2" (India)** |
| 5 | State | `#noc_state` | Standard `<select>` Dropdown | Yes | **Depends on Country** | **Hardcoded: value="30" (Rajasthan)** |
| 6 | NOC Reference Number | `get_by_role("textbox", name="Select NOC Reference Number")` | Textbox | Yes | None | `data["noc_reference_number"]` |
| 7 | Date of NOC | `#noc_date[name='noc_date']` | **Date Picker** (UI calendar) | Yes | None | **Hardcoded: back arrow + day 16** |

---

# 3. AUTOMATION CHALLENGES

## Challenge 1: Date Picker (CRITICAL)

**Current E2E approach:**
```python
page.locator("#noc_date[name='noc_date']").click()    # Open calendar
page.get_by_role("columnheader", name="«").click()     # Go back one month
page.get_by_role("cell", name="16", exact=True).click() # Select day 16
```

**Issues for regression testing:**
- The date is hardcoded (always selects 16th of previous month)
- Date picker starts on CURRENT month — "previous month" changes every month
- No ability to select a specific date like "15/03/2024" directly
- Cannot test future date validation without complex calendar navigation
- Cannot test "date not selected" easily (requires NOT clicking any day after opening)

**Diagnostic required:** 
- Can the date field accept `.fill("15/03/2024")` directly?
- Does the field have an input mask that requires the calendar UI?
- What happens if you type a date string directly?

---

## Challenge 2: Country/State Dropdowns (HARDCODED)

**Current E2E uses:**
```python
page.locator("#noc_country").select_option("2")   # India by value
page.locator("#noc_state").select_option("30")    # Rajasthan by value
```

**Multiple commented-out approaches suggest:**
- `select_option(label=...)` didn't work reliably
- `select_option(str(data["country"]))` didn't work
- Only `select_option("2")` (by value) was stable

**For regression:**
- Country/State are standard `<select>` elements (not Select2)
- They can be changed to different values using `select_option(value=...)`
- State depends on Country (changing Country reloads State options)
- Cannot be reset to blank ("Select") after first save (persistence issue)

---

## Challenge 3: Data Persistence

| Field | Persists After Save? | Can Overwrite? | Can Clear? |
|-------|---------------------|----------------|-----------|
| NOC Authority | Yes | Yes (.fill) | Yes (.fill("")) |
| Designation | Yes | Yes (.fill) | Yes (.fill("")) |
| Office Address | Yes | Yes (.fill) | Yes (.fill("")) |
| Country | Yes | Yes (select_option) | **No** (no blank option) |
| State | Yes | Yes (select_option) | **No** (no blank option) |
| NOC Reference Number | Yes | Yes (.fill) | Yes (.fill("")) |
| Date of NOC | Yes | **Unknown** | **Unknown** — may retain previous date |

---

## Challenge 4: NOC Reference Number

- Locator: `get_by_role("textbox", name="Select NOC Reference Number")`
- Placeholder text suggests it might be a searchable/autocomplete field
- E2E uses `.fill()` directly — works for positive path
- May have format requirements (e.g., alphanumeric pattern)

---

# 4. REQUIRED ADDITIVE PAGE OBJECT METHODS

| # | Method | Purpose |
|---|--------|---------|
| 1 | `click_next()` | Click Next without filling — for validation test |
| 2 | `fill_authority(value)` | Fill only authority field |
| 3 | `fill_designation(value)` | Fill only designation field |
| 4 | `fill_office_address(value)` | Fill only office address field |
| 5 | `fill_reference_number(value)` | Fill only reference number field |
| 6 | `fill_partial_details(data, skip_fields)` | Fill all except specified + click Next |

**Date picker methods (depends on diagnostic):**
| 7 | `fill_date_direct(date_string)` | If `.fill()` works on date field |
| 8 | `select_date_via_picker(day, months_back)` | If calendar UI is required |

---

# 5. ESTIMATED TEST COUNT

| Category | Tests | Rationale |
|----------|-------|-----------|
| Validation | 1 | All text fields blank — consolidated (first visit) |
| Positive | 2–3 | Valid complete form; different authority/designation combos |
| Negative (Format) | 3–5 | Blank individual fields (authority, designation, office address, reference) |
| Boundary | 2–3 | Authority max length, office address max length |
| **Total** | **8–12** | |

**NOTE:** Date picker tests and Country/State blank tests are likely NOT automatable due to persistence + UI complexity.

---

# 6. NON-AUTOMATABLE SCENARIOS

| Scenario | Reason |
|----------|--------|
| Country dropdown blank | Standard `<select>` retains value after save |
| State dropdown blank | Dependent + persistent |
| Date of NOC not selected | Calendar UI — cannot "unselect" a previously saved date |
| Future date validation | Complex calendar navigation required; behavior unknown |
| Date format validation | Unknown if field accepts typed input |

---

# 7. RISKS

| # | Risk | Severity | Likelihood |
|---|------|----------|-----------|
| 1 | Date picker `.fill()` doesn't work (requires UI interaction) | HIGH | High |
| 2 | Country/State values "2"/"30" change between environments | Medium | Low |
| 3 | State options don't load after Country change | Medium | Medium |
| 4 | NOC Reference Number has undocumented format requirements | Medium | Low |
| 5 | Date field retains saved value — cannot test "blank date" | Medium | High |
| 6 | Calendar navigation depends on current month (fragile) | Medium | High |

---

# 8. RECOMMENDATIONS

1. **Run date field diagnostic BEFORE implementation** — determine if `.fill("16/05/2026")` works
2. **Start with text field tests only** — authority, designation, office address, reference number are safe
3. **Defer date picker tests** until diagnostic confirms the approach
4. **Use hardcoded Country/State values** (same as E2E) for regression baseline
5. **Do not attempt dropdown-blank tests** — same persistence issue as School Details and Address Details

---

# 9. EXPECTED IMPLEMENTATION EFFORT

| Task | Effort |
|------|--------|
| Date field diagnostic | 30 min |
| Add methods to noc_details_page.py | 1 hour |
| Create noc_ready_page fixture | 30 min |
| Create Excel sheets | 30 min |
| Implement tests (text field scenarios) | 2 hours |
| Implement date tests (if diagnostic passes) | 1 hour |
| Testing + debugging | 1 hour |
| **Total** | **~1 day** |

---

# 10. DIAGNOSTIC CHECKLIST (Must Verify Before Automation)

| # | Field | Diagnostic Question | How to Verify | Priority |
|---|-------|--------------------|--------------:|----------|
| 1 | Date of NOC | Does `.fill("16/05/2026")` set the date value? | Run test: `page.locator("#noc_date").fill("16/05/2026")` → read value | **HIGH** |
| 2 | Date of NOC | Does `.fill()` trigger the date picker validation? | Fill date → click Next → check for errors | HIGH |
| 3 | Date of NOC | Can a future date be entered? | Fill future date → click Next → observe | HIGH |
| 4 | Date of NOC | What's the field's `type` attribute? | Read `#noc_date` attributes | HIGH |
| 5 | NOC Reference Number | Does the field accept any text or has format requirements? | Fill "TESTREF123" → click Next | Medium |
| 6 | NOC Reference Number | Is it a searchable/autocomplete field or plain textbox? | Inspect DOM | Medium |
| 7 | Country → State | Does changing Country reload State options? | Select different country → check state options | Low |
| 8 | All text fields | Does the app validate blank fields on click Next? | Clear all → Next → check errors | Medium |

---

**STATUS:** Analysis complete. Date field diagnostic is the critical blocker.
**Next Step:** Run date field diagnostic before proceeding with implementation.
