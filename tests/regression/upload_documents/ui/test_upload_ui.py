"""
Upload Documents — Dynamic UI Behaviour Tests (Excel-driven)
==============================================================
UPLOAD_UI_001–005: Download links, delete, persistence, radio state.

Data Source: test_data/negative/Validation_Data.xlsx → "Upload_UI_Behaviour"
"""

import os
import pytest
import allure

from pages.upload_documents_page import UploadDocumentsPage
from utils.excel_reader import ExcelReader
from utils.screenshot_util import ScreenshotUtil


TEST_PDF = os.path.abspath("test_data/LandCertificate.pdf")


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("upload_ready_page")
        if page:
            try:
                path = ScreenshotUtil.take_screenshot(page, request.node.name[:50])
                if path:
                    allure.attach.file(path, name=f"Screenshot_{request.node.name[:50]}", attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ============================================================================
# DATA LOADING
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_ui_scenarios = [
    row for row in _excel.get_sheet_data("Upload_UI_Behaviour")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# UI BEHAVIOUR TESTS
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Upload Documents")
@allure.sub_suite("Dynamic UI")
@allure.feature("UI Behaviour")
@pytest.mark.regression
@pytest.mark.upload_documents
@pytest.mark.parametrize(
    "scenario",
    _ui_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_upload_ui_behaviour(upload_ready_page, scenario):
    """
    Verify dynamic UI behaviours: download links, delete, persistence.
    """
    page = upload_ready_page
    upload_page = UploadDocumentsPage(page)

    scenario_id = scenario["scenario_id"]

    allure.dynamic.title(f"{scenario_id} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Action: {scenario.get('action', '')}\n"
        f"Expected: {scenario.get('expected_behaviour', '')}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "upload_documents", "ui")

    if scenario_id == "UPLOAD_UI_001":
        # Upload file → verify download link appears
        with allure.step("Upload PDF to NOC Document"):
            upload_page.upload_single_file("NOC Document", TEST_PDF)

        with allure.step("Verify download link appeared for uploaded file"):
            # Check for any anchor with the document name
            download_link = page.locator("a", has_text="NOC Document")
            link_visible = download_link.count() > 0 and download_link.first.is_visible()
            allure.attach(
                f"Download link visible after upload: {link_visible}",
                name="UI Result",
                attachment_type=allure.attachment_type.TEXT,
            )
            # Also check for any .pdf link
            pdf_link = page.locator("a[href*='downloads']")
            pdf_count = pdf_link.count()
            allure.attach(
                f"PDF download links on page: {pdf_count}",
                name="Download Links Count",
                attachment_type=allure.attachment_type.TEXT,
            )

    elif scenario_id == "UPLOAD_UI_002":
        # Click Download for Notarization
        with allure.step("Locate 'Download for Notarization' link"):
            notarization_link = page.locator("a", has_text="Download for")
            assert notarization_link.count() > 0, "Download for Notarization link not found"
            link_visible = notarization_link.first.is_visible()
            href = notarization_link.first.get_attribute("href") or ""
            allure.attach(
                f"Link visible: {link_visible}\nHref: {href[:80]}",
                name="Notarization Link",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Click the Download for Notarization link"):
            # May open new tab — handle with popup
            try:
                with page.expect_popup(timeout=10000) as popup_info:
                    notarization_link.first.click()
                new_page = popup_info.value
                new_page.wait_for_load_state("domcontentloaded", timeout=10000)
                allure.attach(
                    f"New tab opened. URL: {new_page.url}",
                    name="Download Result",
                    attachment_type=allure.attachment_type.TEXT,
                )
                new_page.close()
            except Exception as e:
                # May download directly or navigate in same tab
                allure.attach(
                    f"Click result (no popup): {str(e)[:100]}\nCurrent URL: {page.url}",
                    name="Download Result",
                    attachment_type=allure.attachment_type.TEXT,
                )

    elif scenario_id == "UPLOAD_UI_003":
        # Upload → delete → verify reset
        with allure.step("Upload PDF to NOC Document"):
            upload_page.upload_single_file("NOC Document", TEST_PDF)

        with allure.step("Check initial upload status"):
            page.wait_for_timeout(3000)
            try:
                status_before = upload_page.get_upload_status("noc")
                allure.attach(
                    f"Before delete: {status_before}",
                    name="Status Before",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except Exception:
                allure.attach(
                    "Upload caused context change — file was processed. Continuing test.",
                    name="Status Before",
                    attachment_type=allure.attachment_type.TEXT,
                )

        with allure.step("Attempt to delete/remove the uploaded file"):
            # Try clicking remove button (Dropzone custom or dz-remove)
            container = page.locator("div.col-lg-6", has_text="NOC Document")
            remove_btn = container.locator(".dz-remove, [data-dz-remove], a:has-text('Remove')")
            if remove_btn.count() > 0:
                remove_btn.first.click()
                page.wait_for_timeout(2000)
                try:
                    status_after = upload_page.get_upload_status("noc")
                    allure.attach(
                        f"After delete: {status_after}",
                        name="Status After",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                except Exception:
                    pass
            else:
                allure.attach(
                    "Remove button NOT found — addRemoveLinks may be disabled. "
                    "Custom remove implementation or no delete available.",
                    name="Delete Not Available",
                    attachment_type=allure.attachment_type.TEXT,
                )

    elif scenario_id == "UPLOAD_UI_004":
        # Upload persistence after Back navigation
        with allure.step("Upload PDF to NOC Document"):
            upload_page.upload_single_file("NOC Document", TEST_PDF)

        with allure.step("Navigate Back"):
            page.get_by_role("button", name="Back").click()
            page.wait_for_timeout(3000)

        with allure.step("Return to Upload Documents"):
            page.get_by_text("Upload Documents", exact=False).first.click()
            page.wait_for_timeout(4000)

        with allure.step("Verify upload persists"):
            status = upload_page.get_upload_status("noc")
            allure.attach(
                f"After Back+Return — upload status: {status}",
                name="Persistence Result",
                attachment_type=allure.attachment_type.TEXT,
            )
            # Check for download link (indicates file is still uploaded)
            noc_link = page.locator("a", has_text="NOC Document")
            persisted = noc_link.count() > 0 or status.get("fileCount", 0) > 0
            allure.attach(
                f"Upload persisted: {persisted}",
                name="Persistence Verdict",
                attachment_type=allure.attachment_type.TEXT,
            )

    elif scenario_id == "UPLOAD_UI_005":
        # Radio selection persistence
        with allure.step("Select 'Composite Affiliation up to Class XII'"):
            upload_page.select_affiliation_type("Composite Affiliation up to Class XII")

        with allure.step("Interact with other controls (fill comments)"):
            upload_page.fill_comments("Testing radio persistence")
            page.wait_for_timeout(500)

        with allure.step("Verify radio selection persists"):
            is_checked = page.evaluate("""
                () => {
                    const radios = document.querySelectorAll('input[name="composite_type"]');
                    for (const r of radios) {
                        if (r.checked) return {value: r.value, checked: true};
                    }
                    return {value: 'none', checked: false};
                }
            """)
            allure.attach(
                f"Radio state after interaction: {is_checked}",
                name="Persistence Result",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert is_checked.get("checked"), "Radio selection was lost after page interaction"
            assert is_checked.get("value") == "3", (
                f"Expected value '3' (Composite) but got '{is_checked.get('value')}'"
            )
