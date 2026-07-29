# NOC Future Date — Verification Report

---

# TEST PERFORMED

| Parameter | Value |
|-----------|-------|
| Future date set | `03/07/2027` (1 year from today) |
| Method | `ValidationHelper.set_readonly_date()` (JavaScript injection) |
| All other fields | Filled with valid data |
| Action | Click Next |

---

# RESULT

| Check | Outcome |
|-------|---------|
| DOM value after JS | `03/07/2027` ✅ |
| Form navigated to Trust Details | **YES** |
| Validation errors shown | **NONE** |
| Current URL | `https://dev-eaffiliation.cisce.org/preliminary/school/dashboard` |
| Screenshot | `screenshots/debug/noc_future_date_after_next.png` |

---

# CLASSIFICATION

## ⚠️ POTENTIAL APPLICATION DEFECT — Future Date Accepted

The application accepts a NOC date set 1 year in the future without any validation error.

**Business logic expectation:** A No Objection Certificate is issued by a government authority — it cannot have a future issuance date. An NOC dated in 2027 is logically impossible.

**However:** Without confirmed business requirements, this could also be an intentional design decision (e.g., allowing pre-dated certificates for future processing).

---

# RECOMMENDATION

| Action | Detail |
|--------|--------|
| **Keep NOC_FMT_006 in the test matrix** | Do NOT remove |
| **Mark as `@pytest.mark.xfail`** | `reason="Potential app defect: future NOC date accepted without validation"` |
| **Allure classification** | Tag as "Known Issue" in report |
| **Business confirmation needed** | Ask product owner: "Should the Date of NOC reject future dates?" |

### Implementation approach:
```python
@pytest.mark.xfail(reason="Potential app defect: future NOC date accepted without validation")
def test_noc_future_date_rejected(...)
```

This means:
- Test runs every regression cycle
- Failure is expected and documented (doesn't break suite)
- If the app adds future-date validation later → test auto-passes (shows as `xpass`)
- Allure shows it under "Known Issues"

---

# UPDATED NOC TEST MATRIX IMPACT

| TC ID | Previous Status | Updated Status |
|-------|----------------|----------------|
| NOC_FMT_006 | Automatable (Negative) | **Automatable — marked xfail (Potential Defect)** |

All other 11 test cases remain unchanged.

---

**STATUS:** Verification complete. NOC_FMT_006 confirmed as potential application defect. Implementation can proceed.
