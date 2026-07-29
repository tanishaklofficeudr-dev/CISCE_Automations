"""
Certificate of Land — Negative Regression Tests
==================================================
Tests invalid/blank input is rejected by the Certificate of Land form.
Fills all fields with valid baseline, then overwrites target with invalid value.

Data Source: test_data/negative/Validation_Data.xlsx → "Land_Negative"
Page Object: pages/land_certificate_page.py
Fixture: land_ready_page (conftest.py)

Phase 3 implements: LAND_NEG_001–006 (Owned path)
Phase 4 adds: LAND_NEG_007–009 (Leased path)
Phase 5 adds: LAND_NEG_010–011 (Multiple path)

On failure: generates diagnostic evidence classifying root cause.
"""

import pytest
import allure
import json
from datetime import datetime, timedelta

from pages.land_certificate_page import LandCertificatePage
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
        page = request.node.funcargs.get("land_ready_page")
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
    """Check if form navigated AWAY from Certificate of Land."""
    try:
        land_area = page.locator("#land_area_0")
        if land_area.is_visible():
            return False
        return True
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

_all_negative = [
    row for row in _excel.get_sheet_data("Land_Negative")
    if str(row.get("execute", "")).lower() == "yes"
]

# Phase 3: Single_Owned flow
_owned_negative = [
    row for row in _all_negative
    if row.get("flow") == "Single_Owned"
]

# Phase 4: Single_Leased flow
_leased_negative = [
    row for row in _all_negative
    if row.get("flow") == "Single_Leased"
]

# Phase 5: Multiple flow
_multiple_negative = [
    row for row in _all_negative
    if row.get("flow") == "Multiple"
]


# ============================================================================
# NEGATIVE TESTS — Format / Mandatory Validation (Owned Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Negative")
@allure.feature("Validation")
@allure.story("Negative Scenarios — Single Owned")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _owned_negative,
    ids=lambda s: s["scenario_id"],
)
def test_land_negative_validation(land_ready_page, scenario):
    """
    Verify that invalid/blank input is rejected by the Certificate of Land form.
    Fills all fields with valid baseline, then overwrites target with invalid value.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value")
    expected_error = scenario["expected_error"]
    remarks = scenario.get("remarks", "")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Field: {field_name}\n"
        f"Value: '{field_value or '(blank)'}'\n"
        f"Expected: {expected_error}\n"
        f"Remarks: {remarks or 'None'}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "negative", "land_certificate")

    # Valid baseline data
    baseline_data = {
        "area_unit": "Square Meter",
        "land_area": "5000",
        "situated_in": "Survey No(s)",
        "situated_at": "Civil Lines, Jaipur",
        "land_owned_by": "Test Trust",
        "land_title_document": "Conveyance Deed",
        "sale_deed_favor": "",
        "registration_details": "REG-BASELINE-001",
        "executed_by": "Mr. Baseline",
        "registration_office": "Sub-Registrar Office",
        "document_date": "15/03/2020",
    }

    with allure.step("Fill all mandatory fields with valid baseline data"):
        land_page.select_plot_type("Single")
        land_page.select_land_type("Owned")
        page.locator("#land_area_0").wait_for(state="visible", timeout=5000)

        # Fill baseline
        page.locator("#land_unit_0").select_option(label=baseline_data["area_unit"])
        page.locator("#land_area_0").click()
        page.locator("#land_area_0").fill(baseline_data["land_area"])
        page.locator("#situate_speci_0").click()
        page.locator("#situate_speci_0").fill(baseline_data["situated_in"])
        page.locator("#situated_at0").click()
        page.locator("#situated_at0").fill(baseline_data["situated_at"])
        page.locator("#owned_by_0").click()
        page.locator("#owned_by_0").fill(baseline_data["land_owned_by"])
        page.locator("#land_title_doc0").select_option(label=baseline_data["land_title_document"])
        page.locator("#land_title0").click()
        page.locator("#land_title0").fill(baseline_data["registration_details"])
        page.locator("#executed_by0").click()
        page.locator("#executed_by0").fill(baseline_data["executed_by"])
        page.locator("#regid_ofc_details0").click()
        page.locator("#regid_ofc_details0").fill(baseline_data["registration_office"])
        ValidationHelper.set_readonly_date(page, '#land_title_date0', baseline_data["document_date"])

    with allure.step(f"Overwrite '{field_name}' with invalid/blank value: '{field_value or ''}'"):
        if field_name == "land_area":
            page.locator("#land_area_0").click()
            page.locator("#land_area_0").fill(str(field_value) if field_value else "")

        elif field_name == "situated_in":
            page.locator("#situate_speci_0").click()
            page.locator("#situate_speci_0").fill(str(field_value) if field_value else "")

        elif field_name == "document_date":
            if field_value == "FUTURE":
                future = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
                ValidationHelper.set_readonly_date(page, '#land_title_date0', future)
            else:
                ValidationHelper.set_readonly_date(page, '#land_title_date0', str(field_value) if field_value else "")

        elif field_name == "sale_deed_favor":
            # Switch title to Sale Deed first, then leave favor blank
            page.locator("#land_title_doc0").select_option(label="Sale Deed")
            page.locator("#sale_deed_favor_whom_0").wait_for(state="visible", timeout=3000)
            # Leave favor at placeholder (don't select a value)

    with allure.step("Click Next to trigger validation"):
        land_page.click_next()
        page.wait_for_timeout(2000)

    with allure.step("Check if form was blocked"):
        form_navigated = _check_navigation(page)

        if form_navigated:
            page.get_by_text("Certificate of Land", exact=False).first.click()
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
            classification = remarks if remarks else "APPLICATION BEHAVIOR: Form accepted invalid data."
            allure.attach(
                f"FORM NAVIGATED: Field '{field_name}' with value '{field_value}' was accepted.\n"
                f"Expected error: '{expected_error}'\n"
                f"Classification: {classification}\n"
                f"Action: Awaiting business confirmation.",
                name="Business Rule Verification Required",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected validation for '{field_name}' but form navigated. "
                f"Classification: {classification}"
            )


# ============================================================================
# NEGATIVE TESTS — Format / Mandatory Validation (Leased Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Negative")
@allure.feature("Validation")
@allure.story("Negative Scenarios — Single Leased")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _leased_negative,
    ids=lambda s: s["scenario_id"],
)
def test_land_negative_leased_validation(land_ready_page, scenario):
    """
    Verify that invalid/blank input is rejected by the Leased path form.
    Fills all fields with valid baseline, then overwrites target with invalid value.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value")
    expected_error = scenario["expected_error"]
    remarks = scenario.get("remarks", "")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Flow: {scenario['flow']}\n"
        f"Field: {field_name}\n"
        f"Value: '{field_value or '(blank)'}'\n"
        f"Expected: {expected_error}\n"
        f"Remarks: {remarks or 'None'}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "negative", "land_certificate", "leased")

    with allure.step("Fill all Leased fields with valid baseline"):
        land_page.select_plot_type("Single")
        land_page.select_land_type("Leased")
        page.locator("#lease_land_area_0").wait_for(state="visible", timeout=5000)

        # Fill baseline
        page.locator("#lease_area_unit_0").select_option(label="Square Meter")
        page.locator("#lease_land_area_0").click()
        page.locator("#lease_land_area_0").fill("3000")
        page.locator("#leease_name_0").click()
        page.locator("#leease_name_0").fill("ABC School Trust")
        page.locator("#leaser_name_0").click()
        page.locator("#leaser_name_0").fill("State Government")
        ValidationHelper.set_readonly_date(page, '#lease_deed_date_0', "10/05/2015")
        page.locator("#lease_deed_duration_0").click()
        page.locator("#lease_deed_duration_0").fill("30")
        ValidationHelper.set_readonly_date(page, '#date_regis_lease_deed0', "20/06/2015")
        page.locator("#details_regis_ofc0").click()
        page.locator("#details_regis_ofc0").fill("Sub-Registrar Office")
        # Default: Renewal=No (already selected)

    with allure.step(f"Overwrite '{field_name}' with invalid/blank value: '{field_value or ''}'"):
        if field_name == "land_area":
            page.locator("#lease_land_area_0").click()
            page.locator("#lease_land_area_0").fill(str(field_value) if field_value else "")

        elif field_name == "lease_deed_duration":
            page.locator("#lease_deed_duration_0").click()
            page.locator("#lease_deed_duration_0").fill(str(field_value) if field_value else "")

        elif field_name == "renewal_duration":
            # Must select Renewal=Yes first, then leave duration blank
            page.locator("#renewal_yes0").click()
            page.wait_for_timeout(1500)
            page.locator("#renewal_lease_deed_duration_0").wait_for(state="visible", timeout=3000)
            page.locator("#renewal_lease_deed_duration_0").click()
            page.locator("#renewal_lease_deed_duration_0").fill(str(field_value) if field_value else "")

    with allure.step("Click Next to trigger validation"):
        land_page.click_next()
        page.wait_for_timeout(2000)

    with allure.step("Check if form was blocked"):
        form_navigated = not page.locator("#lease_land_area_0").is_visible()

        if form_navigated:
            page.get_by_text("Certificate of Land", exact=False).first.click()
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
            classification = remarks if remarks else "APPLICATION BEHAVIOR: Form accepted invalid data."
            allure.attach(
                f"FORM NAVIGATED: Field '{field_name}' with value '{field_value}' was accepted.\n"
                f"Expected error: '{expected_error}'\n"
                f"Classification: {classification}",
                name="Business Rule Verification Required",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected validation for '{field_name}' but form navigated. "
                f"Classification: {classification}"
            )


# ============================================================================
# NEGATIVE TESTS — Format / Mandatory Validation (Multiple Plot Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Negative")
@allure.feature("Validation")
@allure.story("Negative Scenarios — Multiple Plots")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _multiple_negative,
    ids=lambda s: s["scenario_id"],
)
def test_land_negative_multiple_validation(land_ready_page, scenario):
    """
    Verify that invalid/blank input is rejected by the Multiple Plot form.
    Fills baseline data then overwrites target with invalid value.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value")
    expected_error = scenario["expected_error"]
    remarks = scenario.get("remarks", "")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Flow: {scenario['flow']}\n"
        f"Field: {field_name}\n"
        f"Value: '{field_value or '(blank)'}'\n"
        f"Expected: {expected_error}\n"
        f"Remarks: {remarks or 'None'}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "negative", "land_certificate", "multiple")

    with allure.step("Select Multiple plot type and fill baseline"):
        land_page.select_plot_type("Multiple")
        page.locator("#no_of_plots").wait_for(state="visible", timeout=5000)

        # Fill baseline: valid multiple plot data
        page.locator("#no_of_plots").click()
        page.locator("#no_of_plots").fill("3")
        page.locator("#plot_number_school_building").click()
        page.locator("#plot_number_school_building").fill("1")
        # Select Contiguous=Yes as baseline (simplest valid path)
        page.locator("#renewal_yes").click()
        page.wait_for_timeout(1000)

    with allure.step(f"Overwrite '{field_name}' with invalid/blank value: '{field_value or ''}'"):
        if field_name == "no_of_plots":
            page.locator("#no_of_plots").click()
            page.locator("#no_of_plots").fill(str(field_value) if field_value is not None else "")

        elif field_name == "explanation":
            # Must set Contiguous=No + Boundary=No to make explanation required
            page.locator("#renewal_no").click()
            page.wait_for_timeout(1000)
            # Select Boundary=No (try get_by_role for the nested radio)
            page.get_by_role("radio", name="No").last.click()
            page.wait_for_timeout(1000)
            # Leave explanation blank (don't fill anything)

    with allure.step("Click Next to trigger validation"):
        land_page.click_next()
        page.wait_for_timeout(2000)

    with allure.step("Check if form was blocked"):
        form_navigated = not page.locator("#no_of_plots").is_visible()

        if form_navigated:
            page.get_by_text("Certificate of Land", exact=False).first.click()
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
            classification = remarks if remarks else "APPLICATION BEHAVIOR: Form accepted invalid data."
            allure.attach(
                f"FORM NAVIGATED: Field '{field_name}' with value '{field_value}' was accepted.\n"
                f"Expected error: '{expected_error}'\n"
                f"Classification: {classification}",
                name="Business Rule Verification Required",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected validation for '{field_name}' but form navigated. "
                f"Classification: {classification}"
            )
