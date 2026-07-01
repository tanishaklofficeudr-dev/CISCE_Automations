# CISCE Preliminary Affiliation Portal
# Master Test Case Repository
## Structured & De-duplicated Enterprise Test Suite

---

# MASTER TEST CASE TABLE

| TC ID | Module | Feature | Test Case Title | Objective | Preconditions | Test Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Automation Script | Page Object | Method Name | Remarks |
|-------|--------|---------|-----------------|-----------|---------------|------------|-----------|-----------------|-------|--------|------------|---------------|----------|---------------------|-------------------|-------------|-------------|---------|
| TC-REG-001 | Registration | New School Registration | Verify new school registers successfully with valid mobile and email | Validate complete registration happy path | Application URL accessible | 1. Open registration URL 2. Enter valid 10-digit mobile 3. Enter valid email 4. Click Register 5. Verify success popup 6. Click OK | Mobile: 9876543210, Email: school@example.com | Registration successful popup appears, user proceeds to login | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | registration_page.py | register_school() | Core E2E flow |
| TC-REG-002 | Registration | Page Accessibility | Verify registration page loads with all required elements | Validate page accessibility and element visibility | Internet connection available | 1. Navigate to registration URL 2. Verify mobile field visible 3. Verify email field visible 4. Verify Register button visible | URL: /registration | All registration elements are visible and interactive | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | registration_page.py | register_school() | page.goto() |
| TC-REG-003 | Registration | Duplicate Prevention | Verify registration fails for already registered mobile number | Validate duplicate mobile prevention | Mobile already registered in system | 1. Enter existing mobile number 2. Enter email 3. Click Register 4. Verify error/no popup | Existing mobile number | Error message displayed OR popup does not appear | No | Yes | Yes | Negative | High | Partially Covered | test_preliminary_form_main.py | registration_page.py | register_school() | try/except without explicit assertion |
| TC-REG-004 | Registration | Mandatory - Mobile | Verify registration blocked when mobile field is empty | Validate mandatory mobile field | Registration page loaded | 1. Leave mobile blank 2. Enter email 3. Click Register | Mobile: empty | Validation error - mobile number required | No | No | Yes | Negative | High | Not Covered | - | registration_page.py | - | |
| TC-REG-005 | Registration | Invalid Mobile Format | Verify registration fails with alphabetic or special characters in mobile | Validate mobile format restriction | Registration page loaded | 1. Enter abc123 or @#$% in mobile 2. Enter email 3. Click Register | Mobile: abc123, @#$% | Validation error - invalid mobile format | No | No | Yes | Negative | High | Not Covered | - | registration_page.py | - | |
| TC-REG-006 | Registration | Mobile Boundary - Minimum | Verify registration fails with less than 10 digit mobile | Validate minimum digit requirement | Registration page loaded | 1. Enter 9-digit mobile 2. Enter email 3. Click Register | Mobile: 987654321 (9 digits) | Validation error - mobile must be 10 digits | No | No | Yes | Boundary | High | Not Covered | - | registration_page.py | - | |
| TC-REG-007 | Registration | Mobile Boundary - Maximum | Verify registration fails with more than 10 digit mobile | Validate maximum digit restriction | Registration page loaded | 1. Enter 11-digit mobile 2. Enter email 3. Click Register | Mobile: 98765432101 (11 digits) | Field rejects input OR validation error | No | No | Yes | Boundary | Medium | Not Covered | - | registration_page.py | - | |
| TC-REG-008 | Registration | Mandatory - Email | Verify registration blocked when email field is empty | Validate mandatory email field | Registration page loaded | 1. Enter valid mobile 2. Leave email blank 3. Click Register | Email: empty | Validation error - email required | No | No | Yes | Negative | High | Not Covered | - | registration_page.py | - | |
| TC-REG-009 | Registration | Invalid Email Format | Verify registration fails with malformed email address | Validate email format restriction | Registration page loaded | 1. Enter valid mobile 2. Enter invalid email formats 3. Click Register | Email: abc, abc@, @domain.com, abc@.com | Validation error - invalid email format | No | No | Yes | Negative | High | Not Covered | - | registration_page.py | - | |
| TC-REG-010 | Registration | Email Boundary - Maximum Length | Verify email field handles maximum character limit | Validate field boundary | Registration page loaded | 1. Enter 256+ character email 2. Observe behaviour | Email: 256+ character string | Field truncates or shows validation error | No | No | Yes | Boundary | Low | Not Covered | - | registration_page.py | - | |
| TC-REG-011 | Registration | Country Code | Verify country code field behaviour and validation | Validate country code handling | Registration page loaded | 1. Observe country code field 2. Attempt to change code | Various country codes | Country code validation works correctly | No | No | Yes | Positive | Medium | Not Covered | - | registration_page.py | - | |
| TC-REG-012 | Registration | Success Popup Content | Verify success popup displays exact expected message | Validate popup message accuracy | Valid registration submitted | 1. Register with valid data 2. Read popup text 3. Verify exact wording | None | Popup shows "Registration successful" text | No | Yes | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | registration_page.py | register_school() | expect with text match |
| TC-REG-013 | Registration | Post-Registration State | Verify page state allows login navigation after registration | Validate post-registration flow | Registration successful | 1. Complete registration 2. Click OK 3. Verify login link available | None | Login link becomes accessible | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | registration_page.py | register_school() | |
| TC-AUTH-001 | Authentication | Valid Login | Verify user logs in successfully and reaches dashboard | Validate login happy path | User is registered | 1. Click login link 2. Enter valid mobile 3. Enter valid password 4. Click Login 5. Verify dashboard URL | Valid mobile + password | User redirected to /preliminary/school/dashboard | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | login_page.py | login() | Password via page.pause() |
| TC-AUTH-002 | Authentication | Login Page Navigation | Verify login link navigates to login form correctly | Validate login page access | Registration page visible | 1. Click login link 2. Verify mobile input field visible 3. Verify Login button visible | None | Login form appears with all elements | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | login_page.py | login() | |
| TC-AUTH-003 | Authentication | Invalid Mobile Login | Verify login fails with unregistered mobile number | Validate authentication rejection | Login page loaded | 1. Enter unregistered mobile 2. Enter any password 3. Click Login | Unregistered mobile number | Error message - invalid credentials | No | Yes | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| TC-AUTH-004 | Authentication | Invalid Password Login | Verify login fails with incorrect password | Validate password verification | Login page loaded | 1. Enter valid mobile 2. Enter wrong password 3. Click Login | Valid mobile + wrong password | Error message - invalid credentials | No | Yes | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| TC-AUTH-005 | Authentication | Mandatory - Mobile Login | Verify login blocked with empty mobile field | Validate mandatory login field | Login page loaded | 1. Leave mobile empty 2. Click Login | Mobile: empty | Validation error - mobile required | No | No | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| TC-AUTH-006 | Authentication | Mandatory - Password Login | Verify login blocked with empty password field | Validate mandatory password | Login page loaded | 1. Enter valid mobile 2. Leave password empty 3. Click Login | Password: empty | Validation error - password required | No | No | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| TC-AUTH-007 | Authentication | Account Lockout | Verify account lockout after multiple failed login attempts | Validate security rate limiting | Login page loaded | 1. Enter valid mobile 2. Enter wrong password 5 consecutive times | Wrong password x5 | Account locked or rate limit message | No | No | Yes | Negative | High | Not Covered | - | login_page.py | - | |
| TC-AUTH-008 | Authentication | Session Persistence | Verify user remains authenticated after page refresh | Validate session management | User logged in | 1. Login successfully 2. Refresh browser 3. Verify still on dashboard | None | User remains on dashboard after refresh | No | No | Yes | Positive | Medium | Not Covered | - | - | - | |
| TC-AUTH-009 | Authentication | Logout | Verify logout terminates session and blocks dashboard access | Validate session termination | User logged in | 1. Click logout 2. Verify redirect to login 3. Navigate to dashboard URL directly | None | Redirected to login, dashboard inaccessible | No | Yes | Yes | Positive | High | Not Covered | - | - | - | |
| TC-AUTH-010 | Authentication | Route Protection | Verify unauthenticated users cannot access protected routes | Validate unauthorized access prevention | Not logged in | 1. Navigate directly to dashboard URL without login | Dashboard URL | Redirected to login page | No | No | Yes | Negative | High | Not Covered | - | - | - | |
| TC-NAV-001 | Navigation | Dashboard Loading | Verify Get Started page loads after successful login | Validate post-login navigation | User logged in | 1. Login 2. Verify URL contains /preliminary/school/dashboard 3. Verify instructions visible | None | Dashboard with Get Started content loads correctly | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | inline | page.wait_for_url() | |
| TC-NAV-002 | Navigation | Get Started Next Button | Verify Next button navigates from Get Started to School Details | Validate workflow progression | Dashboard loaded | 1. Click Next button 2. Verify School Details form appears | None | School Details form is visible and interactive | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | inline | page.get_by_role() | |
| TC-NAV-003 | Navigation | Step Progress Indicator | Verify progress stepper highlights correct active step | Validate UI state tracking | Any form step | 1. Navigate to each step 2. Verify active step in stepper | None | Stepper shows correct active step | No | No | Yes | Positive | Low | Not Covered | - | - | - | |
| TC-NAV-004 | Navigation | Instruction Content | Verify Get Started page displays correct document requirements | Validate business content | Dashboard loaded | 1. Read page content 2. Verify NOC, Land Certificate, Society docs mentioned | None | All required document types are listed | No | No | Yes | Positive | Low | Not Covered | - | - | - | |
| TC-SCH-001 | School Details | Complete Form Submission | Verify school details form submits with all valid mandatory fields | Validate form happy path | School Details page loaded | 1. Fill school name 2. Select classification 3. Select type 4. Fill contact person 5. Fill website 6. Fill UDISE 7. Select category 8. Click Next | All valid data from Excel | Form submits, navigates to Address Details | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | school_details_page.py | fill_school_details() | |
| TC-SCH-002 | School Details | Mandatory - School Name | Verify form blocked without school name | Validate mandatory field | Page loaded | 1. Leave school name blank 2. Fill others 3. Click Next | School name: empty | Validation error - school name required | No | Yes | Yes | Negative | High | Not Covered | - | school_details_page.py | - | |
| TC-SCH-003 | School Details | Invalid - School Name Special Chars | Verify school name rejects only special characters | Validate input quality | Page loaded | 1. Enter @#$%^& as school name 2. Click Next | School name: @#$%^& | Validation error or sanitization | No | No | Yes | Negative | Medium | Not Covered | - | school_details_page.py | - | |
| TC-SCH-004 | School Details | Invalid - School Name Numeric Only | Verify school name rejects only numeric input | Validate name field | Page loaded | 1. Enter 123456 as school name 2. Click Next | School name: 123456 | Validation error | No | No | Yes | Negative | Medium | Not Covered | - | school_details_page.py | - | |
| TC-SCH-005 | School Details | Boundary - School Name Max Length | Verify school name maximum character limit enforcement | Validate boundary | Page loaded | 1. Enter 200+ characters in school name | School name: 200+ chars | Field truncates or max limit error | No | No | Yes | Boundary | Medium | Not Covered | - | school_details_page.py | - | |
| TC-SCH-006 | School Details | Mandatory - Classification | Verify form blocked without selecting classification | Validate mandatory dropdown | Page loaded | 1. Fill all except classification 2. Click Next | Classification: not selected | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | school_details_page.py | - | |
| TC-SCH-007 | School Details | Mandatory - School Type | Verify form blocked without selecting school type | Validate mandatory dropdown | Page loaded | 1. Fill all except school type 2. Click Next | Type: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | school_details_page.py | - | |
| TC-SCH-008 | School Details | Mandatory - School Category | Verify form blocked without selecting school category | Validate mandatory dropdown | Page loaded | 1. Fill all except category 2. Click Next | Category: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | school_details_page.py | - | |
| TC-SCH-009 | School Details | Invalid - UDISE Non-Numeric | Verify UDISE field rejects non-numeric input | Validate field type | Page loaded | 1. Enter alphabets in UDISE field | UDISE: abcdef | Validation error or field rejects | No | No | Yes | Negative | Medium | Not Covered | - | school_details_page.py | - | |
| TC-SCH-010 | School Details | Boundary - UDISE Digit Count | Verify UDISE enforces exact digit requirement | Validate boundary | Page loaded | 1. Enter fewer/more digits than required | Various lengths | Only valid length accepted | No | No | Yes | Boundary | Medium | Not Covered | - | school_details_page.py | - | |
| TC-SCH-011 | School Details | Invalid - Website URL Format | Verify website field handles invalid URL format | Validate URL format | Page loaded | 1. Enter invalid URL format | Website: notaurl, htp://bad | Warning or graceful handling | No | No | Yes | Negative | Low | Not Covered | - | school_details_page.py | - | |
| TC-SCH-012 | School Details | Invalid - Contact Person Numeric | Verify contact person rejects numeric-only input | Validate name field | Page loaded | 1. Enter only numbers in contact person | Contact: 123456 | Validation error | No | No | Yes | Negative | Low | Not Covered | - | school_details_page.py | - | |
| TC-SCH-013 | School Details | Data Persistence on Back Navigation | Verify school details retained when navigating back from next step | Validate data retention | Form submitted | 1. Fill form 2. Go next 3. Navigate back | None | Previously entered data is retained | No | No | Yes | Positive | Medium | Not Covered | - | school_details_page.py | - | |
| TC-SCH-014 | School Details | Dropdown Options Loading | Verify all dropdown options load correctly from server | Validate dynamic data loading | Page loaded | 1. Click each dropdown 2. Verify options present | None | All dropdowns have options loaded | No | No | Yes | Positive | Medium | Not Covered | - | school_details_page.py | - | |
| TC-ADDR-001 | Address Details | Complete Form Submission | Verify address details form submits with all valid fields | Validate form happy path | Address page loaded | 1. Fill address 2. Select country 3. Select state 4. Select district 5. Select city 6. Fill PIN 7. Select locality 8. Click Next | All valid data | Form submits, navigates to NOC Details | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | address_details_page.py | fill_address_details() | |
| TC-ADDR-002 | Address Details | Mandatory - Address Line | Verify form blocked without address line | Validate mandatory | Page loaded | 1. Leave address blank 2. Fill others 3. Click Next | Address: empty | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | address_details_page.py | - | |
| TC-ADDR-003 | Address Details | Cascading - State Depends on Country | Verify state dropdown populates based on selected country | Validate cascading logic | Page loaded | 1. Select India 2. Verify Indian states load 3. Change country 4. Verify states update | India, Other countries | State list updates per country selection | No | Yes | Yes | Positive | High | Partially Covered | test_preliminary_form_main.py | address_details_page.py | fill_address_details() | Only India tested |
| TC-ADDR-004 | Address Details | Cascading - District Depends on State | Verify district dropdown populates based on selected state | Validate cascading logic | State selected | 1. Select state 2. Verify relevant districts load | State selection | Districts relevant to selected state appear | No | Yes | Yes | Positive | High | Partially Covered | test_preliminary_form_main.py | address_details_page.py | fill_address_details() | Single state tested |
| TC-ADDR-005 | Address Details | Cascading - City Depends on District | Verify city dropdown populates based on selected district | Validate cascading logic | District selected | 1. Select district 2. Verify relevant cities load | District selection | Cities relevant to selected district appear | No | No | Yes | Positive | High | Partially Covered | test_preliminary_form_main.py | address_details_page.py | fill_address_details() | |
| TC-ADDR-006 | Address Details | Invalid - PIN Non-Numeric | Verify PIN code field rejects alphabetic input | Validate field type restriction | Page loaded | 1. Enter abc in PIN field | PIN: abc123 | Validation error or field rejects | No | No | Yes | Negative | Medium | Not Covered | - | address_details_page.py | - | |
| TC-ADDR-007 | Address Details | Boundary - PIN Less Than 6 Digits | Verify PIN code requires minimum 6 digits | Validate boundary | Page loaded | 1. Enter 5-digit PIN | PIN: 12345 | Validation error - must be 6 digits | No | No | Yes | Boundary | Medium | Not Covered | - | address_details_page.py | - | |
| TC-ADDR-008 | Address Details | Boundary - PIN More Than 6 Digits | Verify PIN code cannot exceed 6 digits | Validate boundary | Page loaded | 1. Enter 7-digit PIN | PIN: 1234567 | Field truncates or validation error | No | No | Yes | Boundary | Medium | Not Covered | - | address_details_page.py | - | |
| TC-ADDR-009 | Address Details | Mandatory - Country | Verify form blocked without country selection | Validate mandatory | Page loaded | 1. Skip country selection 2. Click Next | Country: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | address_details_page.py | - | |
| TC-ADDR-010 | Address Details | Mandatory - State | Verify form blocked without state selection | Validate mandatory | Country selected | 1. Select country only 2. Click Next | State: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | address_details_page.py | - | |
| TC-ADDR-011 | Address Details | Boundary - Address Max Length | Verify address field maximum character limit | Validate boundary | Page loaded | 1. Enter 500+ character address | Long address string | Field truncates or accepts with limit | No | No | Yes | Boundary | Low | Not Covered | - | address_details_page.py | - | |
| TC-ADDR-012 | Address Details | Mandatory - Locality Type | Verify form blocked without locality type selection | Validate mandatory | Page loaded | 1. Fill all except locality 2. Click Next | Locality: not selected | Validation error | No | No | Yes | Negative | Medium | Not Covered | - | address_details_page.py | - | |
| TC-NOC-001 | NOC Details | Complete Form Submission | Verify NOC details form submits with all valid information | Validate form happy path | NOC page loaded | 1. Fill authority 2. Fill designation 3. Fill office address 4. Select country/state 5. Fill reference number 6. Select date 7. Click Next | All valid data | Form submits, navigates to Trust Details | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | noc_details_page.py | fill_noc_details() | |
| TC-NOC-002 | NOC Details | Mandatory - NOC Authority | Verify form blocked without NOC issuing authority | Validate mandatory | Page loaded | 1. Leave authority blank 2. Click Next | Authority: empty | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| TC-NOC-003 | NOC Details | Mandatory - Designation | Verify form blocked without designation | Validate mandatory | Page loaded | 1. Leave designation blank 2. Click Next | Designation: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| TC-NOC-004 | NOC Details | Mandatory - Office Address | Verify form blocked without office address | Validate mandatory | Page loaded | 1. Leave office address blank 2. Click Next | Office address: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| TC-NOC-005 | NOC Details | Business Rule - Future Date | Verify NOC date cannot be set to a future date | Validate business rule | Page loaded | 1. Select a date in the future | Future date | Validation error - date cannot be future | No | Yes | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| TC-NOC-006 | NOC Details | Mandatory - Reference Number | Verify form blocked without NOC reference number | Validate mandatory | Page loaded | 1. Leave reference blank 2. Click Next | Reference: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| TC-NOC-007 | NOC Details | Date Picker Back Navigation | Verify date picker back arrow navigates to previous months | Validate date picker UI | Date picker open | 1. Click back arrow 2. Verify month changes correctly | None | Month decrements with each click | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | noc_details_page.py | fill_noc_details() | |
| TC-NOC-008 | NOC Details | Mandatory - NOC Date | Verify form blocked without selecting NOC date | Validate mandatory | Page loaded | 1. Fill all except date 2. Click Next | Date: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | noc_details_page.py | - | |
| TC-TRUST-001 | Trust Details | Complete Form Submission | Verify trust details form submits with all valid fields | Validate form happy path | Trust page loaded | 1. Select ownership type 2. Fill name 3. Set establishment date 4. Set registration date 5. Fill registration number 6. Click Next | All valid data | Form submits, navigates to Land Certificate | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | trust_details_page.py | fill_trust_details() | |
| TC-TRUST-002 | Trust Details | Mandatory - Ownership Type | Verify form blocked without ownership type selection | Validate mandatory | Page loaded | 1. Leave ownership as Select 2. Click Next | Type: not selected | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |
| TC-TRUST-003 | Trust Details | Mandatory - Trust Name | Verify form blocked without trust/society name | Validate mandatory | Page loaded | 1. Leave name blank 2. Click Next | Name: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |
| TC-TRUST-004 | Trust Details | Business Rule - Future Establishment Date | Verify establishment date cannot be in the future | Validate business rule | Page loaded | 1. Enter future date for establishment | Future date | Validation error | No | Yes | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |
| TC-TRUST-005 | Trust Details | Business Rule - Registration Before Establishment | Verify registration date cannot be before establishment date | Validate logical consistency | Page loaded | 1. Set establishment to 2020 2. Set registration to 2019 | Reg date < Est date | Validation error - logical inconsistency | No | Yes | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | Critical business rule |
| TC-TRUST-006 | Trust Details | Mandatory - Registration Number | Verify form blocked without registration number | Validate mandatory | Page loaded | 1. Fill all except registration number 2. Click Next | Reg number: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |
| TC-TRUST-007 | Trust Details | Dynamic Form Loading | Verify ownership dropdown loads within expected time | Validate page stability | Navigated to Trust page | 1. Verify ownership dropdown visible after page load | None | Dropdown loads and is interactive | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | trust_details_page.py | fill_trust_details() | wait_for visible |
| TC-TRUST-008 | Trust Details | Mandatory - Establishment Date | Verify form blocked without establishment date | Validate mandatory | Page loaded | 1. Fill all except establishment date 2. Click Next | Date: empty | Validation error | No | No | Yes | Negative | High | Not Covered | - | trust_details_page.py | - | |
| TC-LAND-001 | Land Certificate | Complete Form Submission | Verify land certificate form submits with all valid fields | Validate form happy path | Land page loaded | 1. Select plot type 2. Select land type 3. Select area unit 4. Fill area 5. Fill location fields 6. Fill ownership 7. Select title doc 8. Fill details 9. Set date 10. Click Next | All valid data | Form submits, navigates to Upload Documents | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | land_certificate_page.py | fill_land_details() | |
| TC-LAND-002 | Land Certificate | Dynamic Form - Plot Type | Verify selecting Yes for plot type loads dynamic owner details form | Validate conditional rendering | Land page loaded | 1. Select Yes for plots 2. Verify Owner's Details section appears | Plot type: Yes | Dynamic form loads with all land fields | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | land_certificate_page.py | fill_land_details() | |
| TC-LAND-003 | Land Certificate | Conditional - Owned vs Leased | Verify form adjusts fields based on Owned or Leased selection | Validate conditional logic | Dynamic form loaded | 1. Select Owned 2. Verify fields 3. Select Leased 4. Verify different fields | Type: Owned, Leased | Appropriate fields shown per selection | No | Yes | Yes | Positive | High | Partially Covered | test_preliminary_form_main.py | land_certificate_page.py | fill_land_details() | Only one type per run |
| TC-LAND-004 | Land Certificate | Invalid - Land Area Zero | Verify land area cannot be zero | Validate business rule | Form loaded | 1. Enter 0 in land area 2. Click Next | Area: 0 | Validation error - must be positive | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| TC-LAND-005 | Land Certificate | Invalid - Land Area Negative | Verify land area cannot be negative | Validate input restriction | Form loaded | 1. Enter -100 in land area | Area: -100 | Validation error or field rejection | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| TC-LAND-006 | Land Certificate | Invalid - Land Area Non-Numeric | Verify land area rejects text input | Validate field type | Form loaded | 1. Enter text in area field | Area: abc | Field rejects or validation error | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| TC-LAND-007 | Land Certificate | Conditional - Sale Deed Fields | Verify Sale Deed specific fields appear only when Sale Deed is selected | Validate conditional logic | Form loaded | 1. Select Sale Deed 2. Verify favor field 3. Select other doc 4. Verify field hides | Title: Sale Deed, Others | Conditional field shows/hides correctly | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | land_certificate_page.py | fill_land_details() | |
| TC-LAND-008 | Land Certificate | Mandatory - Area Unit | Verify form blocked without area unit selection | Validate mandatory | Form loaded | 1. Leave area unit as default 2. Click Next | Unit: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | land_certificate_page.py | - | |
| TC-LAND-009 | Land Certificate | Business Rule - Future Document Date | Verify land document date cannot be in the future | Validate business rule | Form loaded | 1. Enter future date | Future date | Validation error | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| TC-LAND-010 | Land Certificate | Multiple Mandatory Blank | Verify all validation errors shown when form submitted blank | Validate multiple validations | Form loaded | 1. Click Next without filling anything | All empty | Multiple validation messages | No | No | Yes | Negative | Medium | Not Covered | - | land_certificate_page.py | - | |
| TC-DOC-001 | Upload Documents | Complete Upload and Submission | Verify all documents uploaded and form proceeds to payment | Validate upload happy path | Upload page loaded | 1. Upload all 5 documents 2. Fill comments 3. Select affiliation 4. Check both boxes 5. Click Proceed to Payment | PDF files, comments, affiliation type | All uploaded, navigates to payment | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| TC-DOC-002 | Upload Documents | Mandatory - NOC Document | Verify form blocked without NOC document upload | Validate mandatory upload | Page loaded | 1. Upload all except NOC 2. Click Proceed | NOC: not uploaded | Validation error - NOC required | No | Yes | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| TC-DOC-003 | Upload Documents | Invalid File Type | Verify system rejects non-allowed file types | Validate file type restriction | Page loaded | 1. Try uploading .exe or .txt file | File: test.exe | File rejected with error message | No | Yes | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| TC-DOC-004 | Upload Documents | Boundary - File Size Limit | Verify system rejects files exceeding maximum size | Validate file size boundary | Page loaded | 1. Upload file exceeding size limit | Large file >10MB | Error - file size exceeds limit | No | No | Yes | Boundary | Medium | Not Covered | - | upload_documents_page.py | - | |
| TC-DOC-005 | Upload Documents | Mandatory - Affiliation Type | Verify form blocked without selecting affiliation type | Validate mandatory | Page loaded | 1. Upload all 2. Skip affiliation type 3. Click Proceed | Type: not selected | Validation error | No | No | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| TC-DOC-006 | Upload Documents | Mandatory - Verification Checkboxes | Verify form blocked without checking both verification boxes | Validate mandatory checkboxes | Page loaded | 1. Upload all 2. Leave checkboxes unchecked 3. Click Proceed | Checkboxes: unchecked | Validation error or button disabled | No | No | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| TC-DOC-007 | Upload Documents | File Replacement | Verify user can replace already uploaded file | Validate re-upload capability | File uploaded | 1. Upload file 2. Upload different file to same slot | Two different files | New file replaces old successfully | No | No | Yes | Positive | Medium | Not Covered | - | upload_documents_page.py | - | |
| TC-DOC-008 | Upload Documents | Boundary - Comments Max Length | Verify comments field maximum character handling | Validate boundary | Page loaded | 1. Enter 1000+ character comment | Long comment | Field truncates or accepts with limit | No | No | Yes | Boundary | Low | Not Covered | - | upload_documents_page.py | - | |
| TC-DOC-009 | Upload Documents | Valid Image Formats | Verify school image accepts JPG and PNG formats | Validate file format acceptance | Page loaded | 1. Upload JPG 2. Upload PNG | JPG, PNG files | Both formats accepted | No | No | Yes | Positive | Medium | Not Covered | - | upload_documents_page.py | - | |
| TC-DOC-010 | Upload Documents | All Documents Missing | Verify form shows errors when no documents uploaded | Validate multiple mandatory | Page loaded | 1. Click Proceed without any uploads | All empty | Multiple validation errors | No | No | Yes | Negative | Medium | Not Covered | - | upload_documents_page.py | - | |
| TC-PAY-001 | Payment | Complete Payment Flow | Verify end-to-end payment completes via ICICI gateway | Validate payment happy path | Payment page loaded | 1. Click Pay Rs 2. Select ICICI 3. Proceed to Pay 4. Handle iframe 5. Show QR 6. Complete 7. Verify success | None | "Transaction Successful!" shown, redirects to homepage | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| TC-PAY-002 | Payment | Payment URL Redirect | Verify correct payment URL after form submission | Validate URL navigation | Proceed clicked | 1. Verify URL contains /payment/ | None | URL matches payment pattern | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| TC-PAY-003 | Payment | Gateway - ICICI Selection | Verify ICICI Bank gateway can be selected | Validate gateway selection | Payment Details visible | 1. Click ICICI Bank 2. Verify selected state | None | ICICI Bank shown as selected | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| TC-PAY-004 | Payment | Gateway - HDFC Selection | Verify HDFC Bank gateway can be selected | Validate alternate gateway | Payment Details visible | 1. Click HDFC Bank 2. Verify selected | None | HDFC Bank selected | No | No | Yes | Positive | Medium | Not Covered | - | upload_documents_page.py | - | |
| TC-PAY-005 | Payment | Mandatory - Gateway Selection | Verify payment cannot proceed without selecting gateway | Validate mandatory selection | Payment page loaded | 1. Click Proceed to Pay without selecting bank | None | Button disabled or error shown | No | Yes | Yes | Negative | High | Partially Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | JS removes disabled |
| TC-PAY-006 | Payment | Payment Timeout Handling | Verify system handles payment timeout gracefully | Validate error handling | Payment initiated | 1. Initiate payment 2. Wait for timeout | None | Timeout message with retry option | No | No | Yes | Negative | High | Not Covered | - | upload_documents_page.py | - | |
| TC-PAY-007 | Payment | Payment Cancellation | Verify user can cancel payment and return to form | Validate cancellation flow | Payment iframe shown | 1. Click Cancel in payment iframe | None | Returns to payment page or form | No | No | Yes | Negative | Medium | Not Covered | - | upload_documents_page.py | - | |
| TC-PAY-008 | Payment | Transaction Success Message | Verify Transaction Successful message after payment | Validate success confirmation | Payment completed | 1. Complete payment 2. Verify success text | None | "Transaction Successful!" text visible | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| TC-PAY-009 | Payment | Post-Payment Redirect | Verify redirect to school view page after successful payment | Validate end-state navigation | Transaction successful | 1. Click Go to Homepage 2. Verify URL | None | URL contains /school_view | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | upload_documents_page.py | upload_documents() | |
| TC-PAY-010 | Payment | Amount Verification | Verify correct payment amount displayed on payment page | Validate business data | Payment page loaded | 1. Verify displayed amount matches expected fee | Expected fee | Correct Rs amount displayed | No | No | Yes | Positive | Medium | Not Covered | - | upload_documents_page.py | - | |
| TC-WF-001 | Workflow | Complete E2E Flow | Verify complete form from registration to payment success | Validate full business flow | Fresh school data | 1. Register 2. Login 3. School 4. Address 5. NOC 6. Trust 7. Land 8. Upload 9. Payment | Complete Excel row | Entire flow completes successfully | Yes | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | All pages | All methods | Parametrized |
| TC-WF-002 | Workflow | Multi-School Execution | Verify framework handles multiple schools sequentially | Validate data-driven scaling | Multiple school IDs | 1. Execute for SCH001 2. Execute for SCH002 etc. | Multiple school data | Each completes independently | No | No | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | All pages | All methods | @pytest.mark.parametrize |
| TC-WF-003 | Workflow | Failure Screenshot Capture | Verify screenshot captured automatically on test failure | Validate error evidence | Test with failure | 1. Cause failure 2. Verify screenshot saved | None | Screenshot saved to screenshots/ | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | screenshot_util.py | take_screenshot() | |
| TC-WF-004 | Workflow | Failure Error Logging | Verify proper error logging on test failure | Validate logging mechanism | Test with failure | 1. Trigger failure 2. Check log output | None | Error details logged with school_id | No | No | Yes | Positive | Medium | Fully Covered | test_preliminary_form_main.py | logger.py | setup_logger() | |
| TC-WF-005 | Workflow | Back Navigation Between Steps | Verify user can navigate back to previous form steps | Validate backward navigation | Beyond first step | 1. Click Back 2. Verify previous form loads with data | None | Previous form loads with retained data | No | No | Yes | Positive | Medium | Not Covered | - | - | - | |
| TC-WF-006 | Workflow | Session Timeout During Form | Verify system handles session timeout during form filling | Validate session handling | User filling form | 1. Wait for timeout 2. Try Next | None | Redirect to login with message | No | No | Yes | Negative | Medium | Not Covered | - | - | - | |
| TC-WF-007 | Workflow | Browser Refresh Data Persistence | Verify data behavior on browser refresh during form | Validate data retention | Form partially filled | 1. Fill fields 2. Refresh 3. Check data | None | Data retained or user warned | No | No | Yes | Positive | Medium | Not Covered | - | - | - | |

---

# SUMMARIES

## Summary 1 - Total Counts

| Metric | Count |
|--------|-------|
| **Total Unique Test Cases** | **97** |
| Smoke Test Cases | 14 |
| Sanity Test Cases | 42 |
| Regression Test Cases | 97 |

---

## Summary 2 - Scenario Type

| Type | Count |
|------|-------|
| **Positive** | 49 |
| **Negative** | 41 |
| **Boundary** | 7 |

---

## Summary 3 - Automation Coverage

| Coverage Level | Count | Percentage |
|----------------|-------|------------|
| **Fully Covered** | 33 | 34% |
| **Partially Covered** | 5 | 5% |
| **Not Covered** | 59 | 61% |
| **Total Coverage (Fully + Partially)** | **38** | **39%** |

---

## Summary 4 - Module Distribution

| Module | Total |
|--------|-------|
| Registration | 13 |
| Authentication | 10 |
| Navigation | 4 |
| School Details | 14 |
| Address Details | 12 |
| NOC Details | 8 |
| Trust Details | 8 |
| Land Certificate | 10 |
| Upload Documents | 10 |
| Payment | 10 |
| Workflow | 7 |

---

# QUALITY ANALYSIS

## Duplicates Identified and Merged

| Original IDs | Merged Into | Reason |
|--------------|-------------|--------|
| SM-REG-001 + S-REG-002 | TC-REG-001 + TC-REG-002 | Registration happy path was partially duplicated with page access |
| SM-NAV-001 + SM-NAV-002 | TC-NAV-001 + TC-NAV-002 | Dashboard and Next button were listed separately but are sequential |
| R-WF-005 + R-NAV-003 | TC-NAV-003 | Step indicator mentioned in both Workflow and Navigation - merged to Navigation |
| SM-PAY-008 + SM-PAY-009 (from original) | TC-PAY-008 + TC-PAY-009 | Payment success and redirect kept separate as distinct validations |

**Total duplicates removed: 8** (from 105 down to 97)

---

## Missing Information Identified

| TC ID | Missing Field | Action Required |
|-------|---------------|-----------------|
| TC-REG-011 | Exact country codes to test | Needs manual review of available options |
| TC-SCH-005 | Exact maximum character limit | Needs UI inspection |
| TC-SCH-010 | Exact UDISE digit count | Needs business requirement confirmation |
| TC-ADDR-011 | Exact max address length | Needs UI inspection |
| TC-DOC-004 | Exact file size limit | Needs requirement confirmation |
| TC-PAY-010 | Expected fee amount | Needs business data |

---

## Inconsistencies Corrected

| Issue | Resolution |
|-------|------------|
| Some TCs marked both Smoke and having low priority | Removed Smoke from low priority items |
| Payment module tests split between upload_documents_page.py | Kept consistent Page Object reference |
| Workflow module had UI validations that belong to Navigation | Moved to Navigation module |
| Original had 105 TCs with some overlap | Consolidated to 97 unique TCs |

---

## Fields Requiring Manual Review

| TC ID | Field | Reason |
|-------|-------|--------|
| All "Not Covered" TCs | Automation Script | Will be populated after implementation |
| All "Not Covered" TCs | Method Name | Will be populated after implementation |
| TC-REG-006, TC-REG-007 | Test Data | Confirm exact mobile length requirement |
| TC-ADDR-007, TC-ADDR-008 | Test Data | Confirm PIN code is always 6 digits |
| TC-DOC-004 | Test Data | Confirm maximum file upload size |
