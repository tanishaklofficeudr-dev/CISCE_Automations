# Complete Test Case Inventory
## CISCE Preliminary Form — All Implemented & Planned Test Cases

---

# 0. REGISTRATION (26 tests — 📋 PLANNED)

| # | TC ID | Category |
|---|-------|----------|
| 1 | REG_POS_001 | Positive — Valid new registration |
| 2 | REG_POS_002 | Positive — Valid 10-digit mobile |
| 3 | REG_POS_003 | Positive — Registration with yopmail |
| 4 | REG_NEG_001 | Negative — Mobile blank |
| 5 | REG_NEG_002 | Negative — Email blank |
| 6 | REG_NEG_003 | Negative — Both fields blank |
| 7 | REG_NEG_004 | Negative — Mobile with alphabets |
| 8 | REG_NEG_005 | Negative — Mobile too short |
| 9 | REG_NEG_006 | Negative — Mobile too long |
| 10 | REG_NEG_007 | Negative — Mobile special chars |
| 11 | REG_NEG_008 | Negative — Invalid email format |
| 12 | REG_NEG_009 | Negative — Email without domain |
| 13 | REG_NEG_010 | Negative — Email with spaces |
| 14 | REG_NEG_011 | Negative — Duplicate mobile |
| 15 | REG_NEG_012 | Negative — Duplicate email |
| 16 | REG_VAL_001 | Validation — Required field indicators |
| 17 | REG_BND_001 | Boundary — Mobile exactly 10 digits |
| 18 | REG_BND_002 | Boundary — Email min before @ |
| 19 | REG_BND_003 | Boundary — Email max length |
| 20 | REG_BND_004 | Boundary — Mobile starts with 0 |
| 21 | REG_UI_001 | UI — Page loads correctly |
| 22 | REG_UI_002 | UI — Success popup appears |
| 23 | REG_UI_003 | UI — Navigation after registration |
| 24 | REG_SEC_001 | Security — SQL injection in mobile |
| 25 | REG_SEC_002 | Security — XSS in email |
| 26 | REG_NAV_001 | Navigation — Register navigates |

---

# 0B. LOGIN (30 tests — 📋 PLANNED)

| # | TC ID | Category |
|---|-------|----------|
| 1 | LOGIN_POS_001 | Positive — Valid login |
| 2 | LOGIN_POS_002 | Positive — Login with Excel credentials |
| 3 | LOGIN_NEG_001 | Negative — Invalid mobile |
| 4 | LOGIN_NEG_002 | Negative — Invalid password |
| 5 | LOGIN_NEG_003 | Negative — Mobile blank |
| 6 | LOGIN_NEG_004 | Negative — Password blank |
| 7 | LOGIN_NEG_005 | Negative — Both blank |
| 8 | LOGIN_NEG_006 | Negative — Mobile with alphabets |
| 9 | LOGIN_NEG_007 | Negative — Mobile too short |
| 10 | LOGIN_NEG_008 | Negative — Password spaces only |
| 11 | LOGIN_NEG_009 | Negative — 3 wrong attempts |
| 12 | LOGIN_VAL_001 | Validation — Required indicators |
| 13 | LOGIN_VAL_002 | Validation — Error message format |
| 14 | LOGIN_BND_001 | Boundary — Mobile 10 digits |
| 15 | LOGIN_BND_002 | Boundary — Password min length |
| 16 | LOGIN_BND_003 | Boundary — Password max length |
| 17 | LOGIN_UI_001 | UI — Page loads |
| 18 | LOGIN_UI_002 | UI — Password masking |
| 19 | LOGIN_UI_003 | UI — Button state |
| 20 | LOGIN_SEC_001 | Security — SQL injection mobile |
| 21 | LOGIN_SEC_002 | Security — SQL injection password |
| 22 | LOGIN_SEC_003 | Security — XSS in mobile |
| 23 | LOGIN_NAV_001 | Navigation — Successful login to dashboard |
| 24 | LOGIN_NAV_002 | Navigation — Back after logout |
| 25 | LOGIN_NAV_003 | Navigation — Direct URL without login |
| 26 | LOGIN_SESSION_001 | Session — Timeout |
| 27 | LOGIN_SESSION_002 | Session — Logout |
| 28 | LOGIN_SESSION_003 | Session — Multiple tabs |
| 29 | LOGIN_FORGOT_001 | Password — Forgot password link |
| 30 | LOGIN_FORGOT_002 | Password — Reset with valid mobile |

---

# 1. SCHOOL DETAILS (25 tests)

| # | TC ID | Category |
|---|-------|----------|
| 1 | SCH_VAL_001 (test_school_all_required_fields_blank) | Validation |
| 2 | SCH_POS_01 | Positive |
| 3 | SCH_POS_02 | Positive |
| 4 | SCH_POS_03 | Positive |
| 5 | SCH_POS_04 | Positive |
| 6 | SCH_POS_05 | Positive |
| 7 | SCH_POS_06 | Positive |
| 8 | SCH_POS_07 | Positive |
| 9 | SCH_POS_08 | Positive |
| 10 | SCH_NEG_01 | Negative |
| 11 | SCH_NEG_02 | Negative |
| 12 | SCH_NEG_03 | Negative |
| 13 | SCH_NEG_07 | Negative |
| 14 | SCH_NEG_08 | Negative |
| 15 | SCH_NEG_09 | Negative |
| 16 | SCH_NEG_10 | Negative |
| 17 | SCH_BND_EXT_01 | Boundary |
| 18 | SCH_BND_EXT_02 | Boundary |
| 19 | SCH_BND_EXT_03 | Boundary |
| 20 | SCH_BND_EXT_04 | Boundary |
| 21 | SCH_BND_EXT_05 | Boundary |
| 22 | SCH_BND_EXT_06 | Boundary |
| 23 | SCH_BND_EXT_07 | Boundary |
| 24 | SCH_BND_EXT_08 | Boundary |
| 25 | SCH_BND_EXT_09 | Boundary |

---

# 2. ADDRESS DETAILS (13 tests)

| # | TC ID | Category |
|---|-------|----------|
| 1 | ADDR_VAL_001 (test_address_all_required_fields_blank) | Validation |
| 2 | ADDR_POS_001 | Positive |
| 3 | ADDR_POS_002 | Positive |
| 4 | ADDR_POS_003 | Positive |
| 5 | ADDR_FMT_001 | Negative |
| 6 | ADDR_FMT_002 | Negative |
| 7 | ADDR_FMT_003 | Negative |
| 8 | ADDR_FMT_004 | Negative |
| 9 | ADDR_FMT_005 | Negative |
| 10 | ADDR_FMT_006 | Negative |
| 11 | ADDR_BND_001 | Boundary |
| 12 | ADDR_BND_002 | Boundary |
| 13 | ADDR_BND_003 | Boundary |

---

# 3. NOC DETAILS (12 tests)

| # | TC ID | Category |
|---|-------|----------|
| 1 | NOC_VAL_001 (test_noc_all_required_fields_blank) | Validation |
| 2 | NOC_POS_001 | Positive |
| 3 | NOC_POS_002 | Positive |
| 4 | NOC_FMT_001 | Negative |
| 5 | NOC_FMT_002 | Negative |
| 6 | NOC_FMT_003 | Negative |
| 7 | NOC_FMT_004 | Negative |
| 8 | NOC_FMT_005 | Negative |
| 9 | NOC_FMT_006 | Negative |
| 10 | NOC_BND_001 | Boundary |
| 11 | NOC_BND_002 | Boundary |
| 12 | NOC_BND_003 | Boundary |

---

# 4. TRUST DETAILS (12 tests)

| # | TC ID | Category |
|---|-------|----------|
| 1 | TRUST_VAL_001 (test_trust_all_required_fields_blank) | Validation |
| 2 | TRUST_POS_001 | Positive |
| 3 | TRUST_POS_002 | Positive |
| 4 | TRUST_FMT_001 | Negative |
| 5 | TRUST_FMT_002 | Negative |
| 6 | TRUST_FMT_003 | Negative |
| 7 | TRUST_FMT_004 | Negative |
| 8 | TRUST_FMT_005 | Negative |
| 9 | TRUST_FMT_006 | Negative |
| 10 | TRUST_BND_001 | Boundary |
| 11 | TRUST_BND_002 | Boundary |
| 12 | TRUST_BND_003 | Boundary |

---

# 5. CERTIFICATE OF LAND (34 tests)

| # | TC ID | Category | Flow |
|---|-------|----------|------|
| 1 | LAND_VAL_001 | Validation | Owned |
| 2 | LAND_VAL_002 | Validation | Leased |
| 3 | LAND_VAL_003 | Validation | Multiple |
| 4 | LAND_POS_001 | Positive | Owned — Conveyance |
| 5 | LAND_POS_002 | Positive | Owned — Sale Deed School |
| 6 | LAND_POS_003 | Positive | Owned — Sale Deed Trust |
| 7 | LAND_POS_004 | Positive | Owned — Gift Deed |
| 8 | LAND_POS_005 | Positive | Owned — Square Foot |
| 9 | LAND_POS_006 | Positive | Leased — Renewal No |
| 10 | LAND_POS_007 | Positive | Leased — Renewal Yes |
| 11 | LAND_POS_008 | Positive | Multiple — Contiguous Yes |
| 12 | LAND_POS_009 | Positive | Multiple — Full Nested |
| 13 | LAND_NEG_001 | Negative | Owned — Area blank |
| 14 | LAND_NEG_002 | Negative | Owned — Situated blank |
| 15 | LAND_NEG_003 | Negative | Owned — Alphabets |
| 16 | LAND_NEG_004 | Negative | Owned — Negative value |
| 17 | LAND_NEG_005 | Negative | Owned — Future date |
| 18 | LAND_NEG_006 | Negative | Owned — Favor blank |
| 19 | LAND_NEG_007 | Negative | Leased — Area blank |
| 20 | LAND_NEG_008 | Negative | Leased — Duration alpha |
| 21 | LAND_NEG_009 | Negative | Leased — Renewal blank |
| 22 | LAND_NEG_010 | Negative | Multiple — Plots=0 |
| 23 | LAND_NEG_011 | Negative | Multiple — Explanation blank |
| 24 | LAND_BND_001 | Boundary | Owned — Area=1 |
| 25 | LAND_BND_002 | Boundary | Owned — Area large |
| 26 | LAND_BND_003 | Boundary | Owned — Date today |
| 27 | LAND_BND_004 | Boundary | Owned — 500 chars |
| 28 | LAND_BND_005 | Boundary | Leased — Duration=1 |
| 29 | LAND_BND_006 | Boundary | Multiple — Plots=2 |
| 30 | LAND_BND_007 | Boundary | Multiple — Plots=100 |
| 31 | LAND_UI_001 | UI | Owned form loads |
| 32 | LAND_UI_002 | UI | Sale Deed toggle |
| 33 | LAND_UI_003 | UI | Renewal toggle |
| 34 | LAND_UI_004 | UI | Multiple nested |
| — | LAND_UI_005 | UI | Path switch |

---

# 6. UPLOAD DOCUMENTS (28 tests)

| # | TC ID | Category |
|---|-------|----------|
| 1 | UPLOAD_VAL_001 | Validation |
| 2 | UPLOAD_VAL_002 | Validation |
| 3 | UPLOAD_VAL_003 | Validation |
| 4 | UPLOAD_POS_001 | Positive |
| 5 | UPLOAD_POS_002 | Positive |
| 6 | UPLOAD_POS_003 | Positive |
| 7 | UPLOAD_POS_004 | Positive |
| 8 | UPLOAD_POS_005 | Positive |
| 9 | UPLOAD_POS_006 | Positive |
| 10 | UPLOAD_POS_007 | Positive |
| 11 | UPLOAD_POS_008 | Positive |
| 12 | UPLOAD_POS_009 | Positive |
| 13 | UPLOAD_NEG_001 | Negative |
| 14 | UPLOAD_NEG_002 | Negative |
| 15 | UPLOAD_NEG_003 | Negative |
| 16 | UPLOAD_NEG_004 | Negative |
| 17 | UPLOAD_NEG_005 | Negative |
| 18 | UPLOAD_NEG_006 | Negative |
| 19 | UPLOAD_NEG_007 | Negative |
| 20 | UPLOAD_BND_001 | Boundary |
| 21 | UPLOAD_BND_002 | Boundary |
| 22 | UPLOAD_BND_003 | Boundary |
| 23 | UPLOAD_BND_004 | Boundary |
| 24 | UPLOAD_UI_001 | UI |
| 25 | UPLOAD_UI_002 | UI |
| 26 | UPLOAD_UI_003 | UI |
| 27 | UPLOAD_UI_004 | UI |
| 28 | UPLOAD_UI_005 | UI |

---

# 7. PAYMENT GATEWAY (3 tests)

| # | TC ID | Category | Bank |
|---|-------|----------|------|
| 1 | PAYMENT_POS_001 | Positive | HDFC Collect Now |
| 2 | PAYMENT_POS_002 | Positive | ICICI Bank |
| 3 | PAYMENT_POS_003 | Positive | Federal Bank |

---

# GRAND TOTAL

| Module | Tests |
|--------|-------|
| Registration (📋 Planned) | 26 |
| Login (📋 Planned) | 30 |
| School Details | 25 |
| Address Details | 13 |
| NOC Details | 12 |
| Trust Details | 12 |
| Certificate of Land | 34 |
| Upload Documents | 28 |
| Payment Gateway | 3 |
| **Regression Total** | **179** (123 implemented + 56 planned) |
| E2E | 1 |
| **Grand Total** | **180** |
