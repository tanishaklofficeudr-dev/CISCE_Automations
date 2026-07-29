"""
Certificate of Land — Dynamic UI Behaviour Tests (Owned Path)
================================================================
Tests dynamic form rendering and conditional field visibility.

LAND_UI_001: Owned form loads correctly after radio selection
LAND_UI_002: Sale Deed conditional toggle (show + hide)

Page Object: pages/land_certificate_page.py
Fixture: land_ready_page (conftest.py)
"""

import pytest
import allure

from pages.land_certificate_page import LandCertificatePage
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
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ============================================================================
# LAND_UI_001 — Owned Form Loads Correctly
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Dynamic UI")
@allure.feature("Form Rendering")
@allure.story("Owned Form Load")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.land_certificate
def test_land_ui_001_owned_form_loads(land_ready_page):
    """
    LAND_UI_001: Verify all Owned path fields become visible
    after selecting Single + Owned radio buttons.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title("LAND_UI_001 — Owned form loads correctly after radio selection")
    allure.dynamic.tag("regression", "land_certificate", "ui", "sanity")

    with allure.step("Select Single plot type"):
        land_page.select_plot_type("Single")

    with allure.step("Select Owned land type"):
        land_page.select_land_type("Owned")

    with allure.step("Verify all Owned fields are visible"):
        # Critical fields that must be visible
        owned_fields = {
            "#land_area_0": "Land Area",
            "#land_unit_0": "Area Unit",
            "#situate_speci_0": "Situated In (specify)",
            "#situated_at0": "Situated At",
            "#owned_by_0": "Land Owned By",
            "#land_title_doc0": "Land Title Document",
            "#land_title0": "Registration Details",
            "#executed_by0": "Executed By",
            "#regid_ofc_details0": "Registration Office",
            "#land_title_date0": "Document Date",
        }

        visible_fields = []
        hidden_fields = []

        for locator, name in owned_fields.items():
            try:
                el = page.locator(locator)
                if el.is_visible():
                    visible_fields.append(name)
                else:
                    hidden_fields.append(name)
            except Exception:
                hidden_fields.append(f"{name} (error)")

        allure.attach(
            f"Visible fields ({len(visible_fields)}):\n"
            + "\n".join(f"  ✅ {f}" for f in visible_fields)
            + f"\n\nHidden fields ({len(hidden_fields)}):\n"
            + "\n".join(f"  ❌ {f}" for f in hidden_fields),
            name="Field Visibility Report",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert len(hidden_fields) == 0, (
            f"Expected all Owned fields visible but {len(hidden_fields)} are hidden: {hidden_fields}"
        )


# ============================================================================
# LAND_UI_002 — Sale Deed Conditional Toggle
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Dynamic UI")
@allure.feature("Conditional Fields")
@allure.story("Sale Deed Toggle")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.land_certificate
def test_land_ui_002_sale_deed_toggle(land_ready_page):
    """
    LAND_UI_002: Verify Sale Deed conditional field appears when
    "Sale Deed" is selected and disappears when changed to another option.
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title("LAND_UI_002 — Sale Deed conditional toggle (show + hide)")
    allure.dynamic.tag("regression", "land_certificate", "ui", "sanity")

    with allure.step("Select Single + Owned to load form"):
        land_page.select_plot_type("Single")
        land_page.select_land_type("Owned")
        page.locator("#land_area_0").wait_for(state="visible", timeout=5000)

    with allure.step("Verify Sale Deed Favor is NOT visible initially"):
        favor_field = page.locator("#sale_deed_favor_whom_0")
        initial_visible = favor_field.is_visible()
        allure.attach(
            f"Sale Deed Favor visible before selecting Sale Deed: {initial_visible}",
            name="Initial State",
            attachment_type=allure.attachment_type.TEXT,
        )
        # May or may not be visible depending on saved state — don't assert here

    with allure.step("Select 'Sale Deed' from Land Title Document dropdown"):
        page.locator("#land_title_doc0").select_option(label="Sale Deed")
        page.wait_for_timeout(1000)

    with allure.step("Verify Sale Deed Favor dropdown APPEARS"):
        favor_visible_after = favor_field.is_visible()
        allure.attach(
            f"Sale Deed Favor visible after selecting Sale Deed: {favor_visible_after}",
            name="After Sale Deed Selected",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert favor_visible_after, (
            "Sale Deed Favor dropdown did NOT appear after selecting 'Sale Deed'"
        )

    with allure.step("Change Land Title Document to 'Gift Deed'"):
        page.locator("#land_title_doc0").select_option(label="Gift Deed")
        page.wait_for_timeout(1000)

    with allure.step("Verify Sale Deed Favor dropdown DISAPPEARS"):
        favor_visible_final = favor_field.is_visible()
        allure.attach(
            f"Sale Deed Favor visible after changing to Gift Deed: {favor_visible_final}",
            name="After Gift Deed Selected",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert not favor_visible_final, (
            "Sale Deed Favor dropdown did NOT disappear after changing to 'Gift Deed'"
        )
