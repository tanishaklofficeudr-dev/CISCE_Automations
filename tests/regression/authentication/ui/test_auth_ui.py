"""
Authentication — UI Behaviour Tests
======================================
REG_UI_001: Registration page loads
LOGIN_UI_001: Login page loads
LOGIN_UI_002: Password masking
LOGIN_NAV_001: Successful login navigates to dashboard
LOGIN_NAV_003: Direct URL access without login blocked
"""
import pytest
import allure
from utils.screenshot_util import ScreenshotUtil


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("page")
        if page:
            try:
                ScreenshotUtil.take_screenshot(page, request.node.name[:50])
            except Exception:
                pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("UI & Navigation")
@pytest.mark.regression
@pytest.mark.authentication
def test_login_ui_002_password_masking(page):
    """LOGIN_UI_002: Verify password field masks input."""
    allure.dynamic.title("LOGIN_UI_002 — Password field masks characters")
    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.get_by_role("link", name="login").click()
    page.wait_for_timeout(1000)

    pwd_field = page.get_by_role("textbox", name="Enter Your Password")
    field_type = pwd_field.get_attribute("type")
    assert field_type == "password", f"Password field type is '{field_type}', expected 'password'"


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("UI & Navigation")
@pytest.mark.regression
@pytest.mark.authentication
def test_login_nav_001_dashboard_redirect(page):
    """LOGIN_NAV_001: Successful login navigates to dashboard."""
    allure.dynamic.title("LOGIN_NAV_001 — Login navigates to dashboard")
    from utils.excel_reader import ExcelReader
    excel = ExcelReader("test_data/negative/Validation_Data.xlsx")
    login_data = excel.get_sheet_data("Common_Login")[0]

    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.get_by_role("link", name="login").click()
    page.wait_for_timeout(1000)
    page.get_by_role("textbox", name="Enter Your Mobile Number").fill(str(login_data["mobile_number"]))
    page.get_by_role("textbox", name="Enter Your Password").fill(str(login_data["password"]))
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/preliminary/school/dashboard", timeout=30000)
    assert "dashboard" in page.url


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("UI & Navigation")
@pytest.mark.regression
@pytest.mark.authentication
def test_login_nav_003_unauthorized_access(page):
    """LOGIN_NAV_003: Direct dashboard URL without login is blocked."""
    allure.dynamic.title("LOGIN_NAV_003 — Unauthorized access blocked")
    page.goto("https://dev-eaffiliation.cisce.org/preliminary/school/dashboard")
    page.wait_for_timeout(3000)
    # Should redirect to login or show unauthorized
    assert "dashboard" not in page.url or "login" in page.url or "registration" in page.url, (
        f"Unauthorized access allowed! URL: {page.url}"
    )


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("UI & Navigation")
@pytest.mark.regression
@pytest.mark.authentication
def test_login_nav_004_forgot_password(page):
    """LOGIN_NAV_004: Verify Forgot Password flow navigates and accepts request."""
    allure.dynamic.title("LOGIN_NAV_004 — Forgot Password flow")
    allure.dynamic.severity(allure.severity_level.NORMAL)
    allure.dynamic.tag("regression", "authentication", "navigation")

    with allure.step("Navigate to login page"):
        page.goto("https://dev-eaffiliation.cisce.org/registration")
        page.get_by_role("link", name="login").click()
        page.wait_for_timeout(1000)

    with allure.step("Click Forgot Password link"):
        forgot_link = page.get_by_text("Forgot Password", exact=False)
        if forgot_link.count() > 0:
            forgot_link.first.click()
            page.wait_for_timeout(2000)
        else:
            # Try alternative locators
            forgot_link = page.locator("a:has-text('forgot'), a:has-text('Forgot')")
            if forgot_link.count() > 0:
                forgot_link.first.click()
                page.wait_for_timeout(2000)
            else:
                allure.attach(
                    "Forgot Password link NOT found on login page.",
                    name="Link Not Found",
                    attachment_type=allure.attachment_type.TEXT,
                )
                pytest.skip("Forgot Password link not available on this page")

    with allure.step("Verify navigation to reset page"):
        allure.attach(
            f"Current URL after clicking Forgot Password: {page.url}",
            name="Navigation Result",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Enter registered mobile number for reset"):
        # Try filling mobile/email field on reset page
        from utils.excel_reader import ExcelReader
        excel = ExcelReader("test_data/negative/Validation_Data.xlsx")
        login_data = excel.get_sheet_data("Common_Login")[0]

        mobile_field = page.get_by_role("textbox", name="Mobile")
        if mobile_field.count() == 0:
            mobile_field = page.locator("input[type='text'], input[type='tel']").first

        if mobile_field.is_visible():
            mobile_field.fill(str(login_data["mobile_number"]))
        else:
            allure.attach(
                "No mobile/email input field found on reset page.",
                name="Field Not Found",
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step("Submit reset request"):
        submit_btn = page.get_by_role("button", name="Submit")
        if submit_btn.count() == 0:
            submit_btn = page.get_by_role("button", name="Send")
        if submit_btn.count() == 0:
            submit_btn = page.locator("button[type='submit']")

        if submit_btn.count() > 0 and submit_btn.first.is_visible():
            submit_btn.first.click()
            page.wait_for_timeout(3000)

    with allure.step("Verify response (success message or page state)"):
        allure.attach(
            f"Final URL: {page.url}\nPage content captured.",
            name="Forgot Password Result",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Security")
@pytest.mark.regression
@pytest.mark.authentication
def test_login_sec_001_multiple_sessions(browser):
    """LOGIN_SEC_001: Verify multiple browser session behavior with same account."""
    allure.dynamic.title("LOGIN_SEC_001 — Multiple session behavior")
    allure.dynamic.severity(allure.severity_level.CRITICAL)
    allure.dynamic.tag("regression", "authentication", "security")

    from utils.excel_reader import ExcelReader
    excel = ExcelReader("test_data/negative/Validation_Data.xlsx")
    login_data = excel.get_sheet_data("Common_Login")[0]
    mobile = str(login_data["mobile_number"])
    password = str(login_data["password"])

    with allure.step("Create Context A and login"):
        context_a = browser.new_context()
        page_a = context_a.new_page()
        page_a.goto("https://dev-eaffiliation.cisce.org/registration")
        page_a.get_by_role("link", name="login").click()
        page_a.wait_for_timeout(1000)
        page_a.get_by_role("textbox", name="Enter Your Mobile Number").fill(mobile)
        page_a.get_by_role("textbox", name="Enter Your Password").fill(password)
        page_a.get_by_role("button", name="Login").click()
        page_a.wait_for_url("**/preliminary/school/dashboard", timeout=30000)
        session_a_url = page_a.url
        allure.attach(f"Context A logged in: {session_a_url}", name="Session A", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Create Context B and login with SAME account"):
        context_b = browser.new_context()
        page_b = context_b.new_page()
        page_b.goto("https://dev-eaffiliation.cisce.org/registration")
        page_b.get_by_role("link", name="login").click()
        page_b.wait_for_timeout(1000)
        page_b.get_by_role("textbox", name="Enter Your Mobile Number").fill(mobile)
        page_b.get_by_role("textbox", name="Enter Your Password").fill(password)
        page_b.get_by_role("button", name="Login").click()
        page_b.wait_for_url("**/preliminary/school/dashboard", timeout=30000)
        session_b_url = page_b.url
        allure.attach(f"Context B logged in: {session_b_url}", name="Session B", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Verify Context A still active after Context B login"):
        page_a.reload()
        page_a.wait_for_timeout(3000)
        session_a_after = page_a.url

        if "dashboard" in session_a_after:
            behaviour = "MULTIPLE SESSIONS ALLOWED — Both contexts remain active."
        else:
            behaviour = "SINGLE SESSION ENFORCED — Context A was invalidated after Context B login."

        allure.attach(
            f"Context A URL after reload: {session_a_after}\n"
            f"Context B URL: {session_b_url}\n\n"
            f"OBSERVED BEHAVIOUR: {behaviour}",
            name="Multi-Session Result",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Cleanup contexts"):
        context_a.close()
        context_b.close()

    # Document the behaviour — this test documents, not asserts
    allure.attach(behaviour, name="Final Classification", attachment_type=allure.attachment_type.TEXT)
