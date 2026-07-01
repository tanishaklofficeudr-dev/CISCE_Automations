# CISCE Preliminary Affiliation Portal
# Complete Regression & Sanity Test Suite
## Enterprise QA Test Architecture Document

---

# MODULE 1: REGISTRATION

## TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-REG-001 | Registration | New School Registration | Verify new school can register with valid mobile and email | Validate complete registration happy path | Application URL accessible | 1. Open registration URL 2. Enter valid 10-digit mobile 3. Enter valid email 4. Click Register 5. Verify success popup 6. Click OK | Mobile: 9876543210, Email: school@example.com | Registration successful popup appears, user can proceed to login | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | registration_page.py | register_school() | Core E2E flow |
| S-REG-002 | Registration | Registration Page Access | Verify registration page is accessible and loads correctly | Validate page accessibility | Internet connection available | 1. Navigate to registration URL 2. Verify mobile field visible 3. Verify email field visible 4. Verify Register button visible | URL: /registration | All registration elements are visible and interactive | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | registration_page.py | register_school() | page.goto() |
| R-REG-003 | Registration | Duplicate Mobile Validation | Verify registration fails for already registered mobile number | Validate duplicate prevention | Mobile already registered in system | 1. Enter existing mobile number 2. Enter email 3. Click Register | Existing mobile number | Error message displayed OR popup does not appear, handled gracefully | No | Yes | Yes | Negative | High | Partially Covered | test_preliminary_form_main.py | registration_page.py | register_school() | Handled via try/except but no explicit assertion |
| R-REG-004 | Registration | Blank Mobile Number | Verify registration fails when mobile field is empty | Validate mandatory field | Registration page loaded | 1. Leave mobile blank 2. Enter email 3. Click Register | Mobile: empty | Validation error shown, registration blocked | No | No | Yes | Negative | High | Not Covered | - | registration_page.py | - | Field validation not automated |
| R-REG-005 | Registration | Invalid Mobile Format | Verify registration fails with invalid mobile number format | Validate mobile format | Registration page loaded | 1. Enter alphabetic/special chars in mobile 2. Enter email 3. Click Register | Mobile: abc123, @#$% | Validation error - invalid mobile format | No | No | Yes | Negative | High | Not Covered | - | registration_page.py | - | |
| R-REG-006 | Registration | Mobile Number Boundary - Less than 10 digits | Verify registration fails with less than 10 digit mobile | Validate minimum length | Registration page loaded | 1. Enter 9 digit mobile 2. Enter email 3. Click Register | Mobile: 987654321 (9 digits) | Validation error - mobile must be 10 digits | No | No | Yes | Boundary | High | Not Covered | - | registration_page.py | - | |
| R-REG-007 | Registration | Mobile Number Boundary - More than 10 digits | Verify registration fails with more than 10 digit mobile | Validate maximum length | Registration page loaded | 1. Enter 11 digit mobile 2. Enter email 3. Click Register | Mobile: 98765432101 (11 digits) | Field should not accept >10 digits OR validation error | No | No | Yes | Boundary | Medium | Not Covered | - | registration_page.py | - | |
| R-REG-008 | Registration | Blank Email | Verify registration fails when email is empty | Validate mandatory email | Registration page loaded | 1. Enter valid mobile 2. Leave email blank 3. Click Register | Email: empty | Validation error - email required | No | No | Yes | Negative | High | Not Covered | - | registration_page.py | - | |
| R-REG-009 | Registration | Invalid Email Format | Verify registration fails with invalid email format | Validate email format | Registration page loaded | 1. Enter valid mobile 2. Enter invalid email 3. Click Register | Email: abc, abc@, @domain.com, abc@.com | Validation error - invalid email format | No | No | Yes | Negative | High | Not Covered | - | registration_page.py | - | |
| R-REG-010 | Registration | Email Boundary - Maximum Length | Verify email field maximum character limit | Validate field boundary | Registration page loaded | 1. Enter 256+ character email | Email: very_long_string@domain.com (256 chars) | Field truncates or shows validation error | No | No | Yes | Boundary | Low | Not Covered | - | registration_page.py | - | |
| R-REG-011 | Registration | Country Code Validation | Verify country code is pre-selected or editable | Validate country code behaviour | Registration page loaded | 1. Observe country code field 2. Try changing code | Various country codes | Country code validation works correctly | No | No | Yes | Positive | Medium | Not Covered | - | registration_page.py | - | Field name suggests country code |
| R-REG-012 | Registration | Success Popup Verification | Verify success popup contains correct message text | Validate popup content | Valid registration submitted | 1. Register with valid data 2. Read popup text | None | Popup shows "Registration successful" exactly | No | Yes | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | registration_page.py | register_school() | expect with text match |
| R-REG-013 | Registration | Page Reload After Registration | Verify page state after successful registration | Validate post-registration state | Registration successful | 1. Complete registration 2. Verify page ready for login | None | Login link becomes available | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | registration_page.py | register_school() | |

---

# MODULE 2: LOGIN & AUTHENTICATION

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-AUTH-001 | Authentication | Valid Login | Verify user can login with valid credentials and reach dashboard | Validate login happy path | User registered | 1. Click login link 2. Enter valid mobile 3. Enter password 4. Click Login 5. Verify dashboard URL | Valid mobile + password | User redirected to /preliminary/school/dashboard | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | login_page.py | login() | Password via page.pause() |
| S-AUTH-002 | Authentication | Login Page Navigation | Verify login link navigates to login form | Validate navigation | Registration page visible | 1. Click login link 2. Verify mobile input visible | None | Login form appears with mobile number field | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | login_page.py | login() | |
| R-AUTH-003 | Authentication | Invalid Mobile Login | Verify login fails with unregistered mobile number | Validate authentication | Login page loaded | 1. Enter unregistered mobile 2. Enter any password 3. Click Login | Unregistered mobile | Error message - mobile not registered or invalid credentials | No | Yes | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| R-AUTH-004 | Authentication | Invalid Password Login | Verify login fails with wrong password | Validate password check | Login page loaded | 1. Enter valid mobile 2. Enter wrong password 3. Click Login | Valid mobile + wrong password | Error message - invalid credentials | No | Yes | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| R-AUTH-005 | Authentication | Blank Mobile Login | Verify login fails with empty mobile field | Validate mandatory | Login page loaded | 1. Leave mobile empty 2. Click Login | Mobile: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| R-AUTH-006 | Authentication | Blank Password Login | Verify login fails with empty password | Validate mandatory | Login page loaded | 1. Enter mobile 2. Leave password empty 3. Click Login | Password: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| R-AUTH-007 | Authentication | Multiple Failed Login Attempts | Verify account lockout or rate limiting after multiple failures | Validate security | Login page loaded | 1. Enter valid mobile 2. Enter wrong password 5 times | Wrong password x5 | Account locked or rate limit message after N attempts | No | No | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| R-AUTH-008 | Authentication | Session Persistence | Verify user remains logged in across page refreshes | Validate session | User logged in | 1. Login successfully 2. Refresh page 3. Verify still on dashboard | None | User remains authenticated | No | No | Yes | Positive | Medium | Not Covered | - | - | - | |
| R-AUTH-009 | Authentication | Logout Functionality | Verify user can logout and session terminates | Validate logout | User logged in | 1. Click logout 2. Verify redirect to login 3. Try accessing dashboard directly | None | Session terminated, cannot access protected routes | No | Yes | Yes | Positive | High | Not Covered | - | - | - | |
| R-AUTH-010 | Authentication | Unauthorized Route Access | Verify unauthenticated users cannot access dashboard | Validate route protection | Not logged in | 1. Directly navigate to dashboard URL | Dashboard URL | Redirected to login page | No | No | Yes | Negative | High | Not Covered | - | - | - | |

---

# MODULE 3: GET STARTED / DASHBOARD

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-NAV-001 | Navigation | Dashboard Access | Verify Get Started page loads after successful login | Validate post-login navigation | User logged in | 1. Login successfully 2. Verify dashboard URL 3. Verify Get Started content | None | URL contains /preliminary/school/dashboard, instructions visible | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | inline | page.wait_for_url() | |
| SM-NAV-002 | Navigation | Next Button - Get Started | Verify clicking Next navigates from Get Started to School Details | Validate workflow progression | Dashboard loaded | 1. Click Next button 2. Verify School Details page loads | None | School Details form is visible | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | inline | page.get_by_role() | |
| R-NAV-003 | Navigation | Step Indicator | Verify progress stepper shows correct active step | Validate UI state | Dashboard loaded | 1. Verify Get Started step is active/highlighted | None | Get Started step marker is active | No | No | Yes | Positive | Low | Not Covered | - | - | - | |
| R-NAV-004 | Navigation | Information Content | Verify Get Started page displays correct instructions | Validate business content | Dashboard loaded | 1. Read page content 2. Verify NOC, Land Certificate, Society docs mentioned | None | All required document types listed | No | No | Yes | Positive | Low | Not Covered | - | - | - | |

---

# MODULE 4: SCHOOL DETAILS

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-SCH-001 | School Details | Complete Form Submission | Verify school details can be saved with all valid mandatory fields | Validate complete form happy path | School Details page loaded | 1. Fill school name 2. Select classification 3. Select school type 4. Fill contact person 5. Fill website 6. Fill UDISE 7. Select category 8. Click Next | All valid data from Excel | Form submits, navigates to Address Details | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | school_details_page.py | fill_school_details() | |
| R-SCH-002 | School Details | Blank School Name Submission | Verify form cannot proceed without school name | Validate mandatory field | School Details page loaded | 1. Leave school name blank 2. Fill other fields 3. Click Next | School name: empty | Validation error - school name required | No | Yes | Yes | Negative | High | Not Covered | - | school_details_page.py | - | |
| R-SCH-003 | School Details | School Name - Special Characters | Verify school name does not accept only special characters | Validate input quality | School Details page loaded | 1. Enter @#$%^& in school name 2. Click Next | School name: @#$%^& | Validation error or sanitization | No | No | Yes | Negative | Medium | Not Covered | - | school_details_page.py | - | |
| R-SCH-004 | School Details | School Name - Numeric Only | Verify school name does not accept only numbers | Validate input | School Details page loaded | 1. Enter 123456 in school name 2. Click Next | School name: 123456 | Validation error | No | No | Yes | Negative | Medium | Not Covered | - | school_details_page.py | - | |
| R-SCH-005 | School Details | School Name - Boundary Max | Verify school name maximum character limit | Validate boundary | School Details page loaded | 1. Enter 200+ characters 2. Observe behaviour | School name: 200 chars | Field truncates or shows max limit error | No | No | Yes | Boundary | Medium | Not Covered | - | school_details_page.py | - | |
| R-SCH-006 | School Details | Classification Not Selected | Verify form cannot proceed without selecting classification | Validate mandatory dropdown | Page loaded | 1. Fill all fields except classification 2. Click Next | Classification: not selected | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | school_details_page.py | - | |
| R-SCH-007 | School Details | School Type Not Selected | Verify form cannot proceed without selecting school type | Validate mandatory dropdown | Page loaded | 1. Fill all except school type 2. Click Next | Type: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | school_details_page.py | - | |
| R-SCH-008 | School Details | Category Not Selected | Verify form cannot proceed without selecting school category | Validate mandatory dropdown | Page loaded | 1. Fill all except category 2. Click Next | Category: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | school_details_page.py | - | |
| R-SCH-009 | School Details | UDISE Number - Non-numeric | Verify UDISE field rejects non-numeric input | Validate field type | Page loaded | 1. Enter alphabets in UDISE | UDISE: abcdef | Validation error or field rejects input | No | No | Yes | Negative | Medium | Not Covered | - | school_details_page.py | - | |
| R-SCH-010 | School Details | UDISE Number - Boundary | Verify UDISE number exact digit requirement | Validate boundary | Page loaded | 1. Enter less/more than required digits | Various lengths | Only valid length accepted | No | No | Yes | Boundary | Medium | Not Covered | - | school_details_page.py | - | |
| R-SCH-011 | School Details | Website URL - Invalid Format | Verify website field validation for invalid URLs | Validate URL format | Page loaded | 1. Enter invalid URL format | Website: notaurl, htp://bad | Warning or acceptance (field may be optional) | No | No | Yes | Negative | Low | Not Covered | - | school_details_page.py | - | |
| R-SCH-012 | School Details | Contact Person - Numeric Only | Verify contact person rejects numeric-only input | Validate name field | Page loaded | 1. Enter only numbers | Contact: 123456 | Validation error | No | No | Yes | Negative | Low | Not Covered | - | school_details_page.py | - | |
| R-SCH-013 | School Details | Data Persistence | Verify school details are saved when navigating back | Validate data retention | Form filled and submitted | 1. Fill form 2. Go to next step 3. Navigate back | None | Previously entered data is retained | No | No | Yes | Positive | Medium | Not Covered | - | school_details_page.py | - | |
| R-SCH-014 | School Details | Dropdown Options Loaded | Verify all dropdown options load correctly from server | Validate dynamic data | Page loaded | 1. Click each dropdown 2. Verify options present | None | All dropdowns have options loaded | No | No | Yes | Positive | Medium | Not Covered | - | school_details_page.py | - | |

---

# MODULE 5: ADDRESS DETAILS

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-ADDR-001 | Address Details | Complete Address Submission | Verify address details can be saved with all valid fields | Validate complete form | Address page loaded | 1. Fill address line 2. Select country 3. Select state 4. Select district 5. Select city 6. Fill PIN 7. Select locality 8. Click Next | All valid data | Form submits, navigates to NOC Details | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | address_details_page.py | fill_address_details() | |
| R-ADDR-002 | Address Details | Blank Address Line | Verify form fails without address line | Validate mandatory | Page loaded | 1. Leave address blank 2. Fill others 3. Click Next | Address: empty | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | address_details_page.py | - | |
| R-ADDR-003 | Address Details | Cascading Dropdown - State depends on Country | Verify state dropdown loads based on selected country | Validate cascade logic | Page loaded | 1. Select India 2. Verify states load 3. Select different country 4. Verify states change | India, Other countries | State list updates per country | No | Yes | Yes | Positive | High | Partially Covered | test_preliminary_form_main.py | address_details_page.py | fill_address_details() | Only India tested |
| R-ADDR-004 | Address Details | Cascading Dropdown - District depends on State | Verify district loads based on state | Validate cascade | State selected | 1. Select state 2. Verify districts load | State selection | Districts relevant to state appear | No | Yes | Yes | Positive | High | Partially Covered | test_preliminary_form_main.py | address_details_page.py | fill_address_details() | Single state tested |
| R-ADDR-005 | Address Details | Cascading Dropdown - City depends on District | Verify city loads based on district | Validate cascade | District selected | 1. Select district 2. Verify cities load | District selection | Cities relevant to district appear | No | No | Yes | Positive | High | Partially Covered | test_preliminary_form_main.py | address_details_page.py | fill_address_details() | |
| R-ADDR-006 | Address Details | Invalid PIN Code - Non-numeric | Verify PIN code rejects alphabetic input | Validate field type | Page loaded | 1. Enter abc in PIN field | PIN: abc123 | Validation error or field rejects | No | No | Yes | Negative | Medium | Not Covered | - | address_details_page.py | - | |
| R-ADDR-007 | Address Details | PIN Code - Boundary Less than 6 | Verify PIN code must be 6 digits | Validate boundary | Page loaded | 1. Enter 5 digit PIN | PIN: 12345 | Validation error - must be 6 digits | No | No | Yes | Boundary | Medium | Not Covered | - | address_details_page.py | - | |
| R-ADDR-008 | Address Details | PIN Code - Boundary More than 6 | Verify PIN code cannot exceed 6 digits | Validate boundary | Page loaded | 1. Enter 7 digit PIN | PIN: 1234567 | Field truncates or error | No | No | Yes | Boundary | Medium | Not Covered | - | address_details_page.py | - | |
| R-ADDR-009 | Address Details | Country Not Selected | Verify form cannot proceed without country | Validate mandatory | Page loaded | 1. Skip country 2. Click Next | Country: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | address_details_page.py | - | |
| R-ADDR-010 | Address Details | State Not Selected | Verify form cannot proceed without state | Validate mandatory | Page loaded | 1. Select country only 2. Click Next | State: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | address_details_page.py | - | |
| R-ADDR-011 | Address Details | Address Line - Maximum Length | Verify address field maximum characters | Validate boundary | Page loaded | 1. Enter 500+ character address | Long address string | Field truncates or allows with limit | No | No | Yes | Boundary | Low | Not Covered | - | address_details_page.py | - | |
| R-ADDR-012 | Address Details | Locality Type Not Selected | Verify locality type is mandatory | Validate mandatory | Page loaded | 1. Fill all except locality 2. Click Next | Locality: not selected | Validation error | No | No | Yes | Negative | Medium | Not Covered | - | address_details_page.py | - | |

---

# MODULE 6: NOC DETAILS

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-NOC-001 | NOC Details | Complete NOC Form Submission | Verify NOC details can be saved with all valid information | Validate complete form | NOC page loaded | 1. Fill authority 2. Fill designation 3. Fill office address 4. Select country/state 5. Fill reference number 6. Select NOC date 7. Click Next | All valid data | Form submits, navigates to Trust Details | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | noc_details_page.py | fill_noc_details() | |
| R-NOC-002 | NOC Details | Blank NOC Authority | Verify form fails without NOC issuing authority | Validate mandatory | Page loaded | 1. Leave authority blank 2. Click Next | Authority: empty | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| R-NOC-003 | NOC Details | Blank Designation | Verify form fails without designation | Validate mandatory | Page loaded | 1. Leave designation blank 2. Click Next | Designation: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| R-NOC-004 | NOC Details | Blank Office Address | Verify form fails without office address | Validate mandatory | Page loaded | 1. Leave office address blank 2. Click Next | Office address: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| R-NOC-005 | NOC Details | NOC Date - Future Date | Verify NOC date cannot be a future date | Validate business rule | Page loaded | 1. Select a date in the future | Future date | Validation error - NOC date cannot be future | No | Yes | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | Business rule |
| R-NOC-006 | NOC Details | NOC Reference Number - Blank | Verify reference number is mandatory | Validate mandatory | Page loaded | 1. Leave reference blank 2. Click Next | Reference: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| R-NOC-007 | NOC Details | Date Picker Navigation | Verify date picker back arrow navigates months correctly | Validate date picker UI | Date picker open | 1. Click back arrow multiple times 2. Verify month changes | None | Month decrements correctly | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | noc_details_page.py | fill_noc_details() | columnheader back arrow |
| R-NOC-008 | NOC Details | NOC Date - No Date Selected | Verify form fails without selecting NOC date | Validate mandatory | Page loaded | 1. Fill all except date 2. Click Next | Date: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |

---

# MODULE 7: TRUST / SOCIETY / COMPANY DETAILS

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-TRUST-001 | Trust Details | Complete Trust Form Submission | Verify trust details can be saved with all valid fields | Validate complete form | Trust page loaded | 1. Select ownership type 2. Fill trust name 3. Set establishment date 4. Set registration date 5. Fill registration number 6. Click Next | All valid data | Form submits, navigates to Land Certificate | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | trust_details_page.py | fill_trust_details() | |
| R-TRUST-002 | Trust Details | Ownership Type Not Selected | Verify form fails without ownership type | Validate mandatory | Page loaded | 1. Leave ownership type as Select 2. Click Next | Type: not selected | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |
| R-TRUST-003 | Trust Details | Blank Trust Name | Verify form fails without trust name | Validate mandatory | Page loaded | 1. Leave name blank 2. Click Next | Name: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |
| R-TRUST-004 | Trust Details | Establishment Date - Future | Verify establishment date cannot be in future | Validate business rule | Page loaded | 1. Enter future date | Future date | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | Business rule |
| R-TRUST-005 | Trust Details | Registration Date Before Establishment | Verify registration date cannot be before establishment date | Validate business rule | Page loaded | 1. Set establishment to 2020 2. Set registration to 2019 | Reg < Est | Validation error - logical inconsistency | No | Yes | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | Critical business rule |
| R-TRUST-006 | Trust Details | Blank Registration Number | Verify form fails without registration number | Validate mandatory | Page loaded | 1. Fill all except registration number 2. Click Next | Reg number: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |
| R-TRUST-007 | Trust Details | Dynamic Form Loading | Verify form loads correctly with wait for visibility | Validate page stability | Navigated to Trust page | 1. Verify ownership dropdown visible after wait | None | Dropdown loads within timeout | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | trust_details_page.py | fill_trust_details() | wait_for with visible state |
| R-TRUST-008 | Trust Details | Establishment Date - No Date | Verify form fails without establishment date | Validate mandatory | Page loaded | 1. Fill all except establishment date 2. Click Next | Date: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |

---

# MODULE 8: LAND CERTIFICATE / CERTIFICATE OF LAND

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-LAND-001 | Land Certificate | Complete Land Details Submission | Verify land certificate details can be saved with all valid fields | Validate complete form | Land page loaded | 1. Select plot type 2. Select land type 3. Select area unit 4. Fill area 5. Fill situated in/at 6. Fill owned by 7. Select title doc 8. Fill registration details 9. Fill seller name 10. Fill office details 11. Set date 12. Click Next | All valid data | Form submits, navigates to Upload Documents | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | land_certificate_page.py | fill_land_details() | |
| S-LAND-002 | Land Certificate | Plot Type - Dynamic Form | Verify selecting Yes for plot type loads dynamic form | Validate conditional rendering | Land page loaded | 1. Select Yes for plots 2. Verify Owner's Details form appears | Plot type: Yes | Dynamic form with all land fields appears | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | land_certificate_page.py | fill_land_details() | wait_for_timeout |
| R-LAND-003 | Land Certificate | Owned vs Leased Logic | Verify different fields appear for Owned vs Leased land | Validate conditional logic | Dynamic form loaded | 1. Select Owned 2. Verify fields 3. Select Leased 4. Verify different fields | Type: Owned, Leased | Appropriate fields shown per selection | No | Yes | Yes | Positive | High | Partially Covered | test_preliminary_form_main.py | land_certificate_page.py | fill_land_details() | Only one type tested per run |
| R-LAND-004 | Land Certificate | Land Area - Zero Value | Verify land area cannot be zero | Validate business rule | Form loaded | 1. Enter 0 in land area | Area: 0 | Validation error - area must be positive | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| R-LAND-005 | Land Certificate | Land Area - Negative Value | Verify land area cannot be negative | Validate input | Form loaded | 1. Enter -100 in land area | Area: -100 | Validation error or rejection | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| R-LAND-006 | Land Certificate | Land Area - Non-numeric | Verify land area rejects text input | Validate field type | Form loaded | 1. Enter text in area field | Area: abc | Field rejects or validation error | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| R-LAND-007 | Land Certificate | Sale Deed Conditional Field | Verify Sale Deed specific fields appear only when Sale Deed selected | Validate conditional logic | Form loaded | 1. Select Sale Deed 2. Verify favor field appears 3. Select different doc 4. Verify field disappears | Title: Sale Deed, Others | Conditional field shows/hides correctly | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | land_certificate_page.py | fill_land_details() | if condition |
| R-LAND-008 | Land Certificate | Area Unit Not Selected | Verify form fails without area unit | Validate mandatory | Form loaded | 1. Leave area unit as default 2. Click Next | Unit: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | land_certificate_page.py | - | |
| R-LAND-009 | Land Certificate | Land Document Date - Future | Verify land document date cannot be future | Validate business rule | Form loaded | 1. Enter future date | Future date | Validation error | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| R-LAND-010 | Land Certificate | All Mandatory Fields Blank | Verify form shows all validation errors when all fields blank | Validate multiple validations | Form loaded | 1. Click Next without filling anything | All empty | Multiple validation messages shown | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |

---

# MODULE 9: UPLOAD DOCUMENTS

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-DOC-001 | Upload Documents | Complete Document Upload and Submission | Verify all documents can be uploaded and form proceeds to payment | Validate complete upload flow | Upload page loaded | 1. Upload NOC doc 2. Upload Land cert 3. Upload Trust doc 4. Upload Land ownership 5. Upload School image 6. Fill comments 7. Select affiliation type 8. Check both checkboxes 9. Click Proceed to Payment | PDF file, comments, affiliation type | All files uploaded, form submits to payment | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| R-DOC-002 | Upload Documents | NOC Document - Missing | Verify form fails without NOC document | Validate mandatory upload | Page loaded | 1. Upload all except NOC 2. Click Proceed | NOC: not uploaded | Validation error - NOC required | No | Yes | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| R-DOC-003 | Upload Documents | Invalid File Type Upload | Verify system rejects non-PDF/image file types | Validate file type | Page loaded | 1. Try uploading .exe or .txt file | File: test.exe | File rejected with error message | No | Yes | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| R-DOC-004 | Upload Documents | File Size Exceeds Limit | Verify system rejects files exceeding maximum size | Validate file size | Page loaded | 1. Upload file >10MB (or whatever limit) | Large file | Error - file size exceeds limit | No | No | Yes | Boundary | Medium | Not Covered | - | upload_documents_page.py | - | |
| R-DOC-005 | Upload Documents | Affiliation Type Not Selected | Verify form fails without selecting affiliation type | Validate mandatory | Page loaded | 1. Upload all docs 2. Skip affiliation type 3. Click Proceed | Type: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| R-DOC-006 | Upload Documents | Verification Checkboxes Unchecked | Verify form fails without checking both verification boxes | Validate mandatory | Page loaded | 1. Upload all 2. Leave checkboxes unchecked 3. Click Proceed | Checkboxes: unchecked | Validation error or button disabled | No | No | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| R-DOC-007 | Upload Documents | Upload and Replace File | Verify user can replace an already uploaded file | Validate re-upload | File already uploaded | 1. Upload file 2. Upload different file same slot | Two different files | New file replaces old | No | No | Yes | Positive | Medium | Not Covered | - | upload_documents_page.py | - | |
| R-DOC-008 | Upload Documents | Comments - Maximum Length | Verify comments field maximum characters | Validate boundary | Page loaded | 1. Enter 1000+ character comment | Long comment | Field truncates or accepts with limit | No | No | Yes | Boundary | Low | Not Covered | - | upload_documents_page.py | - | |
| R-DOC-009 | Upload Documents | School Image - Image Formats | Verify school image accepts standard image formats | Validate file format | Page loaded | 1. Upload JPG 2. Upload PNG | JPG, PNG files | Both accepted | No | No | Yes | Positive | Medium | Not Covered | - | upload_documents_page.py | - | |
| R-DOC-010 | Upload Documents | All Documents Missing | Verify form shows errors for all missing documents | Validate multiple | Page loaded | 1. Click Proceed without any uploads | All empty | Multiple validation errors | No | No | Yes | Negative | Medium | Not Covered | - | upload_documents_page.py | - | |

---

# MODULE 10: PAYMENT

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-PAY-001 | Payment | Complete Payment Flow | Verify end-to-end payment completes successfully via ICICI gateway | Validate payment happy path | Redirected to payment page | 1. Click Pay Rs 2. Select ICICI Bank 3. Click Proceed to Pay 4. Handle iframe 5. Click Show QR 6. Complete payment 7. Verify success | None | "Transaction Successful!" displayed, redirects to homepage | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | JS injection for disabled button |
| S-PAY-002 | Payment | Payment URL Validation | Verify correct payment URL after form submission | Validate navigation | Proceed to Payment clicked | 1. Verify URL contains /payment/ | None | URL matches payment pattern | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | wait_for_url |
| S-PAY-003 | Payment | Gateway Selection - ICICI | Verify ICICI Bank can be selected as payment gateway | Validate gateway selection | Payment Details visible | 1. Click ICICI Bank 2. Verify selected state | None | ICICI Bank shown as selected | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| R-PAY-004 | Payment | Gateway Selection - HDFC | Verify HDFC Bank can be selected as payment gateway | Validate alternate gateway | Payment Details visible | 1. Click HDFC Bank 2. Verify selected | None | HDFC Bank selected | No | No | Yes | Positive | Medium | Not Covered | - | upload_documents_page.py | - | |
| R-PAY-005 | Payment | No Gateway Selected | Verify payment cannot proceed without selecting gateway | Validate mandatory | Payment page loaded | 1. Click Proceed to Pay without selecting bank | None | Button remains disabled or error shown | No | Yes | Yes | Negative | High | Partially Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | JS removes disabled |
| R-PAY-006 | Payment | Payment Timeout | Verify system handles payment timeout gracefully | Validate error handling | Payment initiated | 1. Initiate payment 2. Wait for timeout | None | Timeout message shown with retry option | No | No | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| R-PAY-007 | Payment | Payment Cancellation | Verify user can cancel payment and return | Validate cancellation | Payment iframe shown | 1. Click Cancel/Back in payment iframe | None | Returns to payment page or form | No | No | Yes | Negative | Medium | Not Covered | - | upload_documents_page.py | - | |
| SM-PAY-008 | Payment | Transaction Success Validation | Verify Transaction Successful message appears after payment | Validate success confirmation | Payment completed | 1. Complete payment 2. Wait 3. Verify text | None | "Transaction Successful!" text visible | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | 30s timeout |
| SM-PAY-009 | Payment | Post-Payment Homepage Redirect | Verify redirect to school view after successful payment | Validate end state | Transaction successful | 1. Click Go to Homepage 2. Verify URL | None | URL contains /school_view | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| R-PAY-010 | Payment | Payment Amount Validation | Verify correct amount displayed on payment page | Validate business data | Payment page loaded | 1. Verify amount shown matches expected fee | Expected fee amount | Correct Rs amount displayed | No | No | Yes | Positive | Medium | Not Covered | - | upload_documents_page.py | - | |

---

# MODULE 11: CROSS-CUTTING / WORKFLOW

| TC ID | Module | Feature | Business Scenario | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Script | Page Object | Method | Remarks |
|-------|--------|---------|-------------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|--------|-------------|--------|---------|
| SM-WF-001 | Workflow | Complete E2E Flow | Verify complete form from registration to payment success | Validate full business flow | Fresh school data | 1. Register 2. Login 3. School Details 4. Address 5. NOC 6. Trust 7. Land 8. Upload 9. Payment | Complete Excel data row | Entire flow completes without error | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | All pages | All methods | Parametrized by school_id |
| R-WF-002 | Workflow | Multi-School Execution | Verify framework handles multiple school submissions sequentially | Validate data-driven approach | Multiple school IDs in Excel | 1. Execute with SCH001 2. Execute with SCH002 etc. | Multiple school data | Each school completes independently | No | No | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | All pages | All methods | @pytest.mark.parametrize |
| R-WF-003 | Workflow | Screenshot on Failure | Verify screenshot is captured when any step fails | Validate error handling | Test execution with failure | 1. Cause a failure 2. Verify screenshot saved | None | Screenshot saved to screenshots/ folder | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | screenshot_util.py | take_screenshot() | |
| R-WF-004 | Workflow | Error Logging on Failure | Verify proper error logging when test fails | Validate logging | Test with failure | 1. Trigger failure 2. Check logs | None | Error details logged with school_id | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | logger.py | setup_logger() | |
| R-WF-005 | Workflow | Step Progress Indicator | Verify step indicator updates as user progresses through forms | Validate UI state | At any form step | 1. Complete each step 2. Verify stepper highlights | None | Active step updates correctly | No | No | Yes | Positive | Low | Not Covered | - | - | - | |
| R-WF-006 | Workflow | Back Navigation Between Steps | Verify user can navigate back to previous steps | Validate back flow | On any step beyond first | 1. Click Back button 2. Verify previous step loads | None | Previous form loads with retained data | No | No | Yes | Positive | Medium | Not Covered | - | - | - | |
| R-WF-007 | Workflow | Session Timeout During Form Fill | Verify system handles session timeout gracefully | Validate session | User filling form | 1. Wait for session timeout 2. Try Next | None | Redirected to login with appropriate message | No | No | Yes | Negative | Medium | Not Covered | - | - | - | |
| R-WF-008 | Workflow | Browser Refresh During Form | Verify data persistence on page refresh | Validate data retention | Form partially filled | 1. Fill some fields 2. Refresh browser 3. Check data | None | Either data retained or user warned | No | No | Yes | Positive | Medium | Not Covered | - | - | - | |

---

# FINAL REPORT

---

## SUMMARY 1 - Test Suite Classification

| Suite | Count |
|-------|-------|
| **Smoke** | 14 |
| **Sanity** | 44 |
| **Regression** | 105 |
| **Total Unique Test Cases** | **105** |

---

## SUMMARY 2 - Scenario Type Breakdown

| Type | Count |
|------|-------|
| **Positive** | 53 |
| **Negative** | 44 |
| **Boundary** | 8 |

---

## SUMMARY 3 - Module Distribution

| Module | Total TCs |
|--------|-----------|
| Registration | 13 |
| Authentication | 10 |
| Navigation/Dashboard | 4 |
| School Details | 14 |
| Address Details | 12 |
| NOC Details | 8 |
| Trust Details | 8 |
| Land Certificate | 10 |
| Upload Documents | 10 |
| Payment | 10 |
| Cross-Cutting/Workflow | 8 |

---

## SUMMARY 4 - Automation Coverage

| Coverage | Count | Percentage |
|----------|-------|------------|
| **Fully Covered** | 35 | 33% |
| **Partially Covered** | 5 | 5% |
| **Not Covered** | 65 | 62% |

**Current Automation Coverage: 36%** (Fully + Partially)

---

## SUMMARY 5 - Automation Gap Analysis

### Critical Gaps (Must Automate):
1. **Mandatory field validations** - No negative testing for blank fields across all modules
2. **Invalid login scenarios** - Only happy path automated
3. **Invalid file type upload** - No file validation testing
4. **Payment failure/timeout** - No error path for payment
5. **Session timeout handling** - Not tested
6. **Business rule validations** - Date logic, cascading dependencies

### Medium Priority Gaps:
7. **Boundary testing** - Character limits, numeric ranges
8. **Field format validations** - Email, mobile, PIN, UDISE formats
9. **Conditional field logic** - Only Sale Deed path tested
10. **Back navigation** - Never tested
11. **Data persistence** - Not validated

### Low Priority Gaps:
12. **UI state validations** - Step indicator, button states
13. **Cross-browser testing** - Only Chromium
14. **Performance under load** - Not applicable for current scope

---

## SUMMARY 6 - Recommended Automation Priority

| Priority | Scenarios | Estimated Effort |
|----------|-----------|------------------|
| P1 - Immediate | All mandatory field validations (Negative) | 2 days |
| P2 - Next Sprint | Login negative scenarios + field format validations | 2 days |
| P3 - Following Sprint | Boundary testing + Business rules | 3 days |
| P4 - Future | Back navigation + Session + Data persistence | 2 days |
| P5 - Enhancement | File type validations + Payment error paths | 2 days |

**Total estimated effort to reach 90%+ coverage: ~11 days**

---

## NOTES

1. The existing E2E framework provides excellent POSITIVE path coverage
2. The primary gap is NEGATIVE and BOUNDARY testing
3. The framework architecture (POM + Data-Driven) is well-suited for scaling
4. Recommend creating a separate `test_negative_scenarios.py` for negative tests
5. Recommend `test_boundary_scenarios.py` for boundary validations
6. The parametrized approach with Excel allows easy test data expansion
7. Allure steps provide good traceability for the happy path
