# CISCE Preliminary Affiliation Form - Test Case Analysis
## Generated from Existing Automation Framework

---

## TEST CASES TABLE

| TC ID | Module | Feature | Test Case | Objective | Preconditions | Steps | Test Data | Expected Result | Smoke | Sanity | Regression | Scenario Type | Priority | Automation Coverage | Page Object | Method Name | Script Name | Remarks |
|-------|--------|---------|-----------|-----------|---------------|-------|-----------|-----------------|-------|--------|------------|---------------|----------|--------------------:|-------------|-------------|-------------|---------|
| SM01 | Registration | School Registration | Verify registration page loads successfully | Validate that the registration page is accessible and loads all elements | None | 1. Navigate to registration URL 2. Verify page loads | URL: https://dev-eaffiliation.cisce.org/registration | Registration page loads with mobile and email fields visible | Yes | Yes | Yes | Positive | High | Fully Covered | registration_page.py | register_school() | test_preliminary_form_main.py | Page.goto() validates URL accessibility |
| SM02 | Registration | School Registration | Verify school registration with valid mobile and email | Validate that a new school can register with valid credentials | Registration page is loaded | 1. Enter valid mobile number 2. Enter valid email 3. Click Register 4. Verify success popup | mobile_number, email from Excel | Registration success popup appears and OK button is clickable | Yes | Yes | Yes | Positive | High | Fully Covered | registration_page.py | register_school() | test_preliminary_form_main.py | Handles both new and existing registrations |
| SM03 | Registration | Registration Popup | Verify registration success popup handling | Validate that success popup is handled correctly after registration | Registration form submitted | 1. Submit registration 2. Wait for popup 3. Click OK | None | Popup appears with "Registration successful" text, OK dismisses it | No | Yes | Yes | Positive | High | Fully Covered | registration_page.py | register_school() | test_preliminary_form_main.py | Uses expect with 2000ms timeout |
| R01 | Registration | Registration Popup | Verify duplicate registration handling | Validate system behavior when registering with already registered mobile | Mobile already registered | 1. Enter existing mobile 2. Enter email 3. Click Register | Existing mobile_number | Success popup does NOT appear, flow continues gracefully | No | No | Yes | Negative | High | Fully Covered | registration_page.py | register_school() | test_preliminary_form_main.py | try/except handles missing popup |
| SM04 | Login | User Authentication | Verify login page navigation | Validate login link navigates to login form | Registration complete | 1. Click login link 2. Verify login form appears | None | Login form with mobile number field is visible | Yes | Yes | Yes | Positive | High | Fully Covered | login_page.py | login() | test_preliminary_form_main.py | Uses get_by_role("link", name="login") |
| SM05 | Login | User Authentication | Verify login with valid credentials | Validate successful login with correct mobile and password | User is registered | 1. Enter mobile number 2. Enter password 3. Click Login | mobile_number from Excel | User is redirected to dashboard | Yes | Yes | Yes | Positive | High | Fully Covered | login_page.py | login() | test_preliminary_form_main.py | Password entered manually via page.pause() |
| S01 | Navigation | Get Started Page | Verify Get Started page loads after login | Validate dashboard loads with Get Started content | User logged in | 1. Login successfully 2. Wait for dashboard URL 3. Verify Next button | Dashboard URL pattern | Page URL contains /preliminary/school/dashboard | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | inline (page.wait_for_url) | test_preliminary_form_main.py | wait_for_url with 6000ms timeout |
| S02 | Navigation | Get Started Page | Verify Next button click on Get Started page | Validate navigation from Get Started to School Details | Get Started page loaded | 1. Click Next button | None | Navigates to School Details form | No | Yes | Yes | Positive | High | Fully Covered | test_preliminary_form_main.py | inline (page.get_by_role) | test_preliminary_form_main.py | get_by_role("button", name="Next") |
| SM06 | School Details | Form Filling | Verify school name field accepts valid input | Validate school name text field | School Details page loaded | 1. Fill school name from Excel | school_name | Field accepts and retains value | Yes | Yes | Yes | Positive | High | Fully Covered | school_details_page.py | fill_school_details() | test_preliminary_form_main.py | get_by_role("textbox", name="Name of School *") |
| S03 | School Details | Form Filling | Verify School Classification dropdown selection | Validate dropdown selection for classification | School Details page loaded | 1. Select classification from Excel | school_classification | Dropdown shows selected value | No | Yes | Yes | Positive | High | Fully Covered | school_details_page.py | fill_school_details() | test_preliminary_form_main.py | get_by_label with select_option |
| S04 | School Details | Form Filling | Verify School Type dropdown selection | Validate school type dropdown works | School Details page loaded | 1. Select school type | school_type | Dropdown shows selected value | No | Yes | Yes | Positive | High | Fully Covered | school_details_page.py | fill_school_details() | test_preliminary_form_main.py | locator("#school_type") |
| R02 | School Details | Form Filling | Verify contact person field accepts input | Validate contact person text field | School Details page loaded | 1. Fill contact person | contact_person | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | school_details_page.py | fill_school_details() | test_preliminary_form_main.py | locator("#contact_person") |
| R03 | School Details | Form Filling | Verify website field accepts valid URL | Validate website input field | School Details page loaded | 1. Fill website URL | website | Field accepts URL value | No | No | Yes | Positive | Medium | Fully Covered | school_details_page.py | fill_school_details() | test_preliminary_form_main.py | locator("#website") |
| R04 | School Details | Form Filling | Verify UDISE number field accepts numeric input | Validate UDISE number field | School Details page loaded | 1. Fill UDISE number | udise_number | Field accepts numeric value | No | No | Yes | Positive | Medium | Fully Covered | school_details_page.py | fill_school_details() | test_preliminary_form_main.py | locator("#udise") with str() conversion |
| S05 | School Details | Form Filling | Verify School Category dropdown selection | Validate category dropdown | School Details page loaded | 1. Select school category | school_category | Dropdown shows selected value | No | Yes | Yes | Positive | High | Fully Covered | school_details_page.py | fill_school_details() | test_preliminary_form_main.py | get_by_label("School Category *") |
| S06 | School Details | Navigation | Verify Next button submits school details | Validate form submission and navigation | All school details filled | 1. Click Next button | None | Navigates to Address Details page | No | Yes | Yes | Positive | High | Fully Covered | school_details_page.py | fill_school_details() | test_preliminary_form_main.py | get_by_role("button", name="Next") |
| SM07 | Address Details | Form Filling | Verify address line field accepts input | Validate address field | Address Details page loaded | 1. Fill address line | address_line_1 | Field accepts value | Yes | Yes | Yes | Positive | High | Fully Covered | address_details_page.py | fill_address_details() | test_preliminary_form_main.py | locator("#address_1") |
| S07 | Address Details | Dropdown Selection | Verify Country dropdown selection | Validate country autocomplete dropdown | Address page loaded | 1. Click India textbox 2. Select country option | country | Country selected successfully | No | Yes | Yes | Positive | High | Fully Covered | address_details_page.py | fill_address_details() | test_preliminary_form_main.py | Uses role-based option selection |
| S08 | Address Details | Dropdown Selection | Verify State dropdown selection | Validate state dropdown with Select2 | Country selected | 1. Click state container 2. Select state | state | State selected | No | Yes | Yes | Positive | High | Fully Covered | address_details_page.py | fill_address_details() | test_preliminary_form_main.py | select2-state-container |
| S09 | Address Details | Dropdown Selection | Verify District dropdown selection | Validate district selection | State selected | 1. Click Select textbox 2. Choose district | district | District selected | No | Yes | Yes | Positive | High | Fully Covered | address_details_page.py | fill_address_details() | test_preliminary_form_main.py | Cascading dropdown |
| S10 | Address Details | Dropdown Selection | Verify City dropdown selection | Validate city selection | District selected | 1. Click Select 2. Choose city | city | City selected | No | Yes | Yes | Positive | High | Fully Covered | address_details_page.py | fill_address_details() | test_preliminary_form_main.py | Cascading dropdown |
| R05 | Address Details | Form Filling | Verify ZIP/PIN code field | Validate PIN code input | Address page loaded | 1. Fill ZIP code | zip_pin | Field accepts numeric value | No | No | Yes | Positive | Medium | Fully Covered | address_details_page.py | fill_address_details() | test_preliminary_form_main.py | locator("#zip") with str() |
| R06 | Address Details | Form Filling | Verify Locality Type dropdown | Validate locality selection | Address page loaded | 1. Select locality type | locality_type | Dropdown shows selection | No | No | Yes | Positive | Medium | Fully Covered | address_details_page.py | fill_address_details() | test_preliminary_form_main.py | locator("#locality") |
| S11 | Address Details | Navigation | Verify Next button submits address details | Validate address form submission | All address fields filled | 1. Click Next | None | Navigates to NOC Details page | No | Yes | Yes | Positive | High | Fully Covered | address_details_page.py | fill_address_details() | test_preliminary_form_main.py | |
| SM08 | NOC Details | Form Filling | Verify NOC Issuing Authority field | Validate NOC authority input | NOC page loaded | 1. Fill issuing authority | noc_issuing_authority | Field accepts value | Yes | Yes | Yes | Positive | High | Fully Covered | noc_details_page.py | fill_noc_details() | test_preliminary_form_main.py | locator("#noc_authority") |
| R07 | NOC Details | Form Filling | Verify Designation field | Validate designation input | NOC page loaded | 1. Fill designation | designation | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | noc_details_page.py | fill_noc_details() | test_preliminary_form_main.py | locator("#noc_designation") |
| R08 | NOC Details | Form Filling | Verify Office Address field | Validate office address input | NOC page loaded | 1. Fill office address | office_address | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | noc_details_page.py | fill_noc_details() | test_preliminary_form_main.py | locator("#noc_office_address") |
| S12 | NOC Details | Dropdown Selection | Verify Country and State dropdowns | Validate NOC country/state selection | NOC page loaded | 1. Select country 2. Select state | Country value=2, State value=30 | Both dropdowns set correctly | No | Yes | Yes | Positive | High | Fully Covered | noc_details_page.py | fill_noc_details() | test_preliminary_form_main.py | Hardcoded values for India/Rajasthan |
| R09 | NOC Details | Form Filling | Verify NOC Reference Number field | Validate reference number input | NOC page loaded | 1. Fill reference number | noc_reference_number | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | noc_details_page.py | fill_noc_details() | test_preliminary_form_main.py | |
| S13 | NOC Details | Date Picker | Verify NOC Date selection via date picker | Validate date picker navigation and selection | NOC page loaded | 1. Click date field 2. Click back arrow 3. Select day 16 | Date: 16th of previous month | Date is selected and displayed | No | Yes | Yes | Positive | High | Fully Covered | noc_details_page.py | fill_noc_details() | test_preliminary_form_main.py | Uses columnheader back arrow navigation |
| S14 | NOC Details | Navigation | Verify Next button submits NOC details | Validate NOC form submission | All NOC fields filled | 1. Click Next | None | Navigates to Trust Details page | No | Yes | Yes | Positive | High | Fully Covered | noc_details_page.py | fill_noc_details() | test_preliminary_form_main.py | |
| SM09 | Trust Details | Form Filling | Verify Ownership Type dropdown | Validate ownership type selection | Trust page loaded, element visible | 1. Wait for element 2. Select ownership type | ownership_type | Dropdown shows selection | Yes | Yes | Yes | Positive | High | Fully Covered | trust_details_page.py | fill_trust_details() | test_preliminary_form_main.py | Includes wait_for_timeout and wait_for visible |
| S15 | Trust Details | Form Filling | Verify Trust/Society/Company Name field | Validate name input | Trust page loaded | 1. Fill trust name | trust_name | Field accepts value | No | Yes | Yes | Positive | High | Fully Covered | trust_details_page.py | fill_trust_details() | test_preliminary_form_main.py | locator("#owner_name") |
| S16 | Trust Details | Date Input | Verify Establishment Date input via JavaScript | Validate date setting through JS injection | Trust page loaded | 1. Set date via evaluate() | establishment_date | Date field shows value | No | Yes | Yes | Positive | High | Fully Covered | trust_details_page.py | fill_trust_details() | test_preliminary_form_main.py | Uses nativeInputValueSetter for React compatibility |
| S17 | Trust Details | Date Input | Verify Registration Date input via JavaScript | Validate registration date setting | Trust page loaded | 1. Set date via evaluate() | registration_date | Date field shows value | No | Yes | Yes | Positive | High | Fully Covered | trust_details_page.py | fill_trust_details() | test_preliminary_form_main.py | Same JS approach as establishment date |
| R10 | Trust Details | Form Filling | Verify Registration Number field | Validate registration number input | Trust page loaded | 1. Fill registration number | registration_number | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | trust_details_page.py | fill_trust_details() | test_preliminary_form_main.py | locator("#registration_no") |
| S18 | Trust Details | Navigation | Verify Next button submits trust details | Validate trust form submission | All trust fields filled | 1. Click Next | None | Navigates to Land Certificate page | No | Yes | Yes | Positive | High | Fully Covered | trust_details_page.py | fill_trust_details() | test_preliminary_form_main.py | |
| SM10 | Land Certificate | Radio Selection | Verify Plot Type radio button selection | Validate plot type selection triggers dynamic form | Land page loaded | 1. Select plot type radio | plot_type (Yes/No) | Dynamic form loads based on selection | Yes | Yes | Yes | Positive | High | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | wait_for_timeout for dynamic load |
| S19 | Land Certificate | Radio Selection | Verify Type of Land radio selection | Validate Owned/Leased selection | Dynamic form loaded | 1. Select land type | Type_of_Land | Radio selected, form adjusts | No | Yes | Yes | Positive | High | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| S20 | Land Certificate | Dropdown Selection | Verify Area Unit dropdown | Validate area unit selection | Form fields visible | 1. Wait for visibility 2. Select unit | area_unit (Square Meter) | Dropdown shows selected unit | No | Yes | Yes | Positive | High | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | locator("#land_unit_0") |
| R11 | Land Certificate | Form Filling | Verify Land Area numeric input | Validate land area field | Form loaded | 1. Fill land area | land_area | Field accepts numeric value | No | No | Yes | Positive | Medium | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| R12 | Land Certificate | Form Filling | Verify Situated In field | Validate situated in input | Form loaded | 1. Fill situated in | situated_in | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| R13 | Land Certificate | Form Filling | Verify Situated At field | Validate situated at input | Form loaded | 1. Fill situated at | situated_at | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| R14 | Land Certificate | Form Filling | Verify Land Owned By field | Validate ownership field | Form loaded | 1. Fill land owned by | land_owned_by | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| S21 | Land Certificate | Dropdown Selection | Verify Land Title Document dropdown | Validate title document selection | Form loaded | 1. Select land title document | land_title_document | Dropdown shows selection | No | Yes | Yes | Positive | High | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| R15 | Land Certificate | Conditional Logic | Verify Sale Deed conditional form | Validate conditional fields appear for Sale Deed | land_title_document = Sale Deed | 1. Select Sale Deed 2. Wait for field 3. Select favor | sale_deed_favor | Conditional field appears and accepts selection | No | No | Yes | Positive | High | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | if condition checks document type |
| R16 | Land Certificate | Form Filling | Verify Registration Details field | Validate registration details input | Form loaded | 1. Fill registration details | registration_details | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| R17 | Land Certificate | Form Filling | Verify Seller Name (Executed By) field | Validate seller name input | Form loaded | 1. Fill seller name | seller_name | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| R18 | Land Certificate | Form Filling | Verify Registration Office Details field | Validate office details input | Form loaded | 1. Fill office details | registration_office_details | Field accepts value | No | No | Yes | Positive | Medium | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| R19 | Land Certificate | Date Input | Verify Land Document Date field | Validate date input field | Form loaded | 1. Click date field 2. Fill date | land_document_date | Date field accepts value | No | No | Yes | Positive | Medium | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | Uses fill() on textbox |
| S22 | Land Certificate | Navigation | Verify Next button submits land details | Validate land form submission | All fields filled | 1. Click Next | None | Navigates to Upload Documents page | No | Yes | Yes | Positive | High | Fully Covered | land_certificate_page.py | fill_land_details() | test_preliminary_form_main.py | |
| SM11 | Upload Documents | File Upload | Verify NOC Document upload | Validate NOC file upload via file chooser | Upload page loaded | 1. Click NOC upload area 2. Set file | LandCertificate.pdf | File uploaded successfully | Yes | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | Uses expect_file_chooser |
| S23 | Upload Documents | File Upload | Verify Certificate of Land upload | Validate land certificate upload | Upload page loaded | 1. Click upload area 2. Set file | LandCertificate.pdf | File uploaded | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | Uses .dz-message locator |
| S24 | Upload Documents | File Upload | Verify Trust/Society Document upload | Validate trust document upload | Upload page loaded | 1. Click trust upload 2. Set file | LandCertificate.pdf | File uploaded | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | locator("#trust") |
| S25 | Upload Documents | File Upload | Verify Land Ownership Document upload | Validate land ownership upload | Upload page loaded | 1. Click land upload 2. Set file | LandCertificate.pdf | File uploaded | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | locator("#land") |
| S26 | Upload Documents | File Upload | Verify School Image upload | Validate school image upload | Upload page loaded | 1. Click image upload 2. Set file | LandCertificate.pdf | File uploaded | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | locator("#school_image") |
| R20 | Upload Documents | Form Filling | Verify Comments text field | Validate comments input | Upload page loaded | 1. Fill comments | comments | Field accepts text | No | No | Yes | Positive | Medium | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | |
| S27 | Upload Documents | Radio/Checkbox | Verify Affiliation Type selection | Validate affiliation type radio | Upload page loaded | 1. Check affiliation type | affiliation_type | Radio checked | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | Uses force=True |
| R21 | Upload Documents | Checkbox | Verify composite verification checkbox | Validate checkbox check | Upload page loaded | 1. Check verify_composite | None | Checkbox checked | No | No | Yes | Positive | Medium | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | force=True |
| R22 | Upload Documents | Checkbox | Verify information verification checkbox | Validate checkbox check | Upload page loaded | 1. Check verify | None | Checkbox checked | No | No | Yes | Positive | Medium | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | force=True |
| SM12 | Upload Documents | Navigation | Verify Proceed to Payment button | Validate payment navigation | All uploads and checkboxes done | 1. Click Proceed to Payment | None | Redirects to payment page | Yes | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | force=True click |
| SM13 | Payment | Page Navigation | Verify payment page URL redirect | Validate correct payment URL | Proceed to Payment clicked | 1. Wait for payment URL pattern | None | URL contains /payment/ | Yes | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | wait_for_url("**/payment**") |
| S28 | Payment | Button Click | Verify Pay Rs button click | Validate Pay button initiates payment flow | Payment page loaded | 1. Click Pay Rs button | None | Payment Details page appears | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | |
| S29 | Payment | Validation | Verify Payment Details heading visible | Validate payment page content | Pay button clicked | 1. Check heading visibility | None | "Payment Details" heading visible | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | expect().to_be_visible() |
| SM14 | Payment | Gateway Selection | Verify ICICI Bank gateway selection | Validate payment gateway selection | Payment Details visible | 1. Click ICICI Bank image | None | ICICI Bank selected | Yes | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | Includes JS radio selection fallback |
| SM15 | Payment | Payment Initiation | Verify Proceed to Pay Rs button click | Validate payment initiation | Gateway selected | 1. Enable button via JS 2. Click 3. Call initiatePayment() | None | Payment gateway iframe loads | Yes | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | JS removes disabled attribute |
| S30 | Payment | iframe Interaction | Verify Show QR button in payment iframe | Validate QR code display | Payment iframe loaded | 1. Access iframe 2. Click Show QR | None | QR code section appears | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | content_frame access |
| S31 | Payment | iframe Interaction | Verify final pay button in iframe | Validate fee bearer CTA click | QR shown | 1. Access iframe 2. Click fee-bearer-cta | None | Payment processing initiated | No | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | get_by_test_id |
| SM16 | Payment | Validation | Verify Transaction Successful message | Validate payment success confirmation | Payment processed | 1. Wait 2. Check success text | None | "Transaction Successful!" text visible | Yes | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | expect with 30000ms timeout |
| SM17 | Payment | Navigation | Verify Go to Homepage link after payment | Validate post-payment navigation | Transaction successful | 1. Click Go to Homepage | None | Redirects to school_view page | Yes | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | |
| SM18 | Payment | Validation | Verify final URL after complete flow | Validate end-to-end URL | Homepage link clicked | 1. Wait for URL | None | URL contains /school_view | Yes | Yes | Yes | Positive | High | Fully Covered | upload_documents_page.py | upload_documents() | test_preliminary_form_main.py | wait_for_url with 30000ms |

---

## SUMMARY 1 - Test Suite Classification

| Metric | Count |
|--------|-------|
| Total Smoke Test Cases | 18 |
| Total Sanity Test Cases | 46 |
| Total Regression Test Cases | 56 |
| **Total Unique Test Cases** | **56** |

---

## SUMMARY 2 - Scenario Type

| Metric | Count |
|--------|-------|
| Total Positive Test Cases | 55 |
| Total Negative Test Cases | 1 |
| Total Boundary Test Cases | 0 |

---

## SUMMARY 3 - Automation Coverage

| Metric | Count |
|--------|-------|
| Fully Covered | 56 |
| Partially Covered | 0 |
| Not Covered | 0 |
| **Automation Coverage Percentage** | **100%** |

---

## AUTOMATION GAPS

The following validations are NOT covered by the current automation:

| # | Gap Description | Type | Priority |
|---|-----------------|------|----------|
| 1 | Blank mandatory field submission (no negative testing for empty fields) | Negative | High |
| 2 | Invalid mobile number format validation | Negative | High |
| 3 | Invalid email format validation | Negative | High |
| 4 | Invalid file type upload rejection | Negative | High |
| 5 | Maximum file size upload limit validation | Boundary | Medium |
| 6 | Minimum character length for text fields | Boundary | Medium |
| 7 | Maximum character length for text fields | Boundary | Medium |
| 8 | Special characters in name fields validation | Negative | Medium |
| 9 | Invalid UDISE number format | Negative | Medium |
| 10 | Invalid ZIP/PIN code format | Negative | Medium |
| 11 | Back button navigation between steps | Positive | Medium |
| 12 | Session timeout handling | Negative | Medium |
| 13 | Concurrent login from multiple browsers | Negative | Low |
| 14 | Payment failure/cancellation handling | Negative | High |
| 15 | Network interruption during upload | Negative | Low |

---

## NOTES

- All 56 test cases are derived from actual implemented automation code
- The framework follows Data-Driven approach with Excel test data
- Page Object Model ensures maintainability and reusability
- The E2E flow is parametrized by school_id for multi-school execution
- Password entry requires manual intervention (page.pause())
- Payment button handling uses JavaScript injection for disabled button
- Date pickers use both UI interaction (NOC) and JS injection (Trust)
