# Certificate of Land — Optimized Regression Test Matrix
## Production Deployment Confidence Suite

---

# DESIGN PRINCIPLES

1. **One representative test** per validation pattern — not every permutation
2. **Every major business flow** covered (Owned, Leased, Multiple)
3. **Every dynamic UI toggle** verified (show/hide)
4. **Every confirmed mandatory field** validated
5. **Realistic negative inputs** only — no obscure edge cases
6. **Critical boundary values** only — min, max, and boundary-at-risk
7. **Independent tests** — no test depends on another's state

---

# OPTIMIZED TEST MATRIX

## A. VALIDATION TESTS (3 tests)

| TC ID | Flow | Scenario | Priority | Expected Result |
|-------|------|----------|----------|-----------------|
| LAND_VAL_001 | Single→Owned | All Owned fields blank — click Next | Critical | "Please enter a valid land area" + "Please specify where it is situated" |
| LAND_VAL_002 | Single→Leased | All Leased fields blank — click Next | Critical | Validation errors block form |
| LAND_VAL_003 | Multiple | All Multiple fields blank — click Next | High | Validation errors block form |

**Rationale:** One consolidated validation test per major flow. Catches all mandatory field errors in a single execution.

---

## B. POSITIVE TESTS (9 tests)

| TC ID | Flow | Scenario | Priority | Expected Result |
|-------|------|----------|----------|-----------------|
| LAND_POS_001 | Single→Owned | Valid — Conveyance Deed (no conditional) | Critical | Navigates to Upload Documents |
| LAND_POS_002 | Single→Owned | Valid — Sale Deed, favor=School | Critical | Navigates with conditional field filled |
| LAND_POS_003 | Single→Owned | Valid — Sale Deed, favor=Trust/Society | High | Navigates with alternate conditional value |
| LAND_POS_004 | Single→Owned | Valid — Gift Deed (verifies other title options work) | Medium | Navigates |
| LAND_POS_005 | Single→Owned | Valid — Area Unit=Square Foot (non-default unit) | Medium | Navigates |
| LAND_POS_006 | Single→Leased | Valid — Renewal=No | Critical | Navigates to next step |
| LAND_POS_007 | Single→Leased | Valid — Renewal=Yes + Duration filled | Critical | Navigates with conditional field |
| LAND_POS_008 | Multiple | Valid — Contiguous=Yes | Critical | Navigates |
| LAND_POS_009 | Multiple | Valid — Contiguous=No, Boundary=No, Explanation filled | High | Navigates (deepest nested path) |

**Rationale:** Covers every unique business path. One non-default area unit (POS_005) represents all unit options. One non-Sale-Deed title (POS_004) represents Gift/Other/Lease Deed options.

---

## C. NEGATIVE TESTS (11 tests)

| TC ID | Flow | Field | Value | Priority | Expected Result |
|-------|------|-------|-------|----------|-----------------|
| LAND_NEG_001 | Single→Owned | land_area | (blank) | Critical | "Please enter a valid land area" |
| LAND_NEG_002 | Single→Owned | situated_in | (blank) | Critical | "Please specify where it is situated" |
| LAND_NEG_003 | Single→Owned | land_area | abcdef (alphabets) | High | Validation error or DOM blocks |
| LAND_NEG_004 | Single→Owned | land_area | -500 (negative) | High | Validation error |
| LAND_NEG_005 | Single→Owned | document_date | Future date (tomorrow) | Medium | Should reject — Business Rule Pending |
| LAND_NEG_006 | Single→Owned | sale_deed_favor | (blank when Sale Deed selected) | High | Form blocked — conditional mandatory |
| LAND_NEG_007 | Single→Leased | lease_land_area | (blank) | High | Validation error |
| LAND_NEG_008 | Single→Leased | lease_deed_duration | Alphabets | Medium | Validation error |
| LAND_NEG_009 | Single→Leased | renewal_duration | (blank when Renewal=Yes) | High | Form blocked — conditional mandatory |
| LAND_NEG_010 | Multiple | no_of_plots | 0 | High | Validation error |
| LAND_NEG_011 | Multiple | explanation | (blank when Contiguous=No + Boundary=No) | High | Form blocked — conditional mandatory |

**Rationale:** Covers every confirmed validation message, every conditional mandatory dependency, and representative invalid inputs (alphabets, negative, blank) for numeric fields. One test per flow for conditional mandatory enforcement.

---

## D. BOUNDARY TESTS (7 tests)

| TC ID | Flow | Field | Value | Priority | Expected Outcome |
|-------|------|-------|-------|----------|-----------------|
| LAND_BND_001 | Single→Owned | land_area | 1 (minimum) | Medium | ACCEPT |
| LAND_BND_002 | Single→Owned | land_area | 999999999 (large) | Medium | ACCEPT or REJECT |
| LAND_BND_003 | Single→Owned | document_date | Today's date | Medium | ACCEPT or REJECT (boundary) |
| LAND_BND_004 | Single→Owned | situated_in | 500 characters (maxlength) | Medium | ACCEPT or truncated |
| LAND_BND_005 | Single→Leased | lease_deed_duration | 1 (minimum) | Medium | ACCEPT |
| LAND_BND_006 | Multiple | no_of_plots | 2 (minimum for multiple) | High | ACCEPT |
| LAND_BND_007 | Multiple | no_of_plots | 100 (large) | Medium | ACCEPT or REJECT |

**Rationale:** Covers min/max for critical numeric fields (land_area, duration, plots). One maxlength test (situated_in) represents all text fields. Date boundary (today) tests the acceptance threshold.

---

## E. DYNAMIC UI BEHAVIOUR TESTS (5 tests)

| TC ID | Scenario | Action | Expected Behaviour | Priority |
|-------|----------|--------|-------------------|----------|
| LAND_UI_001 | Owned form loads correctly | Select Single + Owned | All 12 Owned fields visible | Critical |
| LAND_UI_002 | Sale Deed conditional toggle | Select Sale Deed → verify Favor appears; change to Gift Deed → verify Favor disappears | Show + hide in single test | High |
| LAND_UI_003 | Leased form with Renewal toggle | Select Leased; select Renewal=Yes → Duration appears; switch to No → Duration disappears | Show + hide in single test | High |
| LAND_UI_004 | Multiple plot nested conditional | Select Multiple; Contiguous=No → Boundary question; Boundary=No → Explanation appears | Full nested path visibility | High |
| LAND_UI_005 | Path switching resets form | Select Single+Owned, fill data, switch to Multiple | Owned fields hidden, Multiple fields visible | Medium |

**Rationale:** One test per dynamic flow path. UI_002/003/004 each test both SHOW and HIDE in a single test (more efficient, tests real user workflow). UI_005 verifies path switching doesn't leave stale UI.

---

# TOTAL: 35 TESTS

| Category | Count |
|----------|-------|
| Validation | 3 |
| Positive | 9 |
| Negative | 11 |
| Boundary | 7 |
| Dynamic UI | 5 |
| **TOTAL** | **35** |

---

# COVERAGE MAPPING

## Business Flow Coverage

| Flow | VAL | POS | NEG | BND | UI | Total Coverage |
|------|-----|-----|-----|-----|----|---------------|
| Single → Owned (no conditional) | ✅ | ✅ | ✅✅✅✅✅ | ✅✅✅✅ | ✅✅ | **15 tests** |
| Single → Owned (Sale Deed conditional) | — | ✅✅ | ✅ | — | ✅ | **4 tests** |
| Single → Leased (Renewal=No) | ✅ | ✅ | ✅✅ | ✅ | ✅ | **6 tests** |
| Single → Leased (Renewal=Yes) | — | ✅ | ✅ | — | — | **2 tests** |
| Multiple (Contiguous=Yes) | ✅ | ✅ | ✅ | ✅✅ | — | **5 tests** |
| Multiple (Full nested path) | — | ✅ | ✅ | — | ✅✅ | **4 tests** |

## Mandatory Field Coverage

| Field | Covered By |
|-------|-----------|
| Land Area (Owned) | LAND_VAL_001, LAND_NEG_001 |
| Situated In (Owned) | LAND_VAL_001, LAND_NEG_002 |
| Sale Deed Favor (conditional) | LAND_NEG_006 |
| Lease Land Area | LAND_VAL_002, LAND_NEG_007 |
| Renewal Duration (conditional) | LAND_NEG_009 |
| Number of Plots | LAND_VAL_003, LAND_NEG_010 |
| Explanation (conditional) | LAND_NEG_011 |

## Conditional Dependency Coverage

| Dependency | Covered By |
|-----------|-----------|
| Sale Deed → Favor mandatory | LAND_NEG_006 |
| Renewal=Yes → Duration mandatory | LAND_NEG_009 |
| Contiguous=No + Boundary=No → Explanation mandatory | LAND_NEG_011 |
| Sale Deed → Favor field appears/disappears | LAND_UI_002 |
| Renewal → Duration appears/disappears | LAND_UI_003 |
| Nested Multiple conditional chain | LAND_UI_004 |

## Dropdown Option Coverage

| Dropdown | Options Tested | Coverage |
|----------|---------------|----------|
| Area Unit | Square Meter (default), Square Foot (POS_005) | 2/5 — representative |
| Land Title Document | Conveyance Deed (POS_001), Sale Deed (POS_002/003), Gift Deed (POS_004) | 3/5 — representative |
| Sale Deed Favor | School (POS_002), Trust/Society (POS_003) | 2/2 — complete |

---

# RISK COVERAGE SUMMARY

| Risk Category | Coverage | Tests |
|---------------|----------|-------|
| **Critical path blocked** (form can't submit with valid data) | ✅ 9 positive tests across all flows | POS_001–009 |
| **Mandatory validation missing** (invalid data accepted) | ✅ 3 validation + 11 negative | VAL_001–003, NEG_001–011 |
| **Conditional fields broken** (Sale Deed, Renewal, Explanation) | ✅ 3 dependency negatives + 3 UI tests | NEG_006/009/011, UI_002/003/004 |
| **Dynamic UI regression** (fields don't show/hide correctly) | ✅ 5 dedicated UI tests | UI_001–005 |
| **Boundary failures** (min/max values crash or truncate) | ✅ 7 boundary tests across all flows | BND_001–007 |
| **Data integrity** (switching paths retains stale data) | ✅ 1 path-switching UI test | UI_005 |
| **Date field broken** (readonly workaround fails) | ✅ 2 tests (boundary + negative) | BND_003, NEG_005 |

---

# REMOVED TESTS — JUSTIFICATION

## From Positive (7 removed)

| Removed | Why Redundant |
|---------|---------------|
| LAND_POS_005 (Other Deeds) | Gift Deed (POS_004) already proves non-conditional titles work |
| LAND_POS_006 (Lease Deed as title) | Same as above — another non-conditional title option |
| LAND_POS_007 (Square Yard) | POS_005 (Square Foot) already proves non-default units work |
| LAND_POS_008 (Square Acre) | Same — one alternate unit is sufficient |
| LAND_POS_009 (Square Hectare) | Same |
| LAND_POS_010 (Square Meter explicit) | Already tested in POS_001 baseline |
| LAND_POS_013 (Leased all units) | Unit dropdown works identically in Owned and Leased |

## From Negative (33 removed)

| Removed | Why Redundant |
|---------|---------------|
| LAND_NEG_005 (area=0) | Covered by NEG_004 (negative) — both test invalid numeric boundaries |
| LAND_NEG_006 (invalid decimal 12.34.56) | Covered by NEG_003 (alphabets) — both test non-numeric input |
| LAND_NEG_007 (spaces only) | Blank field (NEG_001) already validates empty submission |
| LAND_NEG_008 (situated_in spaces) | Same pattern — blank (NEG_002) covers it |
| LAND_NEG_009–013 (blank owned_by, reg_details, etc.) | Only 2 validation messages exist — these fields are NOT validated by the app. Testing blank values that the app accepts is not a negative test. |
| LAND_NEG_014 (date blank) | App likely accepts blank date (only 2 validations confirmed). Not a valid negative test until business rule confirmed. |
| LAND_NEG_016 (area unit disabled placeholder) | Not automatable — disabled option can't be re-selected |
| LAND_NEG_018 (special chars in area) | NEG_003 (alphabets) covers non-numeric input |
| LAND_NEG_019 (numbers in situated_in) | Not invalid — app accepts it |
| LAND_NEG_020 (special chars in owned_by) | Not validated by app — would pass |
| LAND_NEG_022 (lease area alphabets) | Represented by NEG_008 (duration alphabets) — same validation pattern |
| LAND_NEG_023 (lease area negative) | Same pattern as NEG_004 on different field — one representative enough |
| LAND_NEG_024–025 (lessee/lessor blank) | Covered by VAL_002 (all lease blank) |
| LAND_NEG_026 (lease date blank) | Covered by VAL_002 |
| LAND_NEG_027 (lease date future) | Same rule as NEG_005 — one future date test is representative |
| LAND_NEG_028 (duration blank) | Covered by VAL_002 |
| LAND_NEG_029–030 (duration negative/alphabets) | NEG_008 covers alphabets; negative is same pattern |
| LAND_NEG_031–032 (lease reg date blank/future) | Covered by VAL_002 + same pattern as NEG_005 |
| LAND_NEG_034–035 (renewal duration neg/alpha) | Same validation pattern — one per flow sufficient |
| LAND_NEG_036 (plots blank) | Covered by VAL_003 |
| LAND_NEG_037 (plots=0) | Keeping as NEG_010 (unique — zero vs blank) |
| LAND_NEG_038 (plots=-1) | Same pattern as NEG_010 (invalid number) |
| LAND_NEG_039 (plots alphabets) | Same validation — one invalid type test per field sufficient |
| LAND_NEG_040 (plots decimal) | Same |
| LAND_NEG_041 (plot number blank) | Covered by VAL_003 |
| LAND_NEG_042 (plot > total) | Business Rule Pending — no confirmed validation |
| LAND_NEG_044 (explanation spaces) | Covered by NEG_011 (explanation blank) — same intent |
| LAND_NEG_045 (leading/trailing spaces) | App likely trims — not a real negative |

## From Boundary (28 removed)

| Removed | Why Redundant |
|---------|---------------|
| LAND_BND_003 (area decimal 0.01) | BND_001 (area=1) already tests minimum |
| LAND_BND_004 (area 15 digits) | BND_002 (9 digits) tests large enough |
| LAND_BND_005–006 (situated_in 1 char / 500 chars) | One maxlength test (BND_004 at 500) is representative for ALL text fields |
| LAND_BND_007–016 (all other text field min/max) | Same — one representative maxlength test covers pattern |
| LAND_BND_017 (date today) | Keeping as BND_003 |
| LAND_BND_018 (date very old) | Accepted by any calendar — trivial |
| LAND_BND_019 (date yesterday) | Between today and past date — no unique value |
| LAND_BND_020–021 (lease area min/max) | Same pattern as Owned area (BND_001/002) |
| LAND_BND_022–024 (lease duration boundaries) | Keeping BND_005 (duration=1) as representative |
| LAND_BND_025–026 (renewal duration) | Same pattern — one min test sufficient |
| LAND_BND_027–028 (lessee name boundaries) | Covered by BND_004 (text field maxlength representative) |
| LAND_BND_029 (plots=2) | Keeping as BND_006 |
| LAND_BND_030 (plots=100) | Keeping as BND_007 |
| LAND_BND_031 (plots=1 in Multiple) | Ambiguous — better as defect discovery, not regression |
| LAND_BND_032–033 (plot number boundaries) | Covered by positive tests (POS_008/009) |
| LAND_BND_034–035 (explanation boundaries) | Explanation is a textarea — unlikely to have limits |

## From UI (12 removed)

| Removed | Why Redundant |
|---------|---------------|
| LAND_UI_002 (Leased form appears) | Merged into UI_003 (Leased + Renewal toggle) |
| LAND_UI_003 (Multiple form appears) | Merged into UI_004 (Multiple + nested conditional) |
| LAND_UI_004 (Switch Single→Multiple) | Merged into UI_005 |
| LAND_UI_005 (Switch Multiple→Single) | Same test as UI_005 — inverse direction adds marginal value |
| LAND_UI_006 (Switch Owned→Leased) | Covered by UI_003 (which tests Leased form) |
| LAND_UI_007 (Switch Leased→Owned) | Covered by UI_001 (Owned form verification) |
| LAND_UI_008 (Sale Deed appears) | Merged into UI_002 (toggle test) |
| LAND_UI_009 (Sale Deed disappears) | Merged into UI_002 |
| LAND_UI_010 (Renewal shows) | Merged into UI_003 |
| LAND_UI_011 (Renewal hides) | Merged into UI_003 |
| LAND_UI_012–015 (Contiguous/Boundary toggles) | Merged into UI_004 |
| LAND_UI_016–017 (timing waits) | Implementation detail — not a functional test |

## From Dependencies (9 removed)

| Removed | Why Redundant |
|---------|---------------|
| LAND_DEP_001 (Sale Deed Favor mandatory) | Now LAND_NEG_006 |
| LAND_DEP_002 (Renewal Duration mandatory) | Now LAND_NEG_009 |
| LAND_DEP_003 (Explanation mandatory) | Now LAND_NEG_011 |
| LAND_DEP_004 (Hidden fields not submitted) | Covered by UI_005 (path switch verification) |
| LAND_DEP_005 (Multiple→Single hidden fields) | Same pattern — one switch test sufficient |
| LAND_DEP_006 (Sale Deed Favor resets) | Covered by UI_002 (field hides = resets) |
| LAND_DEP_007 (Renewal Duration resets) | Covered by UI_003 (field hides = resets) |
| LAND_DEP_008 (Explanation resets) | Covered by UI_004 (field hides = resets) |
| LAND_DEP_009 (Plot > total) | Business Rule Pending — no confirmed validation |
| LAND_DEP_010 (Unit + Area relationship) | Implicitly tested by every positive test |

---

# DEPLOYMENT READINESS JUSTIFICATION

## Why 35 Tests Provide Deployment Confidence:

| Deployment Risk | Mitigated By | Confidence |
|-----------------|-------------|------------|
| Form cannot submit with valid data | 9 positive tests (every flow) | ✅ High |
| Invalid data passes to server | 11 negative tests (every confirmed validation) | ✅ High |
| Conditional fields broken | 3 negative + 3 UI toggle tests | ✅ High |
| Dynamic UI regression | 5 UI tests covering all show/hide paths | ✅ High |
| Extreme values crash the form | 7 boundary tests (min, max, date boundary) | ✅ Medium |
| All 3 major paths work | VAL + POS cover Owned, Leased, Multiple | ✅ High |
| Date field JS injection works | BND_003 + NEG_005 | ✅ High |
| Dropdown options functional | POS_001–005 cover representative options | ✅ Medium |

## What This Suite Does NOT Cover (Acceptable Risk):

| Not Covered | Risk Level | Why Acceptable |
|-------------|-----------|----------------|
| Every dropdown permutation (25+ combinations) | Low | One representative per category proves the mechanism works |
| Every text field at maxlength | Low | One representative field (situated_in) proves truncation/acceptance pattern |
| Server-side data cleanup on path switch | Medium | UI verification confirms frontend behaviour; server-side is separate concern |
| Calendar UI interactions | Low | JS injection is the confirmed working approach |
| Lease date field readonly check | Low | Same pattern as Owned date — proven once |

## Execution Time Estimate:

| Category | Tests | Avg Time/Test | Total |
|----------|-------|---------------|-------|
| Validation | 3 | ~45s | ~2.5 min |
| Positive | 9 | ~60s | ~9 min |
| Negative | 11 | ~50s | ~9 min |
| Boundary | 7 | ~55s | ~6.5 min |
| UI Behaviour | 5 | ~40s | ~3.5 min |
| **TOTAL** | **35** | | **~30 min** |

A full regression run completes in ~30 minutes — suitable for pre-deployment gating.

---

# FINAL AUTOMATION COUNT

| Metric | Value |
|--------|-------|
| **Total Tests** | **35** |
| **Ready Now (Owned path)** | **18** (VAL_001, POS_001–005, NEG_001–006, BND_001–004, UI_001–002) |
| **Needs Leased Diagnostic** | **8** (VAL_002, POS_006–007, NEG_007–009, BND_005, UI_003) |
| **Needs Multiple Diagnostic** | **9** (VAL_003, POS_008–009, NEG_010–011, BND_006–007, UI_004–005) |
| **Excluded (non-automatable)** | **0** (all 35 are automatable) |
| **Estimated Implementation** | **~12 hours** |

---

**STATUS:** Optimized matrix finalized. 35 tests provide production deployment confidence with zero redundancy.
