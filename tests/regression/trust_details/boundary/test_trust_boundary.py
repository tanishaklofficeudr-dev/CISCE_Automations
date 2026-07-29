"""
Trust/Society/Company Details — Boundary Value Tests
======================================================
Tests field character min/max limits for trust text fields.
Each test overwrites existing values — independently executable.

Data Source: test_data/negative/Validation_Data.xlsx -> "Trust_Boundary"
Page Object: pages/trust_details_page.py
Fixture: trust_ready_page (conftest.py)
"""

import pytest
import allure

from pages.trust_details_page import TrustDetailsPage
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
        page = request.node.funcargs.get("trust_ready_page")
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
                pass


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
    row for row in _excel.get_sheet_data("Trust_Boundary")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# BOUNDARY TESTS — Field Length Limits
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Trust Details")
@allure.sub_suite("Boundary")
@allure.feature("Boundary Validation")
@allure.story("Boundary Value Scenarios")
@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.trust_details
@pytest.mark.parametrize(
    "scenario",
    _boundary_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_trust_boundary(trust_ready_page, scenario):
    """
    Verify field character length boundaries are handled correctly.
    Fills all mandatory fields with valid data, then overwrites target field.
    """
    page = trust_ready_page
    trust_page = TrustDetailsPage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value", "")
    expected_outcome = scenario.get("expected_outcome", "ACCEPT")

    allure.dynamic.title(f"{scenario['scenario_id']} - {scenario['scenario_description']}")
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
    allure.dynamic.tag("regression", "boundary", "trust_details")

    with allure.step("Fill all mandatory fields with valid baseline data"):
        trust_page.fill_name("Boundary Test Trust Organization")
        trust_page.fill_registration_number("BND-REG-2020-001")
        trust_page.set_establishment_date("05/03/2018")
        trust_page.set_registration_date("10/04/2019")
        page.locator("#ownership_type").select_option(label="Trust")
        page.wait_for_timeout(500)

    with allure.step(f"Overwrite '{field_name}' with boundary value ({len(str(field_value or ''))} chars)"):
        if field_name == "owner_name":
            trust_page.fill_name(str(field_value))
        elif field_name == "registration_no":
            trust_page.fill_registration_number(str(field_value))

    with allure.step("Click Next to submit"):
        trust_page.click_next()
        page.wait_for_timeout(2000)

    with allure.step(f"Verify outcome: {expected_outcome}"):
        # Check if Certificate of Land appeared (form submitted)
        form_navigated = False
        try:
            land_el = page.get_by_text("Certificate of Land", exact=False)
            if land_el.count() > 0 and land_el.first.is_visible():
                form_navigated = True
        except Exception:
            pass

        if expected_outcome == "ACCEPT":
            if form_navigated:
                allure.attach(
                    "PASS: Boundary value accepted - form navigated to Certificate of Land.",
                    name="Boundary Result",
                    attachment_type=allure.attachment_type.TEXT,
                )
                with allure.step("Navigate back to Trust Details"):
                    page.get_by_text("Trust /Society /Company", exact=False).first.click()
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
                page.get_by_text("Trust /Society /Company", exact=False).first.click()
                page.wait_for_timeout(2000)
                pytest.fail(
                    f"Expected REJECT but form accepted value of length {len(str(field_value))}."
                )
