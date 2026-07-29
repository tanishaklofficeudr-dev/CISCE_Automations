"""
NOC Details — Negative (Format Validation) Tests
===================================================
Tests invalid/blank input is rejected by the NOC Details form.
Overwrites existing saved values — independently executable.

Data Source: test_data/negative/Validation_Data.xlsx → "NOC_Negative"
Page Object: pages/noc_details_page.py
Fixture: noc_ready_page (conftest.py)

On failure: generates diagnostic evidence classifying root cause.
"""

import pytest
import allure
import json
import os
from datetime import datetime, timedelta

from pages.noc_details_page import NOCDetailsPage
from utils.excel_reader import ExcelReader
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


# ============================================================================
# AUTO SCREENSHOT + DIAGNOSTIC ON FAILURE
# ============================================================================

@pytest.fixture(autouse=True)
def capture_diagnostic_on_failure(request):
    """Capture screenshot and generate diagnostic report on test failure."""
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("noc_ready_page")
        if page:
            try:
                screenshot_path = ScreenshotUtil.take_screenshot(page, request.node.name[:50])
                if screenshot_path:
                    allure.attach.file(
                        screenshot_path,
                        name=f"Screenshot_{request.node.name[:50]}",
                        attachment_type=allure.attachment_type.PNG,
                    )

                scenario = request.node.funcargs.get("scenario", {})
                errors = ValidationHelper.get_all_errors(page, timeout=500)
                diagnostic = {
                    "test_case_id": scenario.get("scenario_id", "UNKNOWN"),
                    "input_data": {
                        "field": scenario.get("field_name", ""),
                        "value": scenario.get("field_value", ""),
                    },
                    "expected_result": scenario.get("expected_error", ""),
                    "actual_result": errors if errors else "No validation messages found",
                    "current_url": page.url,
                    "screenshot_path": screenshot_path or "",
                    "timestamp": datetime.now().isoformat(),
                    "root_cause_classification": _classify_failure(scenario, errors, page),
                    "recommendation": _recommend_action(scenario, errors, page),
                }
                allure.attach(
                    json.dumps(diagnostic, indent=2, default=str),
                    name="Failure Diagnostic Report",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                pass


def _classify_failure(scenario, errors, page):
    """Classify failure root cause."""
    expected = scenario.get("expected_error", "").lower()

    if not errors:
        try:
            trust_visible = page.get_by_text("Trust/Society/Company", exact=False).first.is_visible()
        except Exception:
            trust_visible = False

        if trust_visible:
            return "APPLICATION DEFECT — Form navigated without validation. Invalid data accepted."
        return "AUTOMATION ISSUE — No errors captured, form did not navigate. Possible timing/locator issue."

    actual_lower = " ".join(e.lower() for e in errors)
    if expected and expected not in actual_lower:
        return "BUSINESS RULE MISMATCH — Validation appeared but message differs from expected."

    return "UNKNOWN — requires manual investigation."


def _recommend_action(scenario, errors, page):
    """Generate recommendation."""
    if not errors:
        try:
            trust_visible = page.get_by_text("Trust/Society/Company", exact=False).first.is_visible()
        except Exception:
            trust_visible = False

        if trust_visible:
            return "Verify manually. If validation exists manually but not via automation, investigate interaction method."
        return "Add explicit wait. May be timing issue."

    expected = scenario.get("expected_error", "").lower()
    actual_lower = " ".join(e.lower() for e in errors)
    if expected and expected not in actual_lower:
        return f"Update expected_error in Excel to match actual: {errors}"

    return "Investigate further."


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the request node for diagnostic fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ============================================================================
# DATA LOADING
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_negative_scenarios = [
    row for row in _excel.get_sheet_data("NOC_Negative")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# NEGATIVE TESTS — Format / Mandatory Validation
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("NOC Details")
@allure.sub_suite("Negative")
@allure.feature("Validation")
@allure.story("Negative Scenarios")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.noc_details
@pytest.mark.parametrize(
    "scenario",
    _negative_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_noc_negative_validation(noc_ready_page, scenario):
    """
    Verify that invalid/blank input is rejected by the NOC Details form.
    Fills all fields with valid data, then overwrites target with invalid value.
    """
    page = noc_ready_page
    noc_page = NOCDetailsPage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value")
    expected_error = scenario["expected_error"]

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Field: {field_name}\n"
        f"Value: '{field_value or '(blank)'}'\n"
        f"Expected error: {expected_error}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "High"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "negative", "noc_details")

    with allure.step("Fill all mandatory fields with valid baseline data"):
        noc_page.fill_authority("District Education Officer")
        noc_page.fill_designation("Director of Education")
        noc_page.fill_office_address("State Education Office, Jaipur")
        # Use timestamp-based unique reference to avoid duplicate validation
        import time
        unique_ref = f"NOC-NEG-{int(time.time())}"
        noc_page.fill_reference_number(unique_ref)
        noc_page.set_date("16/05/2025")
        page.locator("#noc_country").select_option("2")
        page.wait_for_timeout(1000)
        page.locator("#noc_state").select_option("30")

    with allure.step(f"Overwrite '{field_name}' with invalid/blank value"):
        if field_name == "noc_authority":
            noc_page.fill_authority(str(field_value) if field_value else "")
        elif field_name == "designation":
            noc_page.fill_designation(str(field_value) if field_value else "")
        elif field_name == "office_address":
            noc_page.fill_office_address(str(field_value) if field_value else "")
        elif field_name == "noc_reference_number":
            noc_page.fill_reference_number(str(field_value) if field_value else "")
        elif field_name == "noc_date":
            if field_value == "FUTURE":
                # Generate future date dynamically
                future_date = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
                noc_page.set_date(future_date)
            else:
                # Clear the date (empty)
                noc_page.set_date("")

    with allure.step("Click Next to trigger validation"):
        noc_page.click_next()
        page.wait_for_timeout(2000)

    with allure.step("Check if form was blocked"):
        form_navigated = False
        try:
            trust_el = page.get_by_text("Trust/Society/Company", exact=False)
            if trust_el.count() > 0 and trust_el.first.is_visible():
                form_navigated = True
        except Exception:
            pass

        if form_navigated:
            # Navigate back for next test
            page.get_by_text("NOC Details", exact=False).first.click()
            page.wait_for_timeout(2000)

    with allure.step(f"Verify error: '{expected_error}'"):
        if not form_navigated:
            errors = ValidationHelper.get_all_errors(page)
            allure.attach(
                f"Actual errors: {errors}",
                name="Captured Validation Messages",
                attachment_type=allure.attachment_type.TEXT,
            )
            ValidationHelper.assert_error_present(page, expected_error)
        else:
            allure.attach(
                f"FORM NAVIGATED: Field '{field_name}' with value '{field_value}' was accepted.\n"
                f"Expected error '{expected_error}' was NOT shown.\n"
                f"This requires investigation — see Failure Diagnostic Report.",
                name="Navigation Without Validation",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected validation for '{field_name}' with value '{field_value}' "
                f"but form navigated. No error '{expected_error}' displayed."
            )
