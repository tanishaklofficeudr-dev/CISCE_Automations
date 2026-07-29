"""
Address Details — Negative (Format Validation) Tests
======================================================
Tests invalid input formats are rejected by the Address Details form.
Overwrites existing saved values with invalid data — independently executable.

Data Source: test_data/negative/Validation_Data.xlsx → "Address_Negative"
Page Object: pages/address_details_page.py
Fixture: address_ready_page (conftest.py)

On failure: generates diagnostic evidence instead of immediately classifying
the failure. Evidence includes actual vs expected, screenshot, and root cause.
"""

import pytest
import allure
import json
import os
from datetime import datetime

from pages.address_details_page import AddressDetailsPage
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
        page = request.node.funcargs.get("address_ready_page")
        if page:
            try:
                # Screenshot
                screenshot_path = ScreenshotUtil.take_screenshot(page, request.node.name[:50])
                if screenshot_path:
                    allure.attach.file(
                        screenshot_path,
                        name=f"Screenshot_{request.node.name[:50]}",
                        attachment_type=allure.attachment_type.PNG,
                    )

                # Diagnostic report
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
    """Classify failure into Automation Issue, App Defect, or Business Rule Mismatch."""
    expected = scenario.get("expected_error", "").lower()

    if not errors:
        # No errors found — could be app defect or form navigated
        try:
            noc_visible = page.locator("#TabNOCDetails").is_visible()
        except Exception:
            noc_visible = False

        if noc_visible:
            return "APPLICATION DEFECT — Form navigated without showing validation. Invalid data was accepted."
        else:
            return "AUTOMATION ISSUE — No errors captured but form did not navigate. Possible locator/timing issue."

    # Errors found but don't match expected
    actual_lower = " ".join(e.lower() for e in errors)
    if expected and expected not in actual_lower:
        return "BUSINESS RULE MISMATCH — Validation appeared but message differs from expected."

    return "UNKNOWN — requires manual investigation."


def _recommend_action(scenario, errors, page):
    """Generate recommendation based on failure classification."""
    if not errors:
        try:
            noc_visible = page.locator("#TabNOCDetails").is_visible()
        except Exception:
            noc_visible = False

        if noc_visible:
            return "Verify manually. If validation exists manually but not via automation, investigate Playwright interaction method (.fill vs .type)."
        return "Add explicit wait before error check. May be timing issue."

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
    row for row in _excel.get_sheet_data("Address_Negative")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# NEGATIVE TESTS — Format Validation
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Address Details")
@allure.sub_suite("Negative")
@allure.feature("Address Details Validation")
@allure.story("Negative Validation Scenarios")
@pytest.mark.regression
@pytest.mark.address_details
@pytest.mark.negative
@pytest.mark.parametrize(
    "scenario",
    _negative_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_address_format_validation(address_ready_page, scenario):
    """
    Verify that invalid input formats are rejected by the Address Details form.
    Overwrites saved data with invalid values and checks for error messages.
    """
    page = address_ready_page
    address_page = AddressDetailsPage(page)

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
    allure.dynamic.tag("regression", "negative", "address_details")

    with allure.step(f"Overwrite '{field_name}' with invalid value"):
        # Overwrite only the target field with invalid data
        if field_name == "zip_pin":
            address_page.fill_zip(str(field_value) if field_value else "")
        elif field_name == "address_line_1":
            address_page.fill_address_line(str(field_value) if field_value else "")

    with allure.step("Click Next to trigger validation"):
        address_page.click_next()
        page.wait_for_timeout(2000)

    with allure.step("Check if form was blocked"):
        # Detect navigation (SPA — check for NOC Details tab)
        form_navigated = False
        try:
            noc_tab = page.locator("#TabNOCDetails")
            if noc_tab.count() > 0 and noc_tab.is_visible():
                form_navigated = True
        except Exception:
            pass

        if form_navigated:
            # Navigate back for next test
            page.get_by_text("Address Details", exact=False).first.click()
            page.wait_for_timeout(2000)

    with allure.step(f"Verify error message: '{expected_error}'"):
        if not form_navigated:
            # Form was blocked — verify error message
            errors = ValidationHelper.get_all_errors(page)
            allure.attach(
                f"Actual errors: {errors}",
                name="Captured Validation Messages",
                attachment_type=allure.attachment_type.TEXT,
            )
            ValidationHelper.assert_error_present(page, expected_error)
        else:
            # Form navigated — test fails with diagnostic
            allure.attach(
                f"FORM NAVIGATED: Field '{field_name}' with value '{field_value}' was accepted.\n"
                f"Expected error '{expected_error}' was NOT shown.\n"
                f"This may indicate missing validation in the application.",
                name="Navigation Without Validation",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected validation for '{field_name}' with value '{field_value}' "
                f"but form navigated to next step. No error '{expected_error}' displayed."
            )
