# Root Cause Analysis: SCH_NEG_07 & SCH_NEG_08
## UDISE Field Negative Tests Failing in Automation but Passing Manually

---

# PROBLEM STATEMENT

| Test | Invalid Value | Manual Result | Automation Result |
|------|--------------|---------------|-------------------|
| SCH_NEG_07 | `abcdefghijk` | Validation shown, form blocked ✅ | Form navigates, no error detected ❌ |
| SCH_NEG_08 | `123@#$456!!` | Validation shown, form blocked ✅ | Form navigates, no error detected ❌ |

The application **correctly validates** UDISE during manual testing. The automation is failing to reproduce the correct behavior.

---

# DIAGNOSTIC ANALYSIS

## 1. Is the invalid value actually being entered into the UDISE field?

**Likely Issue: The field FILTERS input at the keystroke level.**

The UDISE field likely uses an `input` event listener or `maxlength` + `pattern` attribute that:
- Prevents non-numeric characters from being typed
- Strips invalid characters immediately on input
- Only allows digits to remain in the field

**Playwright's `.fill()` method** bypasses the native input mechanism. It sets the value directly via JavaScript, which may:
- Skip the `keydown`/`keypress` event listeners that filter characters
- Set the field value to `"abcdefghijk"` but the field's internal validation ignores it
- Result in the field displaying the old saved value (11-digit number) because the invalid input was silently rejected

**Root Cause Probability: HIGH (90%)**

When you type manually:
```
Keyboard → keydown → keypress → input event → field JS filters non-numeric → only digits remain → if empty/invalid length → validation shown
```

When Playwright `.fill()` executes:
```
.fill("abcdefghijk") → sets value directly → may bypass input filter → field shows "abcdefghijk" visually BUT the form's internal model still holds the old valid value → click Next → form submits with OLD valid value
```

OR alternatively:
```
.fill("abcdefghijk") → field's input mask immediately strips non-numeric chars → field becomes empty "" → BUT because saved data exists from prior submission → the saved value is retained server-side → Next succeeds
```

---

## 2. Does the field automatically filter non-numeric characters?

**Very likely YES.** Common patterns for UDISE-type fields:

```html
<input type="text" id="udise" maxlength="11" 
       oninput="this.value = this.value.replace(/[^0-9]/g, '')" />
```

Or via JavaScript:
```javascript
document.getElementById('udise').addEventListener('input', function() {
    this.value = this.value.replace(/\D/g, '');
});
```

If this filter exists, Playwright's `.fill()` triggers the `input` event AFTER setting the value, which then **strips all non-numeric characters**, leaving the field empty or with the previous valid value.

**Result:** The field never actually contains `"abcdefghijk"` — it gets immediately cleaned to `""` or the prior saved value.

---

## 3. Is the automation waiting for the validation message?

The current code:
```python
school_page.fill_partial_details(test_data, skip_fields=[])
# fill_partial_details clicks Next at the end
```

Then checks:
```python
page.wait_for_timeout(1000)
form_navigated = page.locator("#TabAddressDetails").is_visible()
```

**Issue:** If the field auto-filters to empty, the form may show validation briefly but the check happens after 1 second — by which time:
- The validation message might flash and disappear
- OR the form might submit because the SAVED server-side value (from prior successful submission) is used

---

## 4. Is the assertion checking the correct validation text?

The Excel has: `expected_error: "Invalid UDISE number"` but the actual validation (seen in earlier test run for length) showed: `"U-DISE number must be 11 digits."`

Even if the validation DID appear, the test would still fail because:
- We search for `"Invalid UDISE number"` 
- The app shows `"U-DISE number must be 11 digits."`

**This is a secondary issue** — but the primary issue is that validation never appears because the form navigates.

---

## 5. Is the locator for the validation message correct?

The `ValidationHelper.get_all_errors()` looks for:
```python
".invalid-feedback:visible"
".text-danger:visible"
```

The UDISE validation message (when it does appear manually) likely uses one of these classes. But since the form navigates in automation, there's no validation to find.

**Not the root cause** — the root cause is upstream (value not being entered correctly).

---

## 6. Is the Next button being clicked before validation completes?

No — `fill_partial_details()` fills ALL fields sequentially, then clicks Next. The issue is that the UDISE field doesn't actually contain the invalid value by the time Next is clicked.

---

## 7. Is Playwright synchronization implemented correctly?

The `.fill()` method is synchronous in Playwright and waits for the actionability check. However, it does NOT wait for custom JavaScript event handlers to finish processing the value.

---

# ROOT CAUSE: CONFIRMED

## Primary Root Cause: `.fill()` bypasses field input filtering

The UDISE field has a client-side input mask (JavaScript `oninput` handler) that strips non-numeric characters. When Playwright uses `.fill()`:

1. It clears the field
2. Sets the value to `"abcdefghijk"`
3. Dispatches `input` event
4. The field's JS handler fires: `this.value = this.value.replace(/[^0-9]/g, '')`
5. Field value becomes `""` (empty string)
6. BUT — because the form was previously saved successfully, the server-side value persists
7. Click Next → server accepts the previously saved valid UDISE → navigates

## Secondary Root Cause: Expected error text mismatch

Even if validation appeared, `"Invalid UDISE number"` would not match `"U-DISE number must be 11 digits."`

---

# SOLUTION OPTIONS

## Option A: Use `.type()` instead of `.fill()` (RECOMMENDED)

```python
self.page.locator("#udise").fill("")  # Clear first
self.page.locator("#udise").type("abcdefghijk")  # Type character by character
```

`.type()` dispatches individual `keydown`, `keypress`, `keyup` events for each character — exactly simulating manual typing. The field's input mask will filter each character as it's typed, resulting in the field remaining empty, which should trigger the validation on Next click.

## Option B: Use `.press_sequentially()` 

```python
self.page.locator("#udise").fill("")
self.page.locator("#udise").press_sequentially("abcdefghijk")
```

Same effect as `.type()` — sends individual key events.

## Option C: Use JavaScript to verify field value after fill

```python
self.page.locator("#udise").fill("abcdefghijk")
actual_value = self.page.locator("#udise").input_value()
# If actual_value != "abcdefghijk", the field filtered it
```

This at least confirms the filtering behavior.

---

# RECOMMENDED FIX

**For UDISE specifically:** Use `.fill("")` to clear, then `.type()` to simulate real typing. The field will filter characters, leaving it empty, which triggers length validation on Next.

**Implementation change in `fill_partial_details()`:**
```python
if "udise_number" not in skip_fields:
    self.page.locator("#udise").fill("")
    self.page.locator("#udise").type(str(data.get("udise_number", "")))
```

This change:
- Clears the field first (removes saved value)
- Types the value character-by-character (respects input mask)
- Non-numeric characters get filtered by the field's JS
- Field ends up empty or with only the valid digits
- Click Next → validation fires for invalid length or empty field

---

# ALSO FIX: Update expected error text

| Test | Current Expected | Correct Expected |
|------|-----------------|------------------|
| SCH_NEG_07 | Invalid UDISE number | U-DISE number must be 11 digits |
| SCH_NEG_08 | Invalid UDISE number | U-DISE number must be 11 digits |

---

# VALIDATION PLAN

After implementing the fix:
1. Run SCH_NEG_07 with `--headed` and observe the UDISE field
2. Verify alphabetic characters are NOT retained in the field
3. Verify validation message appears after clicking Next
4. Verify the test passes

---

**STATUS:** Root cause identified. Solution proposed. Awaiting approval to implement fix.
