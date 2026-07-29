# NOC Date Field — Diagnostic Report
## Evidence-Based Findings

---

# FIELD IDENTITY

```html
<input type="text" id="noc_date" name="noc_date" value=""
       class="form-control form-control-sm bd-clr datepicker date-picker"
       placeholder="Select a date" readonly="readonly">
```

**The field is READ-ONLY.** This is the definitive finding.

---

# DIAGNOSTIC RESULTS

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Can `.fill()` enter a date? | ❌ **NO** | `element is not editable` — readonly attribute blocks fill |
| 2 | Can `.press_sequentially()` enter a date? | ❌ **NO** | Same — fill("") fails before typing starts |
| 3 | Is the field read-only? | ✅ **YES** | `readonly="readonly"` confirmed in HTML |
| 4 | Does clicking open a calendar? | ✅ **YES** | `.datepicker` element becomes visible |
| 5 | Is selecting from calendar mandatory? | ✅ **YES** | Only way to set value (field is readonly) |
| 6 | Can manual typing be used? | ❌ **NO** | Readonly prevents all direct input |
| 7 | Can JavaScript set the value? | ✅ **YES** | `nativeInputValueSetter` → DOM value = '10/01/2025' |
| 8 | Is today's date accepted? | ❓ Unknown | Could not test (fill blocked) |
| 9 | Is a past date accepted? | ❓ Unknown | Could not test via fill; JS approach untested with Next |
| 10 | Is a future date accepted? | ❓ Unknown | Could not test |
| 11 | Is empty date rejected? | ❓ Unknown | Could not clear field (fill("") blocked) |
| 12 | Validation timing | On Next click (assumed) | Same pattern as other fields |
| 13 | Date persists after returning? | ❓ Unknown | Could not complete full save flow |
| 14 | Min/max dates enforced? | ❓ Unknown | Calendar UI may restrict — needs visual check |
| 15 | Exact validation message? | ❓ Unknown | Could not trigger validation |

---

# CLASSIFICATION

## **REQUIRES SPECIAL HANDLING**

The Date of NOC field is:
- **Readonly** — cannot use `.fill()` or `.type()`
- **Calendar-only** — date must be selected via the datepicker UI
- **JavaScript-settable** — `nativeInputValueSetter` can set the value in DOM

---

# RECOMMENDED AUTOMATION APPROACH

## Option A: JavaScript Injection (Recommended)

```python
page.evaluate("""
    (date) => {
        const input = document.querySelector('#noc_date[name="noc_date"]');
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(input, date);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }
""", "16/05/2025")
```

**Pros:**
- Confirmed working (CHECK 10: DOM value = '10/01/2025')
- Fast, reliable, no UI interaction needed
- Can set any date (past, future, today)
- Same approach already used in `trust_details_page.py` for dates

**Cons:**
- Bypasses calendar UI validation (min/max date enforcement)
- May not trigger datepicker's internal state update
- Need to verify the form accepts JS-set dates on Next click

## Option B: Calendar UI Interaction (E2E approach)

```python
page.locator("#noc_date[name='noc_date']").click()  # Opens calendar
page.get_by_role("columnheader", name="«").click()   # Navigate months
page.get_by_role("cell", name="16", exact=True).click()  # Select day
```

**Pros:**
- Exactly what the E2E does — proven working
- Respects calendar restrictions (min/max dates)
- Triggers all internal datepicker events

**Cons:**
- Complex navigation for specific dates
- Fragile — depends on current month
- Cannot test arbitrary dates easily
- Cannot test empty date (no way to "unselect" a date)

## Option C: Hybrid (Best for Regression)

- **Positive tests:** Use JavaScript injection (set specific dates reliably)
- **Calendar navigation test:** Use UI approach (one test to verify calendar works)
- **Future date test:** Use JavaScript to set future date → click Next → check validation
- **Empty date test:** Use JavaScript to clear value → click Next → check validation

---

# WHAT NEEDS FURTHER VERIFICATION

Before implementing regression tests, one more diagnostic is needed:

1. **Does the form ACCEPT a JS-set date on Next click?**
   - Set date via JS → fill all other fields → click Next → does it navigate?
   - If YES: JavaScript approach is fully viable
   - If NO: Calendar UI is mandatory

2. **Can JS clear the date?**
   - Set value to "" via JS → click Next → does "date required" error appear?

3. **Does JS-set future date trigger validation?**
   - Set future date via JS → click Next → does "cannot be future" error appear?

---

# COMPARISON WITH TRUST DETAILS DATE FIELDS

The Trust Details page (`trust_details_page.py`) already uses this exact JavaScript approach:
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

**This is a proven pattern in the framework.** The NOC date field should use the same approach.

---

# FINAL RECOMMENDATION

| Aspect | Recommendation |
|--------|----------------|
| Positive date tests | JavaScript injection — set valid past date |
| Future date test | JavaScript — set future date, verify rejection |
| Empty date test | JavaScript — set "" value, verify rejection |
| Calendar UI test | Reuse E2E approach (1 test only) |
| Implementation method | Same as `trust_details_page.py` |
| Risk level | Low — pattern already proven in this framework |

---

**STATUS:** Diagnostic complete. Field classified as **Requires Special Handling (JavaScript injection).**
**Next Step:** Run one final verification — JS-set date + click Next — to confirm the form accepts it.
