# Registration & Login Module — Test Case Catalog
## Complete Test Case Inventory for QA Lead/Manager

---

# 1. REGISTRATION MODULE ANALYSIS

## Application Behaviour (From Page Object)

- URL: `https://dev-eaffiliation.cisce.org/registration`
- Fields: Mobile Number, Email Address
- Action: "Register" button
- Success: "Registration successful" popup → OK button
- Duplicate: Handled gracefully (popup may not appear)

---

## Registration Test Cases

| Test ID | Category | Test Case | Description | Expected Result | Automatable | Remarks |
|---------|----------|-----------|-------------|-----------------|:-----------:|---------|
| REG_POS_001 | Positive | Valid new registration | Register with valid mobile + valid email | "Registration successful" popup | Yes | Happy path |
| REG_POS_002 | Positive | Valid registration with 10-digit mobile | Enter exactly 10-digit mobile + valid email | Registration succeeds | Yes | — |
| REG_POS_003 | Positive | Registration with yopmail email | Use yopmail.com for test email | Registration succeeds | Yes | Used in E2E |
| REG_NEG_001 | Negative | Mobile number blank | Leave mobile empty, fill email, click Register | Validation error shown | Yes | — |
| REG_NEG_002 | Negative | Email blank | Fill mobile, leave email empty, click Register | Validation error shown | Yes | — |
| REG_NEG_003 | Negative | Both fields blank | Click Register with nothing filled | Validation error shown | Yes | — |
| REG_NEG_004 | Negative | Mobile with alphabets | Enter "abcdefghij" as mobile | Validation error or DOM blocks | Yes | — |
| REG_NEG_005 | Negative | Mobile less than 10 digits | Enter "12345" (5 digits) | Validation error shown | Yes | — |
| REG_NEG_006 | Negative | Mobile more than 10 digits | Enter "123456789012" (12 digits) | Validation error or truncated | Yes | — |
| REG_NEG_007 | Negative | Mobile with special characters | Enter "+91-9876543" | Validation error | Yes | — |
| REG_NEG_008 | Negative | Invalid email format | Enter "invalidemail" (no @) | Validation error shown | Yes | — |
| REG_NEG_009 | Negative | Email without domain | Enter "user@" | Validation error | Yes | — |
| REG_NEG_010 | Negative | Email with spaces | Enter "user @email.com" | Validation error | Yes | — |
| REG_NEG_011 | Negative | Duplicate mobile number | Register with already-registered mobile | Error: "Mobile already registered" or similar | Yes | State-dependent |
| REG_NEG_012 | Negative | Duplicate email | Register with already-used email | Error or graceful handling | Yes | State-dependent |
| REG_VAL_001 | Validation | Required field indicators | Verify * (asterisk) on mandatory fields | Asterisk visible on Mobile and Email | Yes | UI check |
| REG_BND_001 | Boundary | Mobile exactly 10 digits | Enter "9876543210" | Accepted | Yes | Minimum valid |
| REG_BND_002 | Boundary | Email 1 character before @ | Enter "a@b.co" | Accepted or rejected | Yes | — |
| REG_BND_003 | Boundary | Email max length (254 chars) | Enter very long email | Accepted or truncated | Yes | — |
| REG_BND_004 | Boundary | Mobile starts with 0 | Enter "0987654321" | May reject (Indian numbers start with 6-9) | Yes | Business rule |
| REG_UI_001 | UI | Page loads correctly | Navigate to registration URL | All fields visible, Register button enabled | Yes | — |
| REG_UI_002 | UI | Success popup appears | Complete valid registration | Popup with "Registration successful" + OK button | Yes | — |
| REG_UI_003 | UI | Navigation to login after registration | After successful registration | Login page accessible | Yes | — |
| REG_SEC_001 | Security | SQL injection in mobile | Enter "' OR 1=1 --" in mobile | Rejected, no server error | Yes | Security |
| REG_SEC_002 | Security | XSS in email | Enter "<script>alert(1)</script>@test.com" | Rejected or sanitized | Yes | Security |
| REG_NAV_001 | Navigation | Register button navigates | Click Register with valid data | Redirects or shows success | Yes | — |
| REG_NAV_002 | Navigation | Back button after registration | Press browser Back after success | Appropriate page shown | Yes | — |

**Total Registration Tests: 26**

---

# 2. LOGIN MODULE ANALYSIS

## Application Behaviour (From Page Object)

- Trigger: Click "login" link on the page
- Fields: Mobile Number ("Enter Your Mobile Number"), Password ("Enter Your Password")
- Action: "Login" button
- Success: Redirects to `/preliminary/school/dashboard`
- Credentials: Stored in Excel `Common_Login` sheet

---

## Login Test Cases

| Test ID | Category | Test Case | Description | Expected Result | Automatable | Remarks |
|---------|----------|-----------|-------------|-----------------|:-----------:|---------|
| LOGIN_POS_001 | Positive | Valid login | Enter valid mobile + correct password | Redirects to dashboard | Yes | Happy path |
| LOGIN_POS_002 | Positive | Login with registered credentials | Use credentials from Common_Login Excel | Dashboard loads | Yes | Used in all regression |
| LOGIN_NEG_001 | Negative | Invalid mobile number | Enter unregistered mobile + any password | Error message shown | Yes | — |
| LOGIN_NEG_002 | Negative | Invalid password | Enter valid mobile + wrong password | Error: "Invalid credentials" | Yes | — |
| LOGIN_NEG_003 | Negative | Mobile number blank | Leave mobile empty, enter password | Validation error | Yes | — |
| LOGIN_NEG_004 | Negative | Password blank | Enter mobile, leave password empty | Validation error | Yes | — |
| LOGIN_NEG_005 | Negative | Both fields blank | Click Login with nothing | Validation error | Yes | — |
| LOGIN_NEG_006 | Negative | Mobile with alphabets | Enter "abcdefghij" as mobile | Validation error | Yes | — |
| LOGIN_NEG_007 | Negative | Mobile too short | Enter "12345" | Validation error | Yes | — |
| LOGIN_NEG_008 | Negative | Password with spaces only | Enter "     " as password | Error or rejected | Yes | — |
| LOGIN_NEG_009 | Negative | Incorrect password 3 times | Attempt login 3 times with wrong password | Account locked or rate limited | Yes | Business rule |
| LOGIN_VAL_001 | Validation | Required field indicators | Verify mandatory field markers | Asterisk or required styling visible | Yes | — |
| LOGIN_VAL_002 | Validation | Error message format | Submit invalid credentials | Error message displayed clearly | Yes | — |
| LOGIN_BND_001 | Boundary | Mobile exactly 10 digits | Enter valid 10-digit mobile | Accepted | Yes | — |
| LOGIN_BND_002 | Boundary | Password minimum length | Enter shortest valid password | Accepted or rejected | Yes | Business rule |
| LOGIN_BND_003 | Boundary | Password maximum length | Enter very long password (100+ chars) | Accepted or truncated | Yes | — |
| LOGIN_UI_001 | UI | Login page loads | Click login link | Mobile and Password fields visible | Yes | — |
| LOGIN_UI_002 | UI | Password masking | Enter password | Characters masked (dots/asterisks) | Yes | — |
| LOGIN_UI_003 | UI | Login button state | Check button enabled/disabled states | Enabled when fields have content | Yes | — |
| LOGIN_SEC_001 | Security | SQL injection in mobile | Enter "' OR 1=1 --" | Rejected, no server compromise | Yes | — |
| LOGIN_SEC_002 | Security | SQL injection in password | Enter "' OR '1'='1" | Rejected | Yes | — |
| LOGIN_SEC_003 | Security | XSS in mobile field | Enter "<script>alert(1)</script>" | Sanitized or rejected | Yes | — |
| LOGIN_NAV_001 | Navigation | Successful login navigates to dashboard | Login with valid credentials | URL: `/preliminary/school/dashboard` | Yes | — |
| LOGIN_NAV_002 | Navigation | Browser back after logout | Logout then press Back | Does NOT return to authenticated page | Yes | Security |
| LOGIN_NAV_003 | Navigation | Direct URL access without login | Navigate to dashboard URL without login | Redirected to login page | Yes | Security |
| LOGIN_SESSION_001 | Session | Session timeout | Stay idle for session timeout period | Logged out automatically | Conditional | Long wait required |
| LOGIN_SESSION_002 | Session | Logout functionality | Click logout link/button | Session terminated, redirected to login | Yes | — |
| LOGIN_SESSION_003 | Session | Multiple tabs same session | Login in one tab, access in another | Same session shared | Yes | — |
| LOGIN_FORGOT_001 | Password | Forgot password link | Click "Forgot Password" | Password reset flow initiated | Yes | If available |
| LOGIN_FORGOT_002 | Password | Password reset with valid mobile | Enter registered mobile for reset | OTP/reset link sent | Conditional | Depends on flow |

**Total Login Tests: 30**

---

# 3. MODULE SUMMARY

| Module | Validation | Positive | Negative | Boundary | UI | Security | Navigation | Session/Password | Total |
|--------|:----------:|:--------:|:--------:|:--------:|:--:|:--------:|:----------:|:----------------:|:-----:|
| Registration | 1 | 3 | 12 | 4 | 3 | 2 | 2 | — | **26** |
| Login | 2 | 2 | 9 | 3 | 3 | 3 | 3 | 5 | **30** |
| **TOTAL** | **3** | **5** | **21** | **7** | **6** | **5** | **5** | **5** | **56** |

---

# 4. SANITY RECOMMENDATIONS

The following Registration and Login test cases should be added to the Sanity Suite:

| Sanity ID | Test ID | Module | Reason |
|-----------|---------|--------|--------|
| SAN-REG-01 | REG_POS_001 | Registration | Proves registration works |
| SAN-REG-02 | REG_NEG_011 | Registration | Proves duplicate detection works |
| SAN-LOGIN-01 | LOGIN_POS_001 | Login | Proves login works |
| SAN-LOGIN-02 | LOGIN_NEG_002 | Login | Proves invalid credentials rejected |
| SAN-LOGIN-03 | LOGIN_NAV_001 | Login | Proves navigation to dashboard |

**Recommended addition to sanity: 5 tests (~3 min additional)**

---

# 5. REGRESSION RECOMMENDATIONS

The following should always execute BEFORE the Preliminary Form regression suite:

| Priority | Test ID | Reason |
|----------|---------|--------|
| P1 | LOGIN_POS_001 | Must verify login works before all other tests |
| P2 | REG_POS_001 | Verify registration (first-time execution only) |
| P3 | LOGIN_NEG_002 | Verify invalid credentials are rejected |
| P4 | LOGIN_NAV_003 | Verify unauthorized access is blocked |

**Pre-condition tests: 4 tests (~2 min)**

---

# 6. INTEGRATION RECOMMENDATION

### Recommended Execution Order:

```
1. Registration (first-time setup)
       ↓
2. Login (authentication verification)
       ↓
3. School Details
       ↓
4. Address Details
       ↓
5. NOC Details
       ↓
6. Trust Details
       ↓
7. Certificate of Land
       ↓
8. Upload Documents
       ↓
9. Payment Gateway (ALWAYS LAST)
```

### Architecture Integration:

| Component | Current Status | Recommendation |
|-----------|---------------|----------------|
| `pages/registration_page.py` | ✅ Exists (used by fixture) | Add regression methods |
| `pages/login_page.py` | ✅ Exists (used by fixture) | Add regression methods |
| `conftest.py` | Uses both for `school_details_ready_page` fixture | No change needed |
| New test folder | ❌ Not exists | Create `tests/regression/authentication/` |
| Excel sheet | ❌ Not exists | Create `Registration_Login` sheet |
| Marker | ❌ Not exists | Register `authentication` marker |

### Implementation Effort:

| Phase | Task | Effort |
|-------|------|--------|
| 1 | Add regression page methods | 1 hr |
| 2 | Create Excel data | 30 min |
| 3 | Implement 15-20 key tests | 4 hrs |
| 4 | Verification | 1 hr |
| **Total** | | **~6.5 hrs** |

---

# 7. PROJECT STATISTICS UPDATE

| Component | Current | Registration | Login | Updated Total |
|-----------|:-------:|:----------:|:-----:|:-------------:|
| Regression Tests | 123 | 26 (planned) | 30 (planned) | **179** |
| Sanity Tests | 20 | +2 | +3 | **25** |
| E2E Tests | 1 | — | — | **1** |
| Modules | 7 | +1 | +1 | **9** |
| **Grand Total Tests** | **124** | | | **180** (planned) |

### Current Implementation Status:

| Module | Status | Tests |
|--------|--------|:-----:|
| Registration | 📋 Planned (test cases defined) | 26 |
| Login | 📋 Planned (test cases defined) | 30 |
| School Details | ✅ Implemented | 22 |
| Address Details | ✅ Implemented | 13 |
| NOC Details | ✅ Implemented | 12 |
| Trust Details | ✅ Implemented | 12 |
| Certificate of Land | ✅ Implemented | 34 |
| Upload Documents | ✅ Implemented | 27 |
| Payment Gateway | ✅ Implemented | 3 |
| **TOTAL** | | **179** |

---

# 8. AUTOMATION FEASIBILITY SUMMARY

| Category | Total | Automatable | Not Automatable | Reason |
|----------|:-----:|:-----------:|:---------------:|--------|
| Registration | 26 | 24 | 2 | OTP-dependent, CAPTCHA |
| Login | 30 | 27 | 3 | Session timeout (long wait), CAPTCHA, OTP reset |
| **Total** | **56** | **51** | **5** | |

### Non-Automatable Scenarios:

| Test ID | Reason |
|---------|--------|
| REG_SEC_001/002 | Security penetration testing — separate tooling |
| LOGIN_SESSION_001 | Requires 30+ min idle wait |
| LOGIN_FORGOT_002 | OTP delivery verification — external system |
| Any CAPTCHA test | Cannot bypass CAPTCHA programmatically |

---

*Document Version: 1.0*
*Generated: July 2026*
*Status: Test Cases Defined — Implementation Pending*
*Prepared for: QA Lead / Manager*
