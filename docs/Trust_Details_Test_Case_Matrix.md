# Trust/Society/Company Details — Final Test Case Matrix
## Based on Diagnostic Evidence Only (Refined)

---

# CATEGORY 1: VALIDATION (Required Fields)

| TC ID | Scenario | Test Type | Expected Result | Automation Status | Remarks |
|-------|----------|-----------|-----------------|-------------------|---------|
| TRUST_VAL_001 | All mandatory fields cleared - verify all errors displayed | Validation | Form blocked. Errors: Ownership name is required, Date of Establishment is required, Date of Registration is required, Registration number is required. | Automatable | Requires first visit |

---

# CATEGORY 2: POSITIVE (Valid Submissions)

| TC ID | Scenario | Test Type | Expected Result | Automation Status | Remarks |
|-------|----------|-----------|-----------------|-------------------|---------|
| TRUST_POS_001 | Valid - Trust type, valid name, past est date, past reg date, valid reg number | Positive | Form submits, navigates to Certificate of Land | Automatable | |
| TRUST_POS_002 | Valid - Society type, different dates | Positive | Form submits successfully | Automatable | |

---

# CATEGORY 3: NEGATIVE (Format/Business Validation)

| TC ID | Scenario | Test Type | Expected Result | Automation Status | Remarks |
|-------|----------|-----------|-----------------|-------------------|---------|
| TRUST_FMT_001 | Trust name blank (cleared) | Negative | Error: Ownership name is required. Form blocked. | Automatable | |
| TRUST_FMT_002 | Registration number blank (cleared) | Negative | Error: Registration number is required. Form blocked. | Automatable | |
| TRUST_FMT_003 | Establishment date empty (cleared via JS) | Negative | Error: Date of Establishment is required. Form blocked. | Automatable | |
| TRUST_FMT_004 | Registration date empty (cleared via JS) | Negative | Error: Date of Registration is required. Form blocked. | Automatable | |
| TRUST_FMT_005 | Future establishment date set | Negative | Current behavior: Form navigates (accepted). Expected: Should reject future date. | Automatable | Business Rule Pending Confirmation |
| TRUST_FMT_006 | Registration date before establishment date (Est=2022, Reg=2019) | Negative | Current behavior: Form navigates (accepted). Expected: Should enforce chronological order. | Automatable | Business Rule Pending Confirmation |

---

# CATEGORY 4: BOUNDARY (Field Length Limits)

| TC ID | Scenario | Test Type | Expected Result | Automation Status | Remarks |
|-------|----------|-----------|-----------------|-------------------|---------|
| TRUST_BND_001 | Trust name - 1 character | Boundary | ACCEPT or min-length error | Automatable | |
| TRUST_BND_002 | Trust name - 300 characters | Boundary | ACCEPT or max-length error / truncation | Automatable | |
| TRUST_BND_003 | Registration number - 50 characters | Boundary | ACCEPT or max-length error | Automatable | |

---

# EXCLUDED SCENARIOS (Not Automatable)

| Scenario | Reason | Remarks |
|----------|--------|---------|
| Ownership Type blank (Select) | Disabled placeholder - cannot be selected by Playwright | Excluded (Not Automatable) |
| Calendar UI date restrictions | JS injection bypasses calendar min/max enforcement | Excluded (Not Automatable) |
| Typed date format validation | Field is readonly - cannot type into it | Excluded (Not Automatable) |
| Invalid date format (99/99/9999) | JS injection accepts any string - no format check | Excluded (Not Automatable) |

---

# SANITY TEST CANDIDATES

| TC ID | Reason |
|-------|--------|
| TRUST_VAL_001 | Critical - validates all mandatory fields |
| TRUST_POS_001 | Critical - proves valid form submits |
| TRUST_FMT_001 | High priority - trust name mandatory |
| TRUST_FMT_003 | High priority - establishment date mandatory |

---

# FINAL SUMMARY

| Category | Count |
|----------|-------|
| Validation | 1 |
| Positive | 2 |
| Negative | 6 |
| Boundary | 3 |
| **Total Automatable** | **12** |
| Excluded | 4 |

---

# REMARKS LEGEND

| Value | Meaning |
|-------|---------|
| Requires first visit | Test only works before first successful save (text fields can be cleared; dropdown retains value) |
| Business Rule Pending Confirmation | Application currently accepts the input; expected business rule has not been confirmed by PO/QA Lead |
| Excluded (Not Automatable) | Scenario cannot be automated due to technical limitation |

---

# REGRESSION COVERAGE SUMMARY

| Metric | Value |
|--------|-------|
| Fields covered | 5 of 5 (100%) |
| Ownership types tested | 2 (Trust, Society) |
| Mandatory validations | 4 exact error messages confirmed |
| Date field approach | ValidationHelper.set_readonly_date() (proven) |
| Business rules tested | 2 (both pending confirmation) |
| Boundary scenarios | 3 |
| Total automatable | 12 |
| Total excluded | 4 |

---

**STATUS:** Test Case Matrix finalized. Ready for implementation approval.
