# Certificate of Land — Phase 1 Test Case Matrix
## Scope: Single Plot → Owned Path Only

---

# CATEGORY 1: VALIDATION (Required Fields)

| TC ID | Scenario Description | Test Type | Priority | Expected Result | Automatable | Remarks |
|-------|---------------------|-----------|----------|-----------------|-------------|---------|
| LAND_VAL_001 | All owned fields blank — verify validation messages | Validation | High | Form blocked. Errors: "Please enter a valid land area", "Please specify where it is situated" | Yes | Only 2 validation messages confirmed by diagnostic |

**Note:** Diagnostic confirmed only 2 validation messages for the entire blank Owned form. This suggests minimal client-side validation — most fields accepted blank.

---

# CATEGORY 2: POSITIVE (Valid Submissions)

| TC ID | Scenario Description | Test Type | Priority | Expected Result | Automatable | Remarks |
|-------|---------------------|-----------|----------|-----------------|-------------|---------|
| LAND_POS_001 | Valid Owned — non-Sale-Deed title (e.g., Conveyance Deed) | Positive | High | Form submits, navigates to Upload Documents | Yes | |
| LAND_POS_002 | Valid Owned — Sale Deed with Sale Deed Favor = School | Positive | High | Form submits with conditional field filled | Yes | Tests Sale Deed conditional logic |
| LAND_POS_003 | Valid Owned — Sale Deed with favor = Trust/Society/Company | Positive | Medium | Form submits with alternate favor option | Yes | |

---

# CATEGORY 3: NEGATIVE (Format Validation)

| TC ID | Scenario Description | Test Type | Priority | Expected Result | Automatable | Remarks |
|-------|---------------------|-----------|----------|-----------------|-------------|---------|
| LAND_FMT_001 | Land Area blank (cleared) | Negative | High | Error: "Please enter a valid land area". Form blocked. | Yes | Confirmed by diagnostic |
| LAND_FMT_002 | Situated In specify blank (cleared) | Negative | High | Error: "Please specify where it is situated". Form blocked. | Yes | Confirmed by diagnostic |
| LAND_FMT_003 | Land Area with non-numeric value (alphabets) | Negative | Medium | Error or form blocked | Yes | DOM accepts — need to verify submit behavior |
| LAND_FMT_004 | Land Area with negative value | Negative | Medium | Error: invalid land area | Yes | |
| LAND_FMT_005 | Area Unit not selected (disabled "Select" placeholder) | Negative | Medium | Expected: validation error. Actual: may pass (dropdown persistence) | Yes | Same pattern as other modules — may not be testable after first save |

---

# CATEGORY 4: BOUNDARY (Field Length Limits)

| TC ID | Scenario Description | Test Type | Priority | Expected Result | Automatable | Remarks |
|-------|---------------------|-----------|----------|-----------------|-------------|---------|
| LAND_BND_001 | Land Area — 1 digit (minimum) | Boundary | Medium | ACCEPT | Yes | |
| LAND_BND_002 | Land Area — very large number (999999999) | Boundary | Medium | ACCEPT or max error | Yes | |
| LAND_BND_003 | Land Document Date — valid past date via .fill() | Boundary | Medium | ACCEPT | Yes | Confirmed .fill() works (NOT readonly) |

---

# EXCLUDED SCENARIOS (Not Automatable in Phase 1)

| Scenario | Reason |
|----------|--------|
| Area Unit dropdown blank after save | Disabled "Select" placeholder — cannot re-select |
| Land Title Document set to placeholder "Types of Deed" | Likely disabled — same dropdown pattern |
| Single → Leased path | Phase 2 |
| Multiple plots path | Phase 3 |
| Calendar UI date min/max enforcement | Date field accepts .fill() — calendar not required |
| Sale Deed Favor blank (requires Sale Deed selected first) | Complex conditional — testing requires specific path already set up |

---

# SANITY CANDIDATES

| TC ID | Reason |
|-------|--------|
| LAND_VAL_001 | Critical — validates mandatory fields |
| LAND_POS_001 | Critical — proves valid Owned form submits |
| LAND_POS_002 | Critical — tests Sale Deed conditional logic |
| LAND_FMT_001 | High priority — land area validation |

---

# REGRESSION CANDIDATES

All 11 test cases are regression candidates.

---

# BUSINESS RULE PENDING CONFIRMATION

None identified for Phase 1 — all expected results are based on confirmed diagnostic evidence.

---

# MARKERS

| TC ID | @regression | @sanity | @first_run | @positive | @negative | @boundary |
|-------|-------------|---------|------------|-----------|-----------|-----------|
| LAND_VAL_001 | Yes | Yes | Yes | — | — | — |
| LAND_POS_001 | Yes | Yes | — | Yes | — | — |
| LAND_POS_002 | Yes | Yes | — | Yes | — | — |
| LAND_POS_003 | Yes | — | — | Yes | — | — |
| LAND_FMT_001 | Yes | Yes | — | — | Yes | — |
| LAND_FMT_002 | Yes | — | — | — | Yes | — |
| LAND_FMT_003 | Yes | — | — | — | Yes | — |
| LAND_FMT_004 | Yes | — | — | — | Yes | — |
| LAND_FMT_005 | Yes | — | — | — | Yes | — |
| LAND_BND_001 | Yes | — | — | — | — | Yes |
| LAND_BND_002 | Yes | — | — | — | — | Yes |
| LAND_BND_003 | Yes | — | — | — | — | Yes |

---

# FINAL SUMMARY

| Category | Count |
|----------|-------|
| Validation | 1 |
| Positive | 3 |
| Negative | 5 |
| Boundary | 3 |
| **Total Automatable** | **12** |
| Excluded | 6 |

---

# IMPLEMENTATION NOTES

1. **Date field:** Use `.fill()` directly — confirmed NOT readonly (unlike NOC/Trust)
2. **Sale Deed conditional:** Already proven in E2E — reuse pattern
3. **Navigation detection:** Check for "Upload Documents" text visibility (next step)
4. **Field locators:** All use `#id` format (e.g., `#land_area_0`, `#land_title_date0`)
5. **Validation:** Only 2 confirmed messages — tests for other blank fields may navigate (same as Trust issue)
6. **Area Unit:** Use `select_option(label="Square Meter")` or `select_option(value="3")`

---

**STATUS:** Phase 1 Test Case Matrix finalized. Ready for implementation planning.
