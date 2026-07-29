# Upload Documents — Optimized Test Case Matrix
## Production Deployment Confidence Suite

---

# DESIGN PRINCIPLES

1. **One representative upload test** covers all 5 dropzones (same mechanism)
2. **School Image difference** tested separately (different accepted types)
3. **Conditional validation** tested per unique condition (not per field)
4. **Every mandatory prerequisite** for Proceed to Payment verified once
5. **No duplicate file upload tests** — one invalid type test represents all dropzones
6. **Download tested once** — same mechanism for all links

---

# OPTIMIZED TEST MATRIX

## A. VALIDATION TESTS (3 tests)

| TC ID | Scenario | Priority | Expected Result |
|-------|----------|----------|-----------------|
| UPLOAD_VAL_001 | Click Proceed with NO uploads + no radio + no checkboxes | Critical | Form blocked — validation error shown |
| UPLOAD_VAL_002 | Click Proceed with all uploads done but no affiliation selected | High | Form blocked — affiliation required |
| UPLOAD_VAL_003 | Click Proceed with all uploads + affiliation but checkboxes unchecked | High | Form blocked — checkboxes required |

---

## B. POSITIVE TESTS (8 tests)

| TC ID | Scenario | Priority | Expected Result |
|-------|----------|----------|-----------------|
| UPLOAD_POS_001 | Upload all 5 documents (valid PDF) + comments + Provisional radio + both checkboxes + Proceed | Critical | Navigates to payment gateway |
| UPLOAD_POS_002 | Upload all 5 documents + Composite Affiliation radio + Proceed | Critical | Navigates (verifies alternate radio) |
| UPLOAD_POS_003 | Upload all 5 documents + Switch Over X radio + Proceed | Medium | Navigates (verifies 3rd radio option) |
| UPLOAD_POS_004 | Upload all 5 documents + Switch Over XII radio + Proceed | Medium | Navigates (verifies 4th radio option) |
| UPLOAD_POS_005 | Upload valid JPEG image to NOC (non-PDF) | High | Upload succeeds (verifies image acceptance) |
| UPLOAD_POS_006 | Upload valid PNG to School Image | High | Upload succeeds |
| UPLOAD_POS_007 | Leave comments empty + all other valid + Proceed | High | Navigates (confirms comments optional) |
| UPLOAD_POS_008 | Comments with special characters + Unicode + multiline | Medium | Accepted without error |

---

## C. NEGATIVE TESTS (10 tests)

| TC ID | Scenario | Priority | Expected Result |
|-------|----------|----------|-----------------|
| UPLOAD_NEG_001 | Upload .exe file to NOC Document | High | Dropzone error: "You can't upload files of this type." |
| UPLOAD_NEG_002 | Upload .docx file to Certificate of Land | High | Dropzone error: invalid type |
| UPLOAD_NEG_003 | Upload file >20MB to any dropzone | High | Dropzone error: "File is too big..." |
| UPLOAD_NEG_004 | Upload BMP to School Image (not in accepted list) | High | Dropzone error: invalid type |
| UPLOAD_NEG_005 | Upload BMP to NOC Document (IS in accepted list) | Medium | Upload succeeds (proves School Image difference) |
| UPLOAD_NEG_006 | Only 4 of 5 documents uploaded + click Proceed | High | Form blocked — missing upload validation |
| UPLOAD_NEG_007 | All uploads + affiliation NOT selected + click Proceed | High | Form blocked |
| UPLOAD_NEG_008 | All uploads + only #verify_composite checked (not #verify) | High | Form blocked |
| UPLOAD_NEG_009 | All uploads + only #verify checked (not #verify_composite) | Medium | Form blocked |
| UPLOAD_NEG_010 | Upload second file to same dropzone (maxFiles=1) | Medium | "You can not upload any more files." or replaces |

---

## D. BOUNDARY TESTS (5 tests)

| TC ID | Scenario | Priority | Expected Outcome |
|-------|----------|----------|-----------------|
| UPLOAD_BND_001 | Upload file exactly at 20MB limit | Medium | ACCEPT or REJECT (boundary threshold) |
| UPLOAD_BND_002 | Upload smallest valid file (1 KB PDF) | Medium | ACCEPT |
| UPLOAD_BND_003 | Comments textarea — 5000 characters (large text) | Medium | ACCEPT (no maxLength) |
| UPLOAD_BND_004 | Comments textarea — 1 character | Low | ACCEPT |
| UPLOAD_BND_005 | Upload file with special characters in filename | Medium | ACCEPT or handled gracefully |

---

## E. DYNAMIC UI / BEHAVIOUR TESTS (6 tests)

| TC ID | Scenario | Priority | Expected Behaviour |
|-------|----------|----------|--------------------|
| UPLOAD_UI_001 | Upload file → verify download link appears for that document | High | Download link with filename visible after upload |
| UPLOAD_UI_002 | Click "Download for Notarization" link | High | PDF download starts or new tab opens |
| UPLOAD_UI_003 | Upload file → delete → verify dropzone resets | Medium | Dropzone returns to empty state, ready for new upload |
| UPLOAD_UI_004 | Upload file → navigate Back → return → verify upload persists | High | Previously uploaded files still shown |
| UPLOAD_UI_005 | Select affiliation type → verify radio persists after page interaction | Medium | Radio selection maintained |
| UPLOAD_UI_006 | Check both checkboxes → verify Proceed button is clickable | Medium | Button responds (validation passes) |

---

# TOTAL: 32 TESTS

| Category | Count |
|----------|-------|
| Validation | 3 |
| Positive | 8 |
| Negative | 10 |
| Boundary | 5 |
| Dynamic UI | 6 |
| **TOTAL** | **32** |

---

# COVERAGE MAPPING

## Feature Coverage

| Feature | VAL | POS | NEG | BND | UI | Total |
|---------|-----|-----|-----|-----|-----|-------|
| File Uploads (all 5) | ✅ | ✅✅✅ | ✅✅✅✅✅✅ | ✅✅✅ | ✅✅ | 16 |
| Download for Notarization | — | — | — | — | ✅ | 1 |
| Comments Textarea | — | ✅✅ | — | ✅✅ | — | 4 |
| Affiliation Type | ✅ | ✅✅✅✅ | ✅ | — | ✅ | 7 |
| Declaration Checkboxes | ✅ | ✅ | ✅✅ | — | ✅ | 5 |
| Proceed to Payment | ✅✅✅ | ✅✅ | ✅✅ | — | ✅ | 7 |

## Mandatory Validation Coverage

| Condition | Covered By |
|-----------|-----------|
| All 5 uploads required | UPLOAD_VAL_001, UPLOAD_NEG_006 |
| Affiliation type required | UPLOAD_VAL_002, UPLOAD_NEG_007 |
| Both checkboxes required | UPLOAD_VAL_003, UPLOAD_NEG_008, UPLOAD_NEG_009 |
| File type validation | UPLOAD_NEG_001, NEG_002, NEG_004 |
| File size validation | UPLOAD_NEG_003 |
| Comments optional | UPLOAD_POS_007 |

## Upload Mechanism Coverage

| Scenario | Test |
|----------|------|
| Valid PDF upload | POS_001 (all 5 via E2E) |
| Valid JPEG upload | POS_005 |
| Valid PNG upload | POS_006 |
| Invalid type (.exe) | NEG_001 |
| Invalid type (.docx) | NEG_002 |
| Invalid type for School Image (BMP) | NEG_004 |
| Valid type for others (BMP to NOC) | NEG_005 |
| Oversize file (>20MB) | NEG_003 |
| Max files exceeded | NEG_010 |
| Boundary file size | BND_001, BND_002 |
| Special filename | BND_005 |
| Upload persistence | UI_004 |
| Delete + re-upload | UI_003 |
| Download after upload | UI_001 |

---

# DUPLICATE ELIMINATION JUSTIFICATION

| Removed Scenario | Reason |
|-----------------|--------|
| Test invalid type for EACH of 5 dropzones (×5) | One test per dropzone type difference (×3: NEG_001 + NEG_002 for standard, NEG_004 for School Image) |
| Test >20MB for each dropzone (×5) | One test sufficient — same config for all (NEG_003) |
| Test valid PDF for each dropzone individually (×5) | POS_001 uploads all 5 in one test — E2E proven |
| Test each affiliation separately with full flow (×4 full tests) | POS_001–004 test each radio but share same upload precondition |
| Test every checkbox combination (4 combos) | VAL_003 + NEG_008 + NEG_009 cover the meaningful states |
| Test upload persistence per document (×5) | One test (UI_004) represents all — same mechanism |
| Test download per document link (×5) | One test (UI_001) represents all |
| Test delete per document (×5) | One test (UI_003) represents all |
| Corrupt file per document (×5) | Excluded — server-side concern, not UI regression |
| Zero-byte file per document (×5) | Represented by BND_002 (small file) |
| Drag & drop (×5) | Excluded — same mechanism as click, unreliable in automation |

**Total scenarios eliminated: ~40+ redundant tests**

---

# SANITY SUITE (8 tests — quick build verification)

| Sanity ID | TC ID | Reason |
|-----------|-------|--------|
| S01 | UPLOAD_VAL_001 | Validation mechanism works |
| S02 | UPLOAD_POS_001 | Full flow works (upload + proceed) |
| S03 | UPLOAD_POS_007 | Optional comments confirmed |
| S04 | UPLOAD_NEG_001 | Invalid file type rejected |
| S05 | UPLOAD_NEG_006 | Missing upload blocks proceed |
| S06 | UPLOAD_NEG_003 | Oversize file rejected |
| S07 | UPLOAD_UI_002 | Download functionality works |
| S08 | UPLOAD_UI_004 | Upload persistence works |

---

# REGRESSION SUITE (Full — 32 tests)

All 32 tests form the complete regression suite (R01–R32).

| R-ID | TC ID | Category | Feature |
|------|-------|----------|---------|
| R01 | UPLOAD_VAL_001 | Validation | All missing |
| R02 | UPLOAD_VAL_002 | Validation | No affiliation |
| R03 | UPLOAD_VAL_003 | Validation | No checkboxes |
| R04 | UPLOAD_POS_001 | Positive | Full flow — Provisional |
| R05 | UPLOAD_POS_002 | Positive | Full flow — Composite |
| R06 | UPLOAD_POS_003 | Positive | Full flow — Switch Over X |
| R07 | UPLOAD_POS_004 | Positive | Full flow — Switch Over XII |
| R08 | UPLOAD_POS_005 | Positive | JPEG upload |
| R09 | UPLOAD_POS_006 | Positive | PNG upload |
| R10 | UPLOAD_POS_007 | Positive | Empty comments |
| R11 | UPLOAD_POS_008 | Positive | Special char comments |
| R12 | UPLOAD_NEG_001 | Negative | .exe rejected |
| R13 | UPLOAD_NEG_002 | Negative | .docx rejected |
| R14 | UPLOAD_NEG_003 | Negative | >20MB rejected |
| R15 | UPLOAD_NEG_004 | Negative | BMP to School Image |
| R16 | UPLOAD_NEG_005 | Negative | BMP to NOC (accepted) |
| R17 | UPLOAD_NEG_006 | Negative | Partial uploads |
| R18 | UPLOAD_NEG_007 | Negative | No affiliation |
| R19 | UPLOAD_NEG_008 | Negative | One checkbox |
| R20 | UPLOAD_NEG_009 | Negative | Other checkbox |
| R21 | UPLOAD_NEG_010 | Negative | Max files exceeded |
| R22 | UPLOAD_BND_001 | Boundary | 20MB limit |
| R23 | UPLOAD_BND_002 | Boundary | Smallest file |
| R24 | UPLOAD_BND_003 | Boundary | Large comments |
| R25 | UPLOAD_BND_004 | Boundary | 1 char comment |
| R26 | UPLOAD_BND_005 | Boundary | Special filename |
| R27 | UPLOAD_UI_001 | UI | Download link after upload |
| R28 | UPLOAD_UI_002 | UI | Download for Notarization |
| R29 | UPLOAD_UI_003 | UI | Delete + re-upload |
| R30 | UPLOAD_UI_004 | UI | Upload persistence (Back) |
| R31 | UPLOAD_UI_005 | UI | Radio persistence |
| R32 | UPLOAD_UI_006 | UI | Checkbox → Proceed |

---

# EXCLUDED SCENARIOS

| # | Scenario | Reason |
|---|----------|--------|
| 1 | Drag & drop upload | Unreliable automation — same Dropzone mechanism as click |
| 2 | Corrupt file upload | Server-side validation — not UI regression |
| 3 | Multiple simultaneous uploads | Not supported (maxFiles=1 per dropzone) |
| 4 | Upload timeout/network failure | Environment issue — not functional test |
| 5 | Payment gateway flow | Separate module — beyond Upload Documents scope |
| 6 | Browser-specific file dialog | Playwright handles cross-browser transparently |
| 7 | Upload progress percentage | Visual/timing — not functionally verifiable |
| 8 | Individual file download per document (×5) | One representative (UI_001) covers mechanism |

---

# ESTIMATED AUTOMATION EFFORT

| Phase | Scope | Tests | Effort |
|-------|-------|-------|--------|
| Phase 1 | Framework (page methods, fixture, folders) | — | 1.5 hrs |
| Phase 2 | Excel data + test files | — | 1 hr |
| Phase 3 | Positive tests (upload flow) | 8 | 3 hrs |
| Phase 4 | Negative tests (invalid uploads, missing prereqs) | 10 | 3 hrs |
| Phase 5 | Boundary + UI behaviour | 11 | 3 hrs |
| Phase 6 | Validation tests | 3 | 1.5 hrs |
| Phase 7 | Verification + Allure | — | 1 hr |
| **TOTAL** | | **32** | **~14 hrs** |

---

# AUTOMATION RISKS & NOTES

| # | Risk | Mitigation |
|---|------|-----------|
| 1 | First upload (NOC) may cause execution context change | Add 3000ms wait after NOC upload |
| 2 | >20MB test file creation | Generate large file dynamically in test setup |
| 3 | Invalid file (.exe) creation | Create minimal .exe-like file for test |
| 4 | `force=True` needed for radio/checkbox/button | Use existing E2E pattern |
| 5 | Download may open new tab instead of file download | Handle with `expect_download()` or `page.expect_popup()` |
| 6 | Delete/remove button may not exist (addRemoveLinks=false) | Investigate custom remove implementation |
| 7 | Upload persistence test requires Back + return navigation | Use browser back + tab re-click |

---

# BUSINESS RULES PENDING CONFIRMATION

| # | Rule | Status |
|---|------|--------|
| 1 | Is affiliation type selection dependent on school category? | Needs confirmation |
| 2 | Can uploaded files be replaced (or only deleted + re-uploaded)? | Needs investigation |
| 3 | Does partial upload save progress server-side? | Likely yes (async) |
| 4 | Is there a minimum file size? | Not configured — needs testing |
| 5 | Does the order of uploads matter? | Likely no — independent dropzones |

---

**STATUS:** Optimized test matrix complete. 32 tests provide deployment confidence. Ready for implementation planning.
