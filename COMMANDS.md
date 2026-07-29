# CISCE E-Affiliation Automation - Commands Reference

python -m pytest tests/test_preliminary_form_main.py --headed -v --alluredir=allure-results

# NEGATIVE 
# SCHOOL_DETAILS
python -m pytest tests/test_school_details_validation.py -v --headed --alluredir=allure-results


# TO REMOVE THE CACHE DATA - 
Remove-Item -Recurse -Force allure-results, allure-report -ErrorAction SilentlyContinue; New-Item -ItemType Directory allure-results | Out-Null

#  To open the Report
allure open allure-report --port 9090

# TO GENERATE A SINGLE FILE 
allure generate allure-results --single-file --clean -o allure-single-report

# TO CLEAN OLD RECORDS
# allure generate allure-results --clean -o allure-report
---------------------------------------------------------------------------------
# All School Details regression
python -m pytest tests/regression/school_details/ -v --headed --alluredir=allure-results

# Only format validation
python -m pytest tests/regression/school_details/negative/ -v --headed --alluredir=allure-results

# Only positive
python -m pytest tests/regression/school_details/positive/ -v --headed --alluredir=allure-results

# Only boundary
python -m pytest tests/regression/school_details/boundary/ -v --headed --alluredir=allure-results

# Only required field validation
python -m pytest tests/regression/school_details/validation/ -v --headed --alluredir=allure-results

# TO RUN THE LAST FAILED CASES
# python -m pytest --lf -v --headed 

# regression/payment_gateway
# -- HDFC Bank --
# python -m pytest tests/regression/payment_gateway/ -v --headed -k "POS_001"  
# -- ICICI Bank --   
# python -m pytest tests/regression/payment_gateway/ -v --headed -k "POS_002" 
# -- Federal Bank --
# python -m pytest tests/regression/payment_gateway/ -v --headed -k "POS_003"


# SANITY TEST CASE -
python -m pytest tests/regression/ -m sanity -v --headed --alluredir=allure-results



---------------------------------------------------------------------------------









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
