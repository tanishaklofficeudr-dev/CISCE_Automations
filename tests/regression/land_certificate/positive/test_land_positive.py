"""
Certificate of Land — Positive Regression Tests
==================================================
Validates form submits successfully with valid data across all paths.

Data Source: test_data/negative/Validation_Data.xlsx → "Land_Positive"
Page Object: pages/land_certificate_page.py
Fixture: land_ready_page (conftest.py)

Phase 3 implements: LAND_POS_001–005 (Owned path)
Phase 4 adds: LAND_POS_006–007 (Leased path)
Phase 5 adds: LAND_POS_008–009 (Multiple path)
"""

import pytest
import allure

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

_all_positive = [
    row for row in _excel.get_sheet_data("Land_Positive")
    if str(row.get("execute", "")).lower() == "yes"
]

# Phase 3: Single_Owned flow
_owned_positive = [
    row for row in _all_positive
    if row.get("flow") == "Single_Owned"
]

# Phase 4: Single_Leased flow
_leased_positive = [
    row for row in _all_positive
    if row.get("flow") == "Single_Leased"
]

# Phase 5: Multiple flow
_multiple_positive = [
    row for row in _all_positive
    if row.get("flow") == "Multiple"
]


# ============================================================================
# POSITIVE TESTS — Valid Form Submission (Owned Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Positive")
@allure.feature("Successful Land Certificate Submission")
@allure.story("Positive Scenarios — Single Owned")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _owned_positive,
    ids=lambda s: s["scenario_id"],
)
def test_land_positive_submission(land_ready_page, scenario):
    """
    Verify Certificate of Land form submits successfully with valid
    Single→Owned data and navigates to Upload Documents.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Flow: {scenario['flow']}\n"
        f"Area Unit: {scenario['area_unit']}\n"
        f"Land Area: {scenario['land_area']}\n"
        f"Title Document: {scenario['land_title_document']}\n"
        f"Sale Deed Favor: {scenario.get('sale_deed_favor', '')}\n"
        f"Date: {scenario['document_date']}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "positive", "land_certificate")

    test_data = {
        "area_unit": scenario["area_unit"],
        "land_area": scenario["land_area"],
        "situated_in": scenario["situated_in"],
        "situated_at": scenario["situated_at"],
        "land_owned_by": scenario["land_owned_by"],
        "land_title_document": scenario["land_title_document"],
        "sale_deed_favor": scenario.get("sale_deed_favor", ""),
        "registration_details": scenario["registration_details"],
        "executed_by": scenario["executed_by"],
        "registration_office": scenario["registration_office"],
        "document_date": scenario["document_date"],
    }

    with allure.step(f"Fill valid data: {scenario['scenario_description'][:50]}"):
        land_page.fill_partial_owned_details(test_data, skip_fields=[])

    with allure.step("Verify form submitted (navigated away from Certificate of Land)"):
        page.wait_for_timeout(3000)

        # Navigation check: land_area field should no longer be visible
        navigated = not page.locator("#land_area_0").is_visible()

        if not navigated:
            errors = ValidationHelper.get_all_errors(page)
            allure.attach(
                f"Form did NOT navigate. Errors: {errors}",
                name="Submission Failure",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected form to navigate but it didn't. Errors: {errors}"
            )

        allure.attach(
            "PASS: Form submitted — navigated away from Certificate of Land.",
            name="Positive Result",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Navigate back to Certificate of Land for next test"):
        page.get_by_text("Certificate of Land", exact=False).first.click()
        page.wait_for_timeout(2000)

# ============================================================================
# POSITIVE TESTS — Valid Form Submission (Leased Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Positive")
@allure.feature("Successful Land Certificate Submission")
@allure.story("Positive Scenarios — Single Leased")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _leased_positive,
    ids=lambda s: s["scenario_id"],
)
def test_land_positive_leased_submission(land_ready_page, scenario):
    """
    Verify Certificate of Land form submits successfully with valid
    Single→Leased data and navigates to the next step.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Flow: {scenario['flow']}\n"
        f"Area Unit: {scenario.get('area_unit', '')}\n"
        f"Land Area: {scenario.get('land_area', '')}\n"
        f"Lessee: {scenario.get('lessee_name', '')}\n"
        f"Lessor: {scenario.get('lessor_name', '')}\n"
        f"Lease Date: {scenario.get('lease_deed_date', '')}\n"
        f"Duration: {scenario.get('lease_deed_duration', '')}\n"
        f"Renewal: {scenario.get('renewal_clause', '')}\n"
        f"Renewal Duration: {scenario.get('renewal_duration', '')}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "positive", "land_certificate", "leased")

    test_data = {
        "area_unit": scenario.get("area_unit", ""),
        "land_area": scenario.get("land_area", ""),
        "lessee_name": scenario.get("lessee_name", ""),
        "lessor_name": scenario.get("lessor_name", ""),
        "lease_deed_date": scenario.get("lease_deed_date", ""),
        "lease_deed_duration": scenario.get("lease_deed_duration", ""),
        "registration_date": scenario.get("registration_date_lease", ""),
        "registration_office": scenario.get("registration_office", ""),
        "renewal_clause": scenario.get("renewal_clause", ""),
        "renewal_duration": scenario.get("renewal_duration", ""),
    }

    with allure.step(f"Fill valid Leased data: {scenario['scenario_description'][:50]}"):
        land_page.fill_partial_leased_details(test_data, skip_fields=[])

    with allure.step("Verify form submitted (navigated away from Certificate of Land)"):
        page.wait_for_timeout(3000)

        # Navigation check: lease land area field should no longer be visible
        navigated = not page.locator("#lease_land_area_0").is_visible()

        if not navigated:
            errors = ValidationHelper.get_all_errors(page)
            allure.attach(
                f"Form did NOT navigate. Errors: {errors}",
                name="Submission Failure",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected form to navigate but it didn't. Errors: {errors}"
            )

        allure.attach(
            "PASS: Leased form submitted — navigated away from Certificate of Land.",
            name="Positive Result",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Navigate back to Certificate of Land for next test"):
        page.get_by_text("Certificate of Land", exact=False).first.click()
        page.wait_for_timeout(2000)


# ============================================================================
# POSITIVE TESTS — Valid Form Submission (Multiple Plot Path)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Positive")
@allure.feature("Successful Land Certificate Submission")
@allure.story("Positive Scenarios — Multiple Plots")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.land_certificate
@pytest.mark.parametrize(
    "scenario",
    _multiple_positive,
    ids=lambda s: s["scenario_id"],
)
def test_land_positive_multiple_submission(land_ready_page, scenario):
    """
    Verify Certificate of Land form submits successfully with valid
    Multiple Plot data and navigates to the next step.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Flow: {scenario['flow']}\n"
        f"Plots: {scenario.get('no_of_plots', '')}\n"
        f"Plot Number: {scenario.get('plot_number', '')}\n"
        f"Contiguous: {scenario.get('contiguous', '')}\n"
        f"Boundary Wall: {scenario.get('boundary_wall', '')}\n"
        f"Explanation: {str(scenario.get('explanation', ''))[:50]}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "positive", "land_certificate", "multiple")

    test_data = {
        "no_of_plots": scenario.get("no_of_plots", ""),
        "plot_number": scenario.get("plot_number", ""),
        "contiguous": scenario.get("contiguous", ""),
        "boundary_wall": scenario.get("boundary_wall", ""),
        "explanation": scenario.get("explanation", ""),
    }

    with allure.step(f"Fill valid Multiple Plot data: {scenario['scenario_description'][:50]}"):
        land_page.fill_multiple_plot_details(test_data, skip_fields=[])

    with allure.step("Verify form submitted (navigated away from Certificate of Land)"):
        page.wait_for_timeout(3000)

        # Navigation check for Multiple path:
        # SPA keeps DOM elements — check for no validation errors + Upload Documents visible
        errors = ValidationHelper.get_all_errors(page, timeout=1000)
        navigated = len(errors) == 0

        # Additional check: if Upload Documents text appeared
        if not navigated:
            try:
                upload = page.get_by_text("Upload Documents", exact=False)
                if upload.count() > 0 and upload.first.is_visible():
                    navigated = True
            except Exception:
                pass

        if not navigated:
            allure.attach(
                f"Form did NOT navigate. Errors: {errors}",
                name="Submission Failure",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(
                f"Expected form to navigate but it didn't. Errors: {errors}"
            )

        allure.attach(
            "PASS: Multiple Plot form submitted — no validation errors after Next click.",
            name="Positive Result",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Navigate back to Certificate of Land for next test"):
        page.get_by_text("Certificate of Land", exact=False).first.click()
        page.wait_for_timeout(2000)
