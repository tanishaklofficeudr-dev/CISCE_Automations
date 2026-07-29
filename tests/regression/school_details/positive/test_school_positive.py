"""
School Details — Positive Regression Tests
=============================================
Validates form submits successfully with various valid data combinations.

Data Source: test_data/negative/Validation_Data.xlsx → "School_Positive"
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
# DATA LOADING
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_positive_scenarios = [
    row for row in _excel.get_sheet_data("School_Positive")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# POSITIVE TESTS — Valid Form Submission
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Preliminary Form")
@allure.sub_suite("Regression")
@allure.feature("School Details")
@allure.story("Valid Form Submission")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.preliminary_form
@pytest.mark.parametrize(
    "scenario",
    _positive_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_school_positive_submission(school_details_ready_page, scenario):
    """
    Verify School Details form submits successfully with valid data.
    """
    page = school_details_ready_page
    school_page = SchoolDetailsPage(page)

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"School: {scenario['school_name']}\n"
        f"Classification: {scenario['school_classification']}\n"
        f"Type: {scenario['school_type']}\n"
        f"Category: {scenario['school_category']}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "High"
        else allure.severity_level.NORMAL
    )

    test_data = {
        "school_name": scenario["school_name"],
        "school_classification": scenario["school_classification"],
        "school_type": scenario["school_type"],
        "contact_person": scenario["contact_person"],
        "contact_number": scenario.get("contact_number") or "9815311210",
        "contact_email": scenario.get("contact_email") or "test.9815311210@gmail.com",
        "website": scenario.get("website") or "",
        "udise_number": str(scenario["udise_number"]),
        "school_category": scenario["school_category"],
    }

    skip_fields = []
    if not test_data["website"]:
        skip_fields.append("website")

    with allure.step(f"Fill valid data: {scenario['school_name']}"):
        url_before = page.url
        school_page.fill_partial_details(test_data, skip_fields=skip_fields)

    with allure.step("Verify form submitted (page navigated)"):
        page.wait_for_timeout(2000)
        ValidationHelper.assert_form_submitted(page, url_before)

    with allure.step("Navigate back for next test"):
        page.get_by_text("School Details", exact=False).first.click()
        page.wait_for_timeout(2000)
