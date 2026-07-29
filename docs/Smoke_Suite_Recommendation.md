# Smoke Suite Classification — Recommendation Report
## test_preliminary_form_main.py

---

# 1. RECOMMENDATION

**YES — `test_preliminary_form_main.py` IS the Smoke Suite for the Preliminary Form module.**

### Rationale:

| Smoke Suite Criteria | Does E2E Meet It? |
|---------------------|-------------------|
| Covers critical business path end-to-end | ✅ Registration → Login → All Forms → Payment → Success |
| Tests core functionality works at all | ✅ Every major module is exercised |
| Fails if any critical feature is broken | ✅ Any broken step causes immediate failure |
| Runs in reasonable time (under 10 min) | ✅ ~2-5 minutes per school |
| Does NOT test edge cases or validations | ✅ Only positive happy path |
| Suitable as build verification test | ✅ If this passes, the app works |

---

# 2. PYTEST MARKERS THAT SHOULD BE APPLIED

### Currently Applied:
```python
@pytest.mark.sanity
@pytest.mark.regression
```

### Should Also Include:
```python
@pytest.mark.smoke
```

### Recommended Final State:
```python
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.regression
```

This allows running the E2E test under any suite filter:
- `pytest -m smoke` → includes this test
- `pytest -m sanity` → includes this test
- `pytest -m regression` → includes this test

---

# 3. ALLURE LABELS THAT SHOULD BE APPLIED

### Currently Applied:
```python
@allure.epic("CISCE Preliminary Affiliation Form")
@allure.feature("End-to-End Form Submission")
@allure.severity(allure.severity_level.CRITICAL)
```

### No Changes Required.

The existing Allure labels are already correct for a Smoke test:
- Epic: Project-level grouping ✅
- Feature: Describes the E2E flow ✅
- Severity: CRITICAL ✅ (correct for smoke)
- Dynamic story, title, tags already applied per test ✅

---

# 4. CODE CHANGES REQUIRED

| Type | Change | Affects Business Logic? |
|------|--------|------------------------|
| Add `@pytest.mark.smoke` decorator | Metadata only (one line) | **NO** |

### Exact Change (single line addition):

**Before:**
```python
@allure.epic("CISCE Preliminary Affiliation Form")
@allure.feature("End-to-End Form Submission")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.parametrize("school_id", school_ids)
def test_preliminary_form(page, school_id):
```

**After:**
```python
@allure.epic("CISCE Preliminary Affiliation Form")
@allure.feature("End-to-End Form Submission")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.parametrize("school_id", school_ids)
def test_preliminary_form(page, school_id):
```

---

# 5. CHANGE CLASSIFICATION

| Question | Answer |
|----------|--------|
| Is this a metadata change? | **YES** — decorator only |
| Does it modify business logic? | **NO** |
| Does it change test steps? | **NO** |
| Does it change assertions? | **NO** |
| Does it change page interactions? | **NO** |
| Does it change data flow? | **NO** |
| Does it affect test execution? | **NO** (unless filtered by `-m smoke`) |
| Is it backward compatible? | **YES** — existing `pytest` runs unchanged |

---

# 6. CONFIRMATION

| Statement | Confirmed |
|-----------|-----------|
| No business logic changes are necessary | ✅ CONFIRMED |
| No Page Object changes needed | ✅ CONFIRMED |
| No fixture changes needed | ✅ CONFIRMED |
| No data changes needed | ✅ CONFIRMED |
| No new files needed | ✅ CONFIRMED |
| Only a single decorator line is added | ✅ CONFIRMED |

---

# 7. EXECUTION AFTER CHANGE

```powershell
# Run ONLY smoke suite
python -m pytest -m smoke --headed -v --alluredir=allure-results

# This will run:
# - test_preliminary_form_main.py (E2E = Smoke)
# - Any future tests marked @pytest.mark.smoke
```

---

# 8. ALSO REQUIRED IN pytest.ini

The `smoke` marker must be registered to avoid warnings:

**Current:**
```ini
markers =
    sanity: Sanity test cases
    regression: Regression test cases
    negative: Negative validation scenarios
    boundary: Boundary value scenarios
```

**Add:**
```ini
    smoke: Smoke test - critical path build verification
```

---

**STATUS:** Recommendation only. No code modified.
**Action Required:** Approve, then apply the single-line decorator addition.
