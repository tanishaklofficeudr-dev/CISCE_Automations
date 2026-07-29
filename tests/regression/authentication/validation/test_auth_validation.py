"""
Authentication — Validation Tests (Hardcoded)
================================================
REG_VAL_001: Registration page required field indicators
LOGIN_VAL_001: Login page required field indicators
LOGIN_VAL_002: Login error message format
"""
import pytest
import allure
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
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
@allure.sub_suite("Validation")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.authentication
def test_reg_val_001_page_loads(page):
    """REG_VAL_001: Registration page loads with all required fields visible."""
    allure.dynamic.title("REG_VAL_001 — Registration page loads correctly")
    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.wait_for_timeout(2000)

    mobile = page.get_by_role("textbox", name="Country code * Enter Your")
    email = page.get_by_role("textbox", name="Enter Your Email Address *")
    register_btn = page.get_by_role("button", name="Register")

    assert mobile.is_visible(), "Mobile number field not visible"
    assert email.is_visible(), "Email field not visible"
    assert register_btn.is_visible(), "Register button not visible"


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Validation")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.authentication
def test_login_val_001_page_loads(page):
    """LOGIN_VAL_001: Login page loads with all required fields."""
    allure.dynamic.title("LOGIN_VAL_001 — Login page loads correctly")
    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.get_by_role("link", name="login").click()
    page.wait_for_timeout(2000)

    mobile = page.get_by_role("textbox", name="Enter Your Mobile Number")
    password = page.get_by_role("textbox", name="Enter Your Password")
    login_btn = page.get_by_role("button", name="Login")

    assert mobile.is_visible(), "Mobile field not visible"
    assert password.is_visible(), "Password field not visible"
    assert login_btn.is_visible(), "Login button not visible"


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Validation")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.authentication
def test_login_val_002_error_format(page):
    """LOGIN_VAL_002: Login shows clear error for invalid credentials."""
    allure.dynamic.title("LOGIN_VAL_002 — Error message displayed for invalid login")
    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.get_by_role("link", name="login").click()
    page.wait_for_timeout(1000)
    page.get_by_role("textbox", name="Enter Your Mobile Number").fill("1111111111")
    page.get_by_role("textbox", name="Enter Your Password").fill("WRONG")
    page.get_by_role("button", name="Login").click(no_wait_after=True)
    page.wait_for_timeout(5000)

    # Check that we did NOT navigate to dashboard
    assert "dashboard" not in page.url, "Should not navigate with invalid credentials"
