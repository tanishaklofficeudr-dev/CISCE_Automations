# Certificate of Land — Complete Regression Test Matrix
## Comprehensive QA Analysis & Test Case Repository

---

# 1. COMPLETE DECISION TREE

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     CERTIFICATE OF LAND MODULE                                │
│                     "Are the Plots?"                                          │
├──────────────────────────────┬───────────────────────────────────────────────┤
│     ○ SINGLE                 │     ○ MULTIPLE                                │
└──────────────┬───────────────┴────────────────────────┬──────────────────────┘
               │                                         │
    ┌──────────▼──────────┐                    ┌────────▼─────────────────────┐
    │  Owner's Details     │                    │  Number of Plots             │
    │  (Plot 1)            │                    │  On which plot building?     │
    │  ○ Owned  ○ Leased   │                    │  Are plots contiguous?       │
    └────┬────────────┬────┘                    │  ○ Yes  ○ No                 │
         │            │                         └────┬──────────────────┬──────┘
    ┌────▼──────┐  ┌──▼──────────┐                   │                  │
    │  OWNED    │  │  LEASED     │              ┌────▼────┐        ┌───▼──────────────┐
    │  FIELDS   │  │  FIELDS     │              │ Yes     │        │ No               │
    └────┬──────┘  └──┬──────────┘              │ (done)  │        │ Single boundary? │
         │            │                         └─────────┘        │ ○ Yes  ○ No      │
         │            │                                            └───┬──────────┬───┘
    ┌────▼───────────────────┐  ┌──────────────────────────┐           │          │
    │ Land Title Document    │  │ Renewal clause?           │     ┌────▼───┐  ┌──▼──────────┐
    │ ┌─────────────────┐    │  │ ○ Yes  ○ No              │     │ Yes    │  │ No           │
    │ │Sale Deed → FAVOR│    │  └────┬─────────────┬───────┘     │ (done) │  │ Explanation  │
    │ │Lease Deed       │    │       │             │             └────────┘  │ (textarea)   │
    │ │Conveyance Deed  │    │  ┌────▼───────┐  ┌─▼─────────┐               └──────────────┘
    │ │Gift Deed        │    │  │ Duration   │  │ (done)    │
    │ │Other Deeds      │    │  │ of Renewal │  └───────────┘
    │ └─────────────────┘    │  └────────────┘
    └────────────────────────┘
```

---

# 2. CORRECTED FIELD INVENTORY (Evidence-Based)

## 2.1 Common Fields (All Paths)
- Plot Type Radio: Single / Multiple

## 2.2 Single → Owned Path (13 fields)

| # | Field | ID | Type | Readonly | Mandatory | Confirmed Validation |
|---|-------|-----|------|----------|-----------|---------------------|
| 1 | Area Unit | `#land_unit_0` | `<select>` | No | Yes | None confirmed |
| 2 | Land Area | `#land_area_0` | text input | No | Yes | "Please enter a valid land area" |
| 3 | Situated In (dropdown) | `#situated_in_0` | `<select>` | No | Unknown | None confirmed |
| 4 | Situated In (specify) | `#situate_speci_0` | text input | No | Yes | "Please specify where it is situated" |
| 5 | Situated At | `#situated_at0` | text input | No | Unknown | None confirmed |
| 6 | Land Owned By | `#owned_by_0` | text input | No | Unknown | None confirmed |
| 7 | Land Title Document | `#land_title_doc0` | `<select>` | No | Unknown | None confirmed |
| 8 | Sale Deed Favor | `#sale_deed_favor_whom_0` | `<select>` | No | Conditional | Only if Title="Sale Deed" |
| 9 | Registration Details | `#land_title0` | text input | No | Unknown | None confirmed |
| 10 | Executed By | `#executed_by0` | text input | No | Unknown | None confirmed |
| 11 | Registration Office | `#regid_ofc_details0` | text input | No | Unknown | None confirmed |
| 12 | Land Document Date | `#land_title_date0` | text (readonly) | **YES** | Unknown | None confirmed |

## 2.3 Single → Leased Path (10 fields)

| # | Field | ID | Type | Readonly | Mandatory |
|---|-------|-----|------|----------|-----------|
| 1 | Lease Area Unit | `#lease_area_unit_0` | `<select>` | No | Yes |
| 2 | Lease Land Area | `#lease_land_area_0` | text input | No | Yes |
| 3 | Name of Lessee | `#leease_name_0` | text input | No | Yes |
| 4 | Name of Lessor | `#leaser_name_0` | text input | No | Yes |
| 5 | Date of Lease Deed | `#lease_deed_date_0` | text (likely readonly) | TBD | Yes |
| 6 | Duration of Lease Deed | `#lease_deed_duration_0` | text input | No | Yes |
| 7 | Date of Registration | `#date_regis_lease_deed0` | text (likely readonly) | TBD | Yes |
| 8 | Registration Office | TBD | text input | No | Yes |
| 9 | Renewal Clause | `#renewal_yes` / `#renewal_no` | radio | No | Yes |
| 10 | Duration of Renewal | TBD | text input | No | Conditional (Yes) |

## 2.4 Multiple Plot Path (5 fields)

| # | Field | ID | Type | Mandatory | Condition |
|---|-------|-----|------|-----------|-----------|
| 1 | Number of Plots | `#no_of_plots` | text/number | Yes | Always |
| 2 | Plot Number (building) | `#plot_number_school_building` | number | Yes | Always |
| 3 | Contiguous? | `#renewal_yes` / `#renewal_no` | radio | Yes | Always |
| 4 | Single Boundary? | TBD | radio | Conditional | contiguous=No |
| 5 | Explanation | TBD | textarea | Conditional | boundary=No |

---

# 3. DROPDOWN OPTIONS (Confirmed)

## Area Unit (`#land_unit_0`)
| Value | Label | Disabled |
|-------|-------|----------|
| (empty) | Select | Yes |
| 1 | Square Foot | No |
| 2 | Square Yard | No |
| 3 | Square Meter | No |
| 4 | Square Acre | No |
| 5 | Square Hectare | No |

## Land Title Document (`#land_title_doc0`)
| Value | Label |
|-------|-------|
| Types of Deed | Types of Deed (placeholder) |
| 1 | Sale Deed |
| 2 | Lease Deed |
| 3 | Conveyance Deed |
| 4 | Gift Deed |
| 5 | Other Deeds |

## Sale Deed Favor (`#sale_deed_favor_whom_0`)
| Value | Label |
|-------|-------|
| (empty) | Type of Sale Deed (placeholder) |
| 1 | School |
| 2 | Trust/Society/Company |

---

# 4. COMPLETE TEST CASE MATRIX

---

## SECTION A: VALIDATION TESTS (Required Field Checks)

| TC ID | Flow | Scenario Description | Priority | Expected Result | Automatable |
|-------|------|---------------------|----------|-----------------|-------------|
| LAND_VAL_001 | Single→Owned | All Owned fields blank — verify validation messages | Critical | "Please enter a valid land area" + "Please specify where it is situated" | Yes |
| LAND_VAL_002 | Single→Leased | All Leased fields blank — verify validation messages | Critical | Form blocked with error messages | Yes (needs diagnostic) |
| LAND_VAL_003 | Multiple | Multiple path — Number of Plots blank | High | Validation error | Yes (needs diagnostic) |
| LAND_VAL_004 | Multiple | Multiple path — Plot Number blank | High | Validation error | Yes (needs diagnostic) |

---

## SECTION B: POSITIVE TESTS (Valid Submissions)

### B1: Single → Owned — Positive

| TC ID | Scenario Description | Key Data | Priority | Expected Result | Automatable |
|-------|---------------------|----------|----------|-----------------|-------------|
| LAND_POS_001 | Valid Owned — Conveyance Deed | Area=5000, Title=Conveyance | Critical | Navigates to Upload Documents | Yes |
| LAND_POS_002 | Valid Owned — Sale Deed, favor=School | Title=Sale Deed, Favor=School | Critical | Navigates with conditional field | Yes |
| LAND_POS_003 | Valid Owned — Sale Deed, favor=Trust/Society | Title=Sale Deed, Favor=Trust | High | Navigates with alternate favor | Yes |
| LAND_POS_004 | Valid Owned — Gift Deed | Title=Gift Deed | Medium | Navigates (no conditional field) | Yes |
| LAND_POS_005 | Valid Owned — Other Deeds | Title=Other Deeds | Medium | Navigates (no conditional field) | Yes |
| LAND_POS_006 | Valid Owned — Lease Deed (as title option) | Title=Lease Deed | Medium | Navigates (no conditional field) | Yes |
| LAND_POS_007 | Valid Owned — Area Unit = Square Foot | unit=Square Foot | Medium | Accepted | Yes |
| LAND_POS_008 | Valid Owned — Area Unit = Square Yard | unit=Square Yard | Medium | Accepted | Yes |
| LAND_POS_009 | Valid Owned — Area Unit = Square Acre | unit=Square Acre | Low | Accepted | Yes |
| LAND_POS_010 | Valid Owned — Area Unit = Square Hectare | unit=Square Hectare | Low | Accepted | Yes |

### B2: Single → Leased — Positive

| TC ID | Scenario Description | Key Data | Priority | Expected Result | Automatable |
|-------|---------------------|----------|----------|-----------------|-------------|
| LAND_POS_011 | Valid Leased — Renewal=No | All lease fields valid, Renewal=No | Critical | Navigates to next step | Yes (needs diagnostic) |
| LAND_POS_012 | Valid Leased — Renewal=Yes with Duration | All fields + Duration of Renewal | Critical | Navigates with conditional field | Yes (needs diagnostic) |
| LAND_POS_013 | Valid Leased — All area units | unit=Square Meter | Medium | Accepted | Yes (needs diagnostic) |

### B3: Multiple Plot — Positive

| TC ID | Scenario Description | Key Data | Priority | Expected Result | Automatable |
|-------|---------------------|----------|----------|-----------------|-------------|
| LAND_POS_014 | Multiple — Contiguous=Yes | 2 plots, contiguous=Yes | Critical | Navigates | Yes (needs diagnostic) |
| LAND_POS_015 | Multiple — Contiguous=No, Boundary=Yes | 3 plots, contiguous=No, boundary=Yes | High | Navigates | Yes (needs diagnostic) |
| LAND_POS_016 | Multiple — Contiguous=No, Boundary=No, Explanation filled | Full nested path | High | Navigates with explanation | Yes (needs diagnostic) |

---

## SECTION C: NEGATIVE TESTS (Invalid Input / Blank Fields)

### C1: Single → Owned — Negative

| TC ID | Field | Value | Priority | Expected Result | Automatable | Remarks |
|-------|-------|-------|----------|-----------------|-------------|---------|
| LAND_NEG_001 | land_area | (blank) | Critical | "Please enter a valid land area" | Yes | Confirmed by diagnostic |
| LAND_NEG_002 | situated_in | (blank) | Critical | "Please specify where it is situated" | Yes | Confirmed by diagnostic |
| LAND_NEG_003 | land_area | abcdef | High | "Please enter a valid land area" or DOM blocks | Yes | |
| LAND_NEG_004 | land_area | -500 | High | "Please enter a valid land area" | Yes | |
| LAND_NEG_005 | land_area | 0 | Medium | Validation error or accept | Yes | Business Rule Pending |
| LAND_NEG_006 | land_area | 12.34.56 (invalid decimal) | Medium | Validation error | Yes | |
| LAND_NEG_007 | land_area | (spaces only) | Medium | Validation error | Yes | |
| LAND_NEG_008 | situated_in | (spaces only) | Medium | Validation error or accept | Yes | Business Rule Pending |
| LAND_NEG_009 | situated_at | (blank) | Medium | Form may accept (not confirmed mandatory) | Yes | Business Rule Pending |
| LAND_NEG_010 | land_owned_by | (blank) | Medium | Form may accept (not confirmed mandatory) | Yes | Business Rule Pending |
| LAND_NEG_011 | registration_details | (blank) | Medium | Form may accept | Yes | Business Rule Pending |
| LAND_NEG_012 | executed_by | (blank) | Medium | Form may accept | Yes | Business Rule Pending |
| LAND_NEG_013 | registration_office | (blank) | Medium | Form may accept | Yes | Business Rule Pending |
| LAND_NEG_014 | document_date | (blank/cleared) | Medium | Form may accept | Yes | Business Rule Pending |
| LAND_NEG_015 | document_date | Future date | Medium | Should reject — Business Rule Pending | Yes | May be app defect |
| LAND_NEG_016 | area_unit | Disabled "Select" placeholder | Medium | May not be testable after first save | Conditional | Dropdown persistence issue |
| LAND_NEG_017 | sale_deed_favor | (blank when Sale Deed selected) | High | Should block | Yes | Conditional field mandatory check |
| LAND_NEG_018 | land_area | Special chars (!@#$%^&*) | Low | Validation error or DOM blocks | Yes | |
| LAND_NEG_019 | situated_in | Only numbers (12345) | Low | May accept | Yes | Business Rule Pending |
| LAND_NEG_020 | land_owned_by | Only special chars | Low | May accept | Yes | Business Rule Pending |

### C2: Single → Leased — Negative

| TC ID | Field | Value | Priority | Expected Result | Automatable | Remarks |
|-------|-------|-------|----------|-----------------|-------------|---------|
| LAND_NEG_021 | lease_land_area | (blank) | Critical | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_022 | lease_land_area | Alphabets | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_023 | lease_land_area | Negative value | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_024 | lessee_name | (blank) | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_025 | lessor_name | (blank) | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_026 | lease_deed_date | (blank) | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_027 | lease_deed_date | Future date | Medium | Should reject | Yes (needs diagnostic) | Business Rule Pending |
| LAND_NEG_028 | lease_deed_duration | (blank) | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_029 | lease_deed_duration | Negative | Medium | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_030 | lease_deed_duration | Alphabets | Medium | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_031 | registration_date_lease | (blank) | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_032 | registration_date_lease | Future date | Medium | Should reject | Yes (needs diagnostic) | Business Rule Pending |
| LAND_NEG_033 | renewal_duration | (blank when Renewal=Yes) | High | Should block | Yes (needs diagnostic) | Conditional mandatory |
| LAND_NEG_034 | renewal_duration | Negative value | Medium | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_035 | renewal_duration | Alphabets | Medium | Validation error | Yes (needs diagnostic) | |

### C3: Multiple Plot — Negative

| TC ID | Field | Value | Priority | Expected Result | Automatable | Remarks |
|-------|-------|-------|----------|-----------------|-------------|---------|
| LAND_NEG_036 | no_of_plots | (blank) | Critical | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_037 | no_of_plots | 0 | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_038 | no_of_plots | -1 | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_039 | no_of_plots | Alphabets | Medium | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_040 | no_of_plots | Decimal (2.5) | Medium | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_041 | plot_number_building | (blank) | High | Validation error | Yes (needs diagnostic) | |
| LAND_NEG_042 | plot_number_building | Greater than total plots | Medium | Should reject | Yes (needs diagnostic) | Business Rule Pending |
| LAND_NEG_043 | explanation | (blank when required) | High | Should block | Yes (needs diagnostic) | Conditional mandatory |
| LAND_NEG_044 | explanation | Spaces only | Medium | May accept | Yes (needs diagnostic) | Business Rule Pending |

---

## SECTION D: BOUNDARY TESTS (Min/Max Limits)

### D1: Single → Owned — Boundary

| TC ID | Field | Value | Expected Outcome | Priority | Automatable |
|-------|-------|-------|------------------|----------|-------------|
| LAND_BND_001 | land_area | 1 (minimum) | ACCEPT | Medium | Yes |
| LAND_BND_002 | land_area | 999999999 (large) | ACCEPT or REJECT | Medium | Yes |
| LAND_BND_003 | land_area | 0.01 (smallest decimal) | ACCEPT or REJECT | Medium | Yes |
| LAND_BND_004 | land_area | 99999999999999 (15 digits) | ACCEPT or truncated | Low | Yes |
| LAND_BND_005 | situated_in | 1 character | ACCEPT | Low | Yes |
| LAND_BND_006 | situated_in | 500 characters (very long) | ACCEPT or truncated | Low | Yes |
| LAND_BND_007 | situated_at | 1 character | ACCEPT | Low | Yes |
| LAND_BND_008 | situated_at | 500 characters | ACCEPT or truncated | Low | Yes |
| LAND_BND_009 | land_owned_by | 1 character | ACCEPT | Low | Yes |
| LAND_BND_010 | land_owned_by | 200 characters | ACCEPT or truncated | Low | Yes |
| LAND_BND_011 | registration_details | 1 character | ACCEPT | Low | Yes |
| LAND_BND_012 | registration_details | 500 characters | ACCEPT or truncated | Low | Yes |
| LAND_BND_013 | executed_by | 1 character | ACCEPT | Low | Yes |
| LAND_BND_014 | executed_by | 200 characters | ACCEPT or truncated | Low | Yes |
| LAND_BND_015 | registration_office | 1 character | ACCEPT | Low | Yes |
| LAND_BND_016 | registration_office | 500 characters | ACCEPT or truncated | Low | Yes |
| LAND_BND_017 | document_date | Today's date | ACCEPT or REJECT | Medium | Yes |
| LAND_BND_018 | document_date | Very old date (01/01/1900) | ACCEPT | Low | Yes |
| LAND_BND_019 | document_date | Yesterday | ACCEPT | Medium | Yes |

### D2: Single → Leased — Boundary

| TC ID | Field | Value | Expected Outcome | Priority | Automatable |
|-------|-------|-------|------------------|----------|-------------|
| LAND_BND_020 | lease_land_area | 1 (minimum) | ACCEPT | Medium | Yes (needs diagnostic) |
| LAND_BND_021 | lease_land_area | 999999999 | ACCEPT or REJECT | Medium | Yes (needs diagnostic) |
| LAND_BND_022 | lease_deed_duration | 1 (minimum) | ACCEPT | Medium | Yes (needs diagnostic) |
| LAND_BND_023 | lease_deed_duration | 99 (years) | ACCEPT | Medium | Yes (needs diagnostic) |
| LAND_BND_024 | lease_deed_duration | 999 | ACCEPT or REJECT | Low | Yes (needs diagnostic) |
| LAND_BND_025 | renewal_duration | 1 (minimum) | ACCEPT | Medium | Yes (needs diagnostic) |
| LAND_BND_026 | renewal_duration | 99 | ACCEPT | Low | Yes (needs diagnostic) |
| LAND_BND_027 | lessee_name | 1 character | ACCEPT | Low | Yes (needs diagnostic) |
| LAND_BND_028 | lessee_name | 200 characters | ACCEPT or truncated | Low | Yes (needs diagnostic) |

### D3: Multiple Plot — Boundary

| TC ID | Field | Value | Expected Outcome | Priority | Automatable |
|-------|-------|-------|------------------|----------|-------------|
| LAND_BND_029 | no_of_plots | 2 (minimum for multiple) | ACCEPT | High | Yes (needs diagnostic) |
| LAND_BND_030 | no_of_plots | 100 (large) | ACCEPT or REJECT | Medium | Yes (needs diagnostic) |
| LAND_BND_031 | no_of_plots | 1 | Business Rule — should this be allowed? | Medium | Yes (needs diagnostic) |
| LAND_BND_032 | plot_number_building | 1 (minimum) | ACCEPT | Medium | Yes (needs diagnostic) |
| LAND_BND_033 | plot_number_building | = total plots (maximum valid) | ACCEPT | Medium | Yes (needs diagnostic) |
| LAND_BND_034 | explanation | 1 character | ACCEPT | Low | Yes (needs diagnostic) |
| LAND_BND_035 | explanation | 2000 characters | ACCEPT or truncated | Low | Yes (needs diagnostic) |

---

## SECTION E: DYNAMIC UI BEHAVIOUR TESTS

| TC ID | Scenario | Action | Expected UI Behaviour | Priority | Automatable |
|-------|----------|--------|----------------------|----------|-------------|
| LAND_UI_001 | Single→Owned form appears | Select Single + Owned | All Owned fields visible | Critical | Yes |
| LAND_UI_002 | Single→Leased form appears | Select Single + Leased | Leased fields visible, Owned fields hidden | Critical | Yes (needs diagnostic) |
| LAND_UI_003 | Multiple form appears | Select Multiple | Multiple fields visible, Single hidden | Critical | Yes (needs diagnostic) |
| LAND_UI_004 | Switch Single→Multiple | Select Single, fill data, switch to Multiple | Owned/Leased form hides, Multiple fields appear | High | Yes |
| LAND_UI_005 | Switch Multiple→Single | Select Multiple, fill data, switch to Single | Multiple fields hide, Single form appears | High | Yes |
| LAND_UI_006 | Switch Owned→Leased | Select Owned, fill, switch to Leased | Owned fields hide, Leased fields appear | High | Yes (needs diagnostic) |
| LAND_UI_007 | Switch Leased→Owned | Select Leased, fill, switch to Owned | Leased fields hide, Owned fields appear | High | Yes (needs diagnostic) |
| LAND_UI_008 | Sale Deed conditional appears | Select Title="Sale Deed" | Sale Deed Favor dropdown becomes visible | High | Yes |
| LAND_UI_009 | Sale Deed conditional disappears | Change Title from Sale Deed to Conveyance | Sale Deed Favor field hides | High | Yes |
| LAND_UI_010 | Renewal=Yes shows duration | Select Renewal=Yes | Duration of Renewal field appears | High | Yes (needs diagnostic) |
| LAND_UI_011 | Renewal=No hides duration | Switch Renewal from Yes to No | Duration field disappears | High | Yes (needs diagnostic) |
| LAND_UI_012 | Contiguous=No shows boundary question | Select Contiguous=No | "Single boundary?" radios appear | High | Yes (needs diagnostic) |
| LAND_UI_013 | Contiguous=Yes hides boundary question | Switch Contiguous from No to Yes | Boundary question hides | High | Yes (needs diagnostic) |
| LAND_UI_014 | Boundary=No shows explanation | Select Boundary=No | Explanation textarea appears | High | Yes (needs diagnostic) |
| LAND_UI_015 | Boundary=Yes hides explanation | Switch Boundary from No to Yes | Explanation textarea hides | High | Yes (needs diagnostic) |
| LAND_UI_016 | Form fields load after radio wait | Select Single radio | 2000ms wait → fields visible | Medium | Yes |
| LAND_UI_017 | Owned/Leased load after radio wait | Select Owned/Leased | 1000ms wait → section fields visible | Medium | Yes |

---

## SECTION F: CROSS-FIELD DEPENDENCY TESTS

| TC ID | Dependency | Test Scenario | Priority | Expected Result | Automatable | Remarks |
|-------|-----------|---------------|----------|-----------------|-------------|---------|
| LAND_DEP_001 | Sale Deed → Favor mandatory | Select Sale Deed, leave Favor blank, submit | Critical | Form blocked — Favor is required | Yes | Business Rule Pending |
| LAND_DEP_002 | Renewal=Yes → Duration mandatory | Select Yes, leave duration blank, submit | Critical | Form blocked | Yes (needs diagnostic) | |
| LAND_DEP_003 | Contiguous=No + Boundary=No → Explanation mandatory | Full nested path, leave explanation blank | High | Form blocked | Yes (needs diagnostic) | |
| LAND_DEP_004 | Hidden fields not submitted | Fill Owned data, switch to Leased, submit | High | Owned data not retained/submitted | Yes | |
| LAND_DEP_005 | Hidden fields not submitted | Fill Multiple data, switch to Single, submit | High | Multiple data not retained/submitted | Yes | |
| LAND_DEP_006 | Sale Deed Favor value reset | Select Sale Deed + fill Favor, change to Gift Deed | Medium | Favor field hides, value should not persist | Yes | |
| LAND_DEP_007 | Renewal Duration reset | Select Yes + fill duration, switch to No | Medium | Duration hides, value should not persist | Yes (needs diagnostic) | |
| LAND_DEP_008 | Explanation reset | Select No + fill explanation, switch boundary to Yes | Medium | Explanation hides, value should not persist | Yes (needs diagnostic) | |
| LAND_DEP_009 | Plot Number ≤ Number of Plots | Enter 3 plots, building on plot 5 | Medium | Should reject (plot > total) | Yes (needs diagnostic) | Business Rule Pending |
| LAND_DEP_010 | Area Unit + Land Area relationship | Verify any unit works with any area value | Low | All combinations accepted | Yes | |

---

## SECTION G: FIELD BEHAVIOUR TESTS (Per-Field Deep Coverage)

### G1: Land Area Field (#land_area_0)

| TC ID | Input | Expected | Priority | Automatable |
|-------|-------|----------|----------|-------------|
| LAND_FLD_001 | Blank | Error: "Please enter a valid land area" | Critical | Yes |
| LAND_FLD_002 | 5000 | Accepted | High | Yes |
| LAND_FLD_003 | abcdef | Error or DOM blocks | High | Yes |
| LAND_FLD_004 | -500 | Error | High | Yes |
| LAND_FLD_005 | 0 | Business Rule Pending | Medium | Yes |
| LAND_FLD_006 | 0.5 | Accepted (decimal) | Medium | Yes |
| LAND_FLD_007 | !@#$%^&* | Error or DOM blocks | Low | Yes |
| LAND_FLD_008 | "   " (spaces only) | Error | Medium | Yes |
| LAND_FLD_009 | " 500 " (leading/trailing spaces) | Accepted (trimmed) or Error | Low | Yes |
| LAND_FLD_010 | 1 | Minimum accepted | Medium | Yes |
| LAND_FLD_011 | 999999999 | Large value accepted | Medium | Yes |

### G2: Situated In (#situate_speci_0)

| TC ID | Input | Expected | Priority | Automatable |
|-------|-------|----------|----------|-------------|
| LAND_FLD_012 | Blank | Error: "Please specify where it is situated" | Critical | Yes |
| LAND_FLD_013 | "Survey No(s)" | Accepted | High | Yes |
| LAND_FLD_014 | "   " (spaces only) | Error or Accept | Medium | Yes |
| LAND_FLD_015 | 1 character | Accepted | Low | Yes |
| LAND_FLD_016 | 500 characters | Accepted or truncated | Low | Yes |

### G3: Document Date (#land_title_date0 — READONLY)

| TC ID | Input | Expected | Priority | Automatable |
|-------|-------|----------|----------|-------------|
| LAND_FLD_017 | Blank (cleared via JS) | May accept or error | Medium | Yes |
| LAND_FLD_018 | "15/03/2020" (valid past) | Accepted | High | Yes |
| LAND_FLD_019 | Future date (tomorrow) | Business Rule Pending — may accept | Medium | Yes |
| LAND_FLD_020 | "01/01/1900" (very old) | Accepted | Low | Yes |
| LAND_FLD_021 | Today's date | Accepted or rejected at boundary | Medium | Yes |
| LAND_FLD_022 | Invalid format "2020-03-15" | JS injection — app behaviour TBD | Low | Yes |

### G4: Area Unit Dropdown (#land_unit_0)

| TC ID | Option | Expected | Priority | Automatable |
|-------|--------|----------|----------|-------------|
| LAND_FLD_023 | Square Foot | Accepted | Medium | Yes |
| LAND_FLD_024 | Square Yard | Accepted | Medium | Yes |
| LAND_FLD_025 | Square Meter | Accepted | Medium | Yes |
| LAND_FLD_026 | Square Acre | Accepted | Low | Yes |
| LAND_FLD_027 | Square Hectare | Accepted | Low | Yes |
| LAND_FLD_028 | "Select" (disabled) | Cannot select after first save | Medium | Conditional |

### G5: Land Title Document Dropdown (#land_title_doc0)

| TC ID | Option | Expected | Priority | Automatable |
|-------|--------|----------|----------|-------------|
| LAND_FLD_029 | Sale Deed | Accepted + Favor field appears | Critical | Yes |
| LAND_FLD_030 | Lease Deed | Accepted (no conditional) | Medium | Yes |
| LAND_FLD_031 | Conveyance Deed | Accepted (no conditional) | Medium | Yes |
| LAND_FLD_032 | Gift Deed | Accepted (no conditional) | Medium | Yes |
| LAND_FLD_033 | Other Deeds | Accepted (no conditional) | Medium | Yes |
| LAND_FLD_034 | "Types of Deed" (placeholder) | Cannot select after first save | Medium | Conditional |

---

## SECTION H: APPLICATION DEFECT DISCOVERY TESTS

| TC ID | Scenario | Hypothesis | Priority | Category |
|-------|----------|-----------|----------|----------|
| LAND_DEFECT_001 | Only 2 validation messages for 12 mandatory fields | Missing validation for most fields | High | Business Rule Pending Confirmation |
| LAND_DEFECT_002 | Document Date accepts future date | Should reject future dates for land title | Medium | Business Rule Pending Confirmation |
| LAND_DEFECT_003 | Land Area accepts alphabets in DOM | Should have input type restriction | Medium | Business Rule Pending Confirmation |
| LAND_DEFECT_004 | Situated In accepts only numbers | Should require descriptive text | Low | Business Rule Pending Confirmation |
| LAND_DEFECT_005 | Sale Deed Favor left blank when Sale Deed selected | Should validate conditional mandatory | High | Business Rule Pending Confirmation |
| LAND_DEFECT_006 | Switching plot type may retain stale hidden data | Server-side data cleanup not verified | Medium | Business Rule Pending Confirmation |
| LAND_DEFECT_007 | Land area=0 accepted | Should minimum be 1? | Medium | Business Rule Pending Confirmation |
| LAND_DEFECT_008 | Duration fields accept alphabets/negative | Should be numeric only | Medium | Business Rule Pending Confirmation |
| LAND_DEFECT_009 | Plot number > total plots accepted | Missing cross-field validation | Medium | Business Rule Pending Confirmation |
| LAND_DEFECT_010 | Contiguous radios have misleading IDs (renewal_yes/no) | Developer naming issue | Low | Non-blocking |

---

# 5. REGRESSION TEST IDS (R-Series)

| Regression ID | Test Case ID | Scenario | Sanity? |
|---------------|-------------|----------|---------|
| R01 | LAND_VAL_001 | Owned — all fields blank validation | ✅ S01 |
| R02 | LAND_POS_001 | Owned — valid Conveyance Deed | ✅ S02 |
| R03 | LAND_POS_002 | Owned — valid Sale Deed + favor | ✅ S03 |
| R04 | LAND_POS_003 | Owned — Sale Deed alternate favor | |
| R05 | LAND_POS_004 | Owned — Gift Deed | |
| R06 | LAND_POS_005 | Owned — Other Deeds | |
| R07 | LAND_POS_006 | Owned — Lease Deed option | |
| R08 | LAND_NEG_001 | Land Area blank | ✅ S04 |
| R09 | LAND_NEG_002 | Situated In blank | |
| R10 | LAND_NEG_003 | Land Area alphabets | |
| R11 | LAND_NEG_004 | Land Area negative | |
| R12 | LAND_NEG_017 | Sale Deed Favor blank | ✅ S05 |
| R13 | LAND_BND_001 | Land Area minimum (1) | |
| R14 | LAND_BND_002 | Land Area large | |
| R15 | LAND_BND_017 | Document Date today | |
| R16 | LAND_UI_001 | Owned form appears | ✅ S06 |
| R17 | LAND_UI_008 | Sale Deed conditional appears | ✅ S07 |
| R18 | LAND_UI_009 | Sale Deed conditional disappears | |
| R19 | LAND_DEP_001 | Sale Deed → Favor mandatory | |
| R20 | LAND_VAL_002 | Leased — all fields blank | ✅ S08 |
| R21 | LAND_POS_011 | Leased — valid Renewal=No | ✅ S09 |
| R22 | LAND_POS_012 | Leased — valid Renewal=Yes | |
| R23 | LAND_UI_002 | Leased form appears | |
| R24 | LAND_UI_010 | Renewal=Yes shows duration | |
| R25 | LAND_UI_011 | Renewal=No hides duration | |
| R26 | LAND_DEP_002 | Renewal→Duration mandatory | |
| R27 | LAND_VAL_003 | Multiple — plots blank | |
| R28 | LAND_POS_014 | Multiple — Contiguous=Yes | ✅ S10 |
| R29 | LAND_POS_015 | Multiple — Contiguous=No, Boundary=Yes | |
| R30 | LAND_POS_016 | Multiple — full nested path | |
| R31 | LAND_UI_003 | Multiple form appears | |
| R32 | LAND_UI_012 | Contiguous=No shows boundary | |
| R33 | LAND_UI_014 | Boundary=No shows explanation | |
| R34 | LAND_DEP_003 | Explanation mandatory | |
| R35 | LAND_UI_004 | Switch Single→Multiple | |
| R36 | LAND_UI_006 | Switch Owned→Leased | |
| R37 | LAND_DEP_004 | Hidden fields not submitted | |

---

# 6. SANITY TEST IDS (S-Series)

| Sanity ID | Test Case ID | Scenario | Critical Path? |
|-----------|-------------|----------|----------------|
| S01 | LAND_VAL_001 | All Owned fields blank shows errors | Yes |
| S02 | LAND_POS_001 | Valid Owned Conveyance Deed navigates | Yes |
| S03 | LAND_POS_002 | Sale Deed with conditional field navigates | Yes |
| S04 | LAND_NEG_001 | Land Area blank shows validation | Yes |
| S05 | LAND_NEG_017 | Sale Deed Favor blank blocks form | Yes |
| S06 | LAND_UI_001 | Owned form loads correctly | Yes |
| S07 | LAND_UI_008 | Sale Deed conditional UI works | Yes |
| S08 | LAND_VAL_002 | Leased blank validation | Yes |
| S09 | LAND_POS_011 | Valid Leased submission | Yes |
| S10 | LAND_POS_014 | Valid Multiple submission | Yes |

---

# 7. FINAL SUMMARY

## Test Count by Category

| Category | Owned | Leased | Multiple | UI/Deps | Total |
|----------|-------|--------|----------|---------|-------|
| Validation | 1 | 1 | 2 | — | **4** |
| Positive | 10 | 3 | 3 | — | **16** |
| Negative | 20 | 15 | 9 | — | **44** |
| Boundary | 19 | 9 | 7 | — | **35** |
| UI Behaviour | — | — | — | 17 | **17** |
| Dependency | — | — | — | 10 | **10** |
| Field Behaviour | 34 | — | — | — | **34** |
| Defect Discovery | — | — | — | 10 | **10** |
| **TOTAL** | | | | | **170** |

## Deduplication (Field Behaviour overlaps with Negative/Boundary)

After removing overlapping test cases (Field Behaviour tests that duplicate Negative/Boundary):

| Category | Unique Tests |
|----------|-------------|
| Validation | 4 |
| Positive | 16 |
| Negative | 44 |
| Boundary | 35 |
| UI Behaviour | 17 |
| Dependency | 10 |
| Defect Discovery | 10 |
| **TOTAL UNIQUE** | **~105** (after dedup from Field Behaviour) |

## Automation Readiness

| Category | Ready Now (Owned) | Needs Diagnostic (Leased) | Needs Diagnostic (Multiple) |
|----------|-------------------|--------------------------|----------------------------|
| Automatable immediately | **37** | — | — |
| Automatable after diagnostic | — | **28** | **21** |
| Conditional/may not be testable | **3** | — | — |
| **Total Automatable** | **37** | **28** | **21** = **86** |

## Excluded Scenarios

| # | Scenario | Reason |
|---|----------|--------|
| 1 | Area Unit "Select" after first save | Disabled placeholder cannot be re-selected |
| 2 | Land Title Document "Types of Deed" after first save | Disabled placeholder persistence |
| 3 | Calendar UI min/max date enforcement | Readonly field uses JS — calendar not used |
| 4 | Cross-browser date format differences | JS injection bypasses browser-specific issues |
| 5 | Multi-plot indexed field stress (50+ plots) | Beyond reasonable functional scope |
| 6 | Server-side validation for hidden fields | Cannot verify without API access |
| 7 | Concurrent user editing | Out of scope for functional UI testing |

---

# 8. RECOMMENDED IMPLEMENTATION ORDER

| Phase | Scope | Tests | Effort | Depends On |
|-------|-------|-------|--------|-----------|
| **Phase 1** (DONE) | Single→Owned — Basic | 12 | 4 hrs | ✅ Complete |
| **Phase 2** | Single→Owned — Extended | +15 | 3 hrs | Phase 1 |
| **Phase 3** | Single→Owned — UI/Deps | +8 | 2 hrs | Phase 2 |
| **Phase 4** | Single→Leased — Full | +20 | 5 hrs | Leased Diagnostic |
| **Phase 5** | Multiple Plot — Full | +15 | 4 hrs | Multiple Diagnostic |
| **Phase 6** | Cross-path switching | +7 | 2 hrs | Phases 4-5 |
| **Phase 7** | Defect Discovery | +10 | 3 hrs | All above |
| **TOTAL** | | **~87** | **~23 hrs** | |

### Phase 2 Breakdown (Immediate Next Step):
1. LAND_POS_004–010 (remaining dropdown options)
2. LAND_NEG_005–020 (extended negative coverage)
3. LAND_BND_003–019 (field length/value boundaries)
4. LAND_NEG_015 (future date test)
5. LAND_NEG_017 (Sale Deed Favor blank)

### Phase 3 Breakdown:
1. LAND_UI_001, UI_008, UI_009 (dynamic visibility)
2. LAND_DEP_001 (Sale Deed mandatory dependency)
3. LAND_DEP_006 (value reset on title change)
4. LAND_UI_016, UI_017 (timing/wait verification)

---

# 9. BUSINESS RULES PENDING CONFIRMATION

| # | Rule | Evidence |
|---|------|----------|
| 1 | Is Land Area = 0 valid? | Only "valid land area" message confirmed — unclear boundary |
| 2 | Can document date be in the future? | No diagnostic evidence of rejection |
| 3 | Are blank text fields (owned_by, executed_by, etc.) accepted? | Only 2 validation messages confirmed for entire form |
| 4 | Is Sale Deed Favor mandatory when Sale Deed selected? | Not tested in diagnostic |
| 5 | Can plot number exceed total plots? | Not tested |
| 6 | Is Renewal Duration mandatory when Yes? | Not tested — locator unclear |
| 7 | Is Explanation mandatory when Boundary=No? | Not tested — field not found in DOM scan |
| 8 | Does switching paths reset hidden field values? | Not verified server-side |
| 9 | Is decimal land area valid (e.g., 500.5)? | Not tested |
| 10 | Maximum allowed number of plots? | Not tested |

---

**STATUS:** Complete QA analysis and test matrix generated. Ready for phased implementation.
