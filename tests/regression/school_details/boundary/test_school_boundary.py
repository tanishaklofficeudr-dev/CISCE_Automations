"""
School Details — Boundary Value Tests
========================================
Tests field character min/max limits for variable-range fields.
Does NOT include UDISE (fixed format, not boundary).

Data Source: test_data/negative/Validation_Data.xlsx → "School_Boundary_Extended"
             (filtered to only true boundary scenarios)
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
# DATA LOADING — Only true boundary (character length) scenarios
# Excludes UDISE (fixed format, not boundary)
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_boundary_scenarios = [
    row for row in _excel.get_sheet_data("School_Boundary_Extended")
    if str(row.get("execute", "")).lower() == "yes"
    and row.get("field_name") in ("school_name", "contact_person", "website")
]

_valid_baseline = {
    "school_name": "Boundary Test School",
    "school_classification": "Day",
    "school_type": "Co-ed.",
    "contact_person": "Test Contact",
    "contact_number": "7979009709",
    "contact_email": "test.7979009709@yopmail.com",
    "website": "https://www.testschool.com",
    "udise_number": "12345678901",
    "school_category": "Private",
}


# ============================================================================
# BOUNDARY TESTS — Character Length Limits
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Preliminary Form")
@allure.sub_suite("Regression")
@allure.feature("School Details")
@allure.story("Boundary Value Analysis")
@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.preliminary_form
@pytest.mark.parametrize(
    "scenario",
    _boundary_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_school_boundary(school_details_ready_page, scenario):
    """
    Verify field character length limits (min/max) are enforced.
    """
    page = school_details_ready_page
    school_page = SchoolDetailsPage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value", "")
    expected_outcome = scenario.get("expected_outcome", "ACCEPT")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Field: {field_name}\n"
        f"Value length: {len(str(field_value))}\n"
        f"Expected: {expected_outcome}"
    )
    allure.dynamic.severity(allure.severity_level.NORMAL)

    with allure.step(f"Fill '{field_name}' with {len(str(field_value or ''))} characters"):
        test_data = _valid_baseline.copy()
        skip_fields = []

        if field_value is None or field_value == "":
            # Empty value means skip this field (leave blank/clear it)
            skip_fields = [field_name]
        else:
            test_data[field_name] = str(field_value)

        url_before = page.url
        school_page.fill_partial_details(test_data, skip_fields=skip_fields)

    with allure.step(f"Verify outcome: {expected_outcome}"):
        page.wait_for_timeout(1000)
        # SPA: check if next step appeared (URL won't change)
        form_navigated = page.locator("#TabAddressDetails").is_visible()

        if expected_outcome == "ACCEPT":
            if form_navigated:
                allure.attach("PASS: Boundary value accepted.", name="Result", attachment_type=allure.attachment_type.TEXT)
                page.get_by_text("School Details", exact=False).first.click()
                page.wait_for_timeout(2000)
            else:
                errors = ValidationHelper.get_all_errors(page)
                pytest.fail(f"Expected ACCEPT but form blocked. Errors: {errors}")

        elif expected_outcome == "REJECT":
            if not form_navigated:
                errors = ValidationHelper.get_all_errors(page)
                allure.attach(f"PASS: Boundary rejected. Errors: {errors}", name="Result", attachment_type=allure.attachment_type.TEXT)
            else:
                page.get_by_text("School Details", exact=False).first.click()
                page.wait_for_timeout(2000)
                pytest.fail(f"Expected REJECT but form accepted value of length {len(str(field_value))}.")
