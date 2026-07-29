"""
NOC Details — Positive Regression Tests
==========================================
Validates form submits successfully with valid NOC data combinations.

Data Source: test_data/negative/Validation_Data.xlsx → "NOC_Positive"
Page Object: pages/noc_details_page.py
Fixture: noc_ready_page (conftest.py)
"""

import pytest
import allure

from pages.noc_details_page import NOCDetailsPage
from utils.excel_reader import ExcelReader
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


# ============================================================================
# AUTO SCREENSHOT ON FAILURE
# ============================================================================

@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    """Capture and attach screenshot to Allure on test failure."""
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("noc_ready_page")
        if page:
            try:
                screenshot_path = ScreenshotUtil.take_screenshot(page, request.node.name[:50])
                if screenshot_path:
                    allure.attach.file(
                        screenshot_path,
                        name=f"Screenshot_{request.node.name[:50]}",
                        attachment_type=allure.attachment_type.PNG,
                    )
            except Exception:
                pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the request node for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ============================================================================
# DATA LOADING
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_positive_scenarios = [
    row for row in _excel.get_sheet_data("NOC_Positive")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# POSITIVE TESTS — Valid Form Submission
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("NOC Details")
@allure.sub_suite("Positive")
@allure.feature("Successful NOC Details Submission")
@allure.story("Positive Scenarios")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.noc_details
@pytest.mark.parametrize(
    "scenario",
    _positive_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_noc_positive_submission(noc_ready_page, scenario):
    """
    Verify NOC Details form submits successfully with valid data.
    """
    page = noc_ready_page
    noc_page = NOCDetailsPage(page)

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Authority: {scenario['noc_authority']}\n"
        f"Designation: {scenario['designation']}\n"
        f"Office Address: {scenario['office_address']}\n"
        f"Country Value: {scenario['country_value']}\n"
        f"State Value: {scenario['state_value']}\n"
        f"Reference: {scenario['noc_reference_number']}\n"
        f"Date: {scenario['noc_date']}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "High"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "positive", "noc_details")

    test_data = {
        "noc_authority": scenario["noc_authority"],
        "designation": scenario["designation"],
        "office_address": scenario["office_address"],
        "country_value": str(scenario["country_value"]),
        "state_value": str(scenario["state_value"]),
        "noc_reference_number": scenario["noc_reference_number"],
        "noc_date": scenario["noc_date"],
    }

    with allure.step(f"Fill valid NOC data: {scenario['noc_authority'][:30]}"):
        url_before = page.url
        noc_page.fill_partial_details(test_data, skip_fields=[])

    with allure.step("Verify form submitted (navigated to Trust/Society Details)"):
        page.wait_for_timeout(2000)
        ValidationHelper.assert_form_submitted(page, url_before)

    with allure.step("Navigate back to NOC Details for next test"):
        page.get_by_text("NOC Details", exact=False).first.click()
        page.wait_for_timeout(2000)
