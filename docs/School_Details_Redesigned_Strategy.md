# School Details Module — Redesigned Test Strategy
## Based on Application State Persistence Behaviour

---

# APPLICATION BEHAVIOUR (Critical Constraint)

| Behaviour | Impact on Testing |
|-----------|-------------------|
| Clicking "Next" saves data to server | Cannot test blank fields after first save |
| Returning to page pre-fills saved data | "Skip field" approach fails on subsequent visits |
| Dropdowns retain selection permanently | Cannot reset dropdown to "Select" default |
| Text fields retain last saved value | Must explicitly clear to test blank validation |
| First visit = truly blank form | Only reliable time to test all-mandatory-blank |

---

# REDESIGNED TEST CASE MATRIX

## Category 1: CONSOLIDATED MANDATORY VALIDATION (First Visit Only)

**One test. Tests ALL mandatory fields at once. Requires fresh account or first-time page access.**

| TC ID | Test Case | Strategy | Fixture Required |
|-------|-----------|----------|------------------|
| SCH_MAND_001 | All mandatory fields blank — verify all errors shown simultaneously | Open School Details first time → Click Next without filling → Assert ALL mandatory errors visible | `school_details_ready_page` (first visit) |

**Fields validated in this single test:**
- School Name → "School name is required"
- Contact Person → "Contact person is required"
- UDISE Number → "UDISE number is required"

**Note:** Dropdown fields (Classification, Type, Category) may have defaults pre-selected by the application. If they show "Select" on first load, they're testable here. If they have a default value, they cannot be tested for blank.

---

## Category 2: FORMAT VALIDATIONS (Testable Anytime — Independent of Saved State)

**These work regardless of previously saved data because they test INVALID values, not BLANK values.**

| TC ID | Test Case | Field | Invalid Value | Expected Error | Independent? |
|-------|-----------|-------|---------------|----------------|-------------|
| SCH_FMT_001 | School name with only special characters | school_name | @#$%^&*() | Invalid school name | ✅ Yes |
| SCH_FMT_002 | School name with only numbers | school_name | 123456789 | Invalid school name | ✅ Yes |
| SCH_FMT_003 | UDISE with alphabetic characters | udise_number | abcdefghijk | Invalid UDISE number | ✅ Yes |
| SCH_FMT_004 | UDISE with special characters | udise_number | 123@#$456!! | Invalid UDISE number | ✅ Yes |
| SCH_FMT_005 | Contact person with only numbers | contact_person | 123456 | Invalid contact name | ✅ Yes |
| SCH_FMT_006 | Invalid website URL format | website | notavalidurl | Invalid website URL | ✅ Yes |

**Why these work anytime:** They fill the field with a BAD value (overwriting any saved data), then click Next. The validation fires on the invalid content, not on "blank."

---

## Category 3: BOUNDARY VALIDATIONS (Testable Anytime — Independent of Saved State)

**These work because they fill with specific boundary values, overwriting saved data.**

| TC ID | Test Case | Field | Value | Expected |
|-------|-----------|-------|-------|----------|
| SCH_BND_001 | School name at 1 character (min) | school_name | "A" | ACCEPT or min-length error |
| SCH_BND_002 | School name at 200 characters (max) | school_name | "A" × 200 | Truncate or max error |
| SCH_BND_003 | School name at 201 characters (max+1) | school_name | "A" × 201 | Truncate or max error |
| SCH_BND_004 | UDISE with 10 digits (min-1) | udise_number | 1234567890 | REJECT — must be 11 |
| SCH_BND_005 | UDISE with 11 digits (exact) | udise_number | 12345678901 | ACCEPT |
| SCH_BND_006 | UDISE with 12 digits (max+1) | udise_number | 123456789012 | REJECT — max 11 |
| SCH_BND_007 | Contact person at 100 characters | contact_person | "A" × 100 | ACCEPT or truncate |
| SCH_BND_008 | Website at 200 characters | website | long URL | ACCEPT or truncate |

---

## Category 4: POSITIVE VALIDATIONS (Testable Anytime — Overwrite with Valid Data)

**These fill all fields with valid data and verify form submits.**

| TC ID | Test Case | Combination | Expected |
|-------|-----------|-------------|----------|
| SCH_POS_001 | Valid complete — Day / Co-ed / Private | All mandatory valid | ACCEPT, navigates |
| SCH_POS_002 | Valid — Residential / Boys / Private | Different dropdown combo | ACCEPT |
| SCH_POS_003 | Valid — Day / Girls / Government | Different combo | ACCEPT |
| SCH_POS_004 | Valid with blank optional website | Website empty, all else valid | ACCEPT |
| SCH_POS_005 | Valid with special chars in name (St. Mary's) | Apostrophe, period, hyphen | ACCEPT |

---

## Category 5: INVALID — Tests That Cannot Be Reliably Automated

| Original TC ID | Test Case | Why Invalid |
|----------------|-----------|-------------|
| SCH_NEG_04 | Classification not selected | Dropdown retains saved value, cannot reset |
| SCH_NEG_05 | School type not selected | Same reason |
| SCH_NEG_06 | Category not selected | Same reason |
| ~~SCH_NEG_01~~ (standalone) | Blank school name ALONE | Works only on fresh form; merged into SCH_MAND_001 |

**Resolution:** SCH_NEG_04/05/06 are marked `execute=No`. SCH_NEG_01 is merged into consolidated mandatory test.

---

# REVISED TEST FILE STRUCTURE

## tests/regression/school_details/

| File | Tests | What It Covers |
|------|-------|----------------|
| `negative/test_school_negative.py` | 6 | Format validations (invalid values that trigger errors anytime) |
| `negative/test_school_mandatory.py` | 1 | Consolidated all-blank mandatory test (first visit) |
| `positive/test_school_positive.py` | 5 | Valid data combinations that submit successfully |
| `boundary/test_school_boundary.py` | 8 | Min/max/exact boundary values |

**Total: 20 tests** (down from 34 — removed duplicates and impossible scenarios)

---

# EXECUTION STRATEGY PER CATEGORY

| Category | When Testable | Fixture Needed | Frequency |
|----------|---------------|----------------|-----------|
| Mandatory (all blank) | First visit only OR with fresh account | `school_details_ready_page` | Per fresh registration |
| Format (invalid values) | Anytime — overwrites saved data | `school_details_ready_page` | Every regression run |
| Boundary | Anytime — overwrites saved data | `school_details_ready_page` | Every regression run |
| Positive | Anytime — fills valid data | `school_details_ready_page` | Every regression run |

---

# TEST APPROACH FOR EACH CATEGORY

## Mandatory Test (SCH_MAND_001):
```
1. Navigate to School Details (first time or fresh account)
2. Clear all text fields: school_name, contact_person, udise, website
3. Click Next
4. Assert: page did NOT navigate
5. Assert: All expected error messages visible simultaneously
6. Count errors >= 3 (school_name, contact_person, udise minimum)
```

## Format Tests (SCH_FMT_001–006):
```
1. Navigate to School Details
2. Fill ALL fields with valid baseline data
3. OVERRIDE the target field with invalid value (overwrites saved data)
4. Click Next
5. If blocked: Assert expected error message
6. If navigated: Navigate back (field had no validation — test documents gap)
```

## Boundary Tests (SCH_BND_001–008):
```
1. Navigate to School Details
2. Fill ALL fields with valid baseline
3. OVERRIDE target field with boundary value
4. Click Next
5. If expected=ACCEPT: Assert navigation happened
6. If expected=REJECT: Assert form blocked + error shown
7. Navigate back if needed
```

## Positive Tests (SCH_POS_001–005):
```
1. Navigate to School Details
2. Fill ALL fields with valid data from Excel
3. Click Next
4. Assert: page navigated (form accepted)
5. Navigate back for next test
```

---

# UPDATED EXCEL SHEET DESIGN

## Sheet: "School_Negative" (UPDATED)

Remove rows SCH_NEG_04, 05, 06 (execute=No, already done).
Keep rows SCH_NEG_01–03, 07–10 as format validations.

**Rename approach:** These are not "blank field" tests anymore. They are "invalid value" tests that work by overwriting existing data with bad values.

| scenario_id | execute | description | field_name | field_value | expected_error |
|---|---|---|---|---|---|
| SCH_NEG_01 | Yes | Blank school name | school_name | (clear) | School name is required |
| SCH_NEG_02 | Yes | Special chars only | school_name | @#$%^&*() | Invalid school name |
| SCH_NEG_03 | Yes | Numbers only | school_name | 123456789 | Invalid school name |
| SCH_NEG_04 | **No** | ~~Classification not selected~~ | — | — | — |
| SCH_NEG_05 | **No** | ~~School type not selected~~ | — | — | — |
| SCH_NEG_06 | **No** | ~~Category not selected~~ | — | — | — |
| SCH_NEG_07 | Yes | UDISE alphabets | udise_number | abcdefghijk | Invalid UDISE |
| SCH_NEG_08 | Yes | UDISE special chars | udise_number | 123@#$456!! | Invalid UDISE |
| SCH_NEG_09 | Yes | Numeric contact | contact_person | 123456 | Invalid contact |
| SCH_NEG_10 | Yes | Invalid website | website | notavalidurl | Invalid URL |

**Active rows: 7** (SCH_NEG_01, 02, 03, 07, 08, 09, 10)

## New Sheet: "School_Mandatory" (OPTIONAL)

| scenario_id | execute | description | fields_to_clear | expected_errors |
|---|---|---|---|---|
| SCH_MAND_001 | Yes | All mandatory blank | school_name,contact_person,udise_number | School name is required;Contact person is required;UDISE is required |

---

# MIGRATION PLAN

| Step | Action | Files Affected |
|------|--------|----------------|
| 1 | Update `School_Negative` sheet — set execute=No for 04/05/06 | Validation_Data.xlsx |
| 2 | Update `negative/test_school_negative.py` — ensure it only loads `execute=Yes` rows | Already done via filter |
| 3 | Create `negative/test_school_mandatory.py` — consolidated mandatory test | New file |
| 4 | Update `boundary/test_school_boundary.py` — align with BND_001–008 | Existing file |
| 5 | Update `positive/test_school_positive.py` — align with POS_001–005 | Existing file |
| 6 | Remove old `School_Boundary` sheet if superseded by `School_Boundary_Extended` | Validation_Data.xlsx |

---

# SUMMARY

| Metric | Before Redesign | After Redesign |
|--------|----------------|----------------|
| Total tests | 34 | **20** |
| Impossible tests removed | 0 | 3 (dropdown blank) |
| Duplicates merged | 0 | Multiple blank → 1 consolidated |
| Always-runnable tests | Unknown | **19 of 20** |
| First-visit-only tests | Unknown | **1** (SCH_MAND_001) |
| State-independent format tests | 0 | **7** |
| Reliable boundary tests | 4 | **8** |
| Positive combinations | 8 | **5** (focused) |
