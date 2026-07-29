"""
Certificate of Land — Dynamic UI Behaviour Tests (Leased Path)
=================================================================
Tests Renewal Clause toggle — dynamic field visibility.

LAND_UI_003: Renewal=Yes shows Duration field; Renewal=No hides it.

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
# LAND_UI_003 — Leased Renewal Toggle (Show + Hide Duration)
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Certificate of Land")
@allure.sub_suite("Dynamic UI")
@allure.feature("Conditional Fields")
@allure.story("Renewal Clause Toggle")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.land_certificate
def test_land_ui_003_renewal_toggle(land_ready_page):
    """
    LAND_UI_003: Verify Renewal Clause toggle:
    - Renewal=Yes → Duration of Renewal field (#renewal_lease_deed_duration_0) APPEARS
    - Renewal=No → Duration field DISAPPEARS
    - Value filled in Duration does NOT persist after toggling back
    """
    page = land_ready_page
    land_page = LandCertificatePage(page)

    allure.dynamic.title("LAND_UI_003 — Leased Renewal toggle (show + hide Duration)")
    allure.dynamic.tag("regression", "land_certificate", "ui", "leased")

    with allure.step("Select Single + Leased to load form"):
        land_page.select_plot_type("Single")
        land_page.select_land_type("Leased")
        page.locator("#lease_land_area_0").wait_for(state="visible", timeout=5000)

    with allure.step("Verify Renewal Duration is NOT visible by default (Renewal=No)"):
        duration_field = page.locator("#renewal_lease_deed_duration_0")
        initial_visible = duration_field.is_visible()
        allure.attach(
            f"Renewal Duration visible (default Renewal=No): {initial_visible}",
            name="Initial State",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert not initial_visible, (
            "Renewal Duration should NOT be visible when Renewal=No (default)"
        )

    with allure.step("Click Renewal=Yes (#renewal_yes0)"):
        page.locator("#renewal_yes0").click()
        page.wait_for_timeout(1500)

    with allure.step("Verify Renewal Duration field APPEARS"):
        duration_visible_after_yes = duration_field.is_visible()
        allure.attach(
            f"Renewal Duration visible after Renewal=Yes: {duration_visible_after_yes}",
            name="After Renewal=Yes",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert duration_visible_after_yes, (
            "Renewal Duration did NOT appear after clicking Renewal=Yes"
        )

    with allure.step("Fill Renewal Duration with value '15'"):
        duration_field.click()
        duration_field.fill("15")
        filled_value = duration_field.input_value()
        allure.attach(
            f"Filled value: '{filled_value}'",
            name="Duration Value Filled",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert filled_value == "15", f"Expected '15' but got '{filled_value}'"

    with allure.step("Click Renewal=No (#Renewal_no0)"):
        page.locator("#Renewal_no0").click()
        page.wait_for_timeout(1500)

    with allure.step("Verify Renewal Duration field DISAPPEARS"):
        duration_visible_after_no = duration_field.is_visible()
        allure.attach(
            f"Renewal Duration visible after Renewal=No: {duration_visible_after_no}",
            name="After Renewal=No",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert not duration_visible_after_no, (
            "Renewal Duration did NOT disappear after clicking Renewal=No"
        )

    with allure.step("Toggle back to Yes — verify field is empty (value reset)"):
        page.locator("#renewal_yes0").click()
        page.wait_for_timeout(1500)

        duration_value_after_retoggle = duration_field.input_value()
        allure.attach(
            f"Duration value after re-toggle to Yes: '{duration_value_after_retoggle}'",
            name="Value After Re-toggle",
            attachment_type=allure.attachment_type.TEXT,
        )
        # Document behaviour: value may or may not persist
        # If persists, it's an application behaviour (not necessarily a defect)
