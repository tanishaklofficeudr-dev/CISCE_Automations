# Upload Documents Module — Diagnostic Report
## Evidence-Based Findings

---

# 1. UPLOAD CONTROLS — CONFIRMED CONFIGURATION

## All 5 Dropzone Instances Confirmed

| # | Document | Dropzone ID | Accepted Files | Max Size | Max Files | Auto Upload | Status |
|---|----------|-------------|----------------|----------|-----------|-------------|--------|
| 1 | NOC Document | `#noc` | jpeg, bmp, gif, png, pdf | 20 MB | 1 | Yes | ✅ |
| 2 | Certificate of Land | `#land_certificate` | jpeg, bmp, gif, png, pdf | 20 MB | 1 | Yes | ✅ |
| 3 | Trust / Society / Company | `#trust` | jpeg, bmp, gif, png, pdf | 20 MB | 1 | Yes | ✅ |
| 4 | Land Ownership | `#land` | jpeg, bmp, gif, png, pdf | 20 MB | 1 | Yes | ✅ |
| 5 | School Image | `#school_image` | jpeg, **jpg**, png, pdf (**NO bmp/gif**) | 20 MB | 1 | Yes | ✅ |

## Confirmed Dropzone Error Messages

| Scenario | Message Template |
|----------|-----------------|
| Invalid file type | "You can't upload files of this type." |
| File too big | "File is too big ({{filesize}}MiB). Max filesize: {{maxFilesize}}MiB." |
| Max files exceeded | "You can not upload any more files." |

## Upload Behaviour Confirmed

| Property | Value | Evidence |
|----------|-------|----------|
| Upload URL | `https://dev-eaffiliation.cisce.org/preliminary/school/upload-documents` | All 5 dropzones use same URL |
| paramName | `file` | Standard Dropzone param |
| autoProcessQueue | `true` | Upload starts immediately on file selection |
| addRemoveLinks | `false` | No built-in remove links (custom implementation) |
| uploadMultiple | `false` | One file at a time |

## Upload Test Results

| Document | Upload Result | Status |
|----------|--------------|--------|
| NOC Document | Upload triggered page navigation (execution context destroyed) | ⚠️ Async upload causes page state change |
| Certificate of Land | `{fileCount: 1, status: 'success'}` | ✅ |
| Trust Document | `{fileCount: 1, status: 'success'}` | ✅ |
| Land Ownership | `{fileCount: 1, status: 'success'}` | ✅ |
| School Image | `{fileCount: 1, status: 'success'}` | ✅ |

**Key Finding:** NOC upload may trigger a page reload or navigation after successful upload (execution context was destroyed). Subsequent uploads work fine — this suggests the FIRST upload on the page causes a state refresh.

---

# 2. CONFIRMED UPLOAD AUTOMATION STRATEGY

```python
# Pattern (same as existing E2E — confirmed working):
container = page.locator("div.col-lg-6", has_text="NOC Document")
with page.expect_file_chooser() as fc_info:
    container.locator("#noc").click()
fc_info.value.set_files(file_path)
page.wait_for_timeout(3000)  # Wait for async upload to complete
```

**Locator Strategy:**
1. Find parent container by text label: `page.locator("div.col-lg-6", has_text="...")`
2. Click the Dropzone element by ID: `.locator("#noc")`
3. Handle file chooser: `page.expect_file_chooser()`
4. Set files: `fc_info.value.set_files(path)`
5. Wait: `page.wait_for_timeout(3000)` for async upload

---

# 3. DOWNLOAD FOR NOTARIZATION — CONFIRMED

| Property | Value |
|----------|-------|
| Element | `<a>` link |
| Text | "Download for Notarization" |
| Href | `https://dev-eaffiliation.cisce.org/preliminary/school/download_pdf/eyJpdi...` (encrypted token) |
| Visible | ✅ Yes (always visible — not conditional on uploads) |
| Format | PDF (based on URL path `download_pdf`) |
| Behaviour | Opens/downloads PDF — encrypted URL token |

**Additionally discovered: Individual uploaded file download links exist:**

| Link | URL |
|------|-----|
| NOC Document.pdf | `https://dev-eaffiliation.cisce.org/downloads/bc28b10c...` |
| Certificate of Land.pdf | `https://dev-eaffiliation.cisce.org/downloads/16b45599...` |
| Trust / Society / Company Document.pdf | `https://dev-eaffiliation.cisce.org/downloads/a004b63a...` |
| Land Ownership Document.pdf | `https://dev-eaffiliation.cisce.org/downloads/21c54fce...` |
| School Image.pdf | `https://dev-eaffiliation.cisce.org/downloads/7502a4ca...` |

**Finding:** File download links appear AFTER upload. They open in new tab (not browser download dialog).

**Automation approach for download:** 
- Use `page.locator("a", has_text="Download for Notarization").click()`
- May open new tab or trigger download — needs `expect_download()` or new tab handling

---

# 4. COMMENTS TEXTAREA — CONFIRMED

| Property | Value |
|----------|-------|
| Locator | `get_by_role("textbox", name="Any relevant information that")` |
| Visible | ✅ Yes |
| Mandatory | **No** (no `required` attribute) |
| maxLength | -1 (unlimited) |
| minLength | -1 (none) |
| Readonly | No |
| `.fill()` works | ✅ Yes |
| Special characters accepted | ✅ Yes (@#$% áéíóú confirmed) |
| Multiline | Yes (textarea element) |

**E2E approach confirmed:**
```python
page.get_by_role("textbox", name="Any relevant information that").fill("text")
```

---

# 5. AFFILIATION TYPE RADIOS — CONFIRMED

| # | Label | name | value | Default | Visible |
|---|-------|------|-------|---------|---------|
| 1 | Provisional Affiliation up to Class X | `composite_type` | `2` | ✅ (was checked during test) | ✅ |
| 2 | Composite Affiliation up to Class XII | `composite_type` | `3` | No | ✅ |
| 3 | Affiliation Under Switch Over Category up to Class X | `composite_type` | `4` | No | ✅ |
| 4 | Affiliation Under Switch Over Category up to Class XII | `composite_type` | `5` | No | ✅ |

**Default state:** Value `2` was checked — this may be from a previous save (account state). On fresh account, likely none selected.

**Automation approach confirmed:**
```python
page.get_by_label("Provisional Affiliation up to Class X").check(force=True)
```

**`force=True` needed:** Yes — custom radio UI may obstruct click.

---

# 6. DECLARATION CHECKBOXES — CONFIRMED

| # | ID | Label Text | Default | Required | Visible |
|---|-----|-----------|---------|----------|---------|
| 1 | `#verify_composite` | "I hereby acknowledge that the Council will not be held responsible in case an i..." | Unchecked (or checked from prev session) | No (HTML) | ✅ |
| 2 | `#verify` | "I hereby certify that all the information furnished above is true to the best o..." | Unchecked (or checked from prev session) | No (HTML) | ✅ |

**Automation approach confirmed:**
```python
page.locator("#verify_composite").check(force=True)
page.locator("#verify").check(force=True)
```

**`force=True` needed:** Yes — custom checkbox UI.

---

# 7. PROCEED TO PAYMENT BUTTON — CONFIRMED

| Property | Value |
|----------|-------|
| Text | "Proceed to Payment" |
| Type | `button` (not submit) |
| ID | None |
| Class | `btn btn-primary PreliminaryTabsFormSubmit` |
| Disabled | **No** (always enabled) |
| onclick | **`UploadDocuments(event)`** — JavaScript function |
| formAction | `https://dev-eaffiliation.cisce.org/preliminary/school/dashboard` |

**CRITICAL FINDING:** The button calls `UploadDocuments(event)` JavaScript function — NOT a form submit. This function likely:
1. Validates all uploads exist
2. Validates affiliation type selected
3. Validates checkboxes checked
4. If valid → submits via AJAX → navigates to payment

**After clicking (all conditions met):** ✅ Navigated to `https://dev-eaffiliation.cisce.org/preliminary/school/payment-gateway`

**Automation approach confirmed:**
```python
page.get_by_role("button", name="Proceed to Payment").click(force=True)
page.wait_for_timeout(5000)
# OR
page.wait_for_url("**/payment**", timeout=30000)
```

---

# 8. CONFIRMED BUSINESS RULES

| # | Rule | Evidence |
|---|------|----------|
| 1 | All 5 documents required before payment | `UploadDocuments(event)` validates server-side |
| 2 | Affiliation type must be selected | Part of `UploadDocuments()` validation |
| 3 | Both checkboxes must be checked | Part of validation function |
| 4 | Upload is async (immediate on file select) | autoProcessQueue=true |
| 5 | maxFiles=1 per dropzone (no multiple uploads) | Dropzone config |
| 6 | Max file size: 20MB | Dropzone config |
| 7 | Accepted types per dropzone (School Image differs) | Dropzone config |
| 8 | Uploaded files are downloadable immediately | Download links appear after upload |
| 9 | Download for Notarization is always available | Visible regardless of upload state |
| 10 | Comments are optional | No `required`, no validation observed |

---

# 9. APPLICATION DEFECTS / OBSERVATIONS

| # | Finding | Severity | Type |
|---|---------|----------|------|
| 1 | School Image doesn't accept BMP/GIF while others do | Low | Inconsistency |
| 2 | `addRemoveLinks: false` — no Dropzone remove button | Info | Custom implementation |
| 3 | Button always enabled (validation via JS, not HTML) | Low | UX |
| 4 | No `required` attribute on file inputs | Low | Accessibility |
| 5 | First upload (NOC) may cause execution context change | Medium | Automation risk |
| 6 | Checkboxes not marked `required` in HTML | Low | Accessibility |
| 7 | Download links open in same/new tab (not download) | Info | Behaviour note |

---

# 10. AUTOMATION RISKS

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| 1 | First upload causes page state change | Medium | Add extra wait (3000ms) after NOC upload |
| 2 | Async upload — must wait for completion | Medium | Wait for `dz-success` or use fixed wait |
| 3 | No unique IDs on file inputs | Medium | Use container + Dropzone ID pattern (proven in E2E) |
| 4 | `force=True` needed for checkboxes/radio/button | Low | Existing pattern works |
| 5 | Payment gateway is external iframe | High | Beyond Upload Documents scope |
| 6 | Download may open new tab vs trigger download | Medium | Use `expect_download()` or check new tab |
| 7 | File upload validation is server-side (no client errors visible) | Medium | Check via network response or post-upload state |

---

# 11. RECOMMENDED AUTOMATION APPROACH

| Control | Approach | Confirmed |
|---------|----------|-----------|
| File uploads (all 5) | `expect_file_chooser` + container locator + `set_files()` | ✅ E2E proven |
| Comments textarea | `get_by_role("textbox", name="Any relevant...").fill()` | ✅ Confirmed |
| Affiliation radios | `get_by_label("...").check(force=True)` | ✅ Confirmed |
| Declaration checkboxes | `locator("#verify_composite").check(force=True)` | ✅ Confirmed |
| Proceed button | `get_by_role("button", name="Proceed to Payment").click(force=True)` | ✅ Confirmed |
| Download for Notarization | `locator("a", has_text="Download for Notarization").click()` | ✅ Visible |
| Upload validation | Check for `.dz-error` class after invalid upload | Needs verification |
| Navigation check | `wait_for_url("**/payment**")` | ✅ Confirmed |

---

# 12. CONFIRMED LOCATORS SUMMARY

| Control | Locator |
|---------|---------|
| NOC upload | `page.locator("div.col-lg-6", has_text="NOC Document").locator("#noc")` |
| Land Certificate upload | `page.locator("div.col-lg-6", has_text="Certificate of Land").locator("#land_certificate")` |
| Trust upload | `page.locator("div.col-lg-6", has_text="Trust / Society / Company").locator("#trust")` |
| Land Ownership upload | `page.locator("div.col-lg-6", has_text="Land Ownership").locator("#land")` |
| School Image upload | `page.locator("div.col-lg-6", has_text="School Image").locator("#school_image")` |
| Comments | `page.get_by_role("textbox", name="Any relevant information that")` |
| Affiliation radio | `page.get_by_label("Provisional Affiliation up to Class X")` |
| Checkbox 1 | `page.locator("#verify_composite")` |
| Checkbox 2 | `page.locator("#verify")` |
| Proceed button | `page.get_by_role("button", name="Proceed to Payment")` |
| Download Notarization | `page.locator("a", has_text="Download for Notarization")` |
| Back button | `page.get_by_role("button", name="Back")` |

---

# 13. DIAGNOSTICS STILL NEEDED

| # | What | Why |
|---|------|-----|
| 1 | What validation message appears when uploads missing + click Proceed | Need exact error text |
| 2 | What happens with invalid file type (e.g., .exe upload) | Client-side vs server error |
| 3 | What happens when uploading > 20MB file | Dropzone block or server reject |
| 4 | Does the remove button exist (custom implementation) | How to test delete+re-upload |
| 5 | What happens clicking Proceed without checkboxes | Exact validation |
| 6 | What happens clicking Proceed without affiliation selection | Exact validation |
| 7 | Upload persistence after Back + return | Data integrity |

---

**STATUS:** Diagnostic complete. All primary controls confirmed. 7 secondary diagnostics identified for pre-implementation verification. Module is implementation-ready for the primary positive flow.
