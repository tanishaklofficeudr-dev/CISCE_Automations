# Sanity Test Summary
## CISCE Preliminary Form — 20-Test Deployment Verification Suite

---

# SANITY TEST LIST

| SAN ID | Regression TC ID | Module | Purpose |
|--------|-----------------|--------|---------|
| SAN-01 | SCH_POS_01 | School Details | Valid school submission works |
| SAN-02 | SCH_NEG_01 | School Details | Mandatory validation blocks empty form |
| SAN-03 | ADDR_POS_001 | Address Details | Valid address submission works |
| SAN-04 | ADDR_FMT_001 | Address Details | PIN code format validation works |
| SAN-05 | NOC_POS_001 | NOC Details | Valid NOC submission works |
| SAN-06 | NOC_VAL_001 | NOC Details | All-blank NOC shows errors |
| SAN-07 | TRUST_POS_001 | Trust Details | Valid Trust submission works |
| SAN-08 | TRUST_FMT_001 | Trust Details | Trust mandatory validation works |
| SAN-09 | LAND_VAL_001 | Certificate of Land | Owned blank validation works |
| SAN-10 | LAND_POS_001 | Certificate of Land | Valid Owned — Conveyance Deed |
| SAN-11 | LAND_POS_002 | Certificate of Land | Valid Owned — Sale Deed conditional |
| SAN-12 | LAND_POS_006 | Certificate of Land | Valid Leased path works |
| SAN-13 | LAND_POS_008 | Certificate of Land | Valid Multiple path works |
| SAN-14 | LAND_UI_002 | Certificate of Land | Sale Deed dynamic toggle |
| SAN-15 | UPLOAD_VAL_001 | Upload Documents | Proceed blocked without prerequisites |
| SAN-16 | UPLOAD_POS_001 | Upload Documents | Full upload + proceed to payment |
| SAN-17 | UPLOAD_NEG_001 | Upload Documents | .exe file rejected |
| SAN-18 | UPLOAD_NEG_004 | Upload Documents | Partial uploads blocked |
| SAN-19 | UPLOAD_UI_002 | Upload Documents | Download for Notarization works |
| SAN-20 | PAYMENT_POS_001 | Payment Gateway | HDFC gateway accessible |

---

# EXECUTION COMMAND

```bash
python -m pytest tests/regression/ -m sanity -v --headed --alluredir=allure-results
```

---

# EXPECTED EXECUTION TIME

| Phase | Tests | Time |
|-------|-------|------|
| School + Address | 4 | ~3 min |
| NOC + Trust | 4 | ~3 min |
| Certificate of Land | 6 | ~4.5 min |
| Upload Documents | 5 | ~3 min |
| Payment Gateway | 1 | ~1.5 min |
| **TOTAL** | **20** | **~14 min** |

---

# MODULE BREAKDOWN

| Module | Sanity Tests |
|--------|-------------|
| School Details | 2 |
| Address Details | 2 |
| NOC Details | 2 |
| Trust Details | 2 |
| Certificate of Land | 6 |
| Upload Documents | 5 |
| Payment Gateway | 1 |
| **Total** | **20** |
