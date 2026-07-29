# Trust/Society/Company Details — Analysis Report

---

# 1. FIELD CLASSIFICATION TABLE

| # | Field Name | Locator | Control Type | Mandatory | Clearable? | Retained? | Readonly? | Automation Approach | E2E Method |
|---|-----------|---------|-------------|-----------|-----------|-----------|-----------|--------------------:|------------|
| 1 | Ownership Type | `#ownership_type` | Standard `<select>` dropdown | Yes | ❌ (no blank option likely) | Yes | No | `select_option(value/label)` | `select_option(data["ownership_type"])` |
| 2 | Trust/Society/Company Name | `#owner_name` | Textbox | Yes | ✅ `.fill("")` | Yes | No | `.fill()` | `.fill(data["trust_name"])` |
| 3 | Date of Establishment | `#establishment_date` | **Readonly datepicker** | Yes | ✅ `set_readonly_date("", "")` | Yes | **Yes** (readonly) | `ValidationHelper.set_readonly_date()` | JavaScript injection |
| 4 | Date of Registration | `#registration_date` | **Readonly datepicker** | Yes | ✅ `set_readonly_date("", "")` | Yes | **Yes** (readonly) | `ValidationHelper.set_readonly_date()` | JavaScript injection |
| 5 | Registration Number | `#registration_no` | Textbox | Yes | ✅ `.fill("")` | Yes | No | `.fill()` | `.fill(str(data["registration_number"]))` |

---

# 2. CRITICAL OBSERVATIONS FROM E2E CODE

## 2.1 Ownership Type Dropdown

```python
self.page.wait_for_timeout(2000)
self.page.locator("#ownership_type").wait_for(state="visible")
self.page.locator("#ownership_type").select_option(data["ownership_type"])
```

**Key findings:**
- 2-second wait BEFORE attempting interaction (page needs time to load)
- Explicit `wait_for(state="visible")` — field loads dynamically
- Uses `select_option(data["ownership_type"])` — value-based selection
- Standard `<select>` element (NOT Select2)
- **Same pattern as NOC Country** — disabled "Select" placeholder likely

## 2.2 Date Fields (BOTH Readonly)

```python
self.page.evaluate("""
    (date) => {
        const input = document.querySelector('#establishment_date');
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(input, date);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }
""", str(data["establishment_date"]))
```

**Key findings:**
- SAME JavaScript injection pattern as NOC Date ✅
- Already confirmed working in NOC diagnostic
- `ValidationHelper.set_readonly_date()` can be reused directly
- Selectors: `#establishment_date` and `#registration_date`
- **No `blur` event** dispatched in E2E (only `input` + `change`) — but NOC diagnostic proved `blur` helps. Use `set_readonly_date()` which includes all three.

## 2.3 Text Fields

- `#owner_name` — standard textbox, clearable
- `#registration_no` — standard textbox, clearable

---

# 3. LESSONS APPLIED (Avoiding Previous Module Issues)

| Lesson From | Issue | Mitigation for Trust Details |
|-------------|-------|------------------------------|
| School Details | Dropdown blank test impossible after save | Do NOT test "Ownership Type = blank" |
| School Details | Field overwrite needed for independent execution | Always fill ALL fields before overwriting target |
| Address Details | Cascading dropdowns + disabled "Select" option | Ownership has no cascade — simpler. But blank placeholder likely disabled. |
| NOC Details | Readonly datepickers need JavaScript | Use `ValidationHelper.set_readonly_date()` — already proven |
| NOC Details | Date field must be filled for form to submit | Always set BOTH dates in every test |
| NOC Details | Future date may be accepted (app defect) | Include future date test — verify actual behavior |
| All Modules | SPA navigation detection | Use `get_by_text("Certificate of Land")` or similar for next-step detection |
| All Modules | Validation occurs on Next click only | All assertions after `click_next()` |

---

# 4. DIAGNOSTICS REQUIRED BEFORE IMPLEMENTATION

| # | Field | Diagnostic Question | Priority | Method |
|---|-------|--------------------|---------:|--------|
| 1 | Ownership Type | Does `select_option(index=0)` fail (disabled "Select" placeholder)? | Medium | Same pattern as NOC Country — likely fails |
| 2 | Ownership Type | What are the available option values/labels? | Medium | Read dropdown options |
| 3 | Establishment Date | Does `set_readonly_date()` work? (Already proven pattern — LOW risk) | Low | Already confirmed for NOC |
| 4 | Registration Date | Same as above | Low | Already confirmed |
| 5 | Establishment Date | Is future date rejected? | Medium | Test future date + Next |
| 6 | Registration Date | Is future date rejected? | Medium | Same |
| 7 | Both Dates | Is Registration Date required to be AFTER Establishment Date? | **HIGH** | Critical business rule |
| 8 | Trust Name | Does it have min/max character limits? | Low | Fill 1 char and 300 chars |
| 9 | Registration Number | Format restrictions? | Low | Fill alphabets, specials |
| 10 | All Fields | Exact validation messages? | Medium | Clear all + Next |

**Critical diagnostic: #7** — Business rule about Registration Date > Establishment Date (identified in original analysis but never verified).

---

# 5. RISK ASSESSMENT

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|-----------|-----------|
| 1 | Ownership dropdown has disabled "Select" — cannot test blank | Medium | High | Exclude from negative tests (same as all previous modules) |
| 2 | Date fields already confirmed with `set_readonly_date()` in NOC | Low | Low | Pattern proven — minimal risk |
| 3 | Registration Date before Establishment Date — unknown validation | **HIGH** | Medium | Must run diagnostic #7 before implementing |
| 4 | Future dates accepted (same as NOC finding) | Medium | High | Include test but expect potential app defect |
| 5 | Dynamic page load — 2s wait needed before interaction | Low | Low | E2E already handles this with wait_for_timeout |
| 6 | Trust Name/Registration Number have undiscovered length limits | Low | Medium | Boundary tests will discover |

---

# 6. ESTIMATED TEST CATEGORIES

| Category | Tests | Rationale |
|----------|-------|-----------|
| Validation | 1 | All text fields + dates cleared → verify errors |
| Positive | 2 | Valid complete form; different ownership type |
| Negative | 5–7 | Blank name, blank reg number, empty dates, future dates, reg date < est date |
| Boundary | 2–3 | Name min/max, registration number max |
| **Total** | **10–13** | |

---

# 7. POTENTIAL NON-AUTOMATABLE SCENARIOS

| Scenario | Reason |
|----------|--------|
| Ownership Type blank | Disabled "Select" placeholder (same as NOC Country) |
| Calendar UI min/max enforcement | JavaScript injection bypasses calendar restrictions |
| Invalid date format typed | Field is readonly — cannot type invalid format |

---

# 8. PROPOSED TEST MATRIX

## Validation (1 test)

| TC ID | Scenario |
|-------|----------|
| TRUST_VAL_001 | All mandatory text fields + dates cleared → verify all errors |

## Positive (2 tests)

| TC ID | Scenario |
|-------|----------|
| TRUST_POS_001 | Valid — Trust ownership, valid name, valid past dates, valid reg number |
| TRUST_POS_002 | Valid — Society ownership, different dates |

## Negative (6 tests)

| TC ID | Scenario | Field |
|-------|----------|-------|
| TRUST_FMT_001 | Trust name blank | owner_name |
| TRUST_FMT_002 | Registration number blank | registration_no |
| TRUST_FMT_003 | Establishment date empty | establishment_date |
| TRUST_FMT_004 | Registration date empty | registration_date |
| TRUST_FMT_005 | Future establishment date | establishment_date |
| TRUST_FMT_006 | Registration date before establishment date | registration_date |

## Boundary (3 tests)

| TC ID | Scenario | Field |
|-------|----------|-------|
| TRUST_BND_001 | Trust name — 1 character (min) | owner_name |
| TRUST_BND_002 | Trust name — 200 characters (potential max) | owner_name |
| TRUST_BND_003 | Registration number — 50 characters | registration_no |

---

# 9. IMPLEMENTATION READINESS

| Aspect | Ready? | Notes |
|--------|--------|-------|
| Date fields | ✅ Yes | `set_readonly_date()` proven in NOC |
| Text fields | ✅ Yes | Standard `.fill()` |
| Dropdown | ⚠️ Needs diagnostic | Verify options + disabled placeholder |
| Date business rule (reg > est) | ❌ Needs diagnostic | Critical — test #7 |
| Validation messages | ❌ Unknown | Must capture on first run |
| Page navigation detection | ⚠️ Verify | Check if "Certificate of Land" text identifies next step |

---

# 10. RECOMMENDED NEXT STEP

**Run ONE diagnostic that verifies:**
1. Ownership dropdown options and blank behavior
2. Both dates set via `set_readonly_date()` → click Next → form navigates?
3. Registration date BEFORE establishment date → validation?
4. Future dates → validation?
5. All blank → capture exact error messages

This single diagnostic covers all unknowns. After results, proceed directly to implementation.

---

**STATUS:** Analysis complete. One combined diagnostic required before implementation.
