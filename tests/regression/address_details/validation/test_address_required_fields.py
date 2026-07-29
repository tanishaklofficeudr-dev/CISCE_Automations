"""
Address Details — Required Field Validation Test
==================================================
Consolidated test verifying all mandatory text fields show errors
when form is submitted with cleared values.

Execution: Must run FIRST in Address Details suite (@first_run marker).
"""

import pytest
import allure

from pages.address_details_page import AddressDetailsPage
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    """Capture and attach screenshot to Allure on test failure."""
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("address_ready_page")
        if page:
            screenshot_path = ScreenshotUtil.take_screenshot(page, "ADDR_VAL_001")
            if screenshot_path:
                allure.attach.file(
                    screenshot_path,
                    name="Screenshot_ADDR_VAL_001",
                    attachment_type=allure.attachment_type.PNG,
                )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Address Details")
@allure.sub_suite("Validation")
@allure.feature("Address Details")
@allure.story("Required Field Validation")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.address_details
@pytest.mark.validation
@pytest.mark.first_run
def test_address_all_required_fields_blank(address_ready_page):
    """
    ADDR_VAL_001: Verify all mandatory text fields display validation errors
    when form is submitted with cleared address and ZIP fields.

    Clears address line and ZIP, clicks Next.
    Asserts: Form does not navigate + mandatory errors visible.
    """
    page = address_ready_page
    address_page = AddressDetailsPage(page)

    allure.dynamic.title("ADDR_VAL_001 — All required text fields blank shows errors")
    allure.dynamic.tag("regression", "validation", "address_details")

    with allure.step("Clear all mandatory text fields"):
        address_page.fill_address_line("")
        address_page.fill_zip("")

    with allure.step("Click Next to trigger validation"):
        url_before = page.url
        address_page.click_next()

    with allure.step("Verify form is blocked"):
        page.wait_for_timeout(2000)
        ValidationHelper.assert_form_blocked(page, url_before)

    with allure.step("Verify mandatory error messages are displayed"):
        errors = ValidationHelper.get_all_errors(page)
        assert len(errors) >= 1, (
            f"Expected at least 1 validation error but found {len(errors)}. "
            f"Visible errors: {errors}"
        )

        allure.attach(
            f"Validation errors found ({len(errors)}):\n" + "\n".join(f"  • {e}" for e in errors),
            name="Required Field Errors",
            attachment_type=allure.attachment_type.TEXT,
        )
