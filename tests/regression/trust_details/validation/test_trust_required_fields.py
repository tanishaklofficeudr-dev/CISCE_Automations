"""
Trust/Society/Company Details — Required Field Validation Test
================================================================
Consolidated test verifying all mandatory fields show errors
when form is submitted with cleared values.

Execution: Must run FIRST in Trust Details suite (@first_run marker).
"""

import pytest
import allure

from pages.trust_details_page import TrustDetailsPage
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    """Capture and attach screenshot to Allure on test failure."""
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("trust_ready_page")
        if page:
            try:
                screenshot_path = ScreenshotUtil.take_screenshot(page, "TRUST_VAL_001")
                if screenshot_path:
                    allure.attach.file(
                        screenshot_path,
                        name="Screenshot_TRUST_VAL_001",
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
@allure.suite("Trust Details")
@allure.sub_suite("Validation")
@allure.feature("Mandatory Field Validation")
@allure.story("All Mandatory Fields Empty")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.trust_details
@pytest.mark.first_run
def test_trust_all_required_fields_blank(trust_ready_page):
    """
    TRUST_VAL_001: Verify all mandatory fields display validation errors
    when form is submitted with all text fields cleared and dates cleared.

    Clears: trust name, registration number, establishment date, registration date.
    Does NOT blank Ownership Type (disabled placeholder - not automatable).
    Asserts: Form does not navigate + mandatory errors visible.
    """
    page = trust_ready_page
    trust_page = TrustDetailsPage(page)

    allure.dynamic.title("TRUST_VAL_001 - All mandatory fields blank shows errors")
    allure.dynamic.tag("regression", "validation", "trust_details")

    with allure.step("Clear trust name (textarea)"):
        trust_page.fill_name("")

    with allure.step("Clear establishment date via JavaScript"):
        trust_page.set_establishment_date("")

    with allure.step("Clear registration date via JavaScript"):
        trust_page.set_registration_date("")

    with allure.step("Clear registration number"):
        trust_page.fill_registration_number("")

    with allure.step("Click Next to trigger validation"):
        trust_page.click_next()

    with allure.step("Verify form is blocked"):
        page.wait_for_timeout(2000)
        ValidationHelper.assert_form_blocked(page, page.url)

    with allure.step("Verify mandatory error messages are displayed"):
        errors = ValidationHelper.get_all_errors(page)
        assert len(errors) >= 1, (
            f"Expected at least 1 validation error but found {len(errors)}. "
            f"Visible errors: {errors}"
        )

        allure.attach(
            f"Validation errors found ({len(errors)}):\n" + "\n".join(f"  - {e}" for e in errors),
            name="Required Field Errors",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Assert individual expected error messages"):
        expected_messages = [
            "Ownership name is required",
            "Date of Establishment is required",
            "Date of Registration is required",
            "Registration number is required",
        ]
        for expected in expected_messages:
            ValidationHelper.assert_error_present(page, expected)
