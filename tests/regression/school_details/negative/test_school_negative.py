"""
School Details — Negative (Format Validation) Tests
=====================================================
Tests invalid input formats are rejected by the School Details form.
Overwrites existing saved values with invalid data — testable anytime.

Data Source: test_data/negative/Validation_Data.xlsx → "School_Negative"
"""

import pytest
import allure

from pages.school_details_page import SchoolDetailsPage
from utils.excel_reader import ExcelReader
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("school_details_ready_page")
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
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ============================================================================
# DATA LOADING — Format validation scenarios only
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_format_scenarios = [
    row for row in _excel.get_sheet_data("School_Negative")
    if str(row.get("execute", "")).lower() == "yes"
]

_valid_baseline = {
    "school_name": "Regression Test School",
    "school_classification": "Day",
    "school_type": "Co-ed.",
    "contact_person": "Test Contact",
    "contact_number": "9815311210",
    "contact_email": "test.9815311210@gmail.com",
    "website": "https://www.testschool.com",
    "udise_number": "12345678901",
    "school_category": "Private",
}


# ============================================================================
# FORMAT VALIDATION TESTS
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Preliminary Form")
@allure.sub_suite("Regression")
@allure.feature("School Details")
@allure.story("Format Validation")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.preliminary_form
@pytest.mark.parametrize(
    "scenario",
    _format_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_school_format_validation(school_details_ready_page, scenario):
    """
    Verify that invalid input formats are rejected by the School Details form.
    Overwrites saved data with invalid values and checks for error messages.
    """
    page = school_details_ready_page
    school_page = SchoolDetailsPage(page)

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Field: {scenario['field_name']}\n"
        f"Value: '{scenario.get('field_value') or '(blank)'}'\n"
        f"Expected: {scenario['expected_error']}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "High"
        else allure.severity_level.NORMAL
    )

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value")

    with allure.step(f"Fill form with invalid value for '{field_name}'"):
        test_data = _valid_baseline.copy()
        url_before = page.url

        if field_value is None or field_value == "" or field_value == "SKIP":
            # Clear the field (test blank mandatory)
            skip_fields = [field_name]
            school_page.fill_partial_details(test_data, skip_fields=skip_fields)
        else:
            # Override with invalid value
            test_data[field_name] = str(field_value)
            school_page.fill_partial_details(test_data, skip_fields=[])

    with allure.step("Check form behavior"):
        page.wait_for_timeout(1000)
        # SPA: URL won't change — check if next step appeared
        form_navigated = page.locator("#TabAddressDetails").is_visible()

        if form_navigated:
            with allure.step("Navigate back to School Details"):
                page.get_by_text("School Details", exact=False).first.click()
                page.wait_for_timeout(2000)

    with allure.step(f"Verify error: '{scenario['expected_error']}'"):
        if not form_navigated:
            ValidationHelper.assert_error_present(page, scenario["expected_error"])
        else:
            allure.attach(
                f"NO VALIDATION: Field '{field_name}' accepted invalid value '{field_value}'. "
                f"Expected error: '{scenario['expected_error']}'",
                name="Missing Validation",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected format error for '{field_name}' but form navigated."
            )
