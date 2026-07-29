# Certificate of Land — Date Field Diagnostic Report
## "Date of Land Title Document" (#land_title_date0)

---

# ROOT CAUSE IDENTIFIED

**The field IS `readonly="readonly"` — identical to NOC and Trust date fields.**

The initial diagnostic report incorrectly stated the field was NOT readonly. This was a diagnostic error. The field has `readonly` attribute set, which means:
- `.fill()` **FAILS** (Playwright refuses to fill readonly elements)
- `.type()` **FAILS** (characters not inserted — value stays empty)
- `.press_sequentially()` **FAILS** (same — readonly blocks keyboard input)
- **Only JavaScript injection works**

---

# EVIDENCE SUMMARY

| # | Question | Answer | Evidence |
|---|----------|--------|----------|
| 1 | Is the locator correct? | ✅ Yes | `.last` resolves to `id='land_title_date0'` |
| 2 | How many "Select a date" textboxes? | **1 visible** (7 total in DOM, 6 hidden) | Only `#land_title_date0` is visible on Owned form |
| 3 | Which one is the Land Title Date? | `#land_title_date0` | Confirmed by ID and visibility |
| 4 | Is the field visible and enabled? | ✅ visible=True, enabled=True | But **readonly=True** |
| 5 | Is another element covering it? | ❌ No | `elementFromPoint()` returns the input itself |
| 6 | Becomes editable after other field? | ❌ No | `readonly=True` before AND after filling other fields |
| 7 | Requires clicking elsewhere first? | ❌ No | Click opens a **Bootstrap datepicker** overlay |
| 8 | Does `.fill()` fail? | ✅ **FAILS** | "element is not editable" — 30s timeout |
| 9 | Does `.type()` work? | ❌ **FAILS** | Characters typed but value stays empty |
| 10 | Does `.press_sequentially()` work? | ❌ **FAILS** | Same — value stays empty |
| 11 | Does JavaScript injection work? | ✅ **YES** | Both `el.value =` and `nativeInputValueSetter` succeed |
| 12 | Does app accept JS-injected value? | ✅ **YES** | Form navigates successfully after Next click |
| 13 | Compare with E2E implementation | **E2E is WRONG for regression** | E2E uses `.fill()` which would also fail in isolation |

---

# FIELD PROPERTIES (ACTUAL)

```
id:          land_title_date0
name:        land_title_date[]
type:        text
placeholder: Select a date
readonly:    TRUE ← THIS IS THE PROBLEM
disabled:    false
class:       form-control form-control-sm bd-clr datepicker date-picker
visible:     true
enabled:     true
value:       (empty)
```

---

# DATEPICKER BEHAVIOR

| Action | Result |
|--------|--------|
| Click on field | Opens **Bootstrap datepicker** (`.datepicker.datepicker-dropdown`) |
| Type characters | Nothing happens (readonly blocks input) |
| `.fill()` | Playwright timeout — "element is not editable" |
| JavaScript injection | Value is set, app accepts it |

The field has class `datepicker date-picker` and is configured as a Bootstrap datepicker with `readonly` so users must pick from the calendar — they cannot type.

---

# WHY THE E2E WORKS (Hypothesis)

The E2E `fill_land_details()` also uses:
```python
self.page.get_by_role("textbox", name="Select a date").last.click()
self.page.get_by_role("textbox", name="Select a date").last.fill(data["land_document_date"])
```

**This SHOULD also fail.** Possible explanations:
1. The E2E runs in a context where a previous step already set date data (account already has saved data)
2. The field state differs after the full E2E flow (other interactions may change readonly state)
3. The E2E test may have passed historically with a calendar-click approach that was later changed
4. **Most likely:** The field retains a previously saved date, so the E2E "fill" silently fails but the test passes because the server has the old date stored

---

# CONFIRMED WORKING APPROACH

**Use `ValidationHelper.set_readonly_date()` — same as NOC and Trust dates.**

```python
ValidationHelper.set_readonly_date(page, '#land_title_date0', '15/03/2020')
```

This uses `nativeInputValueSetter` + event dispatch. Confirmed:
- Value is set: `'15/03/2020'` ✅
- App accepts it: Form navigates on Next ✅

---

# CORRECTION TO INITIAL DIAGNOSTIC

| Original Finding | Actual Finding |
|-----------------|----------------|
| "Date field is NOT readonly" | **WRONG** — field IS `readonly="readonly"` |
| ".fill() WORKS" | **WRONG** — `.fill()` fails with timeout |
| "No JS injection needed" | **WRONG** — JS injection is required |

The initial diagnostic likely tested a different field or tested on an account where the field already had saved data.

---

# RECOMMENDATION

Replace all direct `.fill()` / `.click()` calls for `#land_title_date0` with:
```python
ValidationHelper.set_readonly_date(page, '#land_title_date0', date_value)
```

This is the same pattern used for:
- NOC date: `#noc_date[name='noc_date']`
- Trust establishment date: `#establishment_date`
- Trust registration date: `#registration_date`

---

# IMPACT ON IMPLEMENTATION

| Method | Change Needed |
|--------|---------------|
| `fill_document_date()` | Use `ValidationHelper.set_readonly_date()` |
| `fill_partial_owned_details()` (Step 13) | Use `ValidationHelper.set_readonly_date()` |
| `test_land_required_fields.py` (clear date) | Use `set_readonly_date(page, '#land_title_date0', '')` |
| `test_land_negative.py` (baseline date) | Use `set_readonly_date()` |
| `test_land_boundary.py` (baseline + boundary date) | Use `set_readonly_date()` |

---

**STATUS:** Root cause identified. Fix is clear — use existing `ValidationHelper.set_readonly_date()` pattern.
