# UDISE Field Verification Report
## Evidence-Based Findings

---

# DIAGNOSTIC RESULTS

## Finding 1: Input Mask Does NOT Exist

| Method | Input | Value Retained in DOM | Filtered? |
|--------|-------|----------------------|-----------|
| `.fill("abcdefghijk")` | Alphabets | `abcdefghijk` | **NO** |
| `.fill("123@#$456!!")` | Special chars | `123@#$456!!` | **NO** |
| `.press_sequentially("abcdefghijk")` | Alphabets | `abcdefghijk` | **NO** |
| `.press_sequentially("123@#$456!!")` | Special chars | `123@#$456!!` | **NO** |

**Conclusion: The UDISE field has NO input mask.** It accepts any characters. Both `.fill()` and `.press_sequentially()` place the value in the DOM successfully.

**Previous root cause hypothesis was WRONG.** The field does not filter characters.

---

## Finding 2: Validation IS Server-Side (on Click Next)

When UDISE = `"12345"` (5 digits) and Next is clicked:
```
[class*='invalid'] → 'U-DISE number must be 11 digits.'
```

**The validation works — but only for LENGTH, not for character type.**

---

## Finding 3: Field Accepts 11 Non-Numeric Characters Without Error

When UDISE = `"abcdefghijk"` (11 characters of alphabets):
- The field accepts it
- It's 11 characters long
- The validation checks **length only** (must be 11 digits)
- "abcdefghijk" has length 11 → passes the length check → form navigates

**THIS is the real reason SCH_NEG_07 and SCH_NEG_08 fail:**
- The app validates ONLY the length (11 characters)
- It does NOT validate the character type (numeric only)
- So `"abcdefghijk"` (11 chars) passes validation
- And `"123@#$456!!"` (11 chars) passes validation

---

## Finding 4: Exact Validation Text

| Condition | Actual Error Message |
|-----------|---------------------|
| UDISE < 11 chars | `U-DISE number must be 11 digits.` |
| UDISE = 11 non-numeric chars | **NO ERROR** (form navigates) |

---

## Finding 5: Other Validation Messages Discovered

| Selector | Message |
|----------|---------|
| `[class*='invalid']` | `School classification is required.` |
| `[class*='invalid']` | `The school type field is required.` |
| `[class*='invalid']` | `U-DISE number must be 11 digits.` |
| `[class*='invalid']` | `School Category is required.` |

**Important:** The correct CSS selector for errors is `[class*='invalid']:not(input):not(select)` — this confirms the ValidationHelper pattern works.

---

# REVISED ROOT CAUSE

## SCH_NEG_07 & SCH_NEG_08: Application Does NOT Validate Character Type

| Test | Input | Length | App Behavior | Reason |
|------|-------|--------|--------------|--------|
| SCH_NEG_07 | `abcdefghijk` | 11 | ACCEPTS | Length check passes (11 = 11) |
| SCH_NEG_08 | `123@#$456!!` | 11 | ACCEPTS | Length check passes (11 = 11) |

The application only validates: `length == 11`
The application does NOT validate: `all characters are digits`

**This IS an application gap** — the validation message says "must be 11 **digits**" but it only checks the count, not whether they are digits.

---

# REVISED CLASSIFICATION

| Test | Classification | Evidence |
|------|---------------|----------|
| SCH_NEG_07 | **Valid Defect** | App says "must be 11 digits" but accepts 11 alphabets |
| SCH_NEG_08 | **Valid Defect** | App says "must be 11 digits" but accepts 11 special chars |

The validation message explicitly says "digits" — proving the intent is numeric-only. The implementation only checks length.

---

# AUTOMATION FIX REQUIRED

The automation implementation is correct. No code change needed for the fill mechanism.

However, to make these tests **properly detect the defect**, they should:
1. Submit with 11-character non-numeric values
2. Assert that validation SHOULD appear (but doesn't)
3. Mark as **known defects** with `@pytest.mark.xfail` — the tests correctly identify a bug

**OR** change the test to use values that trigger the existing validation:
- Use fewer than 11 characters (e.g., `"abc"` = 3 chars → triggers length error)
- This would test that the validation message appears, which it does

---

# RECOMMENDATION

| Option | Action | Result |
|--------|--------|--------|
| **A** | Keep tests as-is, mark `@pytest.mark.xfail(reason="App defect: validates length but not character type")` | Tests document the bug, don't break suite |
| **B** | Change invalid values to non-11-length strings (e.g., `"abc"` or `"12345"`) to trigger the LENGTH validation that exists | Tests pass by testing what the app actually validates |
| **C** | Keep both: one test for length validation (passes) + one for char-type validation (xfail as defect) | Best coverage |

**Recommended: Option C** — Reclassify the tests:
- SCH_NEG_07 → Change value to `"abcde"` (5 chars, non-numeric AND wrong length) → triggers `"must be 11 digits"` → test passes
- SCH_NEG_08 → Keep `"123@#$456!!"` (11 chars, correct length, wrong type) → mark as xfail defect

---

# ALSO UPDATE: Expected Error Text in Excel

| Test | Current | Correct |
|------|---------|---------|
| All UDISE tests | `Invalid UDISE number` | `U-DISE number must be 11 digits` |

---

**STATUS:** Verification complete with evidence. Awaiting your decision (Option A, B, or C) before implementing.
