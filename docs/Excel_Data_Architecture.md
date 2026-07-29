# CISCE Preliminary Affiliation Portal
# Excel Data Architecture for Regression & Sanity Automation

---

# CURRENT STATE (LOCKED — DO NOT MODIFY)

| File | Location | Purpose | Sheets |
|------|----------|---------|--------|
| Data_Schools.xlsx | test_data/ | E2E positive path data | Master, Registration, Login, School_Details, Address_Details, NOC_Details, Trust_Details, Land_Certificate, Upload_Documents |
| LandCertificate.pdf | test_data/ | Upload test file | N/A |

**Rule:** These files are consumed by `test_preliminary_form_main.py` and must NEVER be modified.

---

# NEW DATA ARCHITECTURE

## Design Principles

1. **One file per concern** — E2E data stays separate from validation data
2. **Sheets per scenario type** — Positive, Negative, Boundary in separate sheets
3. **Common data sheet** — Shared valid data for fixtures that need to navigate to a specific page
4. **Execute column** — Every row has an `execute` flag (Yes/No) for selective runs
5. **Expected result column** — Every negative/boundary row specifies what should happen
6. **Consumed by existing ExcelReader** — No new reader needed; same `get_sheet_data()` method works

---

# FILE 1: test_data/negative/Validation_Data.xlsx

**Purpose:** All negative and boundary test data for every module

---

## Sheet: Common_Login

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | COMMON_01 |
| mobile_number | Valid mobile for pre-authentication | 9876543210 |
| password | Valid password | ******* |
| description | What this common data is for | Default login for fixtures |

**Usage:** Pre-authenticated fixtures read this sheet to login before testing specific pages.

---

## Sheet: Registration_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | REG_NEG_01 |
| execute | Yes/No flag | Yes |
| scenario_description | What we're testing | Blank mobile number |
| mobile_number | Value to enter (can be blank) | (empty) |
| email | Value to enter | test@school.com |
| expected_error | Expected validation message | Mobile number is required |
| scenario_type | Negative / Boundary | Negative |
| priority | High / Medium / Low | High |

**Sample Rows:**

| scenario_id | execute | scenario_description | mobile_number | email | expected_error | scenario_type |
|---|---|---|---|---|---|---|
| REG_NEG_01 | Yes | Blank mobile | | test@school.com | Mobile number is required | Negative |
| REG_NEG_02 | Yes | Alphabets in mobile | abcdefghij | test@school.com | Invalid mobile number | Negative |
| REG_NEG_03 | Yes | Special chars in mobile | @#$%^&*()! | test@school.com | Invalid mobile number | Negative |
| REG_NEG_04 | Yes | Blank email | 9876543210 | | Email is required | Negative |
| REG_NEG_05 | Yes | Invalid email - no @ | 9876543210 | schoolexample.com | Invalid email format | Negative |
| REG_NEG_06 | Yes | Invalid email - no domain | 9876543210 | school@ | Invalid email format | Negative |
| REG_BND_01 | Yes | Mobile 9 digits | 987654321 | test@school.com | Must be 10 digits | Boundary |
| REG_BND_02 | Yes | Mobile 11 digits | 98765432101 | test@school.com | Must be 10 digits | Boundary |
| REG_BND_03 | Yes | Email 256 chars | 9876543210 | aaa...@domain.com | Field limit exceeded | Boundary |

---

## Sheet: Login_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | LOGIN_NEG_01 |
| execute | Yes/No | Yes |
| scenario_description | What we're testing | Wrong password |
| mobile_number | Value to enter | 9876543210 |
| password | Value to enter | wrongpass123 |
| expected_error | Expected error text | Invalid credentials |
| scenario_type | Negative / Boundary | Negative |

**Sample Rows:**

| scenario_id | execute | scenario_description | mobile_number | password | expected_error | scenario_type |
|---|---|---|---|---|---|---|
| LOGIN_NEG_01 | Yes | Unregistered mobile | 1111111111 | password | Invalid credentials | Negative |
| LOGIN_NEG_02 | Yes | Wrong password | 9876543210 | wrongpass | Invalid credentials | Negative |
| LOGIN_NEG_03 | Yes | Blank mobile | | password | Mobile required | Negative |
| LOGIN_NEG_04 | Yes | Blank password | 9876543210 | | Password required | Negative |
| LOGIN_NEG_05 | Yes | Both blank | | | Mobile required | Negative |

---

## Sheet: School_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | SCH_NEG_01 |
| execute | Yes/No | Yes |
| scenario_description | What we're testing | Blank school name |
| field_name | Which field is invalid | school_name |
| field_value | Invalid value to enter | (empty) |
| other_fields_valid | Fill other fields with valid data? | Yes |
| expected_error | Expected validation | School name is required |
| scenario_type | Negative / Boundary | Negative |

**Sample Rows:**

| scenario_id | execute | scenario_description | field_name | field_value | expected_error | scenario_type |
|---|---|---|---|---|---|---|
| SCH_NEG_01 | Yes | Blank school name | school_name | | School name required | Negative |
| SCH_NEG_02 | Yes | Only special chars | school_name | @#$%^& | Invalid school name | Negative |
| SCH_NEG_03 | Yes | Only numbers | school_name | 123456 | Invalid school name | Negative |
| SCH_NEG_04 | Yes | Classification not selected | school_classification | (not selected) | Classification required | Negative |
| SCH_NEG_05 | Yes | Type not selected | school_type | (not selected) | School type required | Negative |
| SCH_NEG_06 | Yes | Category not selected | school_category | (not selected) | Category required | Negative |
| SCH_NEG_07 | Yes | UDISE alphabets | udise_number | abcdefgh | Invalid UDISE | Negative |
| SCH_BND_01 | Yes | School name 200 chars | school_name | (200 char string) | Field limit exceeded | Boundary |
| SCH_BND_02 | Yes | UDISE 10 digits | udise_number | 1234567890 | (depends on requirement) | Boundary |

---

## Sheet: Address_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | ADDR_NEG_01 |
| execute | Yes/No | Yes |
| scenario_description | What we're testing | Blank address |
| field_name | Which field is invalid | address_line_1 |
| field_value | Invalid value | (empty) |
| expected_error | Expected validation | Address is required |
| scenario_type | Negative / Boundary | Negative |

**Sample Rows:**

| scenario_id | execute | scenario_description | field_name | field_value | expected_error | scenario_type |
|---|---|---|---|---|---|---|
| ADDR_NEG_01 | Yes | Blank address | address_line_1 | | Address required | Negative |
| ADDR_NEG_02 | Yes | Country not selected | country | (not selected) | Country required | Negative |
| ADDR_NEG_03 | Yes | State not selected | state | (not selected) | State required | Negative |
| ADDR_NEG_04 | Yes | Non-numeric PIN | zip_pin | abc123 | Invalid PIN | Negative |
| ADDR_NEG_05 | Yes | Locality not selected | locality_type | (not selected) | Locality required | Negative |
| ADDR_BND_01 | Yes | PIN 5 digits | zip_pin | 12345 | Must be 6 digits | Boundary |
| ADDR_BND_02 | Yes | PIN 7 digits | zip_pin | 1234567 | Must be 6 digits | Boundary |
| ADDR_BND_03 | Yes | Address 500 chars | address_line_1 | (500 char string) | Field limit | Boundary |

---

## Sheet: NOC_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | NOC_NEG_01 |
| execute | Yes/No | Yes |
| scenario_description | What we're testing | Blank authority |
| field_name | Which field is invalid | noc_issuing_authority |
| field_value | Invalid value | (empty) |
| expected_error | Expected validation | Authority is required |
| scenario_type | Negative / Boundary | Negative |

**Sample Rows:**

| scenario_id | execute | scenario_description | field_name | field_value | expected_error | scenario_type |
|---|---|---|---|---|---|---|
| NOC_NEG_01 | Yes | Blank authority | noc_issuing_authority | | Authority required | Negative |
| NOC_NEG_02 | Yes | Blank designation | designation | | Designation required | Negative |
| NOC_NEG_03 | Yes | Blank office address | office_address | | Address required | Negative |
| NOC_NEG_04 | Yes | Blank reference number | noc_reference_number | | Reference required | Negative |
| NOC_NEG_05 | Yes | Future NOC date | noc_date | 15/12/2027 | Date cannot be future | Negative |
| NOC_NEG_06 | Yes | No date selected | noc_date | (not selected) | Date required | Negative |

---

## Sheet: Trust_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | TRUST_NEG_01 |
| execute | Yes/No | Yes |
| scenario_description | What we're testing | Ownership not selected |
| field_name | Which field is invalid | ownership_type |
| field_value | Invalid value | (not selected) |
| expected_error | Expected validation | Ownership type required |
| scenario_type | Negative / Boundary | Negative |

**Sample Rows:**

| scenario_id | execute | scenario_description | field_name | field_value | expected_error | scenario_type |
|---|---|---|---|---|---|---|
| TRUST_NEG_01 | Yes | Ownership not selected | ownership_type | (not selected) | Type required | Negative |
| TRUST_NEG_02 | Yes | Blank trust name | trust_name | | Name required | Negative |
| TRUST_NEG_03 | Yes | Future establishment date | establishment_date | 01/01/2028 | Cannot be future | Negative |
| TRUST_NEG_04 | Yes | Reg date before est date | registration_date | 01/01/2018 | Cannot precede establishment | Negative |
| TRUST_NEG_05 | Yes | Blank registration number | registration_number | | Number required | Negative |
| TRUST_NEG_06 | Yes | No establishment date | establishment_date | (not set) | Date required | Negative |

---

## Sheet: Land_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | LAND_NEG_01 |
| execute | Yes/No | Yes |
| scenario_description | What we're testing | Zero area |
| field_name | Which field is invalid | land_area |
| field_value | Invalid value | 0 |
| expected_error | Expected validation | Area must be positive |
| scenario_type | Negative / Boundary | Negative |

**Sample Rows:**

| scenario_id | execute | scenario_description | field_name | field_value | expected_error | scenario_type |
|---|---|---|---|---|---|---|
| LAND_NEG_01 | Yes | Zero land area | land_area | 0 | Must be positive | Negative |
| LAND_NEG_02 | Yes | Negative land area | land_area | -100 | Must be positive | Negative |
| LAND_NEG_03 | Yes | Non-numeric area | land_area | abc | Invalid number | Negative |
| LAND_NEG_04 | Yes | Area unit not selected | area_unit | (not selected) | Unit required | Negative |
| LAND_NEG_05 | Yes | Future document date | land_document_date | 01/01/2028 | Cannot be future | Negative |
| LAND_NEG_06 | Yes | All fields blank | ALL | | Multiple errors | Negative |

---

## Sheet: Upload_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | DOC_NEG_01 |
| execute | Yes/No | Yes |
| scenario_description | What we're testing | Missing NOC doc |
| missing_document | Which doc is skipped | noc |
| file_path | Path to invalid file (if applicable) | test_data/negative/test.exe |
| expected_error | Expected message | NOC document required |
| scenario_type | Negative / Boundary | Negative |

**Sample Rows:**

| scenario_id | execute | scenario_description | missing_document | file_path | expected_error | scenario_type |
|---|---|---|---|---|---|---|
| DOC_NEG_01 | Yes | NOC not uploaded | noc | | NOC required | Negative |
| DOC_NEG_02 | Yes | Land cert not uploaded | land_certificate | | Land cert required | Negative |
| DOC_NEG_03 | Yes | Invalid file type | noc | test_data/negative/test.exe | Invalid file type | Negative |
| DOC_NEG_04 | Yes | Affiliation not selected | affiliation_type | | Affiliation required | Negative |
| DOC_NEG_05 | Yes | Checkboxes unchecked | checkboxes | | Must agree to terms | Negative |
| DOC_BND_01 | Yes | File over 10MB | noc | test_data/negative/large.pdf | File too large | Boundary |

---

## Sheet: Payment_Negative

| Column | Purpose | Example |
|--------|---------|---------|
| scenario_id | Unique identifier | PAY_NEG_01 |
| execute | Yes/No | Yes |
| scenario_description | What we're testing | No gateway selected |
| gateway | Gateway to select (or blank) | (none) |
| expected_behavior | What should happen | Button stays disabled |
| scenario_type | Negative | Negative |

**Sample Rows:**

| scenario_id | execute | scenario_description | gateway | expected_behavior | scenario_type |
|---|---|---|---|---|---|
| PAY_NEG_01 | Yes | No gateway selected | (none) | Button disabled | Negative |
| PAY_NEG_02 | Yes | HDFC gateway selected | HDFC | Payment initiates | Positive |

---

# FILE 2: test_data/negative/test.exe (DUMMY FILE)

**Purpose:** A small dummy .exe file (0 bytes) used to test invalid file type upload rejection.

---

# FILE 3: test_data/negative/large_file.pdf (OPTIONAL)

**Purpose:** A PDF exceeding the upload size limit, used to test file size boundary.

---

# DATA CONSUMPTION ARCHITECTURE

## How Tests Consume Data

### Pattern 1: E2E Tests (EXISTING — unchanged)

```python
# test_preliminary_form_main.py (LOCKED)
excel = ExcelReader("test_data/Data_Schools.xlsx")
school_ids = excel.get_school_ids_to_execute()

@pytest.mark.parametrize("school_id", school_ids)
def test_preliminary_form(page, school_id):
    data = excel.get_row_by_school_id("Registration", school_id)
    RegistrationPage(page).register_school(data)
```

**Data file:** test_data/Data_Schools.xlsx
**Reader:** utils/excel_reader.py (existing `get_row_by_school_id`)

---

### Pattern 2: Negative Tests (NEW — same ExcelReader)

```python
# test_registration_validation.py (NEW)
validation_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")
scenarios = validation_excel.get_sheet_data("Registration_Negative")
active_scenarios = [s for s in scenarios if str(s["execute"]).lower() == "yes"]

@pytest.mark.parametrize("scenario", active_scenarios, ids=lambda s: s["scenario_id"])
@pytest.mark.regression
@pytest.mark.negative
def test_registration_negative(page, scenario):
    # Navigate to registration
    # Fill data from scenario["mobile_number"], scenario["email"]
    # Click Register
    # Assert scenario["expected_error"] is displayed
```

**Data file:** test_data/negative/Validation_Data.xlsx
**Reader:** Same `ExcelReader.get_sheet_data()` — no new utility needed

---

### Pattern 3: Field-Specific Negative Tests (NEW)

```python
# test_school_details_validation.py (NEW)
validation_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")
school_scenarios = validation_excel.get_sheet_data("School_Negative")
active = [s for s in school_scenarios if str(s["execute"]).lower() == "yes"]

@pytest.mark.parametrize("scenario", active, ids=lambda s: s["scenario_id"])
@pytest.mark.regression
def test_school_field_validation(school_details_ready_page, scenario):
    page = school_details_ready_page  # Pre-authenticated, on School Details
    # Fill invalid value from scenario["field_value"] into scenario["field_name"]
    # Click Next
    # Assert scenario["expected_error"] displayed
```

**Data file:** Same Validation_Data.xlsx, "School_Negative" sheet
**Fixture:** `school_details_ready_page` (pre-navigated)

---

### Pattern 4: Boundary Tests (NEW)

```python
# Within same test file or separate
boundary_scenarios = [s for s in active if s["scenario_type"] == "Boundary"]

@pytest.mark.parametrize("scenario", boundary_scenarios, ids=lambda s: s["scenario_id"])
@pytest.mark.boundary
def test_school_field_boundary(school_details_ready_page, scenario):
    # Same pattern as negative but filtered for Boundary type
```

**Data file:** Same sheet, filtered by `scenario_type == "Boundary"`

---

### Pattern 5: Common Login Data for Fixtures (NEW)

```python
# conftest.py (ADD fixture)
@pytest.fixture
def logged_in_page(page):
    common_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")
    login_data = common_excel.get_sheet_data("Common_Login")[0]
    # Login using login_data
    # Return page on dashboard
    return page
```

**Data file:** Validation_Data.xlsx, "Common_Login" sheet
**Used by:** All regression test fixtures

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  test_data/Data_Schools.xlsx (LOCKED)                       │
│  ├── Master          → E2E execution control                │
│  ├── Registration    → E2E positive data                    │
│  ├── Login           → E2E positive data                    │
│  ├── School_Details  → E2E positive data                    │
│  ├── Address_Details → E2E positive data                    │
│  ├── NOC_Details     → E2E positive data                    │
│  ├── Trust_Details   → E2E positive data                    │
│  ├── Land_Certificate→ E2E positive data                    │
│  └── Upload_Documents→ E2E positive data                    │
│                                                              │
│  test_data/negative/Validation_Data.xlsx (NEW)              │
│  ├── Common_Login        → Fixture authentication           │
│  ├── Registration_Negative → Negative reg tests             │
│  ├── Login_Negative      → Negative login tests             │
│  ├── School_Negative     → School validation tests          │
│  ├── Address_Negative    → Address validation tests         │
│  ├── NOC_Negative        → NOC validation tests             │
│  ├── Trust_Negative      → Trust validation tests           │
│  ├── Land_Negative       → Land validation tests            │
│  ├── Upload_Negative     → Upload validation tests          │
│  └── Payment_Negative    → Payment validation tests         │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    READER LAYER                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  utils/excel_reader.py (EXISTING — no change)               │
│  ├── get_sheet_data(sheet_name) → Returns all rows          │
│  ├── get_school_ids_to_execute() → E2E control              │
│  └── get_row_by_school_id(sheet, id) → Single row           │
│                                                              │
│  Usage in new tests:                                         │
│  ExcelReader("test_data/negative/Validation_Data.xlsx")     │
│  .get_sheet_data("Registration_Negative")                   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    TEST LAYER                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  test_preliminary_form_main.py → Data_Schools.xlsx          │
│  test_registration_validation.py → Validation_Data.xlsx     │
│  test_login_validation.py → Validation_Data.xlsx            │
│  test_school_details_validation.py → Validation_Data.xlsx   │
│  ...etc                                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# SUMMARY

| Aspect | Decision |
|--------|----------|
| New Excel files | 1 (Validation_Data.xlsx in test_data/negative/) |
| Sheets in new file | 10 |
| Existing Excel modified | NEVER |
| New reader utility needed | NO — existing ExcelReader works |
| Parametrization method | `@pytest.mark.parametrize` with `get_sheet_data()` filtered by `execute=Yes` |
| Data isolation | E2E data and validation data in separate files |
| Selective execution | `execute` column in every sheet |
| Expected results stored | In Excel (`expected_error` column) — not hardcoded in tests |
| Scenario classification | `scenario_type` column (Negative/Boundary) — used for marker filtering |
