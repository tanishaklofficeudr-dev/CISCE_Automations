"""
Trust/Society/Company Details — Negative (Format Validation) Tests
====================================================================
Tests invalid/blank input is rejected by the Trust Details form.
Fills all fields with valid baseline, then overwrites target with invalid value.

Data Source: test_data/negative/Validation_Data.xlsx -> "Trust_Negative"
Page Object: pages/trust_details_page.py
Fixture: trust_ready_page (conftest.py)

On failure: generates diagnostic evidence classifying root cause.
"""

import pytest
import allure
import json
from datetime import datetime, timedelta

from pages.trust_details_page import TrustDetailsPage
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

                scenario = request.node.funcargs.get("scenario", {})
                errors = ValidationHelper.get_all_errors(page, timeout=500)
                remarks = scenario.get("remarks", "")

                diagnostic = {
                    "test_case_id": scenario.get("scenario_id", "UNKNOWN"),
                    "field": scenario.get("field_name", ""),
                    "value": scenario.get("field_value", ""),
                    "expected_error": scenario.get("expected_error", ""),
                    "actual_errors": errors if errors else "No validation messages found",
                    "form_navigated": _check_navigation(page),
                    "current_url": page.url,
                    "screenshot": screenshot_path or "",
                    "classification": remarks if remarks else _classify(scenario, errors, page),
                    "timestamp": datetime.now().isoformat(),
                }
                allure.attach(
                    json.dumps(diagnostic, indent=2, default=str),
                    name="Failure Diagnostic Report",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                pass


def _check_navigation(page):
    """Check if form navigated AWAY from Trust Details to Certificate of Land."""
    try:
        # Check if the Trust Details heading/content is GONE (not just tab label)
        # If ownership_type field is still visible, we're still on Trust page
        ownership = page.locator("#ownership_type")
        if ownership.is_visible():
            return False  # Still on Trust page — form was blocked
        return True  # Trust field gone — navigated away
    except Exception:
        return False


def _classify(scenario, errors, page):
    """Classify failure root cause."""
    if _check_navigation(page):
        return "APPLICATION BEHAVIOR: Form navigated without validation. Invalid data accepted."
    if not errors:
        return "AUTOMATION ISSUE: No errors captured, form did not navigate. Possible timing issue."
    expected = scenario.get("expected_error", "").lower()
    actual = " ".join(e.lower() for e in errors)
    if expected and expected not in actual:
        return f"MESSAGE MISMATCH: Expected '{scenario.get('expected_error')}' but got: {errors}"
    return "UNKNOWN: requires manual investigation."


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

_raw_scenarios = [
    row for row in _excel.get_sheet_data("Trust_Negative")
    if str(row.get("execute", "")).lower() == "yes"
]

# Apply scenarios directly — no xfail markers needed (tests now passing)
_negative_scenarios = _raw_scenarios


# ============================================================================
# NEGATIVE TESTS — Format / Mandatory Validation
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Trust Details")
@allure.sub_suite("Negative")
@allure.feature("Validation")
@allure.story("Negative Scenarios")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.trust_details
@pytest.mark.parametrize(
    "scenario",
    _negative_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_trust_negative_validation(trust_ready_page, scenario):
    """
    Verify that invalid/blank input is rejected by the Trust Details form.
    Fills all fields with valid baseline, then overwrites target with invalid value.
    """
    page = trust_ready_page
    trust_page = TrustDetailsPage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value")
    expected_error = scenario["expected_error"]
    remarks = scenario.get("remarks", "")

    allure.dynamic.title(f"{scenario['scenario_id']} - {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Field: {field_name}\n"
        f"Value: '{field_value or '(blank)'}'\n"
        f"Expected: {expected_error}\n"
        f"Remarks: {remarks or 'None'}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "High"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "negative", "trust_details")

    with allure.step("Fill all mandatory fields with valid baseline data"):
        page.locator("#ownership_type").select_option(label="Trust")
        page.wait_for_timeout(500)
        trust_page.fill_name("Valid Baseline Trust Name")
        trust_page.set_establishment_date("05/03/2018")
        trust_page.set_registration_date("10/04/2019")
        # Use timestamp-based unique registration number to avoid duplicate validation
        import time
        unique_reg = f"TRUST-REG-{int(time.time())}"
        trust_page.fill_registration_number(unique_reg)

    with allure.step(f"Overwrite '{field_name}' with invalid/blank value"):
        if field_name == "owner_name":
            trust_page.fill_name(str(field_value) if field_value else "")
        elif field_name == "registration_no":
            trust_page.fill_registration_number(str(field_value) if field_value else "")
        elif field_name == "establishment_date":
            if field_value == "FUTURE":
                future = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
                trust_page.set_establishment_date(future)
            else:
                trust_page.set_establishment_date("")
        elif field_name == "registration_date":
            if field_value == "BEFORE_EST":
                # Set establishment to 2022, registration to 2019
                trust_page.set_establishment_date("01/06/2022")
                trust_page.set_registration_date("15/03/2019")
            else:
                trust_page.set_registration_date("")

    with allure.step("Click Next to trigger validation"):
        trust_page.click_next()
        page.wait_for_timeout(2000)

    with allure.step("Check if form was blocked"):
        form_navigated = _check_navigation(page)

        if form_navigated:
            # Navigate back for next test
            page.get_by_text("Trust /Society /Company", exact=False).first.click()
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
            # Form navigated — generate diagnostic
            classification = remarks if remarks else "APPLICATION BEHAVIOR: Form accepted invalid data."
            allure.attach(
                f"FORM NAVIGATED: Field '{field_name}' with value '{field_value}' was accepted.\n"
                f"Expected error: '{expected_error}'\n"
                f"Classification: {classification}\n"
                f"Action: Awaiting business confirmation before modifying test.",
                name="Business Rule Verification Required",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected validation for '{field_name}' but form navigated. "
                f"Classification: {classification}"
            )
