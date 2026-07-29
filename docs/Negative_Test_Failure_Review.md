# School Details — Negative Test Failure Review
## Individual Assessment of Each Failing Test Case

---

# REVIEW SUMMARY

| Total Negative Tests | Passed | Failed | Pass Rate |
|---------------------|--------|--------|-----------|
| 7 (execute=Yes) | 0 | 7 | 0% |

All negative tests failed because the form **accepted invalid data and navigated to the next step** — meaning no client-side validation exists for these scenarios.

---

# INDIVIDUAL REVIEW

---

## 1. SCH_NEG_01

| Field | Detail |
|-------|--------|
| **Test Case ID** | SCH_NEG_01 |
| **Validation Being Verified** | Blank school name should not be accepted |
| **Current Application Behavior** | Form navigates to Address Details when school name is cleared |
| **Expected Behavior** | Form should block and show "School name is required" |
| **Source of Expected Behavior** | Field is marked with asterisk (*) on the UI indicating mandatory |
| **Classification** | **Valid Defect** — UI indicates mandatory but no client-side validation enforces it |
| **Recommendation** | **Move to Known Defects** — document as bug, keep test but expect failure until fixed |

---

## 2. SCH_NEG_02

| Field | Detail |
|-------|--------|
| **Test Case ID** | SCH_NEG_02 |
| **Validation Being Verified** | School name with only special characters (@#$%^&) should be rejected |
| **Current Application Behavior** | Form accepts "@#$%^&*()" as valid school name and navigates |
| **Expected Behavior** | Form should reject non-alphabetic-only input for a name field |
| **Source of Expected Behavior** | QA assumption — school names should contain at least some alphabetic characters |
| **Classification** | **Test Assumption** — No documented requirement states special chars are invalid |
| **Recommendation** | **Await Business Confirmation** — ask product owner: "Is a school name of only @#$%^ valid?" If no requirement exists, remove from automation |

---

## 3. SCH_NEG_03

| Field | Detail |
|-------|--------|
| **Test Case ID** | SCH_NEG_03 |
| **Validation Being Verified** | School name with only numbers (123456789) should be rejected |
| **Current Application Behavior** | Form accepts "123456789" as valid school name and navigates |
| **Expected Behavior** | Form should reject numeric-only school name |
| **Source of Expected Behavior** | QA assumption — school names should contain alphabetic characters |
| **Classification** | **Test Assumption** — No documented requirement prohibits numeric school names |
| **Recommendation** | **Await Business Confirmation** — ask: "Can a school name be entirely numeric?" Some schools do have numbers (e.g., "School No. 45"). If acceptable, remove from automation |

---

## 4. SCH_NEG_07

| Field | Detail |
|-------|--------|
| **Test Case ID** | SCH_NEG_07 |
| **Validation Being Verified** | UDISE with alphabetic characters should be rejected |
| **Current Application Behavior** | Form accepts "abcdefghijk" in UDISE field and navigates |
| **Expected Behavior** | UDISE field should only accept numeric digits |
| **Source of Expected Behavior** | UDISE (Unified District Information System for Education) is officially a numeric-only code issued by the government |
| **Classification** | **Valid Defect** — UDISE is by definition numeric-only; accepting alphabets is incorrect |
| **Recommendation** | **Move to Known Defects** — this is a legitimate missing validation. UDISE codes are always 11 numeric digits |

---

## 5. SCH_NEG_08

| Field | Detail |
|-------|--------|
| **Test Case ID** | SCH_NEG_08 |
| **Validation Being Verified** | UDISE with special characters (123@#$456!!) should be rejected |
| **Current Application Behavior** | Form accepts special characters in UDISE and navigates |
| **Expected Behavior** | UDISE should only accept 11 numeric digits |
| **Source of Expected Behavior** | Same as above — UDISE is a government-issued numeric code |
| **Classification** | **Valid Defect** — same root cause as SCH_NEG_07 |
| **Recommendation** | **Move to Known Defects** — duplicate of same validation gap as SCH_NEG_07 |

---

## 6. SCH_NEG_09

| Field | Detail |
|-------|--------|
| **Test Case ID** | SCH_NEG_09 |
| **Validation Being Verified** | Contact person with only numbers (123456) should be rejected |
| **Current Application Behavior** | Form accepts "123456" as contact person name and navigates |
| **Expected Behavior** | Contact person name should contain alphabetic characters |
| **Source of Expected Behavior** | QA assumption — person names should have alphabetic content |
| **Classification** | **Test Assumption** — No documented requirement mandates alphabetic-only names |
| **Recommendation** | **Await Business Confirmation** — ask: "Should contact person field reject numeric-only input?" The field is for a human name, but no formal validation spec exists |

---

## 7. SCH_NEG_10

| Field | Detail |
|-------|--------|
| **Test Case ID** | SCH_NEG_10 |
| **Validation Being Verified** | Website with invalid URL format ("notavalidurl") should be rejected |
| **Current Application Behavior** | Form accepts "notavalidurl" as website and navigates |
| **Expected Behavior** | Website field should validate URL format (must contain http/https, domain, etc.) |
| **Source of Expected Behavior** | QA assumption — URL fields typically validate format |
| **Classification** | **Requirement Missing** — Website field has no format validation; likely optional and unvalidated by design |
| **Recommendation** | **Await Business Confirmation** — ask: "Should the website field enforce URL format?" If it's optional and free-text, remove validation test. If it should be a valid URL, log as defect |

---

# CLASSIFICATION SUMMARY

| Classification | Count | Test Case IDs |
|---------------|-------|---------------|
| **Valid Defect** | 3 | SCH_NEG_01, SCH_NEG_07, SCH_NEG_08 |
| **Test Assumption** | 2 | SCH_NEG_02, SCH_NEG_03 |
| **Requirement Missing** | 1 | SCH_NEG_10 |
| **Await Business Confirmation** | 4 | SCH_NEG_02, SCH_NEG_03, SCH_NEG_09, SCH_NEG_10 |

---

# RECOMMENDATION SUMMARY

| Action | Test Cases | Rationale |
|--------|-----------|-----------|
| **Move to Known Defects** | SCH_NEG_01, SCH_NEG_07, SCH_NEG_08 | Application has a clear obligation to validate (mandatory field asterisk, government numeric code) but doesn't |
| **Await Business Confirmation** | SCH_NEG_02, SCH_NEG_03, SCH_NEG_09, SCH_NEG_10 | No documented requirement — needs PO decision |
| **Keep in Regression** | All 7 | Keep executing all — failures are documented with proper classification |

---

# PROPOSED HANDLING IN FRAMEWORK

| Approach | Implementation |
|----------|----------------|
| **Known Defects** (SCH_NEG_01, 07, 08) | Add `@pytest.mark.xfail(reason="Known defect: validation missing")` — test runs, failure is expected and tracked |
| **Pending Confirmation** (SCH_NEG_02, 03, 09, 10) | Add `@pytest.mark.xfail(reason="Awaiting business confirmation")` — test runs, treated as expected failure until requirement confirmed |

Using `xfail` means:
- Tests still execute every run
- Failures don't break the suite
- If the app adds validation later, the test auto-passes (and shows as `xpass` — unexpected pass, prompting review)
- Allure shows them as "known issues" not "regressions"

---

# DECISION REQUIRED FROM YOU

Before I modify the code, confirm:

1. **SCH_NEG_01** (blank school name accepted) — Do you agree this is a defect?
2. **SCH_NEG_07, 08** (UDISE accepts alphabets/special chars) — Do you agree this is a defect?
3. **SCH_NEG_02, 03, 09, 10** — Should I mark as `xfail` pending confirmation, or remove from automation entirely?

---

**STATUS:** Review complete. Awaiting your decision before modifying code.
