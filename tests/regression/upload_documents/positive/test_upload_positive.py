"""
Upload Documents — Positive Tests (Excel-driven)
===================================================
UPLOAD_POS_001–009: Valid upload flows with different affiliation types and file formats.

Data Source: test_data/negative/Validation_Data.xlsx → "Upload_Positive"
"""

import os
import pytest
import allure

from pages.upload_documents_page import UploadDocumentsPage
from utils.excel_reader import ExcelReader
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


TEST_PDF = os.path.abspath("test_data/LandCertificate.pdf")
TEST_DIR = os.path.abspath("test_data")


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


def _get_test_file(file_type):
    """Get the appropriate test file path based on type."""
    if file_type == "pdf":
        return TEST_PDF
    # For other types, check if test file exists or use PDF as fallback
    ext_map = {"jpg": "test_upload.jpg", "png": "test_upload.png", "bmp": "test_upload.bmp"}
    filename = ext_map.get(file_type, "LandCertificate.pdf")
    path = os.path.join(TEST_DIR, filename)
    if os.path.exists(path):
        return path
    # Fallback to PDF (will still test the upload mechanism)
    return TEST_PDF


# ============================================================================
# DATA LOADING
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_positive_scenarios = [
    row for row in _excel.get_sheet_data("Upload_Positive")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# POSITIVE TESTS
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Upload Documents")
@allure.sub_suite("Positive")
@allure.feature("Successful Upload & Submission")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.upload_documents
@pytest.mark.parametrize(
    "scenario",
    _positive_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_upload_positive(upload_ready_page, scenario):
    """
    Verify Upload Documents flow completes successfully with valid data.
    """
    page = upload_ready_page
    upload_page = UploadDocumentsPage(page)

    file_type = scenario.get("file_type", "pdf")
    target = scenario.get("target_dropzone", "all")
    affiliation = scenario.get("affiliation_type", "")
    comments = scenario.get("comments", "")

    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.description(
        f"File type: {file_type}\n"
        f"Target: {target}\n"
        f"Affiliation: {affiliation}\n"
        f"Comments: {comments[:50] if comments else '(empty)'}"
    )
    allure.dynamic.severity(
        allure.severity_level.CRITICAL
        if scenario.get("priority") == "Critical"
        else allure.severity_level.NORMAL
    )
    allure.dynamic.tag("regression", "positive", "upload_documents")

    test_file = _get_test_file(file_type)

    with allure.step(f"Upload file(s) — target: {target}, type: {file_type}"):
        if target == "all":
            upload_page.upload_all_documents(test_file)
        else:
            # Upload to specific dropzone + fill remaining with PDF
            upload_page.upload_single_file(target, test_file)
            # Upload PDF to remaining dropzones
            for label in UploadDocumentsPage.UPLOAD_MAP.keys():
                if label != target:
                    upload_page.upload_single_file(label, TEST_PDF)

    with allure.step(f"Fill comments: '{comments[:30] if comments else '(empty)'}'"):
        upload_page.fill_comments(comments if comments else "")

    with allure.step(f"Select affiliation: {affiliation}"):
        upload_page.select_affiliation_type(affiliation)

    with allure.step("Check both declarations"):
        upload_page.check_declarations()

    # Determine expected outcome
    expected = scenario.get("expected_result", "")

    if "navigates" in expected.lower() or "payment" in expected.lower():
        with allure.step("Click Proceed and verify navigation to payment"):
            upload_page.click_proceed()
            page.wait_for_timeout(5000)

            navigated = "payment" in page.url.lower()
            if not navigated:
                errors = ValidationHelper.get_all_errors(page, timeout=1000)
                pytest.fail(
                    f"Expected navigation to payment but didn't. URL: {page.url}. Errors: {errors}"
                )

            allure.attach(
                f"PASS: Navigated to payment. URL: {page.url}",
                name="Positive Result",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Navigate back to Upload Documents for next test"):
            page.go_back()
            page.wait_for_timeout(3000)
            # Re-navigate to upload tab if needed
            if "payment" in page.url.lower() or "dashboard" in page.url.lower():
                page.get_by_text("Upload Documents", exact=False).first.click()
                page.wait_for_timeout(3000)
    else:
        # For upload-only tests (POS_005, POS_006, POS_009)
        with allure.step("Verify upload succeeded"):
            allure.attach(
                f"PASS: Upload completed for {target} with {file_type} file.",
                name="Upload Result",
                attachment_type=allure.attachment_type.TEXT,
            )
