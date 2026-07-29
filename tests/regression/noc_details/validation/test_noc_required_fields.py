"""
NOC Details — Required Field Validation Test
===============================================
Consolidated test verifying all mandatory fields show errors
when form is submitted with cleared values.

Execution: Must run FIRST in NOC Details suite (@first_run marker).
"""

import pytest
import allure

from pages.noc_details_page import NOCDetailsPage
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    """Capture and attach screenshot to Allure on test failure."""
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("noc_ready_page")
        if page:
            try:
                screenshot_path = ScreenshotUtil.take_screenshot(page, "NOC_VAL_001")
                if screenshot_path:
                    allure.attach.file(
                        screenshot_path,
                        name="Screenshot_NOC_VAL_001",
                        attachment_type=allure.attachment_type.PNG,
                    )
            except Exception:
                pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("NOC Details")
@allure.sub_suite("Validation")
@allure.feature("Mandatory Field Validation")
@allure.story("All Mandatory Fields Empty")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.noc_details
@pytest.mark.first_run
def test_noc_all_required_fields_blank(noc_ready_page):
    """
    NOC_VAL_001: Verify all mandatory fields display validation errors
    when form is submitted with all text fields cleared and date cleared.

    Clears: authority, designation, office address, reference number, date.
    Asserts: Form does not navigate + mandatory errors visible.
    """
    page = noc_ready_page
    noc_page = NOCDetailsPage(page)

    allure.dynamic.title("NOC_VAL_001 — All mandatory fields blank shows errors")
    allure.dynamic.tag("regression", "validation", "noc_details")

    with allure.step("Clear all mandatory text fields"):
        noc_page.fill_authority("")
        noc_page.fill_designation("")
        noc_page.fill_office_address("")
        noc_page.fill_reference_number("")

    with allure.step("Clear date field via JavaScript"):
        noc_page.set_date("")

    with allure.step("Click Next to trigger validation"):
        url_before = page.url
        noc_page.click_next()

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
