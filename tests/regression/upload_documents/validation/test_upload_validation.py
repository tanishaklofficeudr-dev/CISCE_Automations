"""
Upload Documents — Validation Tests (Hardcoded)
=================================================
UPLOAD_VAL_001: Proceed with nothing (no uploads, no radio, no checkboxes)
UPLOAD_VAL_002: All uploads but no affiliation selected
UPLOAD_VAL_003: All uploads + affiliation but no checkboxes
"""

import os
import pytest
import allure

from pages.upload_documents_page import UploadDocumentsPage
from utils.validation_helper import ValidationHelper
from utils.screenshot_util import ScreenshotUtil


TEST_FILE = os.path.abspath("test_data/LandCertificate.pdf")


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


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Upload Documents")
@allure.sub_suite("Validation")
@allure.feature("Mandatory Prerequisites")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.upload_documents
@pytest.mark.first_run
def test_upload_val_001_proceed_with_nothing(upload_ready_page):
    """
    UPLOAD_VAL_001: Click Proceed with NO uploads, no radio, no checkboxes.
    Expected: Form blocked — validation error shown.
    """
    page = upload_ready_page
    upload_page = UploadDocumentsPage(page)

    allure.dynamic.title("UPLOAD_VAL_001 — Proceed with nothing")
    allure.dynamic.tag("regression", "validation", "upload_documents", "sanity")

    with allure.step("Ensure checkboxes are unchecked"):
        page.evaluate("""
            () => {
                const vc = document.querySelector('#verify_composite');
                const v = document.querySelector('#verify');
                if (vc) { vc.checked = false; vc.dispatchEvent(new Event('change', { bubbles: true })); }
                if (v) { v.checked = false; v.dispatchEvent(new Event('change', { bubbles: true })); }
            }
        """)
        page.wait_for_timeout(500)

    with allure.step("Click Proceed to Payment without any prerequisites"):
        upload_page.click_proceed()
        page.wait_for_timeout(3000)

    with allure.step("Verify form did NOT navigate to payment"):
        assert "payment" not in page.url.lower(), (
            f"Form navigated to payment without prerequisites! URL: {page.url}"
        )

    with allure.step("Capture any validation messages or alerts"):
        errors = ValidationHelper.get_all_errors(page, timeout=2000)
        allure.attach(
            f"Validation state after Proceed:\n"
            f"  URL: {page.url}\n"
            f"  Errors: {errors}",
            name="Validation Result",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Upload Documents")
@allure.sub_suite("Validation")
@allure.feature("Mandatory Prerequisites")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.upload_documents
@pytest.mark.first_run
def test_upload_val_002_no_affiliation(upload_ready_page):
    """
    UPLOAD_VAL_002: All uploads done but no affiliation type selected.
    Expected: Form blocked — affiliation required.
    Must run FIRST before any positive test selects an affiliation.
    """
    page = upload_ready_page
    upload_page = UploadDocumentsPage(page)

    allure.dynamic.title("UPLOAD_VAL_002 — All uploads but no affiliation")
    allure.dynamic.tag("regression", "validation", "upload_documents")

    with allure.step("Upload all 5 documents"):
        upload_page.upload_all_documents(TEST_FILE)

    with allure.step("Check both declarations"):
        upload_page.check_declarations()

    with allure.step("Do NOT select affiliation type"):
        pass  # Intentionally leave radio unselected

    with allure.step("Click Proceed to Payment"):
        upload_page.click_proceed()
        page.wait_for_timeout(3000)

    with allure.step("Verify form did NOT navigate to payment"):
        assert "payment" not in page.url.lower(), (
            f"Form navigated without affiliation! URL: {page.url}"
        )
        allure.attach(
            f"Form correctly blocked. URL: {page.url}",
            name="Validation Result",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Upload Documents")
@allure.sub_suite("Validation")
@allure.feature("Mandatory Prerequisites")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.upload_documents
@pytest.mark.first_run
def test_upload_val_003_no_checkboxes(upload_ready_page):
    """
    UPLOAD_VAL_003: All uploads + affiliation selected but checkboxes unchecked.
    Expected: Form blocked — checkboxes required.
    Must run FIRST before any positive test checks the checkboxes.
    """
    page = upload_ready_page
    upload_page = UploadDocumentsPage(page)

    allure.dynamic.title("UPLOAD_VAL_003 — All uploads + affiliation but no checkboxes")
    allure.dynamic.tag("regression", "validation", "upload_documents")

    with allure.step("Upload all 5 documents"):
        upload_page.upload_all_documents(TEST_FILE)

    with allure.step("Select affiliation type"):
        upload_page.select_affiliation_type("Provisional Affiliation up to Class X")

    with allure.step("Ensure checkboxes are unchecked via JS"):
        page.evaluate("""
            () => {
                const vc = document.querySelector('#verify_composite');
                const v = document.querySelector('#verify');
                if (vc) { vc.checked = false; vc.dispatchEvent(new Event('change', { bubbles: true })); }
                if (v) { v.checked = false; v.dispatchEvent(new Event('change', { bubbles: true })); }
            }
        """)
        page.wait_for_timeout(500)

    with allure.step("Click Proceed to Payment"):
        upload_page.click_proceed()
        page.wait_for_timeout(3000)

    with allure.step("Verify form did NOT navigate to payment"):
        assert "payment" not in page.url.lower(), (
            f"Form navigated without checkboxes! URL: {page.url}"
        )
        allure.attach(
            f"Form correctly blocked. URL: {page.url}",
            name="Validation Result",
            attachment_type=allure.attachment_type.TEXT,
        )
