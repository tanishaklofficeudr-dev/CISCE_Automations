"""
conftest.py - Pytest Configuration & Hooks
============================================
Integrates the Excel Report Generator with pytest execution lifecycle.
"""

import os
import sys
import glob
import time
import json
from datetime import datetime
import shutil
import subprocess
import pytest

# Add project root to path so utils can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.report_generator import ExcelReportGenerator, TestResult

# Global report generator instance
report_generator = ExcelReportGenerator()


# ============================================================================
# VIDEO RECORDING CONFIGURATION
# ============================================================================
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Enable video recording for all tests."""
    os.makedirs("recordings", exist_ok=True)
    return {
        **browser_context_args,
        "record_video_dir": "recordings",
        "record_video_size": {"width": 1280, "height": 720},
    }


@pytest.fixture(autouse=True)
def rename_video_after_test(request, page):
    """Rename video recording after test with format: PASSED/FAILED_TEST_ID.webm"""
    yield
    # After test completes, rename the video
    try:
        video = page.video
        if video:
            video_path = video.path()
            if video_path and os.path.exists(video_path):
                # Get test result
                rep = getattr(request.node, "rep_call", None)
                status = "PASSED" if (rep and rep.passed) else "FAILED"

                # Extract test ID
                test_id = _extract_test_id(request.node)

                # Create new filename
                new_name = f"{status}_{test_id}.webm"
                new_path = os.path.join("recordings", new_name)

                # Close the page to finalize video
                page.close()

                # Rename the video file
                if os.path.exists(video_path):
                    # Remove existing file with same name if exists
                    if os.path.exists(new_path):
                        os.remove(new_path)
                    os.rename(video_path, new_path)
    except Exception:
        pass



def pytest_sessionstart(session):
    """Record session start time and preserve allure history for trend analysis."""
    report_generator.set_start_time()

    # Auto-copy allure history for trend analysis (no manual step needed)
    allure_report_history = os.path.join("allure-report", "history")
    allure_results_history = os.path.join("allure-results", "history")

    if os.path.exists(allure_report_history):
        os.makedirs(allure_results_history, exist_ok=True)
        for item in os.listdir(allure_report_history):
            src = os.path.join(allure_report_history, item)
            dst = os.path.join(allure_results_history, item)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)

    # Create executor.json with timestamp for trend chart x-axis labels
    os.makedirs("allure-results", exist_ok=True)
    timestamp = datetime.now().strftime("%d-%b-%Y %H:%M")
    executor_data = {
        "name": "Local Machine",
        "type": "local",
        "buildName": timestamp,
        "buildOrder": int(datetime.now().timestamp()),
        "reportName": f"Test Run - {timestamp}"
    }
    with open(os.path.join("allure-results", "executor.json"), "w") as f:
        json.dump(executor_data, f, indent=2)

    # Create environment.properties for Allure Environment section
    env_props = (
        "Project=CISCE Preliminary Affiliation Form Automation\n"
        "Framework=Playwright + Pytest + POM\n"
        "Python=3.14.5\n"
        "Browser=Chromium\n"
        "Platform=Windows 11\n"
        "Environment=DEV\n"
        "Base.URL=https://dev-eaffiliation.cisce.org\n"
        "Automation.Tool=Playwright MCP\n"
        "Reporting=Allure + HTML + Excel\n"
    )
    with open(os.path.join("allure-results", "environment.properties"), "w") as f:
        f.write(env_props)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture results from each test after the 'call' phase.
    Extracts test ID, status, error info, screenshot, and timing.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Extract test case ID from parametrize marker
        test_id = _extract_test_id(item)
        test_name = item.name
        browser_name = _get_browser_name(item)
        execution_time = report.duration

        if report.passed:
            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                error_message="",
                screenshot_path="",
                execution_time=execution_time,
                browser_name=browser_name,
            )
        elif report.failed:
            error_message = _extract_error_message(report)
            screenshot_path = _find_screenshot_for_test(test_id)

            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                error_message=error_message,
                screenshot_path=screenshot_path,
                execution_time=execution_time,
                browser_name=browser_name,
            )
        else:
            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                error_message=f"SKIPPED: {report.longrepr}",
                screenshot_path="",
                execution_time=execution_time,
                browser_name=browser_name,
            )

        report_generator.add_result(result)


def pytest_sessionfinish(session, exitstatus):
    """Generate the Excel report and Allure report after all tests complete."""
    report_generator.set_end_time()

    if report_generator.results:
        report_generator.generate_report()
    else:
        print("\n[Excel Report] No test results collected. Skipping report generation.")

    # Auto-generate Allure report if allure-results exists
    allure_results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "allure-results")
    if os.path.exists(allure_results_dir) and os.listdir(allure_results_dir):
        try:
            subprocess.run(
                ["allure", "generate", "allure-results", "--clean", "-o", "allure-report"],
                capture_output=True, text=True, timeout=30, shell=True
            )
            print("\n" + "=" * 60)
            print("  ALLURE REPORT GENERATED SUCCESSFULLY")
            print("  View: allure open allure-report --port 9090")
            print("=" * 60 + "\n")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("\n[Allure] Could not auto-generate report. Run manually: allure generate allure-results --clean -o allure-report")


def _extract_test_id(item):
    """Extract test case ID from parametrized test name."""
    if "[" in item.name and "]" in item.name:
        param_value = item.name.split("[")[1].rstrip("]")
        # Handle 'chromium-SCH007' format
        if "-" in param_value:
            return param_value.split("-", 1)[1]
        return param_value
    return item.name


def _get_browser_name(item):
    """Extract browser name from test configuration."""
    if "[" in item.name and "-" in item.name:
        param_value = item.name.split("[")[1].rstrip("]")
        if "-" in param_value:
            return param_value.split("-", 1)[0]
    try:
        browser = item.config.getoption("--browser", default=None)
        if browser:
            if isinstance(browser, list):
                return browser[0] if browser else "chromium"
            return browser
    except (ValueError, AttributeError):
        pass
    return "chromium"


def _extract_error_message(report):
    """Extract a clean error message from a failed test report."""
    if report.longrepr:
        longrepr_str = str(report.longrepr)
        lines = longrepr_str.strip().split("\n")
        # Find lines starting with E (pytest error lines)
        e_lines = [l.strip()[2:].strip() for l in lines if l.strip().startswith("E ")]
        if e_lines:
            return e_lines[0][:500]
        # Fallback
        error_lines = [l for l in lines if l.strip() and not l.startswith(" ")]
        if error_lines:
            return error_lines[-1].strip()[:500]
        return longrepr_str[-500:]
    return "Unknown error"


def _find_screenshot_for_test(test_id):
    """Find the most recent screenshot for a given test ID."""
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        return ""
    pattern = os.path.join(screenshot_dir, f"{test_id}_*.png")
    matching_files = glob.glob(pattern)
    if matching_files:
        matching_files.sort(reverse=True)
        return matching_files[0]
    return ""


# ============================================================================
# TEST EXECUTION ORDERING
# ============================================================================

def pytest_collection_modifyitems(items):
    """
    Reorder test execution so @pytest.mark.first_run tests execute first.

    Tests marked with first_run require fresh application state (no prior saves).
    This hook moves them to the front of the execution queue automatically.
    Works across all modules — any test with this marker gets priority.

    Also dynamically applies @pytest.mark.sanity to the approved 20 sanity tests
    based on their parametrized node IDs.
    """
    # ---- SANITY MARKER ASSIGNMENT ----
    # These are the approved 20 regression test IDs that form the sanity suite.
    # Applied dynamically so no test file logic needs modification.
    SANITY_IDS = {
        "SCH_POS_01", "SCH_NEG_01",
        "ADDR_POS_001", "ADDR_FMT_001",
        "NOC_POS_001",
        "TRUST_POS_001", "TRUST_FMT_001",
        "LAND_VAL_001", "LAND_POS_001", "LAND_POS_002",
        "LAND_POS_006", "LAND_POS_008", "LAND_UI_002",
        "UPLOAD_VAL_001", "UPLOAD_POS_001", "UPLOAD_NEG_001",
        "UPLOAD_NEG_004", "UPLOAD_UI_002",
        "PAYMENT_POS_001",
        "REG_POS_001", "REG_NEG_011",
        "LOGIN_POS_001", "LOGIN_NEG_002", "LOGIN_NAV_001",
    }

    # Match by test node ID suffix or function name
    SANITY_FUNC_NAMES = {
        "test_noc_all_required_fields_blank",  # NOC_VAL_001
        "test_land_val_001_owned_all_blank",   # LAND_VAL_001
        "test_land_ui_002_sale_deed_toggle",   # LAND_UI_002
        "test_upload_val_001_proceed_with_nothing",  # UPLOAD_VAL_001
    }

    for item in items:
        # Check parametrized ID in node name (e.g., [chromium-LAND_POS_001])
        node_name = item.name
        matched = False

        for sid in SANITY_IDS:
            if sid in node_name:
                item.add_marker(pytest.mark.sanity)
                matched = True
                break

        # Check hardcoded function names (non-parametrized tests)
        if not matched:
            func_name = item.originalname if hasattr(item, 'originalname') else item.name.split("[")[0]
            if func_name in SANITY_FUNC_NAMES:
                item.add_marker(pytest.mark.sanity)

    # ---- FIRST RUN / VALIDATION ORDERING ----
    # Validation tests must run FIRST (require fresh state with no prior session data).
    # This applies to all tests marked @first_run OR any test marked @validation.
    first_run_tests = []
    other_tests = []

    for item in items:
        if item.get_closest_marker("first_run") or item.get_closest_marker("validation"):
            first_run_tests.append(item)
        else:
            other_tests.append(item)

    items[:] = first_run_tests + other_tests

    # ---- PAYMENT GATEWAY ORDERING (ALWAYS LAST) ----
    # Payment Gateway tests change application state (moves to payment stage).
    # They must execute AFTER all other regression tests to avoid state conflicts.
    payment_tests = []
    non_payment_tests = []

    for item in items:
        if "payment_gateway" in str(item.fspath):
            payment_tests.append(item)
        else:
            non_payment_tests.append(item)

    items[:] = non_payment_tests + payment_tests


# ============================================================================
# REGRESSION FIXTURES
# ============================================================================

@pytest.fixture
def school_details_ready_page(page):
    """
    Pre-authenticated page positioned on the School Details form.

    Performs:
    1. Navigates to registration URL
    2. Registers (handles duplicate gracefully)
    3. Logs in using login_automated (no manual intervention)
    4. Waits for dashboard
    5. Clicks Next on Get Started page

    Returns:
        page: Playwright Page on School Details step, ready for validation testing.

    Data source:
        test_data/negative/Validation_Data.xlsx → "Common_Login" sheet
    """
    from pages.registration_page import RegistrationPage
    from pages.login_page import LoginPage
    from utils.excel_reader import ExcelReader

    # Load common login credentials
    excel = ExcelReader("test_data/negative/Validation_Data.xlsx")
    login_data = excel.get_sheet_data("Common_Login")[0]

    # Registration (handles duplicate gracefully)
    registration_data = {
        "mobile_number": login_data["mobile_number"],
        "email": login_data.get("email", "tannu.9879090210@yopmail.com"),
    }
    RegistrationPage(page).register_school(registration_data)

    # Automated login (pauses for manual password entry)
    LoginPage(page).login_automated(login_data)

    # Wait for dashboard
    page.wait_for_url("**/preliminary/school/dashboard", timeout=30000)
    page.wait_for_timeout(3000)

    # Navigate to School Details step
    # Click the "School Details" tab/step directly if visible
    school_tab = page.get_by_text("School Details", exact=False).first
    if school_tab.is_visible():
        school_tab.click()
        page.wait_for_timeout(2000)
    else:
        # Fallback: If on Get Started, click Next
        next_btn = page.get_by_role("button", name="Next")
        if next_btn.is_visible():
            next_btn.click()
            page.wait_for_timeout(2000)

    return page


@pytest.fixture
def address_ready_page(school_details_ready_page):
    """
    Pre-authenticated page positioned on the Address Details form.

    Builds on school_details_ready_page by filling School Details
    with valid data and clicking Next to arrive at Address Details.

    Returns:
        page: Playwright Page on Address Details step.
    """
    from pages.school_details_page import SchoolDetailsPage

    page = school_details_ready_page
    school_page = SchoolDetailsPage(page)

    # Fill School Details with valid baseline to proceed
    school_data = {
        "school_name": "Address Test School",
        "school_classification": "Day",
        "school_type": "Co-ed.",
        "contact_person": "Test Person",
        "contact_number": "9815311210",
        "contact_email": "test.9815311210@gmail.com",
        "website": "https://www.test.com",
        "udise_number": "12345678901",
        "school_category": "Private",
    }
    school_page.fill_partial_details(school_data, skip_fields=[])
    page.wait_for_timeout(3000)

    # Verify we arrived at Address Details
    address_field = page.locator("#address_1")
    if not address_field.is_visible():
        # Fallback: click Address Details tab
        page.get_by_text("Address Details", exact=False).first.click()
        page.wait_for_timeout(2000)

    return page


@pytest.fixture
def noc_ready_page(school_details_ready_page):
    """
    Pre-authenticated page positioned on the NOC Details form.

    Navigates directly via "NOC Details" tab click.
    Confirmed working in diagnostic.

    Returns:
        page: Playwright Page on NOC Details step.
    """
    page = school_details_ready_page

    # Navigate to NOC Details via tab (fastest, proven approach)
    page.get_by_text("NOC Details", exact=False).first.click()
    page.wait_for_timeout(3000)

    # Verify on NOC page
    noc_field = page.locator("#noc_authority")
    if not noc_field.is_visible():
        # Retry tab click
        page.get_by_text("NOC Details", exact=False).first.click()
        page.wait_for_timeout(2000)

    return page


@pytest.fixture
def trust_ready_page(school_details_ready_page):
    """
    Pre-authenticated page positioned on the Trust/Society/Company Details form.

    Navigates directly via tab click (confirmed working in diagnostic).

    Returns:
        page: Playwright Page on Trust Details step.
    """
    page = school_details_ready_page

    # Navigate to Trust Details via tab
    page.get_by_text("Trust /Society /Company", exact=False).first.click()
    page.wait_for_timeout(3000)

    # Verify on Trust page
    ownership = page.locator("#ownership_type")
    if not ownership.is_visible():
        # Retry
        page.get_by_text("Trust", exact=False).first.click()
        page.wait_for_timeout(2000)

    return page


@pytest.fixture
def land_ready_page(school_details_ready_page):
    """
    Pre-authenticated page positioned on the Certificate of Land form.

    Navigates directly via "Certificate of Land" tab click.
    Same proven tab-click pattern as NOC and Trust fixtures.

    Returns:
        page: Playwright Page on Certificate of Land step, ready for testing.
    """
    page = school_details_ready_page

    # Navigate to Certificate of Land via tab
    page.get_by_text("Certificate of Land", exact=False).first.click()
    page.wait_for_timeout(3000)

    # Verify on Land Certificate page (check for land area field or radio)
    land_area = page.locator("#land_area_0")
    single_radio = page.get_by_role("radio", name="Single")

    if not land_area.is_visible() and not single_radio.is_visible():
        # Retry tab click
        page.get_by_text("Certificate of Land", exact=False).first.click()
        page.wait_for_timeout(2000)

    return page


@pytest.fixture
def upload_ready_page(school_details_ready_page):
    """
    Pre-authenticated page positioned on the Upload Documents form.

    Navigates directly via "Upload Documents" tab click.
    Same proven tab-click pattern as NOC, Trust, and Land Certificate fixtures.

    Returns:
        page: Playwright Page on Upload Documents step, ready for testing.
    """
    page = school_details_ready_page

    # Navigate to Upload Documents via tab
    page.get_by_text("Upload Documents", exact=False).first.click()
    page.wait_for_timeout(4000)

    # Verify on Upload Documents page (check for a dropzone or Proceed button)
    proceed_btn = page.get_by_role("button", name="Proceed to Payment")
    if not proceed_btn.is_visible():
        # Retry tab click
        page.get_by_text("Upload Documents", exact=False).first.click()
        page.wait_for_timeout(3000)

    return page


@pytest.fixture
def payment_ready_page(upload_ready_page):
    """
    Pre-authenticated page positioned on the Payment Summary page.

    Performs:
    1. Starts from upload_ready_page (authenticated + on Upload Documents)
    2. Uploads all 5 documents (uses existing test PDF)
    3. Selects affiliation type
    4. Checks both declarations
    5. Clicks Proceed to Payment
    6. Waits for payment URL

    Returns:
        page: Playwright Page on Payment Summary, ready for bank selection.
    """
    import os
    from pages.upload_documents_page import UploadDocumentsPage

    page = upload_ready_page
    upload_page = UploadDocumentsPage(page)
    test_file = os.path.abspath("test_data/LandCertificate.pdf")

    # Upload all 5 documents
    upload_page.upload_all_documents(test_file)

    # Wait for page to stabilize after uploads (first upload may cause context change)
    page.wait_for_timeout(5000)

    # Select affiliation type via JS (radio is hidden behind custom UI)
    # Retry if context was destroyed during upload
    for attempt in range(3):
        try:
            page.evaluate("""
                () => {
                    const radios = document.querySelectorAll('input[name="composite_type"]');
                    for (const r of radios) {
                        if (r.value === '2') {
                            r.checked = true;
                            r.dispatchEvent(new Event('change', { bubbles: true }));
                            r.dispatchEvent(new Event('click', { bubbles: true }));
                            break;
                        }
                    }
                }
            """)
            break
        except Exception:
            page.wait_for_timeout(2000)

    page.wait_for_timeout(500)

    # Check both declarations via JS (checkboxes may be hidden behind custom UI)
    for attempt in range(3):
        try:
            page.evaluate("""
                () => {
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

    # Click Proceed to Payment
    upload_page.click_proceed()

    # Wait for payment page
    page.wait_for_url("**/payment**", timeout=30000)
    page.wait_for_timeout(3000)

    return page
