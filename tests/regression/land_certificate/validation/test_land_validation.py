"""
Certificate of Land — Required Field Validation Tests
=======================================================
Consolidated tests verifying mandatory fields show errors
when forms are submitted with all fields blank/cleared.

LAND_VAL_001: Single→Owned — all blank
LAND_VAL_002: Single→Leased — all blank (Phase 4)
LAND_VAL_003: Multiple — all blank (Phase 5)

Execution: Must run FIRST in Land Certificate suite (@first_run marker).
"""

import pytest
import allure

from pages.land_certificate_page import LandCertificatePage
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


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
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ============================================================================
# LAND_VAL_001 — Single → Owned — All Fields Blank
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Validation")
@allure.feature("Mandatory Field Validation")
@allure.story("Owned Path — All Mandatory Fields Empty")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.land_certificate
@pytest.mark.first_run
def test_land_val_001_owned_all_blank(land_ready_page):
    """
    LAND_VAL_001: Verify all mandatory fields display validation errors
    when Single→Owned form is submitted with all text fields blank.

    Confirmed validation messages:
      - "Please enter a valid land area"
      - "Please specify where it is situated"
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title("LAND_VAL_001 — Owned: All mandatory fields blank shows errors")
    allure.dynamic.tag("regression", "validation", "land_certificate", "sanity")

    with allure.step("Select Single plot type"):
        land_page.select_plot_type("Single")

    with allure.step("Select Owned land type"):
        land_page.select_land_type("Owned")

    with allure.step("Wait for form fields to load"):
        page.locator("#land_area_0").wait_for(state="visible", timeout=5000)

    with allure.step("Clear all text fields"):
        page.locator("#land_area_0").click()
        page.locator("#land_area_0").fill("")
        page.locator("#situate_speci_0").click()
        page.locator("#situate_speci_0").fill("")
        page.locator("#situated_at0").click()
        page.locator("#situated_at0").fill("")
        page.locator("#owned_by_0").click()
        page.locator("#owned_by_0").fill("")
        page.locator("#land_title0").click()
        page.locator("#land_title0").fill("")
        page.locator("#executed_by0").click()
        page.locator("#executed_by0").fill("")
        page.locator("#regid_ofc_details0").click()
        page.locator("#regid_ofc_details0").fill("")

    with allure.step("Clear date field via JS injection"):
        ValidationHelper.set_readonly_date(page, '#land_title_date0', "")

    with allure.step("Click Next to trigger validation"):
        land_page.click_next()

    with allure.step("Verify form is blocked (validation errors displayed)"):
        page.wait_for_timeout(2000)
        errors = ValidationHelper.get_all_errors(page)
        assert len(errors) >= 1, (
            f"Expected at least 1 validation error but found {len(errors)}. "
            f"Visible errors: {errors}"
        )

        allure.attach(
            f"Validation errors found ({len(errors)}):\n" + "\n".join(f"  - {e}" for e in errors),
            name="Required Field Errors",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Verify confirmed validation messages"):
        expected_messages = [
            "Please enter a valid land area",
            "Please specify where it is situated",
        ]
        for expected in expected_messages:
            ValidationHelper.assert_error_present(page, expected)


# ============================================================================
# LAND_VAL_002 — Single → Leased — All Fields Blank
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Validation")
@allure.feature("Mandatory Field Validation")
@allure.story("Leased Path — All Mandatory Fields Empty")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.land_certificate
def test_land_val_002_leased_all_blank(land_ready_page):
    """
    LAND_VAL_002: Verify mandatory fields display validation errors
    when Single→Leased form is submitted with all fields blank.

    Confirmed validation messages (from diagnostic):
      - "Please enter the lease land area"
      - "Please enter the leaser name"
      - "Please select a valid date for the 'Date of Lease Deed'"
      - "Please enter the lease deed duration"
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title("LAND_VAL_002 — Leased: All mandatory fields blank shows errors")
    allure.dynamic.tag("regression", "validation", "land_certificate", "sanity", "leased")

    with allure.step("Select Single plot type"):
        land_page.select_plot_type("Single")

    with allure.step("Select Leased land type"):
        land_page.select_land_type("Leased")

    with allure.step("Wait for Leased form fields to load"):
        page.locator("#lease_land_area_0").wait_for(state="visible", timeout=5000)

    with allure.step("Clear all text fields"):
        page.locator("#lease_land_area_0").click()
        page.locator("#lease_land_area_0").fill("")
        page.locator("#leease_name_0").click()
        page.locator("#leease_name_0").fill("")
        page.locator("#leaser_name_0").click()
        page.locator("#leaser_name_0").fill("")
        page.locator("#lease_deed_duration_0").click()
        page.locator("#lease_deed_duration_0").fill("")
        page.locator("#details_regis_ofc0").click()
        page.locator("#details_regis_ofc0").fill("")

    with allure.step("Clear date fields via JS injection"):
        ValidationHelper.set_readonly_date(page, '#lease_deed_date_0', "")
        ValidationHelper.set_readonly_date(page, '#date_regis_lease_deed0', "")

    with allure.step("Click Next to trigger validation"):
        land_page.click_next()

    with allure.step("Verify form is blocked (validation errors displayed)"):
        page.wait_for_timeout(2000)
        errors = ValidationHelper.get_all_errors(page)
        assert len(errors) >= 1, (
            f"Expected at least 1 validation error but found {len(errors)}. "
            f"Visible errors: {errors}"
        )

        allure.attach(
            f"Validation errors found ({len(errors)}):\n" + "\n".join(f"  - {e}" for e in errors),
            name="Required Field Errors",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Verify confirmed validation messages"):
        expected_messages = [
            "Please enter the lease land area",
            "Please enter the leaser name",
            "Please select a valid date",
            "Please enter the lease deed duration",
        ]
        for expected in expected_messages:
            ValidationHelper.assert_error_present(page, expected)


# ============================================================================
# LAND_VAL_003 — Multiple Plot — All Fields Blank
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Validation")
@allure.feature("Mandatory Field Validation")
@allure.story("Multiple Plot — All Mandatory Fields Empty")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.land_certificate
def test_land_val_003_multiple_all_blank(land_ready_page):
    """
    LAND_VAL_003: Verify mandatory fields display validation errors
    when Multiple Plot form is submitted with all fields blank.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title("LAND_VAL_003 — Multiple: All mandatory fields blank shows errors")
    allure.dynamic.tag("regression", "validation", "land_certificate", "sanity", "multiple")

    with allure.step("Select Multiple plot type"):
        land_page.select_plot_type("Multiple")

    with allure.step("Wait for Multiple form fields to load"):
        page.locator("#no_of_plots").wait_for(state="visible", timeout=5000)

    with allure.step("Clear all fields"):
        page.locator("#no_of_plots").click()
        page.locator("#no_of_plots").fill("")
        page.locator("#plot_number_school_building").click()
        page.locator("#plot_number_school_building").fill("")

    with allure.step("Click Next to trigger validation"):
        land_page.click_next()

    with allure.step("Verify form is blocked (validation errors displayed)"):
        page.wait_for_timeout(2000)
        errors = ValidationHelper.get_all_errors(page)
        assert len(errors) >= 1, (
            f"Expected at least 1 validation error but found {len(errors)}. "
            f"Visible errors: {errors}"
        )

        allure.attach(
            f"Validation errors found ({len(errors)}):\n" + "\n".join(f"  - {e}" for e in errors),
            name="Required Field Errors",
            attachment_type=allure.attachment_type.TEXT,
        )
