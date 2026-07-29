# Address Details — Negative Test Execution Summary
## Execution Date: 03-Jul-2026

---

# EXECUTION RESULTS

| Test Case ID | Status | Root Cause | Action Required |
|--------------|--------|-----------|-----------------|
| ADDR_FMT_001 | ✅ **PASSED** | — | None |
| ADDR_FMT_002 | ✅ **PASSED** | — | None |
| ADDR_FMT_003 | ✅ **PASSED** | — | None |
| ADDR_FMT_004 | ✅ **PASSED** | — | None |
| ADDR_FMT_005 | ✅ **PASSED** | — | None |
| ADDR_FMT_006 | ✅ **PASSED** | — | None |

---

# SUMMARY

| Metric | Value |
|--------|-------|
| Total Negative Tests | 6 |
| Passed | 6 |
| Failed | 0 |
| Errors | 0 |
| Pass Rate | **100%** |
| Execution Time | 3 min 20 sec |

---

# DETAILED RESULTS

| TC ID | Field | Invalid Value | Expected Error | Result |
|-------|-------|---------------|----------------|--------|
| ADDR_FMT_001 | zip_pin | "12345" (5 digits) | The zip field must be 6 digits. | ✅ Validation shown, form blocked |
| ADDR_FMT_002 | zip_pin | "1234567" (7 digits) | The zip field must be 6 digits. | ✅ Validation shown, form blocked |
| ADDR_FMT_003 | zip_pin | "123" (3 digits) | The zip field must be 6 digits. | ✅ Validation shown, form blocked |
| ADDR_FMT_004 | address_line_1 | "" (blank) | The address field is required. | ✅ Validation shown, form blocked |
| ADDR_FMT_005 | zip_pin | "abcdef" (6 alphabets) | The zip field must be 6 digits. | ✅ Validation shown, form blocked |
| ADDR_FMT_006 | zip_pin | "12@#56" (6 mixed chars) | The zip field must be 6 digits. | ✅ Validation shown, form blocked |

---

# KEY OBSERVATIONS

1. **PIN code validates character type** — Unlike UDISE (School Details), the PIN field correctly rejects non-numeric input even when it's 6 characters long. The validation message "must be 6 digits" enforces BOTH length AND numeric-only.

2. **Address line mandatory validation works** — Clearing the address field and clicking Next correctly blocks the form.

3. **All validations are server-side (on Next click)** — No client-side input masks or blur-triggered validation.

4. **No diagnostic reports generated** — All tests passed, so no failure classification was needed.

---

# COMPARISON WITH SCHOOL DETAILS MODULE

| Behavior | School Details (UDISE) | Address Details (PIN) |
|----------|----------------------|----------------------|
| 11/6 alphabetic chars accepted? | YES (app defect) | **NO — correctly rejected** ✅ |
| Length validation works? | YES | YES |
| Character type validation? | NO (only length) | **YES (digits enforced)** ✅ |
| Blank field validation? | YES | YES |

**Conclusion:** The Address Details PIN validation is more robust than the School Details UDISE validation. The "6 digits" message correctly enforces numeric-only input.

---

**STATUS:** All 6 negative tests PASSED. No action required.
