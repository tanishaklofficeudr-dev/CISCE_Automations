# NOC Details Module — Test Case Matrix
## Final Regression Suite (Only Automatable Scenarios)

---

# CATEGORY 1: VALIDATION (Required Fields)

| TC ID | Scenario | Test Type | Automation Status | Data Source | Independent | Expected Result |
|-------|----------|-----------|-------------------|-------------|-------------|-----------------|
| NOC_VAL_001 | All mandatory text fields cleared + date cleared → verify all errors | Validation | Automatable | Hardcoded | First-visit only | Form blocked. Errors shown for authority, designation, office address, reference number, and date. |

---

# CATEGORY 2: POSITIVE (Valid Submissions)

| TC ID | Scenario | Test Type | Automation Status | Data Source | Independent | Expected Result |
|-------|----------|-----------|-------------------|-------------|-------------|-----------------|
| NOC_POS_001 | Valid complete NOC — India, Rajasthan, past date | Positive | Automatable | Excel (NOC_Positive) | Yes | Form submits, navigates to Trust/Society Details |
| NOC_POS_002 | Valid NOC with different state (Maharashtra) | Positive | Automatable | Excel (NOC_Positive) | Yes | Form submits successfully with different state |

---

# CATEGORY 3: NEGATIVE (Format Validation)

| TC ID | Scenario | Test Type | Automation Status | Data Source | Independent | Expected Result |
|-------|----------|-----------|-------------------|-------------|-------------|-----------------|
| NOC_FMT_001 | NOC Authority blank (cleared) | Negative | Automatable | Excel (NOC_Negative) | Yes | Error: authority required. Form blocked. |
| NOC_FMT_002 | Designation blank (cleared) | Negative | Automatable | Excel (NOC_Negative) | Yes | Error: designation required. Form blocked. |
| NOC_FMT_003 | Office Address blank (cleared) | Negative | Automatable | Excel (NOC_Negative) | Yes | Error: office address required. Form blocked. |
| NOC_FMT_004 | NOC Reference Number blank (cleared) | Negative | Automatable | Excel (NOC_Negative) | Yes | Error: reference number required. Form blocked. |
| NOC_FMT_005 | Date of NOC cleared (empty via JS) | Negative | Automatable | Excel (NOC_Negative) | Yes | Error: date required. Form blocked. |
| NOC_FMT_006 | Date of NOC set to future date | Negative | Automatable | Excel (NOC_Negative) | Yes | Error: date cannot be future. Form blocked. (If no validation exists, documents gap.) |

---

# CATEGORY 4: BOUNDARY (Field Length Limits)

| TC ID | Scenario | Test Type | Automation Status | Data Source | Independent | Expected Result |
|-------|----------|-----------|-------------------|-------------|-------------|-----------------|
| NOC_BND_001 | Authority — 1 character (minimum) | Boundary | Automatable | Excel (NOC_Boundary) | Yes | Form accepts or shows min-length error |
| NOC_BND_002 | Office Address — 300 characters (long) | Boundary | Automatable | Excel (NOC_Boundary) | Yes | Form accepts or truncates |
| NOC_BND_003 | Reference Number — 50 characters | Boundary | Automatable | Excel (NOC_Boundary) | Yes | Form accepts or shows max-length error |

---

# EXCLUDED SCENARIOS (Non-Automatable)

| Scenario | Reason | Classification |
|----------|--------|---------------|
| Country dropdown blank | "Select" option is `disabled` — cannot select | Persistence constraint |
| State dropdown blank | "Select" option is `disabled` | Persistence constraint |
| Date selected only from calendar (UI interaction) | Covered by E2E; regression uses JS | Covered elsewhere |
| Calendar min/max date enforcement | JS bypasses calendar UI restrictions | UI-only constraint |
| Country/State cascade on fresh account | Cannot unselect after save | First-visit + persistence |

**Total Excluded: 5**

---

# SCENARIO CLASSIFICATION

## First-Visit Only (1):
| TC ID | Reason |
|-------|--------|
| NOC_VAL_001 | Dropdowns + date retain saved values; text fields can be cleared anytime |

## Always Runnable (11):
| TC IDs |
|--------|
| NOC_POS_001, NOC_POS_002, NOC_FMT_001, NOC_FMT_002, NOC_FMT_003, NOC_FMT_004, NOC_FMT_005, NOC_FMT_006, NOC_BND_001, NOC_BND_002, NOC_BND_003 |

---

# DUPLICATE / OVERLAP CHECK

| Check | Result |
|-------|--------|
| Duplicate scenarios? | ✅ None — each TC tests a unique field or value |
| Positive/Boundary overlap? | ✅ None — Positive tests valid full form; Boundary tests single field lengths |
| Impossible Negative tests? | ✅ None — all negative tests clear/overwrite text fields or use JS for date |
| Requires E2E modification? | ✅ None — all additive |

---

# SUMMARY

| Metric | Count |
|--------|-------|
| **Validation tests** | 1 |
| **Positive tests** | 2 |
| **Negative tests** | 6 |
| **Boundary tests** | 3 |
| **Total Automatable** | **12** |
| **Total Excluded** | 5 |
| **Estimated Regression Coverage** | 100% of automatable scope |

---

# MARKERS & EXECUTION

| TC ID | @regression | @sanity | @first_run | @positive | @negative | @boundary |
|-------|-------------|---------|------------|-----------|-----------|-----------|
| NOC_VAL_001 | Yes | Yes | Yes | — | — | — |
| NOC_POS_001 | Yes | Yes | — | Yes | — | — |
| NOC_POS_002 | Yes | — | — | Yes | — | — |
| NOC_FMT_001 | Yes | Yes | — | — | Yes | — |
| NOC_FMT_002 | Yes | — | — | — | Yes | — |
| NOC_FMT_003 | Yes | — | — | — | Yes | — |
| NOC_FMT_004 | Yes | — | — | — | Yes | — |
| NOC_FMT_005 | Yes | Yes | — | — | Yes | — |
| NOC_FMT_006 | Yes | — | — | — | Yes | — |
| NOC_BND_001 | Yes | — | — | — | — | Yes |
| NOC_BND_002 | Yes | — | — | — | — | Yes |
| NOC_BND_003 | Yes | — | — | — | — | Yes |

---

**STATUS:** Test Case Matrix final and verified. Ready for implementation.
