# CISCE Preliminary Affiliation Form
# Automation Test Inventory Report
## Date: 03-Jul-2026

---

# COMPLETE TEST INVENTORY

## Smoke Suite

| Auto ID | Test Case ID | Module | Test Case Description | Test Type | Suite | Priority | Status | Remarks |
|---------|-------------|--------|----------------------|-----------|-------|----------|--------|---------|
| SM01 | E2E_SMOKE | Preliminary Form | Complete E2E flow: Registration → Login → School → Address → NOC → Trust → Land → Upload → Payment | Smoke | Smoke | High | Implemented | Requires manual password entry (page.pause) |

---

## Sanity Suite

| Auto ID | Test Case ID | Module | Test Case Description | Test Type | Suite | Priority | Status | Remarks |
|---------|-------------|--------|----------------------|-----------|-------|----------|--------|---------|
| S01 | SANITY_SUITE | All Modules | 20 test cases covering S1-S13 + R1-R18 from Test Report sheet | Sanity | Sanity | High | Implemented | Allure showcase for management |
| S02 | SCH_SANITY_POS | School Details | Valid school details submission (high priority positive) | Sanity | Sanity | High | Implemented | Filtered from School_Positive (priority=High) |
| S03 | SCH_SANITY_NEG | School Details | Mandatory field blocking (high priority negative) | Sanity | Sanity | High | Implemented | Filtered from School_Negative (priority=High) |

---

## Regression Suite — School Details

| Auto ID | Test Case ID | Module | Test Case Description | Test Type | Suite | Priority | Status | Remarks |
|---------|-------------|--------|----------------------|-----------|-------|----------|--------|---------|
| R01 | SCH_VAL_001 | School Details | All mandatory fields blank — verify all errors displayed | Validation | Regression | High | Implemented | First-run only (@first_run) |
| R02 | SCH_POS_01 | School Details | Valid complete school — Day / Co-ed / Private | Positive | Regression | High | Implemented | |
| R03 | SCH_POS_02 | School Details | Valid school — Residential / Boys / Private | Positive | Regression | High | Implemented | |
| R04 | SCH_POS_03 | School Details | Valid school — Day / Girls / Private | Positive | Regression | Medium | Implemented | |
| R05 | SCH_POS_04 | School Details | Valid school — Day / Co-ed / Government | Positive | Regression | Medium | Implemented | |
| R06 | SCH_POS_05 | School Details | Valid school — minimum fields only (no website) | Positive | Regression | High | Implemented | |
| R07 | SCH_POS_06 | School Details | Valid school name with special characters (St. Mary's) | Positive | Regression | Medium | Implemented | |
| R08 | SCH_POS_07 | School Details | Valid school with long school name | Positive | Regression | Low | Implemented | |
| R09 | SCH_POS_08 | School Details | Valid UDISE number with exactly 11 digits | Positive | Regression | Medium | Implemented | |
| R10 | SCH_NEG_01 | School Details | Blank school name — form blocked | Negative | Regression | High | Implemented | Clears field to test |
| R11 | SCH_NEG_02 | School Details | Special characters only in school name | Negative | Regression | Medium | Implemented | Pending business confirmation |
| R12 | SCH_NEG_03 | School Details | Numbers only in school name | Negative | Regression | Medium | Implemented | Pending business confirmation |
| R13 | SCH_NEG_07 | School Details | UDISE number with alphabets | Negative | Regression | Medium | Implemented | Pending business confirmation |
| R14 | SCH_NEG_08 | School Details | UDISE number with special characters | Negative | Regression | Medium | Implemented | Pending business confirmation |
| R15 | SCH_NEG_09 | School Details | Numeric-only contact person | Negative | Regression | Low | Implemented | Pending business confirmation |
| R16 | SCH_NEG_10 | School Details | Invalid website URL format | Negative | Regression | Low | Implemented | Pending business confirmation |
| R17 | SCH_BND_EXT_01 | School Details | School name — 1 character (min) | Boundary | Regression | Medium | Implemented | |
| R18 | SCH_BND_EXT_02 | School Details | School name — 2 characters | Boundary | Regression | Low | Implemented | |
| R19 | SCH_BND_EXT_03 | School Details | School name — 100 characters | Boundary | Regression | Medium | Implemented | |
| R20 | SCH_BND_EXT_04 | School Details | School name — 200 characters (max) | Boundary | Regression | Medium | Implemented | |
| R21 | SCH_BND_EXT_05 | School Details | School name — 201 characters (max+1) | Boundary | Regression | Medium | Implemented | |
| R22 | SCH_BND_EXT_06 | School Details | UDISE — 10 digits (min-1) | Boundary | Regression | High | Implemented | |
| R23 | SCH_BND_EXT_07 | School Details | UDISE — 11 digits (valid) | Boundary | Regression | High | Implemented | |
| R24 | SCH_BND_EXT_08 | School Details | UDISE — 12 digits (max+1) | Boundary | Regression | High | Implemented | |
| R25 | SCH_BND_EXT_09 | School Details | Website field empty (optional boundary) | Boundary | Regression | Medium | Implemented | |

---

## Regression Suite — Address Details

| Auto ID | Test Case ID | Module | Test Case Description | Test Type | Suite | Priority | Status | Remarks |
|---------|-------------|--------|----------------------|-----------|-------|----------|--------|---------|
| R26 | ADDR_VAL_001 | Address Details | All mandatory text fields blank — verify errors | Validation | Regression | High | Implemented | First-run only (@first_run) |
| R27 | ADDR_POS_001 | Address Details | Valid complete address — India, Rajasthan | Positive | Regression | High | Implemented | |
| R28 | ADDR_POS_002 | Address Details | Valid address — different state (Maharashtra) | Positive | Regression | Medium | Implemented | |
| R29 | ADDR_POS_003 | Address Details | Valid address — Rural locality | Positive | Regression | Medium | Implemented | |
| R30 | ADDR_FMT_001 | Address Details | PIN code less than 6 digits | Negative | Regression | High | Executed — Passed ✅ | |
| R31 | ADDR_FMT_002 | Address Details | PIN code more than 6 digits | Negative | Regression | Medium | Executed — Passed ✅ | |
| R32 | ADDR_FMT_003 | Address Details | PIN code with 3 digits only | Negative | Regression | Medium | Executed — Passed ✅ | |
| R33 | ADDR_FMT_004 | Address Details | Address line blank (cleared) | Negative | Regression | High | Executed — Passed ✅ | |
| R34 | ADDR_FMT_005 | Address Details | PIN code with 6 alphabetic characters | Negative | Regression | High | Executed — Passed ✅ | |
| R35 | ADDR_FMT_006 | Address Details | PIN code with 6 mixed special characters | Negative | Regression | Medium | Executed — Passed ✅ | |
| R36 | ADDR_BND_001 | Address Details | Address line — 1 character (min) | Boundary | Regression | Medium | Implemented | |
| R37 | ADDR_BND_002 | Address Details | Address line — 300 characters (long) | Boundary | Regression | Medium | Implemented | |
| R38 | ADDR_BND_003 | Address Details | PIN code — exactly 6 digits (valid) | Boundary | Regression | High | Implemented | |

---

## Regression Suite — NOC Details

| Auto ID | Test Case ID | Module | Test Case Description | Test Type | Suite | Priority | Status | Remarks |
|---------|-------------|--------|----------------------|-----------|-------|----------|--------|---------|
| R39 | NOC_VAL_001 | NOC Details | All mandatory fields blank — verify errors | Validation | Regression | High | Implemented | First-run only (@first_run) |
| R40 | NOC_POS_001 | NOC Details | Valid complete NOC — India, Rajasthan, past date | Positive | Regression | High | Implemented | |
| R41 | NOC_POS_002 | NOC Details | Valid NOC — different state (Maharashtra) | Positive | Regression | Medium | Implemented | |
| R42 | NOC_FMT_001 | NOC Details | NOC Authority blank (cleared) | Negative | Regression | High | Implemented | |
| R43 | NOC_FMT_002 | NOC Details | Designation blank (cleared) | Negative | Regression | Medium | Implemented | |
| R44 | NOC_FMT_003 | NOC Details | Office Address blank (cleared) | Negative | Regression | Medium | Implemented | |
| R45 | NOC_FMT_004 | NOC Details | Reference Number blank (cleared) | Negative | Regression | Medium | Implemented | |
| R46 | NOC_FMT_005 | NOC Details | Date of NOC cleared (empty) | Negative | Regression | High | Implemented | |
| R47 | NOC_FMT_006 | NOC Details | Future date set — verify rejection | Negative | Regression | Medium | Implemented | Potential app defect — awaiting confirmation |
| R48 | NOC_BND_001 | NOC Details | Authority — 1 character (min below 3) | Boundary | Regression | Medium | Implemented | Expected: REJECT (min 3 chars) |
| R49 | NOC_BND_002 | NOC Details | Office Address — 201 characters (over max 200) | Boundary | Regression | Medium | Implemented | Expected: REJECT (max 200) |
| R50 | NOC_BND_003 | NOC Details | Reference Number — 50 characters | Boundary | Regression | Low | Implemented | Expected: ACCEPT |

---

# MODULE-WISE SUMMARY

## School Details

| Category | Count |
|----------|-------|
| Validation | 1 |
| Positive | 8 |
| Negative | 7 |
| Boundary | 9 |
| **Total Regression** | **25** |
| Sanity | 2 (subset) |
| Smoke | 0 (covered by E2E) |

## Address Details

| Category | Count |
|----------|-------|
| Validation | 1 |
| Positive | 3 |
| Negative | 6 |
| Boundary | 3 |
| **Total Regression** | **13** |
| Sanity | 0 |
| Smoke | 0 |

## NOC Details

| Category | Count |
|----------|-------|
| Validation | 1 |
| Positive | 2 |
| Negative | 6 |
| Boundary | 3 |
| **Total Regression** | **12** |
| Sanity | 0 |
| Smoke | 0 |

---

# AUTOMATION SUMMARY

| Metric | Count |
|--------|-------|
| **Total Regression Tests** | 50 |
| **Total Sanity Tests** | 24 (20 showcase + 4 school sanity) |
| **Total Smoke Tests** | 1 |
| **Grand Total Automated Tests** | **75** |

---

# TEST LISTS

## Regression Tests (R01–R50):

```
R01 - SCH_VAL_001 - School Details Validation (all blank)
R02 - SCH_POS_01 - Valid School Day/Co-ed/Private
R03 - SCH_POS_02 - Valid School Residential/Boys
R04 - SCH_POS_03 - Valid School Day/Girls
R05 - SCH_POS_04 - Valid School Day/Co-ed/Government
R06 - SCH_POS_05 - Valid School minimum fields
R07 - SCH_POS_06 - Valid School special chars name
R08 - SCH_POS_07 - Valid School long name
R09 - SCH_POS_08 - Valid UDISE 11 digits
R10 - SCH_NEG_01 - Blank school name
R11 - SCH_NEG_02 - Special chars only name
R12 - SCH_NEG_03 - Numbers only name
R13 - SCH_NEG_07 - UDISE alphabets
R14 - SCH_NEG_08 - UDISE special chars
R15 - SCH_NEG_09 - Numeric contact person
R16 - SCH_NEG_10 - Invalid website URL
R17 - SCH_BND_EXT_01 - Name 1 char
R18 - SCH_BND_EXT_02 - Name 2 chars
R19 - SCH_BND_EXT_03 - Name 100 chars
R20 - SCH_BND_EXT_04 - Name 200 chars
R21 - SCH_BND_EXT_05 - Name 201 chars
R22 - SCH_BND_EXT_06 - UDISE 10 digits
R23 - SCH_BND_EXT_07 - UDISE 11 digits
R24 - SCH_BND_EXT_08 - UDISE 12 digits
R25 - SCH_BND_EXT_09 - Website empty boundary
R26 - ADDR_VAL_001 - Address validation all blank
R27 - ADDR_POS_001 - Valid address India/Rajasthan
R28 - ADDR_POS_002 - Valid address Maharashtra
R29 - ADDR_POS_003 - Valid address Rural
R30 - ADDR_FMT_001 - PIN < 6 digits
R31 - ADDR_FMT_002 - PIN > 6 digits
R32 - ADDR_FMT_003 - PIN 3 digits
R33 - ADDR_FMT_004 - Address blank
R34 - ADDR_FMT_005 - PIN alphabets
R35 - ADDR_FMT_006 - PIN special chars
R36 - ADDR_BND_001 - Address 1 char
R37 - ADDR_BND_002 - Address 300 chars
R38 - ADDR_BND_003 - PIN exactly 6 digits
R39 - NOC_VAL_001 - NOC validation all blank
R40 - NOC_POS_001 - Valid NOC India/Rajasthan
R41 - NOC_POS_002 - Valid NOC Maharashtra
R42 - NOC_FMT_001 - Authority blank
R43 - NOC_FMT_002 - Designation blank
R44 - NOC_FMT_003 - Office address blank
R45 - NOC_FMT_004 - Reference number blank
R46 - NOC_FMT_005 - Date empty
R47 - NOC_FMT_006 - Future date
R48 - NOC_BND_001 - Authority 1 char
R49 - NOC_BND_002 - Office address 201 chars
R50 - NOC_BND_003 - Reference 50 chars
```

## Sanity Tests (S01–S04):

```
S01 - SANITY_SUITE - 20 test cases (Allure showcase)
S02 - SCH_SANITY_POS - School positive (high priority)
S03 - SCH_SANITY_NEG - School negative (high priority)
S04 - SCH_SANITY_VAL - School mandatory validation
```

## Smoke Tests (SM01):

```
SM01 - E2E_SMOKE - Complete Preliminary Form End-to-End
```

---

**Report Status:** FINAL
**Generated:** 03-Jul-2026
**Total Automated Tests:** 75
