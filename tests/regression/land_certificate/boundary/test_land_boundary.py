"""
Certificate of Land — Boundary Value Tests
=============================================
Tests field value min/max limits for Land Certificate fields.
Each test fills valid baseline + overwrites target field with boundary value.

Data Source: test_data/negative/Validation_Data.xlsx → "Land_Boundary"
Page Object: pages/land_certificate_page.py
Fixture: land_ready_page (conftest.py)

Phase 3 implements: LAND_BND_001–004 (Owned path)
Phase 4 adds: LAND_BND_005 (Leased path)
Phase 5 adds: LAND_BND_006–007 (Multiple path)
"""

import pytest
import allure
from datetime import datetime

from pages.land_certificate_page import LandCertificatePage
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

_all_boundary = [
    row for row in _excel.get_sheet_data("Land_Boundary")
    if str(row.get("execute", "")).lower() == "yes"
]

# Phase 3: Single_Owned flow
_owned_boundary = [
    row for row in _all_boundary
    if row.get("flow") == "Single_Owned"
]

# Phase 4: Single_Leased flow
_leased_boundary = [
    row for row in _all_boundary
    if row.get("flow") == "Single_Leased"
]

# Phase 5: Multiple flow
_multiple_boundary = [
    row for row in _all_boundary
    if row.get("flow") == "Multiple"
]


# ============================================================================
# BOUNDARY TESTS — Field Value Limits (Owned Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Boundary")
@allure.feature("Boundary Validation")
@allure.story("Boundary Value Scenarios — Single Owned")
@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _owned_boundary,
    ids=lambda s: s["scenario_id"],
)
def test_land_boundary(land_ready_page, scenario):
    """
    Verify field boundary values are handled correctly.
    Fills valid baseline, overwrites target field, then submits.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value", "")
    expected_outcome = scenario.get("expected_outcome", "ACCEPT")

    # Handle dynamic values
    if field_value == "TODAY":
        field_value = datetime.now().strftime("%d/%m/%Y")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Field: {field_name}\n"
        f"Value: '{field_value}' (length={len(str(field_value or ''))})\n"
        f"Expected outcome: {expected_outcome}\n"
        f"Message: {scenario.get('expected_message', '')}"
    )
    allure.dynamic.severity(allure.severity_level.NORMAL)
    allure.dynamic.tag("regression", "boundary", "land_certificate")

    with allure.step("Fill all mandatory fields with valid baseline + boundary target"):
        land_page.select_plot_type("Single")
        land_page.select_land_type("Owned")
        page.locator("#land_area_0").wait_for(state="visible", timeout=5000)

        # Fill ALL fields with valid baseline
        page.locator("#land_unit_0").select_option(label="Square Meter")
        page.locator("#land_area_0").click()
        page.locator("#land_area_0").fill("5000")
        page.locator("#situate_speci_0").click()
        page.locator("#situate_speci_0").fill("Survey No(s)")
        page.locator("#situated_at0").click()
        page.locator("#situated_at0").fill("Civil Lines, Jaipur")
        page.locator("#owned_by_0").click()
        page.locator("#owned_by_0").fill("Test Trust")
        page.locator("#land_title_doc0").select_option(label="Conveyance Deed")
        page.locator("#land_title0").click()
        page.locator("#land_title0").fill("REG-BND-TEST-001")
        page.locator("#executed_by0").click()
        page.locator("#executed_by0").fill("Mr. Boundary Test")
        page.locator("#regid_ofc_details0").click()
        page.locator("#regid_ofc_details0").fill("Sub-Registrar Office, Test")
        ValidationHelper.set_readonly_date(page, '#land_title_date0', "15/03/2020")

    with allure.step(f"Overwrite '{field_name}' with boundary value: '{str(field_value)[:50]}'"):
        if field_name == "land_area":
            page.locator("#land_area_0").click()
            page.locator("#land_area_0").fill(str(field_value))
        elif field_name == "document_date":
            ValidationHelper.set_readonly_date(page, '#land_title_date0', str(field_value))
        elif field_name == "situated_in":
            page.locator("#situate_speci_0").click()
            page.locator("#situate_speci_0").fill(str(field_value))

    with allure.step("Click Next to submit"):
        land_page.click_next()
        page.wait_for_timeout(3000)

    with allure.step(f"Verify outcome: {expected_outcome}"):
        form_navigated = not page.locator("#land_area_0").is_visible()

        if expected_outcome == "ACCEPT":
            if form_navigated:
                allure.attach(
                    f"PASS: Boundary value accepted — form navigated.",
                    name="Boundary Result",
                    attachment_type=allure.attachment_type.TEXT,
                )
                with allure.step("Navigate back to Certificate of Land"):
                    page.get_by_text("Certificate of Land", exact=False).first.click()
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
                page.get_by_text("Certificate of Land", exact=False).first.click()
                page.wait_for_timeout(2000)
                pytest.fail(
                    f"Expected REJECT but form accepted value '{str(field_value)[:50]}'."
                )


# ============================================================================
# BOUNDARY TESTS — Field Value Limits (Leased Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Boundary")
@allure.feature("Boundary Validation")
@allure.story("Boundary Value Scenarios — Single Leased")
@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _leased_boundary,
    ids=lambda s: s["scenario_id"],
)
def test_land_boundary_leased(land_ready_page, scenario):
    """
    Verify Leased path field boundary values are handled correctly.
    Fills valid baseline, overwrites target field, then submits.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value", "")
    expected_outcome = scenario.get("expected_outcome", "ACCEPT")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Flow: {scenario['flow']}\n"
        f"Field: {field_name}\n"
        f"Value: '{field_value}'\n"
        f"Expected outcome: {expected_outcome}"
    )
    allure.dynamic.severity(allure.severity_level.NORMAL)
    allure.dynamic.tag("regression", "boundary", "land_certificate", "leased")

    with allure.step("Fill all Leased fields with valid baseline"):
        land_page.select_plot_type("Single")
        land_page.select_land_type("Leased")
        page.locator("#lease_land_area_0").wait_for(state="visible", timeout=5000)

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
        page.locator("#Renewal_no0").click()
        page.wait_for_timeout(500)

    with allure.step(f"Overwrite '{field_name}' with boundary value: '{field_value}'"):
        if field_name == "lease_deed_duration":
            page.locator("#lease_deed_duration_0").click()
            page.locator("#lease_deed_duration_0").fill(str(field_value))

    with allure.step("Click Next to submit"):
        land_page.click_next()
        page.wait_for_timeout(3000)

    with allure.step(f"Verify outcome: {expected_outcome}"):
        form_navigated = not page.locator("#lease_land_area_0").is_visible()

        if expected_outcome == "ACCEPT":
            if form_navigated:
                allure.attach(
                    "PASS: Boundary value accepted — form navigated.",
                    name="Boundary Result",
                    attachment_type=allure.attachment_type.TEXT,
                )
                with allure.step("Navigate back to Certificate of Land"):
                    page.get_by_text("Certificate of Land", exact=False).first.click()
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
                page.get_by_text("Certificate of Land", exact=False).first.click()
                page.wait_for_timeout(2000)
                pytest.fail(
                    f"Expected REJECT but form accepted value '{field_value}'."
                )


# ============================================================================
# BOUNDARY TESTS — Field Value Limits (Multiple Plot Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Boundary")
@allure.feature("Boundary Validation")
@allure.story("Boundary Value Scenarios — Multiple Plots")
@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _multiple_boundary,
    ids=lambda s: s["scenario_id"],
)
def test_land_boundary_multiple(land_ready_page, scenario):
    """
    Verify Multiple Plot boundary values are handled correctly.
    Fills valid baseline, overwrites target field, then submits.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    field_name = scenario["field_name"]
    field_value = scenario.get("field_value", "")
    expected_outcome = scenario.get("expected_outcome", "ACCEPT")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Flow: {scenario['flow']}\n"
        f"Field: {field_name}\n"
        f"Value: '{field_value}'\n"
        f"Expected outcome: {expected_outcome}"
    )
    allure.dynamic.severity(allure.severity_level.NORMAL)
    allure.dynamic.tag("regression", "boundary", "land_certificate", "multiple")

    with allure.step("Select Multiple and fill baseline with boundary target"):
        land_page.select_plot_type("Multiple")
        page.locator("#no_of_plots").wait_for(state="visible", timeout=5000)

        # Fill baseline
        page.locator("#no_of_plots").click()
        page.locator("#no_of_plots").fill("3")
        page.locator("#plot_number_school_building").click()
        page.locator("#plot_number_school_building").fill("1")
        # Contiguous=Yes (simplest valid path)
        page.locator("#renewal_yes").click()
        page.wait_for_timeout(1000)

    with allure.step(f"Overwrite '{field_name}' with boundary value: '{field_value}'"):
        if field_name == "no_of_plots":
            page.locator("#no_of_plots").click()
            page.locator("#no_of_plots").fill(str(int(field_value)))
            # Adjust plot_number if needed (must be <= no_of_plots)
            page.locator("#plot_number_school_building").click()
            page.locator("#plot_number_school_building").fill("1")

    with allure.step("Click Next to submit"):
        land_page.click_next()
        page.wait_for_timeout(3000)

    with allure.step(f"Verify outcome: {expected_outcome}"):
        # SPA keeps DOM elements — check for no validation errors instead
        errors = ValidationHelper.get_all_errors(page, timeout=1000)
        form_navigated = len(errors) == 0

        if expected_outcome == "ACCEPT":
            if form_navigated:
                allure.attach(
                    "PASS: Boundary value accepted — form navigated.",
                    name="Boundary Result",
                    attachment_type=allure.attachment_type.TEXT,
                )
                with allure.step("Navigate back to Certificate of Land"):
                    page.get_by_text("Certificate of Land", exact=False).first.click()
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
                page.get_by_text("Certificate of Land", exact=False).first.click()
                page.wait_for_timeout(2000)
                pytest.fail(
                    f"Expected REJECT but form accepted value '{field_value}'."
                )
