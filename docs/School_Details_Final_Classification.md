# School Details Module — Final Test Classification
## Updated Strategy Based on Application Behaviour

---

# FINAL TEST STRUCTURE

```
School Details
├── Validation
│   └── Required Field Validation (1 test)
├── Positive (5 tests)
├── Negative — Format Validation (8 tests)
└── Boundary (4 tests)

Total: 18 tests
```

---

# 1. VALIDATION — Required Field Validation

**Purpose:** Verify all mandatory fields display errors when form submitted blank.
**Execution:** First visit only (before any successful save).
**Count:** 1 test

| TC ID | Test Case | Condition | Expected Result |
|-------|-----------|-----------|-----------------|
| SCH_VAL_001 | All required fields blank — verify all mandatory errors displayed | First visit, no data entered, click Next | Page does not navigate. All mandatory error messages shown: School name required, Contact person required, UDISE required. No data saved. |

---

# 2. POSITIVE — Valid Business Scenarios

**Purpose:** Verify form accepts valid data combinations.
**Execution:** Anytime — overwrites saved data with valid values.
**Count:** 5 tests

| TC ID | Test Case | Data Combination | Expected Result |
|-------|-----------|------------------|-----------------|
| SCH_POS_001 | Valid complete — Day / Co-ed / Private | All mandatory fields valid | Form submits, navigates to Address Details |
| SCH_POS_002 | Valid — Residential / Boys / Private | Different dropdown combination | Form submits successfully |
| SCH_POS_003 | Valid — Day / Girls / Government | Another valid combination | Form submits successfully |
| SCH_POS_004 | Valid with blank optional website | All mandatory filled, website empty | Form submits (website is optional) |
| SCH_POS_005 | Valid name with special characters (St. Mary's High School - Branch) | Apostrophe, period, hyphen in name | Form submits (valid chars accepted) |

---

# 3. NEGATIVE — Format Validation

**Purpose:** Verify invalid input formats are rejected.
**Execution:** Anytime — overwrites saved data with invalid values.
**Count:** 8 tests

| TC ID | Test Case | Field | Invalid Value | Expected Error |
|-------|-----------|-------|---------------|----------------|
| SCH_FMT_001 | School name — only special characters | school_name | @#$%^&*() | Invalid school name |
| SCH_FMT_002 | School name — only numbers | school_name | 123456789 | Invalid school name |
| SCH_FMT_003 | UDISE — alphabetic characters | udise_number | abcdefghijk | Invalid UDISE number |
| SCH_FMT_004 | UDISE — special characters | udise_number | 123@#$456!! | Invalid UDISE number |
| SCH_FMT_005 | UDISE — less than 11 digits | udise_number | 1234567890 | Must be exactly 11 digits |
| SCH_FMT_006 | UDISE — more than 11 digits | udise_number | 123456789012 | Must be exactly 11 digits |
| SCH_FMT_007 | Contact person — only numbers | contact_person | 123456 | Invalid contact name |
| SCH_FMT_008 | Website — invalid URL format | website | notavalidurl | Invalid website URL |

---

# 4. BOUNDARY — Value Length Limits

**Purpose:** Verify field character limits (min/max length enforcement).
**Execution:** Anytime — fills boundary-length values.
**Count:** 4 tests

| TC ID | Test Case | Field | Value | Expected |
|-------|-----------|-------|-------|----------|
| SCH_BND_001 | School name — minimum (1 character) | school_name | "A" | ACCEPT or min-length error |
| SCH_BND_002 | School name — maximum (200 characters) | school_name | "A" × 200 | Truncate or max-length error |
| SCH_BND_003 | School name — over maximum (201 characters) | school_name | "A" × 201 | Truncate or reject |
| SCH_BND_004 | Contact person — maximum (100 characters) | contact_person | "A" × 100 | ACCEPT or truncate |

---

# CHANGES FROM PREVIOUS DESIGN

## Removed Test Cases

| Old TC ID | Old Classification | Reason for Removal |
|-----------|-------------------|--------------------|
| SCH_NEG_04 | Negative | Dropdown cannot be reset — untestable on existing account |
| SCH_NEG_05 | Negative | Dropdown cannot be reset — untestable |
| SCH_NEG_06 | Negative | Dropdown cannot be reset — untestable |
| SCH_BND_004 (old) | Boundary | UDISE 10 digits — reclassified to Format Validation |
| SCH_BND_005 (old) | Boundary | UDISE 11 digits — already covered in Positive (valid) |
| SCH_BND_006 (old) | Boundary | UDISE 12 digits — reclassified to Format Validation |
| SCH_BND_007 (old) | Boundary | Contact 1 char — insufficient value as standalone |
| SCH_BND_008 (old) | Boundary | Website 200 chars — insufficient value as standalone |

## Reclassified Test Cases

| TC ID | From | To | Reason |
|-------|------|-----|--------|
| SCH_NEG_01 (blank name) | Negative | **Validation** (merged into SCH_VAL_001) | Blank mandatory is Required Field Validation, not format validation |
| UDISE 10 digits | Boundary | **Negative/Format** (SCH_FMT_005) | Fixed-length field — wrong length is a format error, not a boundary |
| UDISE 12 digits | Boundary | **Negative/Format** (SCH_FMT_006) | Same reason — exact digit requirement is format, not boundary |
| UDISE alphabets | Negative | **Negative/Format** (SCH_FMT_003) | Correctly classified — stays in format |
| UDISE special chars | Negative | **Negative/Format** (SCH_FMT_004) | Correctly classified — stays in format |

## New Test Cases

| TC ID | Classification | Reason |
|-------|---------------|--------|
| SCH_VAL_001 | Validation | Dedicated consolidated mandatory test (not mixed into Negative) |
| SCH_FMT_005 | Format | UDISE < 11 digits — moved from Boundary |
| SCH_FMT_006 | Format | UDISE > 11 digits — moved from Boundary |

---

# CLASSIFICATION RATIONALE

## Why UDISE is Format, Not Boundary:

| Criterion | Boundary | Format |
|-----------|----------|--------|
| Definition | Testing min/max limits of a range | Testing correct input structure |
| UDISE requirement | Exactly 11 digits | Fixed format — not a range |
| Example boundary | Name: 1 char → 200 chars (variable range) | - |
| Example format | - | UDISE: must be exactly 11 numeric digits |
| Conclusion | UDISE has no valid range — it's a fixed format | **UDISE is Format Validation** |

## Why Blank Fields are Validation, Not Negative:

| Criterion | Negative/Format | Required Field Validation |
|-----------|-----------------|---------------------------|
| Definition | Invalid VALUE provided | NO value provided |
| Example negative | school_name = "@#$%" | - |
| Example validation | - | school_name = "" (blank) |
| Distinction | User entered something wrong | User didn't enter anything |
| Conclusion | Blank mandatory is Required Field Validation | **Separate from format errors** |

---

# FINAL TEST CASE MATRIX

| TC ID | Category | Test Case | Field | Value/Condition | Expected | Testable When |
|-------|----------|-----------|-------|-----------------|----------|---------------|
| SCH_VAL_001 | Validation | All required fields blank | ALL mandatory | All cleared | All errors shown, no navigation | First visit |
| SCH_POS_001 | Positive | Valid — Day / Co-ed / Private | All | Valid | Navigates | Anytime |
| SCH_POS_002 | Positive | Valid — Residential / Boys / Private | All | Valid | Navigates | Anytime |
| SCH_POS_003 | Positive | Valid — Day / Girls / Government | All | Valid | Navigates | Anytime |
| SCH_POS_004 | Positive | Valid with blank optional website | All except website | Valid | Navigates | Anytime |
| SCH_POS_005 | Positive | Valid with special chars in name | school_name | St. Mary's | Navigates | Anytime |
| SCH_FMT_001 | Format | Special chars only in name | school_name | @#$%^&*() | Error shown | Anytime |
| SCH_FMT_002 | Format | Numbers only in name | school_name | 123456789 | Error shown | Anytime |
| SCH_FMT_003 | Format | UDISE — alphabets | udise_number | abcdefghijk | Error shown | Anytime |
| SCH_FMT_004 | Format | UDISE — special chars | udise_number | 123@#$456!! | Error shown | Anytime |
| SCH_FMT_005 | Format | UDISE — less than 11 digits | udise_number | 1234567890 | Error shown | Anytime |
| SCH_FMT_006 | Format | UDISE — more than 11 digits | udise_number | 123456789012 | Error shown | Anytime |
| SCH_FMT_007 | Format | Contact person — numbers only | contact_person | 123456 | Error shown | Anytime |
| SCH_FMT_008 | Format | Website — invalid format | website | notavalidurl | Error shown | Anytime |
| SCH_BND_001 | Boundary | Name — 1 character | school_name | A | Accept or error | Anytime |
| SCH_BND_002 | Boundary | Name — 200 characters | school_name | A × 200 | Truncate or error | Anytime |
| SCH_BND_003 | Boundary | Name — 201 characters | school_name | A × 201 | Truncate or error | Anytime |
| SCH_BND_004 | Boundary | Contact — 100 characters | contact_person | A × 100 | Accept or truncate | Anytime |

---

# FINAL FOLDER STRUCTURE

```
tests/regression/school_details/
├── validation/
│   └── test_school_required_fields.py     ← 1 test (SCH_VAL_001)
├── positive/
│   └── test_school_positive.py            ← 5 tests (SCH_POS_001–005)
├── negative/
│   └── test_school_negative.py            ← 8 tests (SCH_FMT_001–008)
└── boundary/
    └── test_school_boundary.py            ← 4 tests (SCH_BND_001–004)
```

---

# SUMMARY

| Metric | Value |
|--------|-------|
| **Total test cases** | 18 |
| Validation (required fields) | 1 |
| Positive | 5 |
| Negative (format) | 8 |
| Boundary | 4 |
| **Removed** | 8 (3 impossible dropdowns + 5 reclassified) |
| **Reclassified** | 5 (UDISE from boundary → format, blank from negative → validation) |
| **Always-runnable** | 17 of 18 |
| **First-visit-only** | 1 (SCH_VAL_001) |
