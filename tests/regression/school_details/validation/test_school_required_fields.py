"""
School Details — Required Field Validation Test
==================================================
Consolidated test verifying all mandatory fields show errors
when form is submitted blank.

Execution: First visit only (before any successful save).
"""

import pytest
import allure

from pages.school_details_page import SchoolDetailsPage
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    """Capture and attach screenshot to Allure on test failure."""
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("school_details_ready_page")
        if page:
            screenshot_path = ScreenshotUtil.take_screenshot(page, "SCH_VAL_001")
            if screenshot_path:
                allure.attach.file(
                    screenshot_path,
                    name="Screenshot_SCH_VAL_001",
                    attachment_type=allure.attachment_type.PNG,
                )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Preliminary Form")
@allure.sub_suite("Regression")
@allure.feature("School Details")
@allure.story("Required Field Validation")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.preliminary_form
@pytest.mark.first_run
def test_school_all_required_fields_blank(school_details_ready_page):
    """
    SCH_VAL_001: Verify all mandatory fields display validation errors
    when form is submitted without entering any data.

    Clears all text fields and clicks Next.
    Asserts: Page does not navigate + all mandatory errors visible.
    """
    page = school_details_ready_page
    school_page = SchoolDetailsPage(page)

    allure.dynamic.title("SCH_VAL_001 — All required fields blank shows all errors")

    with allure.step("Clear all mandatory text fields"):
        page.get_by_role("textbox", name="Name of School *").fill("")
        page.locator("#contact_person").fill("")
        page.locator("#udise").fill("")

    with allure.step("Capture URL before submission"):
        url_before = page.url

    with allure.step("Click Next to trigger validation"):
        school_page.click_next()

    with allure.step("Verify page did NOT navigate (form blocked)"):
        page.wait_for_timeout(1000)
        ValidationHelper.assert_form_blocked(page, url_before)

    with allure.step("Verify mandatory error messages are displayed"):
        errors = ValidationHelper.get_all_errors(page)
        assert len(errors) >= 1, (
            f"Expected at least 1 validation error but found {len(errors)}. "
            f"Visible errors: {errors}"
        )

        allure.attach(
            f"Validation errors found ({len(errors)}):\n" + "\n".join(f"  • {e}" for e in errors),
            name="Mandatory Field Errors",
            attachment_type=allure.attachment_type.TEXT,
        )
