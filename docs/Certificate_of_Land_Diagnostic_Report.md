# Certificate of Land — Diagnostic Report
## Evidence-Based Findings

---

# FLOW 1: PLOT TYPE

| Check | Result |
|-------|--------|
| "Single" radio visible | ✅ Yes |
| "Multiple" radio visible | ✅ Yes |
| Locator | `get_by_role("radio", name="Single")` / `get_by_role("radio", name="Multiple")` |
| Default selection | Previously saved (depends on account state) |

---

# FLOW 2: SINGLE → OWNED (E2E Path)

## All Owned Path Fields Confirmed:

| # | Field | ID / Locator | Type | Readonly | Confirmed |
|---|-------|-------------|------|----------|-----------|
| 1 | Area Unit | `#land_unit_0` | `<select>` | No | ✅ |
| 2 | Land Area | `#land_area_0` | text input | No | ✅ |
| 3 | Situated In (dropdown) | `#situated_in_0` | `<select>` | No | ✅ |
| 4 | Situated In (specify) | `#situate_speci_0` | text input | No | ✅ |
| 5 | Situated At | `#situated_at0` | text input | No | ✅ |
| 6 | Land Owned By | `#owned_by_0` | text input | No | ✅ |
| 7 | Land Title Document | `#land_title_doc0` | `<select>` | No | ✅ |
| 8 | Sale Deed Favor | `#sale_deed_favor_whom_0` | `<select>` | No | ✅ (conditional) |
| 9 | Registration Details | `#land_title0` | text input | No | ✅ |
| 10 | Executed By | `#executed_by0` | text input | No | ✅ |
| 11 | Registration Office | `#regid_ofc_details0` | text input | No | ✅ |
| 12 | Land Document Date | `#land_title_date0` | text input | **No (NOT readonly!)** | ✅ |

## Area Unit Dropdown Options:

| Index | Value | Text | Disabled |
|-------|-------|------|----------|
| 0 | (empty) | Select | ✅ Yes |
| 1 | 1 | Square Foot | No |
| 2 | 2 | Square Yard | No |
| 3 | 3 | Square Meter | No |
| 4 | 4 | Square Acre | No |
| 5 | 5 | Square Hectare | No |

## Land Title Document Options:

| Index | Value | Text |
|-------|-------|------|
| 0 | Types of Deed | Types of Deed (placeholder) |
| 1 | 1 | Sale Deed |
| 2 | 2 | Lease Deed |
| 3 | 3 | Conveyance Deed |
| 4 | 4 | Gift Deed |
| 5 | 5 | Other Deeds |

## Sale Deed Favor Options (conditional — appears only when Title = "Sale Deed"):

| Value | Text |
|-------|------|
| (empty) | Type of Sale Deed (placeholder) |
| 1 | School |
| 2 | Trust/Society/Company |

## CRITICAL FINDING: Date Field is NOT Readonly

```
type: text
readonly: False
placeholder: Select a date
id: land_title_date0
```

**`.fill('15/03/2024')` WORKS!** Value = '15/03/2024' ✅

This is DIFFERENT from NOC/Trust dates. The Land Document Date can be filled directly — no JavaScript injection needed.

---

# FLOW 3: SINGLE → LEASED

## All Leased Path Fields Discovered:

| # | Field | ID | Type | Readonly |
|---|-------|-----|------|----------|
| 1 | Lease Area Unit | `#lease_area_unit_0` | `<select>` | No |
| 2 | Lease Land Area | `#lease_land_area_0` | text input | No |
| 3 | Name of Lessee | `#leease_name_0` | text input | No |
| 4 | Name of Lessor | `#leaser_name_0` | text input | No |
| 5 | Date of Lease Deed | `#lease_deed_date_0` | text input | No |
| 6 | Duration of Lease Deed | `#lease_deed_duration_0` | text input | No |
| 7 | Date of Registration | `#date_regis_lease_deed0` | text input | No |
| 8 | Registration Office | (shared with owned?) | text input | No |

## Renewal Clause Radio:

**NOT FOUND** as standard `get_by_role("radio", name="Yes"/"No")`.

However, in the Multiple path scan, these were discovered:
```
[6] id='renewal_yes' name='plotTypeyes' type='radio'
[7] id='renewal_no' name='plotTypeyes' type='radio'
```

These may be the Renewal clause radios but they appeared in the Multiple path context — likely they exist in both paths or are misplaced in the DOM. **Needs further investigation on the actual Leased form.**

---

# FLOW 4: MULTIPLE PLOTS

## Fields Discovered:

| # | Field | ID | Type |
|---|-------|-----|------|
| 1 | Number of Plots | `#no_of_plots` | text input |
| 2 | Plot Number (school building) | `#plot_number_school_building` | number input |
| 3 | Contiguous Yes | `#renewal_yes` (name=`plotTypeyes`) | radio |
| 4 | Contiguous No | `#renewal_no` (name=`plotTypeyes`) | radio |

**Note:** The "contiguous" radios have ID `renewal_yes`/`renewal_no` and name `plotTypeyes` — misleading naming. These are the "Are plots contiguous?" radios.

**Boundary/Explanation fields NOT visible in scan** — they likely appear dynamically after selecting "No" for contiguous.

---

# VALIDATION MESSAGES (Blank Owned Form)

When clicking Next with blank Owned fields:
```
- Please enter a valid land area
- Please specify where it is situated
```

**Only 2 validation messages** — minimal client-side validation. Many fields may be accepted blank.

---

# IMPLEMENTATION READINESS

## Confirmed Automation Approach:

| Field Category | Approach | Risk |
|----------------|----------|------|
| Radio buttons | `get_by_role("radio", name=...)` | ✅ Low |
| Text inputs (all editable) | `.fill()` | ✅ Low |
| Standard dropdowns | `select_option(label/value)` | ✅ Low |
| Land Document Date | **`.fill()` directly** (NOT readonly!) | ✅ Low |
| Sale Deed conditional | `if title == "Sale Deed"` then fill favor | ✅ Low (proven in E2E) |
| Dynamic form waits | `wait_for_timeout(2000)` after radio | ✅ Low |
| Leased path | New locators discovered | ⚠️ Medium (untested in E2E) |
| Multiple path | Minimal fields; contiguous logic | ⚠️ Medium |

## Automatable Scenarios (Phase 1 — Owned):

| TC ID | Scenario |
|-------|----------|
| LAND_VAL_001 | All owned fields blank — verify errors |
| LAND_POS_001 | Valid owned — non-Sale-Deed |
| LAND_POS_002 | Valid owned — Sale Deed with favor |
| LAND_FMT_001 | Land area blank |
| LAND_FMT_002 | Situated In blank |
| LAND_FMT_003 | Area Unit not selected |
| LAND_BND_001 | Land area — 1 digit |
| LAND_BND_002 | Land area — large number |
| **Total Phase 1** | **~8** |

## Excluded Scenarios:

| Scenario | Reason |
|----------|--------|
| Area Unit blank after save | Disabled "Select" placeholder |
| Land Title Document blank | Placeholder "Types of Deed" may not trigger error |
| Calendar UI restrictions | Date field is editable — not applicable |

## Potential Application Gaps:

| Finding | Evidence |
|---------|----------|
| Only 2 validation messages for entire Owned form | Many fields may be accepted blank |
| Leased path renewal radios have misleading IDs | `renewal_yes`/`renewal_no` used for contiguous question |

---

# DIAGNOSTICS STILL NEEDED (Phase 2/3)

| # | What | For Phase |
|---|------|-----------|
| 1 | Leased path date fields — are they readonly or fillable? | Phase 2 |
| 2 | Leased renewal clause — exact locator and behavior | Phase 2 |
| 3 | Multiple path — contiguous=No → boundary radios appear? | Phase 3 |
| 4 | Multiple path — boundary=No → explanation textarea? | Phase 3 |
| 5 | Lease area validation messages | Phase 2 |

---

**STATUS:** Phase 1 (Owned path) implementation-ready. Phases 2-3 need additional diagnostics.
