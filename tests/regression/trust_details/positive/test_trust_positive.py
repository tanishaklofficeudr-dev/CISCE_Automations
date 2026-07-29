"""
Trust/Society/Company Details — Positive Regression Tests
============================================================
Validates form submits successfully with valid trust data combinations.

Data Source: test_data/negative/Validation_Data.xlsx -> "Trust_Positive"
Page Object: pages/trust_details_page.py
Fixture: trust_ready_page (conftest.py)
"""

import pytest
import allure

from pages.trust_details_page import TrustDetailsPage
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
        page = request.node.funcargs.get("trust_ready_page")
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
    row for row in _excel.get_sheet_data("Trust_Positive")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# POSITIVE TESTS — Valid Form Submission
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Trust Details")
@allure.sub_suite("Positive")
@allure.feature("Successful Trust Details Submission")
@allure.story("Positive Scenarios")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.trust_details
@pytest.mark.parametrize(
    "scenario",
    _positive_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_trust_positive_submission(trust_ready_page, scenario):
    """
    Verify Trust Details form submits successfully with valid data.
    """
    page = trust_ready_page
    trust_page = TrustDetailsPage(page)

    allure.dynamic.title(f"{scenario['scenario_id']} - {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Ownership: {scenario['ownership_type']}\n"
        f"Name: {scenario['trust_name']}\n"
        f"Est Date: {scenario['establishment_date']}\n"
        f"Reg Date: {scenario['registration_date']}\n"
        f"Reg Number: {scenario['registration_number']}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "High"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "positive", "trust_details")

    test_data = {
        "ownership_type": scenario["ownership_type"],
        "trust_name": scenario["trust_name"],
        "establishment_date": str(scenario["establishment_date"]),
        "registration_date": str(scenario["registration_date"]),
        "registration_number": str(scenario["registration_number"]),
    }

    with allure.step(f"Fill valid trust data: {scenario['ownership_type']} - {scenario['trust_name'][:30]}"):
        trust_page.fill_partial_details(test_data, skip_fields=[])

    with allure.step("Verify form submitted (navigated to Certificate of Land)"):
        page.wait_for_timeout(2000)
        ValidationHelper.assert_form_submitted(page, page.url)

    with allure.step("Navigate back to Trust Details for next test"):
        page.get_by_text("Trust /Society /Company", exact=False).first.click()
        page.wait_for_timeout(2000)
