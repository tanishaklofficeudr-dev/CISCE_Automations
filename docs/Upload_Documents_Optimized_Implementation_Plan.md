# Upload Documents — Optimized Implementation Plan
## Based on QA-Approved 28-Test Matrix

---

# SCOPE

Implement the optimized regression suite (28 tests) for the Upload Documents module covering:
- File uploads (5 dropzones)
- Download for Notarization
- Comments textarea
- Affiliation type radio buttons
- Declaration checkboxes
- Proceed to Payment navigation

---

# CURRENT STATE (What Already Exists)

| Item | Status |
|------|--------|
| `pages/upload_documents_page.py` — E2E method `upload_documents(data)` | ✅ Exists (READ-ONLY) |
| `tests/regression/upload_documents/` folder | ❌ Does NOT exist (to create) |
| Regression fixture for Upload Documents | ❌ Does NOT exist (to create) |
| `pytest.ini` — `upload_documents` marker | ❌ Does NOT exist (to register) |
| Excel sheets for Upload Documents | ❌ Do NOT exist (to create) |
| Test files | ❌ Do NOT exist (to create) |

---

# PHASE 1 — FRAMEWORK ADDITIONS

## Objective: Add regression page methods + fixture + folder structure + marker

### 1.1 Folder Structure to Create

```
tests/regression/upload_documents/
├── __init__.py
├── validation/
│   ├── __init__.py
│   └── test_upload_validation.py
├── positive/
│   ├── __init__.py
│   └── test_upload_positive.py
├── negative/
│   ├── __init__.py
│   └── test_upload_negative.py
├── boundary/
│   ├── __init__.py
│   └── test_upload_boundary.py
└── ui/
    ├── __init__.py
    └── test_upload_ui.py
```

### 1.2 Files to Extend

| # | File | Change |
|---|------|--------|
| 1 | `pages/upload_documents_page.py` | Add 7 new regression methods at bottom |
| 2 | `conftest.py` | Add `upload_ready_page` fixture |
| 3 | `pytest.ini` | Register `upload_documents` marker |

### 1.3 New Page Methods (7)

| # | Method | Purpose |
|---|--------|---------|
| 1 | `upload_single_file(document_label, file_path)` | Upload one file to a specific dropzone by label |
| 2 | `upload_all_documents(file_path)` | Upload same file to all 5 dropzones |
| 3 | `select_affiliation_type(label)` | Select affiliation radio by label text |
| 4 | `check_declarations()` | Check both declaration checkboxes |
| 5 | `fill_comments(text)` | Fill the comments textarea |
| 6 | `click_proceed()` | Click Proceed to Payment button |
| 7 | `get_upload_status(dropzone_id)` | Get Dropzone file status (success/error/count) |

### 1.4 New Fixture

| Fixture | Scope | Depends On | Logic |
|---------|-------|-----------|-------|
| `upload_ready_page` | function | `school_details_ready_page` | Click "Upload Documents" tab → wait 4000ms → verify dropzone visible → return page |

### 1.5 Existing Methods Reused (NOT modified)

| Method | From | Used By |
|--------|------|---------|
| `upload_documents(data)` | upload_documents_page.py | E2E ONLY — NOT used by regression |
| `ValidationHelper.get_all_errors()` | validation_helper.py | All tests |
| `ValidationHelper.assert_error_present()` | validation_helper.py | Negative tests |
| `ScreenshotUtil.take_screenshot()` | screenshot_util.py | All tests on failure |
| `ExcelReader.get_sheet_data()` | excel_reader.py | Parametrized tests |

### 1.6 Test Data Files to Create

| File | Purpose |
|------|---------|
| `test_data/test_upload.pdf` | Valid small PDF for upload tests (if not exists) |
| `test_data/test_upload.jpg` | Valid JPEG for POS_005 |
| `test_data/test_upload.png` | Valid PNG for POS_006 |
| `test_data/test_upload.bmp` | Valid BMP for POS_009, NEG_003 |
| `test_data/test_upload.exe` | Minimal .exe-like file for NEG_001 |
| `test_data/test_upload_large.pdf` | >20MB file for NEG_002 (generate dynamically) |

**Note:** `test_data/LandCertificate.pdf` (267 KB) already exists — can reuse as valid PDF.

### Estimated Effort: 2.5 hours
### Risk: Low (additive only, proven patterns from Land Certificate)
### Expected Outcome: Framework ready, all imports work, tests collect with 0 items

---

# PHASE 2 — EXCEL DATA

## Objective: Create data sheets for parametrized tests

### File to Extend

`test_data/negative/Validation_Data.xlsx` — add 4 new sheets

### Sheets Required

#### Sheet: `Upload_Positive` (9 rows)

| scenario_id | execute | scenario_description | affiliation_type | file_type | comments | expected_result | priority |
|---|---|---|---|---|---|---|---|

**Rows:** UPLOAD_POS_001 through UPLOAD_POS_009

#### Sheet: `Upload_Negative` (7 rows)

| scenario_id | execute | scenario_description | test_type | target_dropzone | file_path | condition | expected_error | priority | remarks |
|---|---|---|---|---|---|---|---|---|---|

**Rows:** UPLOAD_NEG_001 through UPLOAD_NEG_007

#### Sheet: `Upload_Boundary` (4 rows)

| scenario_id | execute | scenario_description | field_name | field_value | expected_outcome | priority |
|---|---|---|---|---|---|---|

**Rows:** UPLOAD_BND_001 through UPLOAD_BND_004

#### Sheet: `Upload_UI_Behaviour` (5 rows)

| scenario_id | execute | scenario_description | action | expected_behaviour | priority |
|---|---|---|---|---|---|

**Rows:** UPLOAD_UI_001 through UPLOAD_UI_005

### Estimated Effort: 1 hour
### Risk: Low (data entry only)
### Expected Outcome: All sheets load via ExcelReader without error

---

# PHASE 3 — CORE AUTOMATION (28 tests)

## Objective: Implement all test files

### 3.1 Validation Tests (3 tests)

**File:** `tests/regression/upload_documents/validation/test_upload_validation.py`

| TC ID | Approach |
|-------|----------|
| UPLOAD_VAL_001 | Navigate to page → click Proceed without anything → verify blocked |
| UPLOAD_VAL_002 | Upload all 5 → click Proceed without radio → verify blocked |
| UPLOAD_VAL_003 | Upload all 5 + select radio → click Proceed without checkboxes → verify blocked |

**Pattern:** Hardcoded (not parametrized) — each has unique preconditions.

### 3.2 Positive Tests (9 tests)

**File:** `tests/regression/upload_documents/positive/test_upload_positive.py`

| TC ID | Approach |
|-------|----------|
| UPLOAD_POS_001–004 | Upload all 5 PDF + select specific radio + check both + Proceed → verify navigation |
| UPLOAD_POS_005 | Upload JPEG to NOC → verify success |
| UPLOAD_POS_006 | Upload PNG to School Image → verify success |
| UPLOAD_POS_007 | Full flow with empty comments → verify navigates |
| UPLOAD_POS_008 | Fill comments with special chars → verify accepted |
| UPLOAD_POS_009 | Upload BMP to NOC → verify success |

**Pattern:** Parametrized for POS_001–004 (same flow, different radio). POS_005–009 may be parametrized or individual.

### 3.3 Negative Tests (7 tests)

**File:** `tests/regression/upload_documents/negative/test_upload_negative.py`

| TC ID | Approach |
|-------|----------|
| UPLOAD_NEG_001 | Upload .exe → check for Dropzone error message |
| UPLOAD_NEG_002 | Upload >20MB → check for Dropzone size error |
| UPLOAD_NEG_003 | Upload BMP to School Image → check for type error |
| UPLOAD_NEG_004 | Upload only 4 of 5 + Proceed → verify blocked |
| UPLOAD_NEG_005 | Check only 1 checkbox + Proceed → verify blocked |
| UPLOAD_NEG_006 | Upload second file to same dropzone → check maxFiles error |
| UPLOAD_NEG_007 | Double-click Proceed rapidly → verify no duplicate navigation |

### 3.4 Boundary Tests (4 tests)

**File:** `tests/regression/upload_documents/boundary/test_upload_boundary.py`

| TC ID | Approach |
|-------|----------|
| UPLOAD_BND_001 | Upload exactly 20MB file → verify accept/reject |
| UPLOAD_BND_002 | Upload 1KB file → verify accepts |
| UPLOAD_BND_003 | Fill 5000 chars in comments → verify accepted |
| UPLOAD_BND_004 | Upload file with special chars in name → verify handles |

### 3.5 Dynamic UI Tests (5 tests)

**File:** `tests/regression/upload_documents/ui/test_upload_ui.py`

| TC ID | Approach |
|-------|----------|
| UPLOAD_UI_001 | Upload → check download link appeared |
| UPLOAD_UI_002 | Click "Download for Notarization" → verify download/new tab |
| UPLOAD_UI_003 | Upload → delete → verify dropzone reset |
| UPLOAD_UI_004 | Upload → Back → return → verify persistence |
| UPLOAD_UI_005 | Select radio → interact with page → verify radio persists |

### Estimated Effort: 8 hours
### Risk: Medium (Dropzone async behaviour, file creation, download handling)
### Expected Outcome: 28 tests collected, majority PASS

---

# PHASE 4 — COVERAGE VERIFICATION

## Objective: Verify 28/28 tests collected + E2E unaffected

### Actions

| # | Action | Command |
|---|--------|---------|
| 1 | Collect all tests | `python -m pytest tests/regression/upload_documents/ --collect-only -q` |
| 2 | Verify 28 items | Expected: "28 tests collected" |
| 3 | Verify E2E | `python -m pytest tests/test_preliminary_form_main.py --collect-only -q` |
| 4 | Run sanity subset | `python -m pytest tests/regression/upload_documents/ -k "VAL_001 or POS_001 or POS_007 or NEG_001 or NEG_002 or NEG_004 or UI_002 or UI_004"` |
| 5 | Verify markers | `python -m pytest --markers` → `upload_documents` present |

### Estimated Effort: 1 hour
### Risk: Low

---

# PHASE 5 — ALLURE VERIFICATION

## Objective: Verify Allure report hierarchy + attachments

### Verification Points

| # | Check |
|---|-------|
| 1 | Parent Suite: "CISCE E-Affiliation" |
| 2 | Suite: "Upload Documents" |
| 3 | Sub-suites: Validation, Positive, Negative, Boundary, UI |
| 4 | Screenshots attached on failure |
| 5 | Validation messages captured in Allure |
| 6 | Severity levels correct (Critical/Normal) |
| 7 | Tags: regression, upload_documents, positive/negative/boundary/validation |

### Estimated Effort: 30 minutes
### Risk: Low

---

# GRAND SUMMARY

## Files to Create (12)

| # | File | Purpose |
|---|------|---------|
| 1 | `tests/regression/upload_documents/__init__.py` | Package |
| 2 | `tests/regression/upload_documents/validation/__init__.py` | Package |
| 3 | `tests/regression/upload_documents/validation/test_upload_validation.py` | 3 tests |
| 4 | `tests/regression/upload_documents/positive/__init__.py` | Package |
| 5 | `tests/regression/upload_documents/positive/test_upload_positive.py` | 9 tests |
| 6 | `tests/regression/upload_documents/negative/__init__.py` | Package |
| 7 | `tests/regression/upload_documents/negative/test_upload_negative.py` | 7 tests |
| 8 | `tests/regression/upload_documents/boundary/__init__.py` | Package |
| 9 | `tests/regression/upload_documents/boundary/test_upload_boundary.py` | 4 tests |
| 10 | `tests/regression/upload_documents/ui/__init__.py` | Package |
| 11 | `tests/regression/upload_documents/ui/test_upload_ui.py` | 5 tests |
| 12 | `test_data/test_upload.exe` | Minimal invalid file for NEG_001 |

**Total new files: 12**

## Files to Extend (3)

| # | File | Change |
|---|------|--------|
| 1 | `pages/upload_documents_page.py` | Add 7 regression methods at bottom |
| 2 | `conftest.py` | Add `upload_ready_page` fixture |
| 3 | `pytest.ini` | Register `upload_documents` marker |
| 4 | `test_data/negative/Validation_Data.xlsx` | Add 4 sheets |

**Total extended files: 4**

## New Page Methods: 7

| # | Method | Purpose |
|---|--------|---------|
| 1 | `upload_single_file(document_label, file_path)` | Upload to specific dropzone |
| 2 | `upload_all_documents(file_path)` | Upload to all 5 |
| 3 | `select_affiliation_type(label)` | Select radio |
| 4 | `check_declarations()` | Check both checkboxes |
| 5 | `fill_comments(text)` | Fill textarea |
| 6 | `click_proceed()` | Click Proceed button |
| 7 | `get_upload_status(dropzone_id)` | Check upload state |

## Existing Methods Reused: 6

| Method | From |
|--------|------|
| `upload_documents(data)` | E2E method — NOT used, NOT modified |
| `ValidationHelper.get_all_errors()` | All modules |
| `ValidationHelper.assert_error_present()` | Negative tests |
| `ScreenshotUtil.take_screenshot()` | All tests |
| `ExcelReader.get_sheet_data()` | Parametrized tests |
| `school_details_ready_page` fixture | Base fixture chain |

## Existing Methods Left Untouched

| Method/File | Status |
|-------------|--------|
| `upload_documents(data)` | 🔒 E2E — LOCKED |
| `test_preliminary_form_main.py` | 🔒 LOCKED |
| `conftest.py` existing fixtures | 🔒 LOCKED |
| All other page objects | 🔒 LOCKED |
| All other test files | 🔒 LOCKED |

---

## Estimated Implementation Effort

| Phase | Effort |
|-------|--------|
| Phase 1 — Framework | 2.5 hrs |
| Phase 2 — Excel data | 1 hr |
| Phase 3 — Core automation | 8 hrs |
| Phase 4 — Coverage verification | 1 hr |
| Phase 5 — Allure verification | 30 min |
| **TOTAL** | **~13 hrs** |

---

## Expected Execution Time

| Suite | Tests | Time |
|-------|-------|------|
| Sanity (build verification) | 7 | ~3.5 min |
| Full Regression | 28 | ~20 min |

---

## Risk Summary

| Phase | Risk | Mitigation |
|-------|------|-----------|
| 1 (Framework) | Low | Proven patterns from Land Certificate |
| 2 (Excel) | Low | Data entry only |
| 3 (Automation) | Medium | Dropzone async, file generation, download handling |
| 4 (Verification) | Low | Collection only |
| 5 (Allure) | Low | Report generation |

---

## Backward Compatibility: ✅ CONFIRMED

| Check | Guaranteed |
|-------|-----------|
| `test_preliminary_form_main.py` unchanged | ✅ |
| `upload_documents(data)` E2E method unchanged | ✅ |
| Existing locators unchanged | ✅ |
| Existing fixtures unchanged | ✅ |
| Existing Excel data (Master/Schools sheets) unchanged | ✅ |
| E2E execution flow identical | ✅ |
| All other modules (School/Address/NOC/Trust/Land) unchanged | ✅ |

---

## ✅ End-to-End automation remains 100% unchanged.

---

**STATUS:** Implementation plan complete. Ready for phased execution starting Phase 1.
