# Certificate of Land — Test Matrix QA Review Report
## Peer Review of Complete Regression Test Matrix

---

# REVIEW OBJECTIVE

Verify the Complete Regression Test Matrix for:
1. No duplicate test cases
2. No Positive vs Boundary overlap
3. No Boundary vs Negative overlap
4. No duplicate business rule tests
5. No duplicate UI behaviour tests
6. No redundant dependency tests
7. Every scenario maps to a unique requirement
8. Every automatable scenario is actually feasible
9. Impossible or redundant scenarios identified

---

# 1. DUPLICATE TEST CASES IDENTIFIED

## 1.1 Section G (Field Behaviour) duplicates Sections C & D entirely

Section G ("Field Behaviour Tests") is a **complete subset** of Negative + Boundary + Positive sections. Every single LAND_FLD_xxx maps to an already-existing test:

| Section G ID | Duplicates | Category |
|--------------|-----------|----------|
| LAND_FLD_001 | LAND_NEG_001 | Negative — land_area blank |
| LAND_FLD_002 | LAND_POS_001 | Positive — land_area=5000 valid |
| LAND_FLD_003 | LAND_NEG_003 | Negative — land_area alphabets |
| LAND_FLD_004 | LAND_NEG_004 | Negative — land_area negative |
| LAND_FLD_005 | LAND_NEG_005 | Negative — land_area=0 |
| LAND_FLD_006 | LAND_BND_003 | Boundary — land_area=0.01 (decimal) |
| LAND_FLD_007 | LAND_NEG_018 | Negative — land_area special chars |
| LAND_FLD_008 | LAND_NEG_007 | Negative — land_area spaces |
| LAND_FLD_009 | (unique — leading/trailing spaces) | **KEEP — reassign to LAND_NEG_XXX** |
| LAND_FLD_010 | LAND_BND_001 | Boundary — land_area=1 |
| LAND_FLD_011 | LAND_BND_002 | Boundary — land_area=999999999 |
| LAND_FLD_012 | LAND_NEG_002 | Negative — situated_in blank |
| LAND_FLD_013 | LAND_POS_001 | Positive — situated_in valid |
| LAND_FLD_014 | LAND_NEG_008 | Negative — situated_in spaces |
| LAND_FLD_015 | LAND_BND_005 | Boundary — situated_in 1 char |
| LAND_FLD_016 | LAND_BND_006 | Boundary — situated_in 500 chars |
| LAND_FLD_017 | LAND_NEG_014 | Negative — date blank |
| LAND_FLD_018 | LAND_POS_001 | Positive — date valid past |
| LAND_FLD_019 | LAND_NEG_015 | Negative — date future |
| LAND_FLD_020 | LAND_BND_018 | Boundary — date very old |
| LAND_FLD_021 | LAND_BND_017 | Boundary — date today |
| LAND_FLD_022 | (unique — invalid format) | **KEEP — reassign to LAND_NEG_XXX** |
| LAND_FLD_023–027 | LAND_POS_007–010 | Positive — area unit options |
| LAND_FLD_028 | LAND_NEG_016 | Negative — disabled placeholder |
| LAND_FLD_029 | LAND_POS_002 + LAND_UI_008 | Positive + UI — Sale Deed |
| LAND_FLD_030–033 | LAND_POS_004–006 | Positive — title options |
| LAND_FLD_034 | LAND_NEG_016 pattern | Negative — disabled placeholder |

**VERDICT:** Remove ENTIRE Section G. Absorb 2 unique scenarios into Negative section.

---

## 1.2 Negative vs Negative Overlap within Owned

| Pair | Overlap |
|------|---------|
| LAND_NEG_001 (land_area blank) vs LAND_VAL_001 | LAND_VAL_001 tests ALL blank; NEG_001 tests ONLY land_area blank with other fields valid. **Not a duplicate** — different test strategy (isolation vs bulk). ✅ |
| LAND_NEG_002 (situated_in blank) vs LAND_VAL_001 | Same analysis. ✅ Keep both. |

---

## 1.3 LAND_DEP_001 vs LAND_NEG_017

| LAND_DEP_001 | "Select Sale Deed, leave Favor blank, submit — should block" |
| LAND_NEG_017 | "sale_deed_favor (blank when Sale Deed selected) — Should block" |

**These are IDENTICAL tests.**

**VERDICT:** Remove LAND_NEG_017. Keep LAND_DEP_001 (better categorization as a dependency test).

---

## 1.4 LAND_DEP_002 vs LAND_NEG_033

| LAND_DEP_002 | "Renewal=Yes → Duration mandatory — leave duration blank, submit" |
| LAND_NEG_033 | "renewal_duration (blank when Renewal=Yes) — Should block" |

**These are IDENTICAL tests.**

**VERDICT:** Remove LAND_NEG_033. Keep LAND_DEP_002.

---

## 1.5 LAND_DEP_003 vs LAND_NEG_043

| LAND_DEP_003 | "Contiguous=No + Boundary=No → Explanation mandatory — leave blank" |
| LAND_NEG_043 | "explanation (blank when required) — Should block" |

**These are IDENTICAL tests.**

**VERDICT:** Remove LAND_NEG_043. Keep LAND_DEP_003.

---

## 1.6 LAND_UI_008 and LAND_FLD_029

Both verify Sale Deed conditional appearance. Already handled by removing Section G.

---

## 1.7 LAND_DEFECT_005 vs LAND_DEP_001 / LAND_NEG_017

| LAND_DEFECT_005 | "Sale Deed Favor left blank when Sale Deed selected — should validate" |

This is the same scenario as LAND_DEP_001.

**VERDICT:** Remove LAND_DEFECT_005. Already covered by LAND_DEP_001.

---

## 1.8 LAND_DEFECT_007 vs LAND_NEG_005

| LAND_DEFECT_007 | "Land area=0 accepted — should minimum be 1?" |
| LAND_NEG_005 | "land_area=0 — Validation error or accept" |

**Same scenario.**

**VERDICT:** Remove LAND_DEFECT_007. Keep LAND_NEG_005 with "Business Rule Pending" remark.

---

## 1.9 LAND_DEFECT_002 vs LAND_NEG_015

| LAND_DEFECT_002 | "Document Date accepts future date — should reject" |
| LAND_NEG_015 | "document_date — Future date — Should reject" |

**Same scenario.**

**VERDICT:** Remove LAND_DEFECT_002. Keep LAND_NEG_015.

---

## 1.10 LAND_DEFECT_003 vs LAND_NEG_003

| LAND_DEFECT_003 | "Land Area accepts alphabets in DOM — should restrict" |
| LAND_NEG_003 | "land_area — abcdef — Error or DOM blocks" |

**Same scenario.**

**VERDICT:** Remove LAND_DEFECT_003. Keep LAND_NEG_003.

---

## 1.11 LAND_DEFECT_008 vs LAND_NEG_030 / LAND_NEG_035

| LAND_DEFECT_008 | "Duration fields accept alphabets/negative — should be numeric" |
| LAND_NEG_030 | "lease_deed_duration — Alphabets" |
| LAND_NEG_035 | "renewal_duration — Alphabets" |

**Same scenarios — already covered individually.**

**VERDICT:** Remove LAND_DEFECT_008.

---

## 1.12 LAND_DEFECT_009 vs LAND_DEP_009

| LAND_DEFECT_009 | "Plot number > total plots accepted — missing cross-field validation" |
| LAND_DEP_009 | "Enter 3 plots, building on plot 5 — should reject" |

**Same scenario.**

**VERDICT:** Remove LAND_DEFECT_009. Keep LAND_DEP_009.

---

# 2. POSITIVE vs BOUNDARY OVERLAP

| Positive ID | Boundary ID | Overlap? | Verdict |
|-------------|-------------|----------|---------|
| LAND_POS_001 (area=5000) | LAND_BND_001 (area=1) | ❌ No — different values, different intent | Keep both |
| LAND_POS_007 (unit=Square Foot) | — | No boundary for unit | ✅ |
| LAND_POS_011 (valid Leased) | LAND_BND_020 (lease_area=1) | ❌ No — POS tests full valid form, BND tests single field | Keep both |
| LAND_POS_014 (Multiple contiguous=Yes) | LAND_BND_029 (plots=2) | ⚠️ **OVERLAP** — Both test the minimum valid multiple-plot scenario | **MERGE** |

**VERDICT:** LAND_BND_029 (no_of_plots=2) and LAND_POS_014 (2 plots, contiguous=Yes) **overlap**. The positive test already validates 2 plots. Remove LAND_BND_029 or clarify intent (if BND_029 tests ONLY that 2 is accepted and does NOT click Next, keep it; if it submits the full form, it's a duplicate).

**Decision:** Keep LAND_BND_029 but redefine: "Fill ONLY no_of_plots=2, leave other fields valid, verify acceptance" (single-field boundary). Keep LAND_POS_014 as full positive flow. **No removal needed — different scope.**

---

# 3. BOUNDARY vs NEGATIVE OVERLAP

| Boundary ID | Negative ID | Overlap? | Verdict |
|-------------|-------------|----------|---------|
| LAND_BND_001 (area=1) | — | No negative for area=1 | ✅ |
| LAND_BND_003 (area=0.01) | LAND_NEG_005 (area=0) | ❌ No — 0.01 vs 0 are different values | Keep both |
| LAND_BND_017 (date=today) | LAND_NEG_015 (date=future) | ❌ No — today is boundary, future is negative | Keep both |
| LAND_BND_031 (plots=1 in Multiple) | LAND_NEG_037 (plots=0) | ❌ No — 1 is boundary (may/may not be valid), 0 is clearly invalid | Keep both |

**No true Boundary vs Negative overlaps found.** ✅

---

# 4. DUPLICATE UI BEHAVIOUR TESTS

| Pair | Analysis | Verdict |
|------|----------|---------|
| LAND_UI_004 (Switch Single→Multiple) vs LAND_UI_005 (Switch Multiple→Single) | ❌ Different — opposite directions | Keep both |
| LAND_UI_006 (Switch Owned→Leased) vs LAND_UI_007 (Switch Leased→Owned) | ❌ Different — opposite directions | Keep both |
| LAND_UI_008 vs LAND_UI_009 | ❌ Show vs hide are inverse tests | Keep both |
| LAND_UI_010 vs LAND_UI_011 | ❌ Show vs hide | Keep both |
| LAND_UI_012 vs LAND_UI_013 | ❌ Show vs hide | Keep both |
| LAND_UI_014 vs LAND_UI_015 | ❌ Show vs hide | Keep both |
| LAND_UI_016 vs LAND_UI_017 | ⚠️ **Partially redundant** — both test "fields load after radio wait". UI_016 is for plot type radio, UI_017 is for owned/leased radio. | **MERGE into single test** — "Dynamic form loading waits" |

**VERDICT:** Merge LAND_UI_016 + LAND_UI_017 into a single test. Net reduction: 1.

---

# 5. REDUNDANT DEPENDENCY TESTS

| Pair | Analysis | Verdict |
|------|----------|---------|
| LAND_DEP_004 (Owned→Leased hidden data) vs LAND_DEP_005 (Multiple→Single hidden data) | ❌ Different paths | Keep both |
| LAND_DEP_006 (Sale Deed Favor reset) vs LAND_UI_009 (Sale Deed conditional disappears) | ⚠️ **OVERLAP** — UI_009 verifies the field HIDES; DEP_006 verifies the VALUE RESETS. | **Keep both** — different assertions (visibility vs value persistence) |
| LAND_DEP_007 (Renewal Duration reset) vs LAND_UI_011 (Renewal=No hides duration) | Same pattern — different assertions | Keep both |
| LAND_DEP_008 (Explanation reset) vs LAND_UI_015 (Boundary=Yes hides explanation) | Same pattern | Keep both |
| LAND_DEP_010 (Area Unit + Area relationship) | **REDUNDANT** — Any positive test already validates this implicitly. Every positive test uses a unit + area combination. | **REMOVE** |

**VERDICT:** Remove LAND_DEP_010. Already proven by every positive test.

---

# 6. INFEASIBLE / IMPOSSIBLE SCENARIOS

| TC ID | Scenario | Issue | Verdict |
|-------|----------|-------|---------|
| LAND_NEG_016 | Area Unit = disabled "Select" | Cannot re-select disabled placeholder after first save (proven pattern from all modules) | **MARK AS NON-AUTOMATABLE** — move to Excluded |
| LAND_FLD_028 | Same as above | Already removed with Section G | N/A |
| LAND_FLD_034 | Title Document placeholder "Types of Deed" | Same issue — disabled | N/A (removed) |
| LAND_FLD_022 | Invalid date format "2020-03-15" via JS | Arbitrary — no clear business requirement; JS injection can set anything | **REMOVE** — not a valid user scenario |
| LAND_DEFECT_010 | Misleading IDs (renewal_yes/no for contiguous) | Not a test case — it's a code observation | **REMOVE** — not automatable, developer issue |
| LAND_BND_004 | Land area 15 digits (99999999999999) | If LAND_BND_002 (9 digits) already passes, 15 digits adds marginal value | **KEEP but mark LOW priority** |
| LAND_NEG_044 | Explanation spaces only | Requires navigating to deepest nested path (Multiple → Contiguous=No → Boundary=No) just to test whitespace. Same result likely as LAND_NEG_008. | **KEEP — unique conditional context** |

---

# 7. SCENARIOS TO MERGE

| Merge Group | IDs to Merge | Merged Test | Reason |
|-------------|-------------|-------------|--------|
| 1 | LAND_UI_016 + LAND_UI_017 | LAND_UI_016 "Dynamic form loading waits (all radio selections)" | Both test timing after radio click |
| 2 | LAND_POS_007 + LAND_POS_008 + LAND_POS_009 + LAND_POS_010 | LAND_POS_007 "Valid Owned — All non-default Area Units (parametrized)" | Same test with different dropdown value — should be a single parametrized test |
| 3 | LAND_POS_004 + LAND_POS_005 + LAND_POS_006 | LAND_POS_004 "Valid Owned — Non-Sale-Deed Title Options (parametrized)" | Same test with different title — single parametrized test |

**Note on merging:** Merging does NOT reduce test execution count — parametrized tests still execute separately. It reduces test FILE/FUNCTION count for maintainability.

---

# 8. REVISED TEST COUNTS

## Removals Summary

| Removed ID | Reason |
|------------|--------|
| Section G (LAND_FLD_001–034) | Entire section is duplicate of C+D+B |
| LAND_NEG_017 | Duplicate of LAND_DEP_001 |
| LAND_NEG_033 | Duplicate of LAND_DEP_002 |
| LAND_NEG_043 | Duplicate of LAND_DEP_003 |
| LAND_DEFECT_002 | Duplicate of LAND_NEG_015 |
| LAND_DEFECT_003 | Duplicate of LAND_NEG_003 |
| LAND_DEFECT_005 | Duplicate of LAND_DEP_001 |
| LAND_DEFECT_007 | Duplicate of LAND_NEG_005 |
| LAND_DEFECT_008 | Covered by LAND_NEG_030 + LAND_NEG_035 |
| LAND_DEFECT_009 | Duplicate of LAND_DEP_009 |
| LAND_DEFECT_010 | Not automatable — developer naming issue |
| LAND_DEP_010 | Redundant — implicitly covered by positive tests |
| LAND_UI_017 | Merged into LAND_UI_016 |
| LAND_NEG_016 | Non-automatable — move to Excluded |

**Total Removed:** 34 (Section G) + 13 (individual) = **47 removed**

## Additions (from Section G unique scenarios)

| New ID | Scenario | From |
|--------|----------|------|
| LAND_NEG_045 | Land Area with leading/trailing spaces " 500 " | LAND_FLD_009 |

**Total Added:** 1

---

# 9. FINAL RECOMMENDED TEST COUNT

| Category | Original | After Review | Net Change |
|----------|----------|-------------|------------|
| Validation | 4 | 4 | 0 |
| Positive | 16 | 16 | 0 |
| Negative | 44 | 41 | -3 (NEG_017, NEG_033, NEG_043 → DEPs; NEG_016 → Excluded; +NEG_045) |
| Boundary | 35 | 35 | 0 |
| UI Behaviour | 17 | 16 | -1 (merged UI_017) |
| Dependency | 10 | 9 | -1 (DEP_010 removed) |
| Field Behaviour | 34 | **0** | -34 (entire section removed) |
| Defect Discovery | 10 | 4 | -6 (duplicates removed) |
| **TOTAL** | **170** | **125** | **-45** |

## Final Deduped Automatable Count

| Scope | Ready Now | Needs Diagnostic | Total |
|-------|-----------|-----------------|-------|
| Owned (Single) | 35 | — | 35 |
| Leased (Single) | — | 26 | 26 |
| Multiple | — | 19 | 19 |
| UI/Dependencies | 12 | 13 | 25 |
| Defect Discovery | 2 | 2 | 4 |
| **Non-automatable** | | | **2** (NEG_016 + excluded) |
| **TOTAL AUTOMATABLE** | **49** | **60** | **107** |

---

# 10. REMAINING DEFECT DISCOVERY TESTS (After Dedup)

| TC ID | Scenario | Unique Value |
|-------|----------|-------------|
| LAND_DEFECT_001 | Only 2 validation messages for 12 mandatory fields | Exposes missing validation architecture |
| LAND_DEFECT_004 | Situated In accepts only numbers | Character-type validation gap |
| LAND_DEFECT_006 | Switching plot type may retain stale hidden data | Server-side data integrity |
| LAND_DEFECT_010 | — | REMOVED (not automatable) |

**Remaining: 3 unique defect discovery tests**

Updated count: Defect Discovery = **3** (not 4)

**Corrected total: 124 tests**

---

# 11. FINAL IMPLEMENTATION ORDER (Revised)

| Phase | Scope | Tests | Effort | Status |
|-------|-------|-------|--------|--------|
| **Phase 1** | Single→Owned — Basic (VAL, POS×3, NEG×5, BND×3) | 12 | 4 hrs | ✅ DONE |
| **Phase 2** | Single→Owned — Extended Positive + Negative | +14 | 3 hrs | Next |
| **Phase 3** | Single→Owned — Boundary (all fields) + Date | +16 | 2.5 hrs | After Phase 2 |
| **Phase 4** | Single→Owned — UI Behaviour + Dependencies | +10 | 2 hrs | After Phase 3 |
| **Phase 5** | Single→Leased — Full (requires diagnostic first) | +26 | 6 hrs | After Leased Diagnostic |
| **Phase 6** | Multiple Plot — Full (requires diagnostic first) | +19 | 5 hrs | After Multiple Diagnostic |
| **Phase 7** | Cross-path switching + Defect Discovery | +7 | 2 hrs | After Phases 5-6 |
| **TOTAL** | | **~104** | **~24.5 hrs** | |

### Phase 2 Detail (Immediate Next):

| # | TC ID | Scenario |
|---|-------|----------|
| 1 | LAND_POS_004 | Gift Deed |
| 2 | LAND_POS_005 | Other Deeds |
| 3 | LAND_POS_006 | Lease Deed (as title option) |
| 4 | LAND_POS_007 | Square Foot |
| 5 | LAND_POS_008 | Square Yard |
| 6 | LAND_POS_009 | Square Acre |
| 7 | LAND_POS_010 | Square Hectare |
| 8 | LAND_NEG_003 | Land Area alphabets |
| 9 | LAND_NEG_004 | Land Area negative |
| 10 | LAND_NEG_005 | Land Area=0 |
| 11 | LAND_NEG_006 | Invalid decimal |
| 12 | LAND_NEG_007 | Spaces only |
| 13 | LAND_NEG_015 | Future date |
| 14 | LAND_NEG_045 | Leading/trailing spaces |

---

# 12. EXCLUDED SCENARIOS (Final)

| # | Scenario | Reason |
|---|----------|--------|
| 1 | Area Unit "Select" after first save (LAND_NEG_016) | Disabled placeholder cannot be re-selected |
| 2 | Land Title Document "Types of Deed" after first save | Disabled placeholder persistence |
| 3 | Calendar UI min/max date enforcement | Readonly field uses JS — calendar not used |
| 4 | Cross-browser date format differences | JS injection bypasses browser-specific issues |
| 5 | Multi-plot indexed field stress (50+ plots) | Beyond reasonable functional scope |
| 6 | Server-side validation for hidden fields | Cannot verify without API access |
| 7 | Concurrent user editing | Out of scope for functional UI testing |
| 8 | Invalid date format injection (LAND_FLD_022) | Arbitrary — no user scenario maps to this |
| 9 | Developer naming convention (LAND_DEFECT_010) | Not an automation test — code review finding |

---

# 13. REVIEW VERDICT

| Check | Result |
|-------|--------|
| No duplicate test cases | ✅ After removing Section G + 13 individual duplicates |
| No Positive vs Boundary overlap | ✅ Confirmed (different scope/intent) |
| No Boundary vs Negative overlap | ✅ Confirmed (different values/categories) |
| No duplicate business rule tests | ✅ After removing DEFECT_002/003/005/007/008/009 |
| No duplicate UI behaviour tests | ✅ After merging UI_016+017 |
| No redundant dependency tests | ✅ After removing DEP_010 |
| Every scenario maps to unique requirement | ✅ Confirmed |
| Every automatable scenario is feasible | ✅ (2 moved to Excluded) |
| Impossible scenarios marked | ✅ (NEG_016, FLD_022, DEFECT_010) |

---

# FINAL NUMBERS

| Metric | Value |
|--------|-------|
| **Total Unique Tests (Revised)** | **124** |
| **Total Automatable** | **107** |
| **Ready to Implement Now** | **49** (Owned path) |
| **Needs Diagnostic First** | **60** (Leased + Multiple) |
| **Non-automatable / Excluded** | **9** |
| **Implementation Phases** | **7** |
| **Total Estimated Effort** | **~24.5 hours** |
| **Duplicates Removed** | **47** |
| **Sanity Suite** | **10 tests** |
| **Regression Suite** | **37 core (R-series)** |

---

**STATUS:** QA Review complete. Matrix is clean after deduplication. Ready for phased implementation.
