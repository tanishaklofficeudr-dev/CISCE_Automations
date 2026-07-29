# Trust Negative Tests — Evidence-Based Investigation Report

---

# EXECUTIVE FINDING

**The Trust Details form has NO mandatory field validation.**

The application accepts blank/empty values for ALL fields and navigates successfully. This is NOT an automation issue — it is confirmed application behavior.

---

# EVIDENCE PER SCENARIO

## TRUST_FMT_001 — owner_name blank

| Check | Evidence |
|-------|----------|
| DOM value before Next | `owner_name: ''` (confirmed blank) |
| All other fields valid? | Yes — ownership=1, est=05/03/2018, reg=10/04/2019, reg_no=VALID-REG-001 |
| Navigated after Next? | **YES** — form accepted blank name |
| Validation errors? | **NONE** |
| Value after returning | `owner_name: ''` — remained blank (NOT restored by server) |
| Classification | **APPLICATION BEHAVIOR: No validation for blank trust name** |

---

## TRUST_FMT_002 — registration_no blank

| Check | Evidence |
|-------|----------|
| DOM value before Next | `registration_no: ''` (confirmed blank) |
| All other fields valid? | Yes |
| Navigated after Next? | **YES** |
| Validation errors? | **NONE** |
| Value after returning | `registration_no: ''` — remained blank |
| Classification | **APPLICATION BEHAVIOR: No validation for blank registration number** |

---

## TRUST_FMT_003 — establishment_date empty

| Check | Evidence |
|-------|----------|
| DOM value before Next | `establishment_date: ''` (confirmed blank via JS clear) |
| All other fields valid? | Yes |
| Navigated after Next? | **YES** |
| Validation errors? | **NONE** |
| Value after returning | `establishment_date: ''` — remained blank |
| Server restored value? | **NO** — date stayed blank |
| Classification | **APPLICATION BEHAVIOR: No validation for blank establishment date** |

---

## TRUST_FMT_004 — registration_date empty

| Check | Evidence |
|-------|----------|
| DOM value before Next | `registration_date: ''` (confirmed blank via JS clear) |
| Navigated after Next? | **YES** |
| Validation errors? | **NONE** |
| Value after returning | `registration_date: ''` — remained blank |
| Server restored value? | **NO** |
| Classification | **APPLICATION BEHAVIOR: No validation for blank registration date** |

---

## TRUST_FMT_005 — Future establishment date

| Check | Evidence |
|-------|----------|
| Previous diagnostic result | Future date (04/07/2027) accepted — form navigated |
| Classification | **Business Rule Pending Confirmation** |

---

## TRUST_FMT_006 — Registration date before establishment date

| Check | Evidence |
|-------|----------|
| Previous diagnostic result | Est=2022, Reg=2019 accepted — form navigated |
| Classification | **Business Rule Pending Confirmation** |

---

# ROOT CAUSE DETERMINATION

## Is this an Automation Issue?

| Question | Answer | Evidence |
|----------|--------|----------|
| Was the field actually cleared? | ✅ YES | DOM value = '' confirmed in every scenario |
| Did automation click Next? | ✅ YES | Form navigated |
| Was there a timing issue? | ❌ NO | 3-second wait used; navigation confirmed |
| Was the locator wrong? | ❌ NO | Values read back correctly |
| Was the assertion wrong? | ❌ NO | Assert checks for errors; none exist |

**Conclusion: NOT an automation issue.**

## Is this an Application Defect?

| Question | Answer | Evidence |
|----------|--------|----------|
| Does the form accept blank mandatory fields? | ✅ YES | All 4 blank scenarios navigated |
| Does it save blank values? | ✅ YES | Values remained blank after returning |
| Does server restore old values? | ❌ NO | Blank values persisted |
| Is there any field validation on Next? | ❌ NO | Zero validation messages for any field |

**Conclusion: The application has NO mandatory validation for Trust Details fields after the initial save.**

---

# CONTRADICTION WITH DIAGNOSTIC #9

The earlier diagnostic showed validation messages when ALL fields were blank:
```
• Ownership name is required.
• Date of Establishment is required.
• Date of Registration is required.
• Registration number is required.
```

**BUT** those messages appeared on the FIRST visit (before any save). Once the form has been saved at least once (which the positive test or E2E did), validation no longer fires for individual blank fields.

**The validation is ONE-TIME ONLY — on first submission.**

This is the same pattern discovered in School Details: after first save, the server has data and does not re-validate on subsequent submissions.

---

# FINAL CLASSIFICATION

| TC ID | Root Cause | Evidence |
|-------|-----------|----------|
| TRUST_FMT_001 | Application Behavior — no validation after first save | DOM blank, navigated, no errors, blank persisted |
| TRUST_FMT_002 | Application Behavior — no validation after first save | Same evidence |
| TRUST_FMT_003 | Application Behavior — no validation after first save | Same evidence |
| TRUST_FMT_004 | Application Behavior — no validation after first save | Same evidence |
| TRUST_FMT_005 | Business Rule Pending Confirmation | Future date accepted (no validation exists) |
| TRUST_FMT_006 | Business Rule Pending Confirmation | Reg < Est accepted (no validation exists) |

---

# RECOMMENDATION

| Option | Action | Impact |
|--------|--------|--------|
| **A** | Keep all 6 tests as-is — they document the application behavior gap | Tests will always fail (expected) |
| **B** | Mark TRUST_FMT_001–004 as `@pytest.mark.xfail(reason="App has no validation after first save")` | Tests run but don't break suite |
| **C** | Move TRUST_FMT_001–004 to TRUST_VAL_001 (consolidated first-visit test) and remove individual negative tests | Reduces false failures |
| **D** | Set `execute=No` in Excel for TRUST_FMT_001–004 | Disables them without code change |

**Recommended: Option B or C** — depends on your manager's preference.

- If manager wants to see the gaps documented → Option B (xfail)
- If manager wants clean pass rate → Option C (merge into validation test)

---

# KEY LESSON FOR FUTURE MODULES

**Trust Details (and likely Land Certificate, Upload Documents) have NO individual field re-validation after first save.** Only TRUST_VAL_001 (all-blank on first visit) catches the validation. Individual blank tests will always pass through because the server doesn't re-validate saved forms.

This is consistent across the framework:
- School Details: same behavior
- Trust Details: same behavior (now confirmed)
- Likely applies to all remaining modules

---

**STATUS:** Investigation complete with full evidence. Awaiting decision on TRUST_FMT_001–004.
