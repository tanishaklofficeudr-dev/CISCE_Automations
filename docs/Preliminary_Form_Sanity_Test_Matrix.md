# CISCE Preliminary Form — Sanity Test Matrix
## Minimum Deployment Verification Suite

---

# SELECTION CRITERIA

Each test was selected because it:
1. Validates the **primary happy path** for its module
2. Detects **application-breaking defects** (form won't submit, page won't load)
3. Covers **critical mandatory validation** (at least one per module)
4. Verifies **navigation between steps** works
5. Is **independently executable** (no dependency on other sanity tests)

---

# SANITY TEST SUITE (20 tests)

| Sanity ID | Regression TC ID | Module | Scenario | Reason for Inclusion | Priority | Est. Time |
|-----------|-----------------|--------|----------|---------------------|----------|-----------|
| SAN-01 | SCH_POS_01 | School Details | Valid submission with all mandatory fields | Proves School Details form accepts valid data and navigates | Critical | 45s |
| SAN-02 | SCH_NEG_01 | School Details | School name blank — validation error | Proves mandatory validation mechanism works | Critical | 30s |
| SAN-03 | ADDR_POS_001 | Address Details | Valid address submission | Proves Address form works end-to-end | Critical | 45s |
| SAN-04 | ADDR_FMT_001 | Address Details | PIN code invalid (alphabets) | Proves format validation works | High | 30s |
| SAN-05 | NOC_POS_001 | NOC Details | Valid NOC submission | Proves NOC form submits correctly | Critical | 45s |
| SAN-06 | NOC_VAL_001 | NOC Details | All NOC fields blank — errors shown | Proves NOC validation catches missing fields | High | 30s |
| SAN-07 | TRUST_POS_001 | Trust Details | Valid Trust submission | Proves Trust form works | Critical | 45s |
| SAN-08 | TRUST_FMT_001 | Trust Details | Owner name blank — validation error | Proves Trust mandatory validation | High | 30s |
| SAN-09 | LAND_VAL_001 | Certificate of Land | Owned — all blank shows errors | Proves Land validation mechanism works | Critical | 40s |
| SAN-10 | LAND_POS_001 | Certificate of Land | Valid Owned — Conveyance Deed | Proves Owned path submits | Critical | 50s |
| SAN-11 | LAND_POS_002 | Certificate of Land | Valid Owned — Sale Deed + favor | Proves conditional field (Sale Deed) works | Critical | 50s |
| SAN-12 | LAND_POS_006 | Certificate of Land | Valid Leased — Renewal=No | Proves Leased path works | Critical | 50s |
| SAN-13 | LAND_POS_008 | Certificate of Land | Valid Multiple — Contiguous=Yes | Proves Multiple path works | Critical | 50s |
| SAN-14 | LAND_UI_002 | Certificate of Land | Sale Deed conditional toggle | Proves dynamic UI conditional works | High | 35s |
| SAN-15 | UPLOAD_VAL_001 | Upload Documents | Proceed with nothing — blocked | Proves upload validation blocks incomplete submissions | Critical | 30s |
| SAN-16 | UPLOAD_POS_001 | Upload Documents | Full flow — Provisional Affiliation | Proves upload + proceed to payment works | Critical | 60s |
| SAN-17 | UPLOAD_NEG_001 | Upload Documents | .exe file rejected | Proves file type validation works | High | 25s |
| SAN-18 | UPLOAD_NEG_004 | Upload Documents | Partial uploads (4/5) — blocked | Proves all-uploads-required validation | High | 40s |
| SAN-19 | UPLOAD_UI_002 | Upload Documents | Download for Notarization click | Proves download functionality works | High | 20s |
| SAN-20 | PAYMENT_POS_001 | Payment Gateway | HDFC gateway accessible | Proves payment gateway is functional | Critical | 90s |

---

# MODULE-WISE BREAKDOWN

| Module | Sanity Tests | IDs |
|--------|-------------|-----|
| School Details | 2 | SAN-01, SAN-02 |
| Address Details | 2 | SAN-03, SAN-04 |
| NOC Details | 2 | SAN-05, SAN-06 |
| Trust Details | 2 | SAN-07, SAN-08 |
| Certificate of Land | 5 | SAN-09, SAN-10, SAN-11, SAN-12, SAN-13, SAN-14 |
| Upload Documents | 5 | SAN-15, SAN-16, SAN-17, SAN-18, SAN-19 |
| Payment Gateway | 1 | SAN-20 |
| **TOTAL** | **20** | |

---

# PRIORITY DISTRIBUTION

| Priority | Count | Percentage |
|----------|-------|-----------|
| Critical | 13 | 65% |
| High | 7 | 35% |
| Medium | 0 | 0% |
| Low | 0 | 0% |

---

# ESTIMATED EXECUTION TIME

| Component | Time |
|-----------|------|
| Login + navigation overhead (shared) | ~60s |
| SAN-01 to SAN-08 (School → Trust) | ~5 min |
| SAN-09 to SAN-14 (Certificate of Land) | ~4.5 min |
| SAN-15 to SAN-19 (Upload Documents) | ~3 min |
| SAN-20 (Payment Gateway) | ~1.5 min |
| **TOTAL** | **~14 min** |

Within the 10–15 minute target. ✅

---

**STATUS:** Sanity matrix defined. 20 tests from existing regression suite provide deployment confidence.
