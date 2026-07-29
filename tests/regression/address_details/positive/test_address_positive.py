"""
Address Details — Positive Regression Tests
=============================================
Validates form submits successfully with various valid address data.

Data Source: test_data/negative/Validation_Data.xlsx → "Address_Positive"
Page Object: pages/address_details_page.py
Fixture: address_ready_page (conftest.py)
"""

import pytest
import allure

from pages.address_details_page import AddressDetailsPage
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
        page = request.node.funcargs.get("address_ready_page")
        if page:
            screenshot_path = ScreenshotUtil.take_screenshot(page, request.node.name[:50])
            if screenshot_path:
                allure.attach.file(
                    screenshot_path,
                    name=f"Screenshot_{request.node.name[:50]}",
                    attachment_type=allure.attachment_type.PNG,
                )


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
    row for row in _excel.get_sheet_data("Address_Positive")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# POSITIVE TESTS — Valid Form Submission
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Address Details")
@allure.sub_suite("Positive")
@allure.feature("Address Details")
@allure.story("Valid Form Submission")
@pytest.mark.regression
@pytest.mark.address_details
@pytest.mark.positive
@pytest.mark.parametrize(
    "scenario",
    _positive_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_address_positive_submission(address_ready_page, scenario):
    """
    Verify Address Details form submits successfully with valid data.
    """
    page = address_ready_page
    address_page = AddressDetailsPage(page)

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Address: {scenario['address_line_1']}\n"
        f"Country: {scenario['country']}\n"
        f"State: {scenario['state']}\n"
        f"ZIP: {scenario['zip_pin']}\n"
        f"Locality: {scenario['locality_type']}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "High"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "positive", "address_details")

    test_data = {
        "address_line_1": scenario["address_line_1"],
        "country": scenario["country"],
        "state": scenario["state"],
        "district": scenario.get("district") or "",
        "city": scenario.get("city") or "",
        "zip_pin": str(scenario["zip_pin"]),
        "locality_type": scenario["locality_type"],
    }

    with allure.step(f"Fill valid address: {scenario['address_line_1'][:30]}..."):
        url_before = page.url
        address_page.fill_partial_details(test_data, skip_fields=[])

    with allure.step("Verify form submitted (navigated to NOC Details)"):
        page.wait_for_timeout(2000)
        ValidationHelper.assert_form_submitted(page, url_before)

    with allure.step("Navigate back to Address Details for next test"):
        page.get_by_text("Address Details", exact=False).first.click()
        page.wait_for_timeout(2000)
