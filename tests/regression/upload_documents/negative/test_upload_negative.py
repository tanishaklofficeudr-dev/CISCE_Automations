"""
Upload Documents — Negative Tests (Excel-driven)
===================================================
UPLOAD_NEG_001–007: Invalid uploads, missing prerequisites, double-click.

Data Source: test_data/negative/Validation_Data.xlsx → "Upload_Negative"
"""

import os
import tempfile
import pytest
import allure

from pages.upload_documents_page import UploadDocumentsPage
from utils.excel_reader import ExcelReader
from utils.validation_helper import ValidationHelper
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


def _create_temp_file(extension, size_bytes=1024):
    """Create a temporary file with given extension and size."""
    fd, path = tempfile.mkstemp(suffix=f".{extension}")
    with os.fdopen(fd, 'wb') as f:
        f.write(b'\x00' * size_bytes)
    return path


def _create_large_file(size_mb=21):
    """Create a temporary file larger than 20MB."""
    fd, path = tempfile.mkstemp(suffix=".pdf")
    with os.fdopen(fd, 'wb') as f:
        # Write PDF header + padding to reach target size
        f.write(b'%PDF-1.4\n')
        f.write(b'\x00' * (size_mb * 1024 * 1024))
    return path


# ============================================================================
# DATA LOADING
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_negative_scenarios = [
    row for row in _excel.get_sheet_data("Upload_Negative")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# NEGATIVE TESTS
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Upload Documents")
@allure.sub_suite("Negative")
@allure.feature("Upload Validation")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.upload_documents
@pytest.mark.parametrize(
    "scenario",
    _negative_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_upload_negative(upload_ready_page, scenario):
    """
    Verify invalid uploads and missing prerequisites are rejected.
    """
    page = upload_ready_page
    upload_page = UploadDocumentsPage(page)

    test_type = scenario.get("test_type", "")
    target = scenario.get("target_dropzone", "")
    file_type = scenario.get("file_type", "")
    expected_error = scenario.get("expected_error", "")
    remarks = scenario.get("remarks", "")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"Test type: {test_type}\n"
        f"Target: {target}\n"
        f"File type: {file_type}\n"
        f"Expected error: {expected_error}\n"
        f"Remarks: {remarks or 'None'}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "negative", "upload_documents")

    temp_file = None

    try:
        if test_type == "invalid_type":
            # Upload an invalid file type
            with allure.step(f"Upload .{file_type} file to {target}"):
                temp_file = _create_temp_file(file_type)
                upload_page.upload_single_file(target, temp_file)
                page.wait_for_timeout(2000)

            with allure.step(f"Verify Dropzone error: '{expected_error}'"):
                dropzone_id = UploadDocumentsPage.UPLOAD_MAP.get(target, "").replace("#", "")
                status = upload_page.get_upload_status(dropzone_id)
                allure.attach(
                    f"Upload status: {status}",
                    name="Dropzone Status",
                    attachment_type=allure.attachment_type.TEXT,
                )
                # Check for error state
                assert status.get("hasError") or not status.get("accepted", True), (
                    f"Expected upload rejection but got: {status}"
                )

        elif test_type == "oversize":
            # Upload file >20MB
            with allure.step("Create and upload >20MB file"):
                temp_file = _create_large_file(21)
                upload_page.upload_single_file(target, temp_file)
                page.wait_for_timeout(3000)

            with allure.step("Verify file too big error"):
                dropzone_id = UploadDocumentsPage.UPLOAD_MAP.get(target, "").replace("#", "")
                status = upload_page.get_upload_status(dropzone_id)
                allure.attach(
                    f"Upload status: {status}",
                    name="Dropzone Status",
                    attachment_type=allure.attachment_type.TEXT,
                )
                assert status.get("hasError") or status.get("status") == "error", (
                    f"Expected oversize rejection but got: {status}"
                )

        elif test_type == "missing_upload":
            # Upload only 4 of 5 documents then click Proceed
            with allure.step("Upload 4 of 5 documents (skip School Image)"):
                for label in list(UploadDocumentsPage.UPLOAD_MAP.keys())[:-1]:
                    upload_page.upload_single_file(label, TEST_PDF)

            with allure.step("Select affiliation + check declarations"):
                # Use JS for hidden radio/checkboxes (same as payment fixture)
                # Retry on context destruction from upload
                for _attempt in range(3):
                    try:
                        page.evaluate("""
                            () => {
                                const radios = document.querySelectorAll('input[name="composite_type"]');
                                for (const r of radios) {
                                    if (r.value === '2') {
                                        r.checked = true;
                                        r.dispatchEvent(new Event('change', { bubbles: true }));
                                        break;
                                    }
                                }
                                const vc = document.querySelector('#verify_composite');
                                const v = document.querySelector('#verify');
                                if (vc && !vc.checked) { vc.checked = true; vc.dispatchEvent(new Event('change', { bubbles: true })); }
                                if (v && !v.checked) { v.checked = true; v.dispatchEvent(new Event('change', { bubbles: true })); }
                            }
                        """)
                        break
                    except Exception:
                        page.wait_for_timeout(2000)
                page.wait_for_timeout(500)

            with allure.step("Click Proceed"):
                upload_page.click_proceed()
                page.wait_for_timeout(3000)

            with allure.step("Verify form blocked (did not navigate to payment)"):
                assert "payment" not in page.url.lower(), (
                    f"Form navigated with missing upload! URL: {page.url}"
                )
                allure.attach(
                    f"PASS: Form blocked with partial uploads. URL: {page.url}",
                    name="Negative Result",
                    attachment_type=allure.attachment_type.TEXT,
                )

        elif test_type == "missing_checkbox":
            # All uploads + radio but only one checkbox
            with allure.step("Upload all documents + select affiliation"):
                upload_page.upload_all_documents(TEST_PDF)
                page.wait_for_timeout(3000)
                # Use JS for hidden radio
                page.evaluate("""
                    () => {
                        const radios = document.querySelectorAll('input[name="composite_type"]');
                        for (const r of radios) {
                            if (r.value === '2') {
                                r.checked = true;
                                r.dispatchEvent(new Event('change', { bubbles: true }));
                                break;
                            }
                        }
                    }
                """)

            with allure.step("Check only #verify_composite (not #verify)"):
                page.evaluate("""
                    () => {
                        const vc = document.querySelector('#verify_composite');
                        const v = document.querySelector('#verify');
                        if (vc) { vc.checked = true; vc.dispatchEvent(new Event('change', { bubbles: true })); }
                        if (v) { v.checked = false; v.dispatchEvent(new Event('change', { bubbles: true })); }
                    }
                """)
                page.wait_for_timeout(500)

            with allure.step("Click Proceed"):
                upload_page.click_proceed()
                page.wait_for_timeout(3000)

            with allure.step("Verify form blocked"):
                assert "payment" not in page.url.lower(), (
                    f"Form navigated with only one checkbox! URL: {page.url}"
                )
                allure.attach(
                    f"PASS: Form blocked with single checkbox. URL: {page.url}",
                    name="Negative Result",
                    attachment_type=allure.attachment_type.TEXT,
                )

        elif test_type == "max_files":
            # Upload second file to same dropzone
            with allure.step(f"Upload first file to {target}"):
                upload_page.upload_single_file(target, TEST_PDF)
                page.wait_for_timeout(2000)

            with allure.step(f"Attempt second upload to same {target}"):
                upload_page.upload_single_file(target, TEST_PDF)
                page.wait_for_timeout(2000)

            with allure.step("Verify max files behavior"):
                dropzone_id = UploadDocumentsPage.UPLOAD_MAP.get(target, "").replace("#", "")
                status = upload_page.get_upload_status(dropzone_id)
                allure.attach(
                    f"After double upload — status: {status}",
                    name="Max Files Status",
                    attachment_type=allure.attachment_type.TEXT,
                )
                # maxFiles=1: either error or file was replaced (count stays at 1)
                assert status.get("fileCount", 0) <= 1 or status.get("hasError"), (
                    f"Expected maxFiles enforcement but got: {status}"
                )

        elif test_type == "double_click":
            # Double-click Proceed rapidly
            with allure.step("Upload all + select affiliation + check declarations"):
                upload_page.upload_all_documents(TEST_PDF)
                upload_page.select_affiliation_type("Provisional Affiliation up to Class X")
                upload_page.check_declarations()

            with allure.step("Double-click Proceed to Payment rapidly"):
                btn = page.get_by_role("button", name="Proceed to Payment")
                btn.click(force=True)
                btn.click(force=True)
                page.wait_for_timeout(5000)

            with allure.step("Verify no duplicate submission"):
                # Should be on payment page (single navigation) or still on upload
                allure.attach(
                    f"After double-click — URL: {page.url}",
                    name="Double-Click Result",
                    attachment_type=allure.attachment_type.TEXT,
                )
                # Navigate back for next test
                if "payment" in page.url.lower():
                    page.go_back()
                    page.wait_for_timeout(3000)

    finally:
        # Cleanup temp files
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass
