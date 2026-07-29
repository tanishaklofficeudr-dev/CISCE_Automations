"""
School Details Module — Sanity Suite
=======================================
High-priority business validations that must pass after every deployment.
Verifies critical functionality works without deep edge-case testing.

This file does NOT duplicate regression logic. It imports and re-runs
a targeted subset of existing regression scenarios filtered by priority.

Data Source: test_data/negative/Validation_Data.xlsx
Page Object: pages/school_details_page.py
Fixture: school_details_ready_page (conftest.py)
"""

import pytest
import allure

from pages.school_details_page import SchoolDetailsPage
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
    """Store test result on the request node for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ============================================================================
# DATA LOADING — Sanity subset (High priority only)
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

# Sanity = High priority mandatory field validations only
_sanity_negative = [
    row for row in _excel.get_sheet_data("School_Negative")
    if str(row.get("execute", "")).lower() == "yes"
    and str(row.get("priority", "")).lower() == "high"
]

# Sanity positive = First valid submission scenario
_sanity_positive = [
    row for row in _excel.get_sheet_data("School_Positive")
    if str(row.get("execute", "")).lower() == "yes"
    and str(row.get("priority", "")).lower() == "high"
]

# Valid baseline
_valid_data = {
    "school_name": "Sanity Test School",
    "school_classification": "Day",
    "school_type": "Co-ed.",
    "contact_person": "Sanity Contact",
    "contact_number": "9815311210",
    "contact_email": "test.9815311210@gmail.com",
    "website": "https://www.sanityschool.com",
    "udise_number": "12345678901",
    "school_category": "Private",
}


# ============================================================================
# SANITY — Valid Form Submission (Happy Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Preliminary Form")
@allure.sub_suite("Sanity")
@allure.feature("School Details")
@allure.story("Valid Form Submission")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
@pytest.mark.preliminary_form
@pytest.mark.parametrize(
    "scenario",
    _sanity_positive,
    ids=lambda s: s["scenario_id"],
)
def test_school_sanity_valid_submission(school_details_ready_page, scenario):
    """
    Sanity: Verify School Details form submits with valid mandatory data.
    """
    page = school_details_ready_page
    school_page = SchoolDetailsPage(page)

    allure.dynamic.title(f"SANITY — {scenario['scenario_description']}")

    test_data = {
        "school_name": scenario["school_name"],
        "school_classification": scenario["school_classification"],
        "school_type": scenario["school_type"],
        "contact_person": scenario["contact_person"],
        "contact_number": scenario.get("contact_number") or "9815311210",
        "contact_email": scenario.get("contact_email") or "test.9815311210@gmail.com",
        "website": scenario.get("website") or "",
        "udise_number": scenario["udise_number"],
        "school_category": scenario["school_category"],
    }

    skip_fields = []
    if not test_data["website"]:
        skip_fields.append("website")

    with allure.step("Fill School Details with valid data"):
        url_before = page.url
        school_page.fill_partial_details(test_data, skip_fields=skip_fields)

    with allure.step("Verify form submitted successfully"):
        page.wait_for_timeout(2000)
        ValidationHelper.assert_form_submitted(page, url_before)

    with allure.step("Navigate back for next test"):
        page.get_by_role("button", name="Back").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(1000)


# ============================================================================
# SANITY — Mandatory Field Blocking (High Priority Only)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Preliminary Form")
@allure.sub_suite("Sanity")
@allure.feature("School Details")
@allure.story("Mandatory Field Validation")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
@pytest.mark.preliminary_form
@pytest.mark.parametrize(
    "scenario",
    _sanity_negative,
    ids=lambda s: s["scenario_id"],
)
def test_school_sanity_mandatory_blocked(school_details_ready_page, scenario):
    """
    Sanity: Verify critical mandatory fields block form submission.
    """
    page = school_details_ready_page
    school_page = SchoolDetailsPage(page)

    allure.dynamic.title(f"SANITY — {scenario['scenario_description']}")

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value")

    with allure.step(f"Submit form with missing/invalid '{field_name}'"):
        test_data = _valid_data.copy()
        url_before = page.url

        if field_value is None or field_value == "" or field_value == "SKIP":
            school_page.fill_partial_details(test_data, skip_fields=[field_name])
        else:
            test_data[field_name] = field_value
            school_page.fill_partial_details(test_data, skip_fields=[])

    with allure.step("Verify form blocked or navigate back"):
        page.wait_for_timeout(1000)
        if page.url != url_before:
            # Form navigated — no validation exists, navigate back
            page.get_by_role("button", name="Back").click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(1000)
            pytest.fail(
                f"SANITY FAIL: Mandatory field '{field_name}' has no validation. "
                f"Form navigated without error."
            )

    with allure.step(f"Verify error: '{scenario['expected_error']}'"):
        ValidationHelper.assert_error_present(page, scenario["expected_error"])
