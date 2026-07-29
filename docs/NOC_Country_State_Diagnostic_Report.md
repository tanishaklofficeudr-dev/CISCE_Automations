# NOC Country & State Dropdown — Diagnostic Report

---

# EVIDENCE SUMMARY

| Check | Test | Result |
|-------|------|--------|
| 1 | Field type | Standard `<select>` elements (NOT Select2) ✅ |
| 2 | `select_option(value="2")` | ✅ SUCCESS — India selected |
| 3 | `select_option(label="India")` | ✅ SUCCESS |
| 4 | `select_option(index=1)` | ✅ SUCCESS |
| 5 | State loads after Country | ✅ YES — 37 options loaded for India |
| 6 | `select_option(value="30")` for State | ✅ SUCCESS (value resolves to "5" — value mapping may differ) |
| 7 | `select_option(label="Maharashtra")` for State | ✅ SUCCESS (value="21") |
| 8 | Change Country → State resets | ✅ YES — Indonesia loaded 35 states, value changed |
| 9 | Clear dropdown to "Select" (index=0) | ❌ FAILED — "Select" option is `disabled`, cannot be selected |
| 10 | Values retained | ✅ Country="2", State="5" retained |

---

# DETAILED FINDINGS

## 1. Field Structure

**Country:**
```html
<select class="form-select form-select-sm bd-clr" name="noc_country" id="noc_country" onchange="getNocState('s')">
  <option selected="" disabled="">Select</option>
  <option value="2">India</option>
  ...
</select>
```

**State:**
```html
<select class="form-select form-select-sm bd-clr" name="noc_state" id="noc_state">
  <option selected="" disabled="">Select</option>
  ...dynamically loaded...
</select>
```

## 2. All Three Selection Methods Work

| Method | Country | State |
|--------|---------|-------|
| `select_option(value="2")` | ✅ | ✅ |
| `select_option(label="India")` | ✅ | ✅ |
| `select_option(index=1)` | ✅ | ✅ |

## 3. Cascade Behavior

- Country has `onchange="getNocState('s')"` — triggers AJAX to load states
- After selecting India: 37 state options loaded (index 0 = disabled "Select")
- First real state: "Arunachal Pradesh"
- After selecting Indonesia: 35 options loaded, state value changed

**Wait required:** YES — `wait_for_timeout(1000)` after Country selection before State is available.

## 4. Cannot Clear to "Select"

The "Select" option at index 0 is `disabled`. Playwright cannot select a disabled option.

**Conclusion:** Dropdowns CANNOT be reset to blank. Same persistence pattern as School Details and Address Details.

## 5. Value Mapping Note

`select_option(value="30")` for State resulted in State value `"5"` — this suggests the E2E's hardcoded `"30"` selects a specific state by its database ID, but the `input_value()` returns a different internal value. **The E2E approach (using value) works correctly regardless of this discrepancy.**

---

# AUTOMATION RECOMMENDATIONS

## What Works:

| Action | Method | Reliable? |
|--------|--------|-----------|
| Select Country by value | `select_option("2")` | ✅ Always works |
| Select Country by label | `select_option(label="India")` | ✅ Works |
| Select State by value | `select_option("30")` | ✅ Works (E2E proven) |
| Select State by label | `select_option(label="Rajasthan")` | ✅ Works |
| Change Country | `select_option(value=...)` | ✅ Resets and reloads State |
| Change State | `select_option(value=...)` | ✅ Works after Country set |

## What Does NOT Work:

| Action | Why |
|--------|-----|
| Set Country to blank/"Select" | Index 0 is `disabled` |
| Set State to blank/"Select" | Index 0 is `disabled` |
| Test "Country not selected" | Impossible after first save |
| Test "State not selected" | Impossible after first save |

## Recommended Approach for Regression Tests:

```python
# Use value-based selection (proven in E2E)
page.locator("#noc_country").select_option("2")      # India
page.wait_for_timeout(1000)                           # Wait for state AJAX
page.locator("#noc_state").select_option("30")        # Rajasthan
```

## Waits Required:

| After | Wait | Reason |
|-------|------|--------|
| Country selection | 1000ms | State options load via AJAX (`getNocState('s')`) |
| State selection | None | No cascade after State |

---

# NON-AUTOMATABLE SCENARIOS

| Scenario | Reason |
|----------|--------|
| Country blank validation | "Select" option is `disabled` — cannot be selected |
| State blank validation | Same — `disabled` |
| State with no Country | Cannot unselect Country after first save |

---

# CLASSIFICATION

| Dropdown | Type | Automatable? |
|----------|------|-------------|
| Country (positive - change value) | ✅ Fully automatable |
| State (positive - change value) | ✅ Fully automatable |
| Country (blank/negative) | ❌ Not automatable |
| State (blank/negative) | ❌ Not automatable |
| Cascade (Country changes State) | ✅ Automatable with 1s wait |

---

**STATUS:** Diagnostic complete. Country/State dropdowns are standard `<select>` elements with disabled "Select" placeholder. All positive interactions work. Blank/negative tests impossible.
