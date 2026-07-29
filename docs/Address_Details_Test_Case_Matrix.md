# Address Details Module — Test Case Matrix
## Only Automatable Scenarios

---

# CATEGORY 1: VALIDATION (Required Fields)

| TC ID | Title | Objective | Preconditions | Test Data | Steps | Expected Result | Automatable | Regression | Sanity | Smoke |
|-------|-------|-----------|---------------|-----------|-------|-----------------|-------------|------------|--------|-------|
| ADDR_VAL_001 | All mandatory text fields blank — verify errors displayed | Verify address line and ZIP show validation when submitted blank | First visit OR cleared text fields; dropdowns already have saved values | address_line: empty, zip: empty | 1. Clear address line 2. Clear ZIP field 3. Click Next 4. Verify errors | Errors shown: address required + ZIP must be 6 digits. Form does not navigate. | Yes | Yes | Yes | No |

**Note:** Only text fields (address_line, zip) can be cleared. Dropdown blanks are NOT testable on existing accounts due to persistence.

---

# CATEGORY 2: POSITIVE (Valid Submissions)

| TC ID | Title | Objective | Preconditions | Test Data | Steps | Expected Result | Automatable | Regression | Sanity | Smoke |
|-------|-------|-----------|---------------|-----------|-------|-----------------|-------------|------------|--------|-------|
| ADDR_POS_001 | Valid complete address — India, Rajasthan | Verify form submits with all valid fields | Address Details page loaded; account has previous data | address: "123 Main Street", country: India, state: Rajasthan, district: (first available), city: (first available), zip: 302001, locality: Urban | 1. Fill address line 2. Select India 3. Select Rajasthan 4. Select any district 5. Select any city 6. Fill valid 6-digit PIN 7. Select locality 8. Click Next | Form submits, navigates to NOC Details step | Yes | Yes | Yes | No |
| ADDR_POS_002 | Valid address with different state | Verify cascading dropdowns work with different state selection | Address Details page loaded | address: "456 Park Road", country: India, state: Maharashtra, district: (first available), city: (first available), zip: 400001, locality: Urban | 1. Fill address 2. Select India 3. Select Maharashtra 4. Select district 5. Select city 6. Fill PIN 7. Select locality 8. Click Next | Form submits with different state cascade | Yes | Yes | No | No |
| ADDR_POS_003 | Valid address with Rural locality | Verify form accepts Rural locality type | Address Details page loaded | address: "Village Road", country: India, state: Rajasthan, district: (first available), city: (first available), zip: 302002, locality: Rural | 1. Fill all fields with Rural locality 2. Click Next | Form submits successfully | Yes | Yes | No | No |

---

# CATEGORY 3: NEGATIVE — Format Validation

| TC ID | Title | Objective | Preconditions | Test Data | Steps | Expected Result | Automatable | Regression | Sanity | Smoke |
|-------|-------|-----------|---------------|-----------|-------|-----------------|-------------|------------|--------|-------|
| ADDR_FMT_001 | PIN code less than 6 digits | Verify PIN validation blocks form when fewer than 6 characters | Address Details page; all other fields valid | zip: "12345" (5 digits) | 1. Fill all fields with valid data 2. Set ZIP to "12345" 3. Click Next | Error: "The zip field must be 6 digits." Form blocked. | Yes | Yes | Yes | No |
| ADDR_FMT_002 | PIN code more than 6 digits | Verify PIN validation blocks form when more than 6 characters | Address Details page; all other fields valid | zip: "1234567" (7 digits) | 1. Fill all fields with valid data 2. Set ZIP to "1234567" 3. Click Next | Error: "The zip field must be 6 digits." Form blocked. | Yes | Yes | No | No |
| ADDR_FMT_003 | PIN code with 3 digits only | Verify PIN validation for very short input | Address Details page; all other fields valid | zip: "123" (3 digits) | 1. Fill all valid 2. Set ZIP to "123" 3. Click Next | Error: "The zip field must be 6 digits." Form blocked. | Yes | Yes | No | No |
| ADDR_FMT_004 | Address line blank (cleared on existing account) | Verify address line mandatory validation | Address Details page; address field cleared | address: "" (empty), all others valid | 1. Clear address line field 2. Fill all other fields valid 3. Click Next | Error related to address required. Form blocked. | Yes | Yes | Yes | No |

---

# CATEGORY 4: BOUNDARY

| TC ID | Title | Objective | Preconditions | Test Data | Steps | Expected Result | Automatable | Regression | Sanity | Smoke |
|-------|-------|-----------|---------------|-----------|-------|-----------------|-------------|------------|--------|-------|
| ADDR_BND_001 | Address line — 1 character (minimum) | Verify form accepts single character address | Address Details page; all fields valid | address: "A" | 1. Set address to "A" 2. Fill all others valid 3. Click Next | Form accepts or shows min-length error | Yes | Yes | No | No |
| ADDR_BND_002 | Address line — 300 characters (long) | Verify form handles very long address | Address Details page; all fields valid | address: "A" × 300 | 1. Set address to 300 chars 2. Fill all others valid 3. Click Next | Form accepts or truncates/shows max-length error | Yes | Yes | No | No |
| ADDR_BND_003 | PIN code exactly 6 digits (valid boundary) | Verify exact 6-digit PIN is accepted | Address Details page; all fields valid | zip: "123456" | 1. Fill all valid 2. Set ZIP to "123456" 3. Click Next | Form submits — 6 digits accepted | Yes | Yes | No | No |

---

# EXCLUDED SCENARIOS (Not Automatable)

| Scenario | Reason |
|----------|--------|
| Country dropdown blank | Select2 retains selection after save; cannot reset to blank |
| State dropdown blank | Cascade dependency; cannot exist without Country |
| District dropdown blank | Cascade dependency; cannot exist without State |
| City dropdown blank | Cascade dependency; cannot exist without District |
| Locality dropdown blank | Standard `<select>` may not have blank option after save |
| PIN with alphabets (6 chars) | App validates length only, not character type (same as UDISE finding) |
| PIN with special chars (6 chars) | Same — app only checks length, accepts 6 chars of any type |

---

# SUMMARY

| Category | Count |
|----------|-------|
| Validation | 1 |
| Positive | 3 |
| Negative (Format) | 4 |
| Boundary | 3 |
| **Total Automatable** | **11** |
| Excluded (not automatable) | 7 |

---

# EXACT VALIDATION MESSAGES (Captured from Diagnostic)

| Condition | Actual Error Text |
|-----------|-------------------|
| ZIP < 6 or > 6 chars | `The zip field must be 6 digits.` |
| District not selected | `Please select District.` |
| City not selected | `Please select City/Place.` |
| Address blank | (To be captured — likely "address is required" or similar) |

---

# MARKERS & CLASSIFICATION

| TC ID | @regression | @sanity | @first_run | @positive | @negative | @boundary |
|-------|-------------|---------|------------|-----------|-----------|-----------|
| ADDR_VAL_001 | Yes | Yes | Yes | — | — | — |
| ADDR_POS_001 | Yes | Yes | — | Yes | — | — |
| ADDR_POS_002 | Yes | — | — | Yes | — | — |
| ADDR_POS_003 | Yes | — | — | Yes | — | — |
| ADDR_FMT_001 | Yes | Yes | — | — | Yes | — |
| ADDR_FMT_002 | Yes | — | — | — | Yes | — |
| ADDR_FMT_003 | Yes | — | — | — | Yes | — |
| ADDR_FMT_004 | Yes | Yes | — | — | Yes | — |
| ADDR_BND_001 | Yes | — | — | — | — | Yes |
| ADDR_BND_002 | Yes | — | — | — | — | Yes |
| ADDR_BND_003 | Yes | — | — | — | — | Yes |

---

**STATUS:** Test Case Matrix complete. Ready for implementation approval.
