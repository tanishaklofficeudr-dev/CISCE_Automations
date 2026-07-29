# Regression Test Summary
## CISCE Preliminary Form Automation

---

# MODULE-WISE REGRESSION COUNT

| Module | Positive | Negative | Boundary | Validation | UI Behaviour | Security/Session | Total |
|--------|----------|----------|----------|------------|-------------|-----------------|-------|
| Registration (📋 Planned) | 3 | 12 | 4 | 1 | 3 | 3 | **26** |
| Login (📋 Planned) | 2 | 9 | 3 | 2 | 3 | 11 | **30** |
| School Details | 8 | 4 | 9 | 1 | — | — | **22** |
| Address Details | 3 | 6 | 3 | 1 | — | — | **13** |
| NOC Details | 2 | 6 | 3 | 1 | — | — | **12** |
| Trust Details | 2 | 6 | 3 | 1 | — | — | **12** |
| Certificate of Land | 9 | 10 | 7 | 3 | 5 | — | **34** |
| Upload Documents | 9 | 7 | 4 | 3 | 4 | — | **27** |
| Payment Gateway | 3 | — | — | — | — | — | **3** |
| **TOTAL** | **41** | **60** | **36** | **13** | **15** | **14** | **179** |

---

# CATEGORY BREAKDOWN

| Category | Count | Percentage |
|----------|-------|-----------|
| Positive | 36 | 28% |
| Negative | 42 | 33% |
| Boundary | 29 | 23% |
| Validation | 10 | 8% |
| UI Behaviour | 10 | 8% |
| **Grand Total** | **127** | 100% |

---

# ADDITIONAL TESTS (Non-Regression)

| Suite | Tests |
|-------|-------|
| E2E (test_preliminary_form_main.py) | 1 |
| Legacy Sanity (tests/sanity/) | 4 |
| Legacy Sanity/Regression Suite | 20 |
| **Total Non-Regression** | **25** |

---

# GRAND TOTAL

| Metric | Value |
|--------|-------|
| **Regression tests (implemented)** | 123 |
| **Regression tests (planned: Reg + Login)** | 56 |
| **Total regression (all)** | **179** |
| **E2E** | 1 |
| **Grand Total** | **180** |
