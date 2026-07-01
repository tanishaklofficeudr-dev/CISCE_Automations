# CISCE E-Affiliation Automation - Commands Reference

python -m pytest tests/test_preliminary_form_main.py --headed -v --alluredir=allure-results


## Run Tests

### Run Sanity and Regression Suite (20 test cases)
python -m pytest tests/test_sanity_regression_suite.py -v --alluredir=allure-results

### Run E2E Preliminary Form (actual browser automation)
python -m pytest tests/test_preliminary_form_main.py --headed -v --alluredir=allure-results

### Run Only Sanity Tests
python -m pytest tests/test_sanity_regression_suite.py -m sanity -v --alluredir=allure-results

### Run Only Regression Tests
python -m pytest tests/test_sanity_regression_suite.py -m regression -v --alluredir=allure-results

---

## Allure Report

### View Report (fixed port 9090)
allure open allure-report --port 9090

### Export as Single HTML (to share with manager)
allure generate allure-results --single-file --clean -o allure-single-report
# File location: allure-single-report/index.html

### Export as Zip
Compress-Archive -Path allure-report/* -DestinationPath CISCE_Test_Report.zip -Force

---

## Clean / Reset

### Clean Allure Data (removes all history and trend)
Remove-Item -Recurse -Force allure-results, allure-report -ErrorAction SilentlyContinue
New-Item -ItemType Directory allure-results | Out-Null

### Clean Pytest Cache
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue

---

## Notes
- Always run from the project root folder (not from tests/)
- Trend chart needs at least 2 runs to show data
- History is preserved automatically between runs (no manual copy needed)
- Timestamps appear on trend x-axis after each run
- Report is auto-generated after every pytest run
- Excel report saves to: reports/Preliminary_Form_Test_Report_<timestamp>.xlsx
- Allure report is at: http://localhost:9090
