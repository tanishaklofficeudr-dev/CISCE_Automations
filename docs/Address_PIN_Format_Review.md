# Address PIN Format Scenarios — Exclusion Review

---

# REVIEW QUESTION

Should PIN format tests (alphabets/special chars of 6 characters) be excluded or included?

---

# EVIDENCE REVIEW

## Diagnostic Result (from `debug_pin_code_field.py`):

| Test | Value | Chars | DOM Accepts? | Next Clicked? | Validation Observed? |
|------|-------|-------|-------------|---------------|---------------------|
| .fill("abcdef") | abcdef | 6 | Yes | **NOT TESTED** | **NOT TESTED** |
| .fill("12@#56") | 12@#56 | 6 | Yes | **NOT TESTED** | **NOT TESTED** |
| .fill("12345") | 12345 | 5 | Yes | Yes | Yes → "The zip field must be 6 digits." |

**Critical observation:** The diagnostic verified that `.fill()` with alphabets/specials places the value in DOM. But it did **NOT test what happens when Next is clicked with those 6-character non-numeric values.**

The diagnostic only clicked Next with `"12345"` (5 digits) — which triggered the length error.

---

## Basis of Original Exclusion:

The exclusion was based on:
- ❌ **Assumption** that "6 digits" validation only checks length (count = 6)
- ❌ **Inference** from UDISE behavior (which also says "11 digits" but only checks length)
- ❌ **DOM acceptance** of the value (field holds the value)
- ✅ None of the above constitutes actual verification of Next-click behavior

**The exclusion was made WITHOUT clicking Next with 6-character non-numeric values.**

---

## Manual Testing Says:

> "Entering alphabetic or special-character PIN values shows the validation message: 'The zip field must be 6 digits.'"

This means:
1. The validation message `"The zip field must be 6 digits."` uses "digits" literally
2. The server-side validation checks: **is the value exactly 6 NUMERIC digits?**
3. `"abcdef"` (6 chars, not digits) → BLOCKED with error
4. `"12@#56"` (6 chars, not all digits) → BLOCKED with error

---

# REVISED CLASSIFICATION

| Scenario | Previous Classification | Revised Classification | Reason |
|----------|----------------------|----------------------|--------|
| PIN = "abcdef" (6 alphabets) | Excluded | **INCLUDE** | Manual confirms validation fires |
| PIN = "12@#56" (6 mixed) | Excluded | **INCLUDE** | Manual confirms validation fires |

---

# ROOT CAUSE OF ORIGINAL MIS-CLASSIFICATION

The error was:
1. Diagnostic tested DOM value acceptance ≠ server-side validation on submit
2. Assumed behavior from UDISE was projected onto PIN (different fields, different validators)
3. Next-click with 6-char non-numeric was never executed in the diagnostic

**Lesson:** DOM acceptance does NOT equal form acceptance. Always test the full submit flow before excluding scenarios.

---

# UPDATED TEST CASES TO ADD

| TC ID | Title | Test Data | Expected Result |
|-------|-------|-----------|-----------------|
| ADDR_FMT_005 | PIN code with 6 alphabetic characters | zip: "abcdef" | Error: "The zip field must be 6 digits." Form blocked. |
| ADDR_FMT_006 | PIN code with mixed special characters (6 chars) | zip: "12@#56" | Error: "The zip field must be 6 digits." Form blocked. |

---

# UPDATED NEGATIVE (FORMAT) CATEGORY — FINAL

| TC ID | Title | Value | Expected Error |
|-------|-------|-------|----------------|
| ADDR_FMT_001 | PIN code less than 6 digits | "12345" | The zip field must be 6 digits. |
| ADDR_FMT_002 | PIN code more than 6 digits | "1234567" | The zip field must be 6 digits. |
| ADDR_FMT_003 | PIN code with 3 digits only | "123" | The zip field must be 6 digits. |
| ADDR_FMT_004 | Address line blank (cleared) | "" | Address required error |
| ADDR_FMT_005 | PIN code with 6 alphabetic characters | "abcdef" | The zip field must be 6 digits. |
| ADDR_FMT_006 | PIN code with 6 special/mixed characters | "12@#56" | The zip field must be 6 digits. |

**Total Negative tests: 6** (was 4, added 2)

---

# UPDATED TOTAL COUNT

| Category | Previous | Updated |
|----------|----------|---------|
| Validation | 1 | 1 |
| Positive | 3 | 3 |
| Negative (Format) | 4 | **6** |
| Boundary | 3 | 3 |
| **Total** | **11** | **13** |

---

# ALSO APPLICABLE TO UDISE (School Details)

This same logic applies to SCH_NEG_07 and SCH_NEG_08 (UDISE with alphabets/specials). If manual testing confirms the UDISE validation also fires on Next click with 11-character non-numeric values, those tests should also remain included — the automation failure needs to be fixed, not the test excluded.

**Action required:** Run a diagnostic that clicks Next with UDISE = `"abcdefghijk"` (11 chars) while ALL other fields (including dropdowns) are correctly filled. The previous diagnostics had dropdown validation errors masking the UDISE behavior.

---

**STATUS:** Review complete. ADDR_FMT_005 and ADDR_FMT_006 are restored to the matrix.
**Updated total: 13 automatable test cases.**
