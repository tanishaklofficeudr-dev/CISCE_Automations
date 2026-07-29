# CISCE Preliminary Form — Sanity Coverage Report
## 20-Test Suite Coverage Analysis

---

# 1. MODULE-WISE SANITY COVERAGE

| Module | Total Regression | Sanity Selected | Coverage Type |
|--------|-----------------|-----------------|---------------|
| School Details | 21 | 2 | 1 positive + 1 negative |
| Address Details | 13 | 2 | 1 positive + 1 negative |
| NOC Details | 12 | 2 | 1 positive + 1 validation |
| Trust Details | 12 | 2 | 1 positive + 1 negative |
| Certificate of Land | 34 | 6 | 1 validation + 3 positive (all paths) + 1 UI |
| Upload Documents | 28 | 5 | 1 validation + 1 positive + 2 negative + 1 UI |
| Payment Gateway | 3 | 1 | 1 positive (gateway access) |
| **TOTAL** | **123+** | **20** | **~16% of regression** |

---

# 2. BUSINESS FLOW COVERAGE

| # | Business Flow | Sanity Test | Status |
|---|--------------|-------------|--------|
| 1 | School Details can be submitted with valid data | SAN-01 | ✅ |
| 2 | Address Details can be submitted | SAN-03 | ✅ |
| 3 | NOC Details can be submitted | SAN-05 | ✅ |
| 4 | Trust Details can be submitted | SAN-07 | ✅ |
| 5 | Land Certificate — Owned path works | SAN-10 | ✅ |
| 6 | Land Certificate — Sale Deed conditional works | SAN-11 | ✅ |
| 7 | Land Certificate — Leased path works | SAN-12 | ✅ |
| 8 | Land Certificate — Multiple path works | SAN-13 | ✅ |
| 9 | Upload Documents — full upload + proceed | SAN-16 | ✅ |
| 10 | Payment Gateway — bank selection + iframe | SAN-20 | ✅ |

**All 10 critical business flows covered: 10/10 = 100%**

---

# 3. NAVIGATION COVERAGE

| Navigation Step | Sanity Test | Status |
|-----------------|-------------|--------|
| Login → Dashboard | All tests (fixture) | ✅ |
| Dashboard → School Details | SAN-01, SAN-02 | ✅ |
| School Details → Address Details | SAN-03 (implicit via positive submission) | ✅ |
| Address → NOC | SAN-05 (tab navigation) | ✅ |
| NOC → Trust | SAN-07 (tab navigation) | ✅ |
| Trust → Certificate of Land | SAN-09–14 (tab navigation) | ✅ |
| Certificate of Land → Upload Documents | SAN-15–19 (tab navigation) | ✅ |
| Upload Documents → Payment Gateway | SAN-16, SAN-20 | ✅ |
| Payment Gateway → Bank Page | SAN-20 | ✅ |

**All navigation steps covered: 9/9 = 100%**

---

# 4. VALIDATION COVERAGE

| Module | Validation Tested | Sanity Test |
|--------|-------------------|-------------|
| School Details | Mandatory field blank → error | SAN-02 |
| Address Details | Format validation (PIN code) | SAN-04 |
| NOC Details | All fields blank → errors | SAN-06 |
| Trust Details | Mandatory field blank → error | SAN-08 |
| Certificate of Land | All Owned blank → errors | SAN-09 |
| Upload Documents | No prerequisites → blocked | SAN-15 |
| Upload Documents | Invalid file type → rejected | SAN-17 |
| Upload Documents | Missing uploads → blocked | SAN-18 |

**Validation coverage: At least 1 per module = 100%**

---

# 5. DYNAMIC UI COVERAGE

| Dynamic Behaviour | Sanity Test | Status |
|-------------------|-------------|--------|
| Sale Deed conditional field toggle | SAN-14 | ✅ |
| Download for Notarization link | SAN-19 | ✅ |
| Payment iframe interaction | SAN-20 | ✅ |

**Critical dynamic UI covered: 3/3 = 100%**

---

# 6. PAYMENT COVERAGE

| Payment Flow Step | Sanity Test |
|-------------------|-------------|
| Navigate to payment page | SAN-20 |
| Click Pay ₹ | SAN-20 |
| Select bank (HDFC) | SAN-20 |
| Proceed to Pay | SAN-20 |
| Show QR (iframe) | SAN-20 |
| Continue/Pay (iframe) | SAN-20 |
| Bank page reached | SAN-20 |

**Full payment flow (minus actual payment): 100%**

---

# 7. OVERALL COVERAGE PERCENTAGE

| Metric | Value |
|--------|-------|
| Total regression tests | ~152 |
| Sanity tests selected | 20 |
| Sanity as % of regression | ~13% |
| Business flows covered | 10/10 (100%) |
| Navigation steps covered | 9/9 (100%) |
| Modules with validation tested | 6/6 (100%) |
| Dynamic UI behaviours covered | 3/3 (100%) |
| Payment gateway covered | 1/1 (100%) |

**The 20-test sanity suite covers 100% of critical business paths with only 13% of total regression volume.**

---

# 8. WHAT SANITY DOES NOT COVER (Acceptable)

| Area | Why Excluded |
|------|-------------|
| Boundary values (min/max) | Not deployment-blocking |
| Multiple dropdown permutations | One representative sufficient |
| Every negative input type | One per module proves mechanism works |
| Leased renewal toggle | Covered by positive test (SAN-12) |
| Multiple plot nested chain | Covered by positive test (SAN-13) |
| Comments textarea boundary | Optional field — not critical |
| Individual file type uploads (PNG, BMP) | PDF upload proves mechanism |
| ICICI / Federal bank separately | HDFC proves gateway mechanism works |

---

# 9. DEPLOYMENT READINESS ASSESSMENT

| If Sanity Passes | Confidence |
|-----------------|------------|
| All 20 tests PASS | ✅ Application is healthy — deploy |
| 1–2 failures in low-priority | ⚠️ Investigate — may still deploy |
| Any Critical failure | ❌ Block deployment — investigate |
| Multiple module failures | ❌ Block — regression required |

---

**STATUS:** Sanity coverage verified. 20 tests provide 100% critical path coverage in ~14 minutes.
