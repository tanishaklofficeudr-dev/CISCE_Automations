# Upload Documents Module — Complete Functional Analysis Report

---

# 1. MODULE OVERVIEW

The Upload Documents page is the final step before payment in the Preliminary Affiliation workflow. It contains:
- 5 mandatory file upload controls (Dropzone.js)
- 1 textarea for additional comments
- 4 radio buttons for affiliation type selection
- 2 declaration checkboxes
- 1 "Proceed to Payment" button
- 1 "Back" button
- Download for Notarization link (needs investigation)
- Payment flow (post-submission)

---

# 2. COMPLETE DECISION TREE

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     UPLOAD DOCUMENTS MODULE                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │  SECTION A: FILE UPLOADS (5 mandatory)                       │          │
│  │  1. NOC Document *                                           │          │
│  │  2. Certificate of Land *                                    │          │
│  │  3. Trust / Society / Company Document *                     │          │
│  │  4. Land Ownership Document *                                │          │
│  │  5. School Image *                                           │          │
│  └─────────────────────────────────────────────────────────────┘          │
│                           ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │  SECTION B: DOWNLOAD FOR NOTARIZATION                        │          │
│  │  (Link/Button — generates downloadable form)                 │          │
│  └─────────────────────────────────────────────────────────────┘          │
│                           ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │  SECTION C: COMMENTS TEXTAREA                                │          │
│  │  "Any relevant information that the school wants to provide" │          │
│  │  (Optional — no maxlength, no minlength)                     │          │
│  └─────────────────────────────────────────────────────────────┘          │
│                           ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │  SECTION D: AFFILIATION TYPE (4 radio options)               │          │
│  │  ○ Provisional Affiliation up to Class X (value=2)           │          │
│  │  ○ Composite Affiliation up to Class XII (value=3)           │          │
│  │  ○ Switch Over Category up to Class X (value=4)              │          │
│  │  ○ Switch Over Category up to Class XII (value=5)            │          │
│  └─────────────────────────────────────────────────────────────┘          │
│                           ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │  SECTION E: DECLARATION CHECKBOXES (2 mandatory)             │          │
│  │  ☐ #verify_composite                                         │          │
│  │  ☐ #verify                                                   │          │
│  └─────────────────────────────────────────────────────────────┘          │
│                           ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │  SECTION F: PROCEED TO PAYMENT                               │          │
│  │  [Proceed to Payment] button                                 │          │
│  │  Navigates → /payment → bank selection → QR → Success        │          │
│  └─────────────────────────────────────────────────────────────┘          │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

---

# 3. SECTION 1 — DOCUMENT UPLOADS (Detailed)

## 3.1 Upload Controls Inventory

| # | Document | Dropzone ID | Accepted Files | Max Size | Max Files | Multiple | Mandatory |
|---|----------|-------------|----------------|----------|-----------|----------|-----------|
| 1 | NOC Document | `#noc` | jpeg, bmp, gif, png, pdf | **20 MB** | 1 | No | **Yes** (*) |
| 2 | Certificate of Land | `#land_certificate` | jpeg, bmp, gif, png, pdf | **20 MB** | 1 | No | **Yes** (*) |
| 3 | Trust / Society / Company Document | `#trust` | jpeg, bmp, gif, png, pdf | **20 MB** | 1 | No | **Yes** (*) |
| 4 | Land Ownership Document | `#land` | jpeg, bmp, gif, png, pdf | **20 MB** | 1 | No | **Yes** (*) |
| 5 | School Image | `#school_image` | jpeg, **jpg**, png, pdf | **20 MB** | 1 | No | **Yes** (*) |

**Key observation:** School Image does NOT accept BMP or GIF — only JPEG/JPG/PNG/PDF. All other 4 uploads accept BMP and GIF additionally.

## 3.2 Upload Technology: Dropzone.js

| Property | Value |
|----------|-------|
| Library | Dropzone.js |
| Upload URL | `https://dev-eaffiliation.cisce.org/preliminary/school/upload-documents` |
| paramName | `file` |
| uploadMultiple | false |
| Auto-upload | Yes (immediate on file selection) |
| Click-to-upload | Yes (`.dz-clickable` class) |
| Drag & Drop | Yes (Dropzone default) |
| Preview | Yes (`dz-preview` generated after upload) |
| Remove button | Yes (`.dz-remove` available) |

## 3.3 Per-Upload Behaviour Analysis

| Behaviour | Status | Notes |
|-----------|--------|-------|
| Replace existing file | Needs investigation | maxFiles=1 suggests replacing |
| Delete uploaded file | ✅ Available | `.dz-remove` button present |
| Preview after upload | ✅ Dropzone creates preview | `.dz-preview` |
| Download uploaded file | Needs investigation | May have download link |
| Upload progress | ✅ Dropzone default | Progress bar built-in |
| Invalid file type rejection | ✅ Client-side via `acceptedFiles` | Dropzone shows error message |
| Zero-byte file | Needs investigation | May pass client, fail server |
| Corrupted file | Needs investigation | Likely passes to server |
| File size > 20MB | ✅ Blocked | Dropzone `maxFilesize` enforcement |
| Duplicate upload (same file) | Needs investigation | maxFiles=1 — may replace |

## 3.4 Automation Approach (from existing E2E)

```python
container = page.locator("div.col-lg-6", has_text="NOC Document")
with page.expect_file_chooser() as fc_info:
    container.locator("#noc").click()
fc_info.value.set_files(file_path)
```

**Pattern:** Click dropzone element → expect_file_chooser → set_files
**Confirmed working** in E2E for all 5 uploads.

---

# 4. SECTION 2 — DOWNLOAD FOR NOTARIZATION

| Property | Finding |
|----------|---------|
| Element type | Needs DOM investigation (link or button) |
| Label | "Download for Notarization" (based on module requirement) |
| Visibility | Not captured in initial scan — may be conditional |
| File format | Likely PDF |
| Behaviour | Download a notarization form document |

**Status:** Needs further investigation — element may appear only after all uploads complete, or may be a link generated server-side.

---

# 5. SECTION 3 — COMMENTS TEXTAREA

| Property | Value |
|----------|-------|
| Locator | `get_by_role("textbox", name="Any relevant information that")` |
| ID | Not found on visible textareas — likely a dynamically rendered field |
| Mandatory | **No** (`required=False`) |
| maxLength | -1 (unlimited) |
| minLength | -1 (none) |
| Rows | Unknown (not in captured visible textareas) |
| Placeholder | Not captured |

**Note:** The two textareas found (`#owner_name` and `#plot_explanation`) are HIDDEN and belong to Certificate of Land module (SPA keeps them in DOM). The comments textarea may be rendered differently — possibly a contenteditable div or dynamically created after scroll.

**E2E approach (confirmed working):**
```python
page.get_by_role("textbox", name="Any relevant information that").fill(data["comments"])
```

---

# 6. SECTION 4 — AFFILIATION TYPE

| # | Option | name | value | Default | Mandatory |
|---|--------|------|-------|---------|-----------|
| 1 | Provisional Affiliation up to Class X | `composite_type` | `2` | No | Yes (one must be selected) |
| 2 | Composite Affiliation up to Class XII | `composite_type` | `3` | No | |
| 3 | Affiliation Under Switch Over Category up to Class X | `composite_type` | `4` | No | |
| 4 | Affiliation Under Switch Over Category up to Class XII | `composite_type` | `5` | No | |

**No default selection** — none are checked initially.

**E2E approach (confirmed):**
```python
page.get_by_label(data["affiliation_type"]).check(force=True)
```

**Potential business rules:**
- Is the selection dependent on other form data (e.g., trust type, school category)?
- Does selecting "Switch Over" require additional documentation?
- Can the selection be changed after initial submission?

---

# 7. SECTION 5 — DECLARATION CHECKBOXES

| # | ID | Mandatory | Default | Label |
|---|-----|-----------|---------|-------|
| 1 | `#verify_composite` | Yes (assumed — blocks payment if unchecked) | Unchecked | (Label text not captured — likely declaration statement) |
| 2 | `#verify` | Yes (assumed) | Unchecked | (Label text not captured) |

**E2E approach:**
```python
page.locator("#verify_composite").check(force=True)
page.locator("#verify").check(force=True)
```

**`force=True` used** — suggests the checkboxes may be visually obscured or have a custom UI layer. The underlying `<input type="checkbox">` is programmatically checked.

---

# 8. SECTION 6 — PROCEED TO PAYMENT

| Property | Value |
|----------|-------|
| Button text | "Proceed to Payment" |
| Type | `button` (not submit) |
| ID | None |
| Disabled state | Not disabled by default |
| Locator | `get_by_role("button", name="Proceed to Payment")` |

**Behaviour when clicked:**
- If all conditions met → Navigates to `/payment` page
- If conditions not met → Likely shows validation errors or alert

**Conditions (assumed):**
1. All 5 documents uploaded
2. Affiliation type selected
3. Both checkboxes checked

**E2E uses `force=True`:**
```python
page.get_by_role("button", name="Proceed to Payment").click(force=True)
```
This bypasses any disabled state — suggests the button may be conditionally disabled.

---

# 9. SECTION 7 — END-TO-END BEHAVIOUR

| Behaviour | Status |
|-----------|--------|
| Upload order dependency | Likely none — each is independent |
| All documents required | **Yes** (all marked with *) |
| Replace document affects submission | Needs investigation |
| Uploads persist after Back button | Likely YES (server-side storage) |
| Uploads persist after page Refresh | Likely YES (async upload to server) |
| Uploads persist after re-login | Likely YES (stored against application) |

---

# 10. SECTION 8 — DYNAMIC BEHAVIOUR

| Dynamic Aspect | Evidence |
|----------------|----------|
| Upload preview appears after file selection | Dropzone.js creates `.dz-preview` |
| Remove button appears after upload | `.dz-remove` available |
| Proceed button may enable after all uploads | Uses `force=True` in E2E — suggests conditional |
| Affiliation type may affect required documents | Not confirmed — needs investigation |
| Checkboxes may be conditionally required | Both always visible |
| Download for Notarization may appear after uploads | Not visible in initial scan |

---

# 11. SECTION 9 — AUTOMATION RISKS

| # | Risk | Severity | Description | Mitigation |
|---|------|----------|-------------|-----------|
| 1 | Dropzone.js async upload | High | Files upload immediately via XHR — must wait for completion | Wait for `.dz-success` class or network idle |
| 2 | File chooser dialog handling | Medium | Must use `expect_file_chooser()` pattern | Existing E2E pattern works |
| 3 | No element IDs on file inputs | Medium | Dropzone creates hidden file inputs — no stable IDs | Use container-based locators (existing pattern) |
| 4 | force=True on checkbox/button | Medium | Custom UI may block normal clicks | Keep using `force=True` |
| 5 | Payment gateway iframe | High | External payment in iframe — fragile | Existing E2E handles with `content_frame` |
| 6 | Upload validation timing | Medium | Server validates asynchronously | Wait after each upload |
| 7 | Large file upload timeout | Low | 20MB files may take time over slow network | Use small test files |
| 8 | Drag & Drop testing | Low | Hard to automate reliably | Use click-to-upload (proven) |
| 9 | SPA DOM pollution | Low | Previous module fields visible but hidden | Use specific container locators |
| 10 | Browser download dialog | Medium | "Download for Notarization" may trigger browser dialog | Use download event handling |

---

# 12. LIST OF EVERY UI CONTROL

| # | Control | Type | Section | ID/Locator |
|---|---------|------|---------|-----------|
| 1 | NOC Document upload | Dropzone | Upload | `#noc` |
| 2 | Certificate of Land upload | Dropzone | Upload | `#land_certificate` |
| 3 | Trust Document upload | Dropzone | Upload | `#trust` |
| 4 | Land Ownership upload | Dropzone | Upload | `#land` |
| 5 | School Image upload | Dropzone | Upload | `#school_image` |
| 6 | Comments textarea | Textarea | Comments | `get_by_role("textbox", name="Any relevant...")` |
| 7 | Provisional Affiliation radio | Radio | Affiliation | `name='composite_type' value='2'` |
| 8 | Composite Affiliation radio | Radio | Affiliation | `name='composite_type' value='3'` |
| 9 | Switch Over X radio | Radio | Affiliation | `name='composite_type' value='4'` |
| 10 | Switch Over XII radio | Radio | Affiliation | `name='composite_type' value='5'` |
| 11 | Declaration checkbox 1 | Checkbox | Declaration | `#verify_composite` |
| 12 | Declaration checkbox 2 | Checkbox | Declaration | `#verify` |
| 13 | Proceed to Payment button | Button | Action | `get_by_role("button", name="Proceed to Payment")` |
| 14 | Back button | Button | Navigation | `get_by_role("button", name="Back")` |
| 15 | Download for Notarization | Link/Button | Download | Needs investigation |

**Total: 15 UI controls**

---

# 13. LIST OF EVERY DEPENDENCY

| # | Dependency | Type |
|---|-----------|------|
| 1 | All 5 uploads must be complete before Proceed | Upload → Button |
| 2 | Both checkboxes must be checked before Proceed | Checkbox → Button |
| 3 | Affiliation type must be selected before Proceed | Radio → Button |
| 4 | Upload uses async XHR — must wait for completion | Upload → Validation |
| 5 | Proceed button may be disabled until conditions met | Conditions → Button state |
| 6 | Payment page requires all prior steps complete | Proceed → Payment |
| 7 | Download for Notarization may require uploads complete | Upload → Download |

---

# 14. LIST OF EVERY VALIDATION

| # | Validation | Trigger | Expected |
|---|-----------|---------|----------|
| 1 | File type not accepted | Upload invalid type (e.g., .exe) | Dropzone error message |
| 2 | File size > 20MB | Upload large file | Dropzone error message |
| 3 | Affiliation type not selected | Click Proceed without radio | Form blocks or alert |
| 4 | Checkboxes not checked | Click Proceed without checkboxes | Form blocks or alert |
| 5 | Missing upload | Click Proceed without all 5 uploads | Form blocks or alert |
| 6 | Empty textarea | Click Proceed | May accept (not mandatory) |
| 7 | maxFiles exceeded (upload second file) | Upload to already-occupied dropzone | Dropzone blocks or replaces |

---

# 15. LIST OF EVERY UPLOAD SCENARIO

| # | Scenario | Category |
|---|----------|----------|
| 1 | Valid PDF upload (each control) | Positive |
| 2 | Valid JPEG upload | Positive |
| 3 | Valid PNG upload | Positive |
| 4 | Valid BMP upload (where accepted) | Positive |
| 5 | Valid GIF upload (where accepted) | Positive |
| 6 | Invalid file type (.exe, .docx, .txt) | Negative |
| 7 | File > 20MB | Negative |
| 8 | Zero-byte file | Negative |
| 9 | File exactly 20MB | Boundary |
| 10 | Very small file (1 byte) | Boundary |
| 11 | Upload, delete, re-upload | Positive |
| 12 | Upload, replace with new file | Positive |
| 13 | Upload then navigate Back, return | Persistence |
| 14 | Upload then refresh page | Persistence |
| 15 | Upload all 5 in sequence | Positive (E2E) |
| 16 | Only partial uploads (1-4 of 5) | Negative |
| 17 | Drag & drop upload | Positive (risky to automate) |
| 18 | Corrupted file (invalid header) | Edge case |
| 19 | File with special characters in name | Edge case |
| 20 | School Image with BMP (not accepted) | Negative |

---

# 16. POTENTIAL APPLICATION DEFECTS

| # | Potential Defect | Reason |
|---|-----------------|--------|
| 1 | School Image doesn't accept BMP/GIF while others do | Inconsistent accepted types |
| 2 | `force=True` needed for Proceed button | Button may be incorrectly disabled |
| 3 | No `required` attribute on file inputs | Client-side mandatory not enforced via HTML |
| 4 | No maxLength on textarea | Unlimited text input possible |
| 5 | Checkboxes have no visible label text captured | Accessibility issue |
| 6 | File inputs have no IDs | Automation/accessibility concern |
| 7 | No explicit "all uploads required" validation message | Unclear UX for missing uploads |

---

# 17. RECOMMENDED IMPLEMENTATION PHASES

| Phase | Scope | Tests (Est.) | Effort |
|-------|-------|-------------|--------|
| **Phase 1** | Valid upload flow (all 5 docs + comment + radio + checkboxes + proceed) | 3-5 | 4 hrs |
| **Phase 2** | Negative uploads (invalid type, size, missing docs) | 5-8 | 3 hrs |
| **Phase 3** | Boundary (file size limits, text field limits) | 3-5 | 2 hrs |
| **Phase 4** | Dynamic UI (upload/delete/replace, preview, progress) | 4-6 | 3 hrs |
| **Phase 5** | Declaration & affiliation validation | 3-4 | 2 hrs |
| **Phase 6** | Persistence (back/refresh/re-login) | 2-3 | 2 hrs |
| **TOTAL** | | **~25-30 tests** | **~16 hrs** |

---

# 18. DIAGNOSTICS NEEDED BEFORE IMPLEMENTATION

| # | What | Why |
|---|------|-----|
| 1 | What happens when clicking Proceed without all uploads | Validation message? Alert? |
| 2 | What happens with invalid file type upload | Dropzone message or server error? |
| 3 | What happens when uploading > 20MB | Client-side or server-side rejection? |
| 4 | Does Download for Notarization link exist? Where? | Not found in initial scan |
| 5 | Are checkboxes mandatory for Proceed | Does button disable without them? |
| 6 | Does replacing an upload work correctly | maxFiles=1 — overwrite or block? |
| 7 | What validation messages appear for missing uploads | Exact text needed |
| 8 | Is textarea mandatory at all | Submit with blank comments |
| 9 | Upload persistence after navigation | Back button → return |

---

**STATUS:** Functional analysis complete. Ready for diagnostic phase before implementation.
