# CISCE Preliminary Form — Sanity Execution Plan
## Operational Execution Guide

---

# 1. RECOMMENDED EXECUTION ORDER

The tests should execute in workflow order (matching the actual user journey):

| Order | Sanity ID | Module | Dependency |
|-------|-----------|--------|-----------|
| 1 | SAN-01 | School Details | None (first module) |
| 2 | SAN-02 | School Details | None |
| 3 | SAN-03 | Address Details | None (tab navigation) |
| 4 | SAN-04 | Address Details | None |
| 5 | SAN-05 | NOC Details | None |
| 6 | SAN-06 | NOC Details | None |
| 7 | SAN-07 | Trust Details | None |
| 8 | SAN-08 | Trust Details | None |
| 9 | SAN-09 | Certificate of Land | None |
| 10 | SAN-10 | Certificate of Land | None |
| 11 | SAN-11 | Certificate of Land | None |
| 12 | SAN-12 | Certificate of Land | None |
| 13 | SAN-13 | Certificate of Land | None |
| 14 | SAN-14 | Certificate of Land | None |
| 15 | SAN-15 | Upload Documents | None |
| 16 | SAN-16 | Upload Documents | None |
| 17 | SAN-17 | Upload Documents | None |
| 18 | SAN-18 | Upload Documents | None |
| 19 | SAN-19 | Upload Documents | None |
| 20 | SAN-20 | Payment Gateway | Requires upload_ready_page fixture |

---

# 2. DEPENDENCY BETWEEN TESTS

| Test | Depends On | Type |
|------|-----------|------|
| SAN-01 to SAN-19 | `school_details_ready_page` fixture | Login + tab navigation |
| SAN-20 | `payment_ready_page` fixture | Full upload + proceed |
| All tests | Same account credentials | Shared login state |

**Each test is independently executable** — fixtures handle all setup. No test depends on another test's output.

---

# 3. PARALLEL EXECUTION OPPORTUNITIES

| Strategy | Feasibility | Notes |
|----------|-------------|-------|
| Full parallel (all 20 at once) | ❌ Not possible | Same account — concurrent logins may conflict |
| Module-level parallel | ⚠️ Risky | SPA state shared — forms may interfere |
| Sequential (recommended) | ✅ Safe | Each test uses its own page instance |
| 2-worker parallel (school+noc vs address+trust) | ⚠️ Possible | Requires separate accounts |

**Recommendation:** Execute **sequentially** for sanity. Speed is already ~14 min — parallelization adds complexity without significant gain.

---

# 4. EXECUTION COMMANDS

## Full Sanity Suite
```bash
python -m pytest tests/regression/ -k "SCH_POS_01 or SCH_NEG_01 or ADDR_POS_001 or ADDR_FMT_001 or NOC_POS_001 or NOC_VAL or TRUST_POS_001 or TRUST_FMT_001 or LAND_VAL_001 or LAND_POS_001 or LAND_POS_002 or LAND_POS_006 or LAND_POS_008 or LAND_UI_002 or UPLOAD_VAL_001 or UPLOAD_POS_001 or UPLOAD_NEG_001 or UPLOAD_NEG_004 or UPLOAD_UI_002 or PAYMENT_POS_001" -v --headed
```

## Module-Specific Sanity
```bash
# School + Address
python -m pytest tests/regression/school_details/ tests/regression/address_details/ -k "POS_01 or NEG_01 or POS_001 or FMT_001" -v

# NOC + Trust
python -m pytest tests/regression/noc_details/ tests/regression/trust_details/ -k "POS_001 or VAL or FMT_001" -v

# Certificate of Land
python -m pytest tests/regression/land_certificate/ -k "VAL_001 or POS_001 or POS_002 or POS_006 or POS_008 or UI_002" -v

# Upload Documents
python -m pytest tests/regression/upload_documents/ -k "VAL_001 or POS_001 or NEG_001 or NEG_004 or UI_002" -v

# Payment Gateway
python -m pytest tests/regression/payment_gateway/ -k "POS_001" -v --headed
```

---

# 5. EXPECTED EXECUTION DURATION

| Phase | Tests | Duration |
|-------|-------|----------|
| Login + setup (shared) | — | ~30s per test |
| School Details (2) | SAN-01, SAN-02 | ~1.5 min |
| Address Details (2) | SAN-03, SAN-04 | ~1.5 min |
| NOC Details (2) | SAN-05, SAN-06 | ~1.5 min |
| Trust Details (2) | SAN-07, SAN-08 | ~1.5 min |
| Certificate of Land (6) | SAN-09 to SAN-14 | ~4.5 min |
| Upload Documents (5) | SAN-15 to SAN-19 | ~3 min |
| Payment Gateway (1) | SAN-20 | ~1.5 min |
| **TOTAL** | **20** | **~14 min** |

---

# 6. EXPECTED ALLURE REPORT STRUCTURE

```
CISCE E-Affiliation (Parent Suite)
├── School Details
│   ├── Positive: SAN-01
│   └── Negative: SAN-02
├── Address Details
│   ├── Positive: SAN-03
│   └── Negative: SAN-04
├── NOC Details
│   ├── Positive: SAN-05
│   └── Validation: SAN-06
├── Trust Details
│   ├── Positive: SAN-07
│   └── Negative: SAN-08
├── Certificate of Land
│   ├── Validation: SAN-09
│   ├── Positive: SAN-10, SAN-11, SAN-12, SAN-13
│   └── Dynamic UI: SAN-14
├── Upload Documents
│   ├── Validation: SAN-15
│   ├── Positive: SAN-16
│   ├── Negative: SAN-17, SAN-18
│   └── Dynamic UI: SAN-19
└── Payment Gateway
    └── Positive: SAN-20
```

---

# 7. CI/CD EXECUTION RECOMMENDATIONS

## Pipeline Integration

| Stage | Action | Command |
|-------|--------|---------|
| Post-deploy (DEV) | Run sanity | `python -m pytest ... -k "SANITY_FILTER" --alluredir=allure-results` |
| Pre-UAT | Run sanity + summary | Same + generate Allure report |
| Pre-Production | Run full regression | `python -m pytest tests/regression/ -v` |
| Nightly | Full regression + E2E | All tests |

## CI/CD Environment Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.14+ |
| Playwright browsers installed | Yes (`playwright install`) |
| Headed mode | Not required for CI (use headless) |
| Video recording | Optional (configured in conftest) |
| Allure CLI | Required for report generation |
| Execution timeout | 20 min (with buffer) |
| Network access | Required (external payment gateway) |

## Failure Handling

| Scenario | Action |
|----------|--------|
| 0 failures | ✅ Deploy |
| 1–2 High failures | ⚠️ Investigate — may deploy if non-blocking |
| Any Critical failure | ❌ Block deployment |
| >3 failures | ❌ Run full regression before deploy |
| Payment Gateway failure | ⚠️ May be external — check gateway status |

---

# 8. MAINTENANCE NOTES

| When | Action |
|------|--------|
| New module added | Add 2 sanity tests (1 positive + 1 negative) |
| Existing validation changes | Update expected error message in Excel |
| Locator changes | Update page object only — tests stay unchanged |
| New business rule added | Consider if it's deployment-critical for sanity |
| Test consistently flaky | Replace with a more stable equivalent |

---

# 9. FINAL SUMMARY

| Metric | Value |
|--------|-------|
| **Total sanity tests** | 20 |
| **Execution time** | ~14 minutes |
| **Business flows covered** | 10/10 (100%) |
| **Modules covered** | 7/7 (100%) |
| **Navigation steps covered** | 9/9 (100%) |
| **New code required** | 0 (reuses existing regression tests) |
| **Maintenance effort** | Minimal (filter by test ID) |
| **CI/CD ready** | Yes (headless execution supported) |

---

**STATUS:** Sanity execution plan complete. Suite is ready for operational use.
