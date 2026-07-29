"""
Address Details — Boundary Value Tests
========================================
Tests field character min/max limits for address line and PIN code.
Each test overwrites existing values — independently executable.

Data Source: test_data/negative/Validation_Data.xlsx → "Address_Boundary"
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
            try:
                screenshot_path = ScreenshotUtil.take_screenshot(page, request.node.name[:50])
                if screenshot_path:
                    allure.attach.file(
                        screenshot_path,
                        name=f"Screenshot_{request.node.name[:50]}",
                        attachment_type=allure.attachment_type.PNG,
                    )
            except Exception:
                pass  # Page may be closed after timeout


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

_boundary_scenarios = [
    row for row in _excel.get_sheet_data("Address_Boundary")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# BOUNDARY TESTS — Field Length Limits
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Address Details")
@allure.sub_suite("Boundary")
@allure.feature("Address Details Validation")
@allure.story("Boundary Value Validation")
@pytest.mark.regression
@pytest.mark.address_details
@pytest.mark.boundary
@pytest.mark.parametrize(
    "scenario",
    _boundary_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_address_boundary(address_ready_page, scenario):
    """
    Verify field length boundaries are handled correctly.
    Overwrites existing saved values — independently executable.
    """
    page = address_ready_page
    address_page = AddressDetailsPage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value", "")
    expected_outcome = scenario.get("expected_outcome", "ACCEPT")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Field: {field_name}\n"
        f"Value length: {len(str(field_value or ''))}\n"
        f"Expected outcome: {expected_outcome}\n"
        f"Message: {scenario.get('expected_message', '')}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "High"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "boundary", "address_details")

    with allure.step(f"Overwrite '{field_name}' with boundary value ({len(str(field_value or ''))} chars)"):
        # Overwrite only the target field — leave others with saved values
        if field_name == "address_line_1":
            address_page.fill_address_line(str(field_value))
        elif field_name == "zip_pin":
            address_page.fill_zip(str(field_value))

    with allure.step("Click Next to submit"):
        url_before = page.url
        address_page.click_next()
        page.wait_for_timeout(2000)

    with allure.step(f"Verify outcome: {expected_outcome}"):
        # Check if NOC Details appeared (form submitted)
        form_navigated = False
        try:
            noc_tab = page.locator("#TabNOCDetails")
            if noc_tab.count() > 0 and noc_tab.is_visible():
                form_navigated = True
        except Exception:
            pass

        if expected_outcome == "ACCEPT":
            if form_navigated:
                allure.attach(
                    "PASS: Boundary value accepted — form navigated to NOC Details.",
                    name="Boundary Result",
                    attachment_type=allure.attachment_type.TEXT,
                )
                # Navigate back for next test
                with allure.step("Navigate back to Address Details"):
                    page.get_by_text("Address Details", exact=False).first.click()
                    page.wait_for_timeout(2000)
            else:
                errors = ValidationHelper.get_all_errors(page)
                pytest.fail(
                    f"Expected ACCEPT but form was blocked. Errors: {errors}"
                )

        elif expected_outcome == "REJECT":
            if not form_navigated:
                errors = ValidationHelper.get_all_errors(page)
                allure.attach(
                    f"PASS: Boundary value rejected. Errors: {errors}",
                    name="Boundary Result",
                    attachment_type=allure.attachment_type.TEXT,
                )
            else:
                # Navigate back
                page.get_by_text("Address Details", exact=False).first.click()
                page.wait_for_timeout(2000)
                pytest.fail(
                    f"Expected REJECT but form accepted value of length {len(str(field_value))}."
                )
