# 🏫 CISCE Preliminary Form Automation Framework

A Playwright + Python automation framework developed for the **CISCE E-Affiliation – Preliminary Form**. The framework automates end-to-end business workflows along with Regression, Sanity, and Authentication test suites using the Page Object Model (POM) and Data-Driven Testing approach.

---

# 📌 Project Overview

This automation framework covers the complete Preliminary Form workflow, including:

- Registration
- Login
- School Details
- Address Details
- NOC Details
- Trust Details
- Certificate of Land
- Upload Documents
- Payment Gateway
- End-to-End Preliminary Form Submission

The framework is designed to support:

- ✅ End-to-End Automation
- ✅ Regression Testing
- ✅ Sanity Testing
- ✅ Data-Driven Testing
- ✅ Allure Reporting
- ✅ HTML Reporting
- ✅ Screenshot & Video Capture
- ✅ CI/CD Ready Architecture

---

# 📊 Automation Coverage

| Test Suite | Count |
|------------|------:|
| Regression Tests | 155 |
| Sanity Tests | 25 |
| End-to-End Tests | 1 |
| **Total Automated Tests** | **156** |

> *(Update these counts whenever new test cases are added.)*

---

# 🛠 Tech Stack

- Python 3.x
- Playwright
- Pytest
- Allure Report
- HTML Report
- OpenPyXL
- Page Object Model (POM)
- Data Driven Framework

---

# 📁 Project Structure

```text
.
├── pages/                  # Page Object Model classes
├── tests/
│   ├── regression/
│   ├── sanity/
│   └── test_preliminary_form_main.py
├── utils/                  # Utility classes
├── test_data/              # Excel data & upload documents
├── reports/                # HTML Reports
├── allure-results/         # Allure execution results
├── allure-report/          # Generated Allure report
├── screenshots/            # Failure screenshots
├── videos/                 # Playwright videos
├── traces/                 # Playwright traces
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# ⚙️ Project Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Preliminary_Form_School_End
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Install Playwright Browsers

```bash
playwright install
```

---

# ▶️ Test Execution

## Run Complete Regression Suite

```bash
python -m pytest tests/regression/ -v --headed
```

---

## Run Sanity Suite

```bash
python -m pytest tests/regression/ -m sanity -v --headed
```

---

## Run End-to-End Test

```bash
python -m pytest tests/test_preliminary_form_main.py -v --headed
```

---

## Run with Slow Motion

```bash
python -m pytest tests/test_preliminary_form_main.py -v --headed --slowmo=1000
```

---

# 📄 Generate HTML Report

```bash
python -m pytest --html=reports/report.html --self-contained-html
```

Report Location

```
reports/report.html
```

---

# 📊 Generate Allure Report

## Execute Tests

```bash
python -m pytest --alluredir=allure-results
```

Generate Report

```bash
allure generate allure-results --clean -o allure-report
```

Open Report

```bash
allure open allure-report
```

---

# 📸 Screenshots

Capture screenshots on failures

```bash
pytest --screenshot=only-on-failure
```

Location

```
screenshots/
```

---

# 🎥 Video Recording

```bash
pytest --video=on
```

Location

```
videos/
```

---

# 🔍 Playwright Trace

```bash
pytest --tracing=on
```

Location

```
traces/
```

Open Trace Viewer

```bash
playwright show-trace traces/<trace-file>.zip
```

---

# 📈 Reports

The framework supports:

- HTML Reports
- Allure Reports
- Screenshots
- Video Recording
- Playwright Trace
- Pytest Logs

---

# 🧪 Framework Features

- Page Object Model (POM)
- Data-Driven Testing
- Excel-based Test Data
- Reusable Fixtures
- Custom Utilities
- Retry Mechanism
- Validation Helpers
- Screenshot Utility
- HTML Reporting
- Allure Reporting
- Playwright Trace Support

---

# 🚀 Execution Order

Recommended execution sequence:

1. Authentication Tests
2. Regression Tests
3. Sanity Tests
4. End-to-End Test
5. Payment Gateway Tests (Execute Last)

---

# 📌 Notes

- Activate the virtual environment before running tests.
- Install Playwright browsers before the first execution.
- Payment Gateway tests should be executed after all other regression tests.
- Update the Excel test data before execution if required.
- Review Allure and HTML reports after each execution.

---

# 👩‍💻 Developed By

**Tanisha Maratha**

QA Automation Engineer

Playwright • Python • Pytest

---

# 📄 License

This repository is intended for internal project use.
