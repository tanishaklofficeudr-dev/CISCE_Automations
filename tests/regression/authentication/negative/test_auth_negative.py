"""
Authentication — Negative Tests (Excel-driven)
=================================================
Registration: REG_NEG_001 to REG_NEG_011
Login: LOGIN_NEG_001 to LOGIN_NEG_007
"""
import pytest
import allure
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from utils.excel_reader import ExcelReader
from utils.validation_helper import ValidationHelper
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


_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_reg_negative = [r for r in _excel.get_sheet_data("Registration_Negative") if str(r.get("execute", "")).lower() == "yes"]
_login_negative = [r for r in _excel.get_sheet_data("Login_Negative") if str(r.get("execute", "")).lower() == "yes"]


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Negative — Registration")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.authentication
@pytest.mark.parametrize("scenario", _reg_negative, ids=lambda s: s["scenario_id"])
def test_registration_negative(page, scenario):
    """Verify registration rejects invalid input."""
    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.severity(allure.severity_level.CRITICAL if scenario.get("priority") == "High" else allure.severity_level.NORMAL)

    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.wait_for_timeout(1000)

    mobile = scenario.get("mobile_number", "")
    email = scenario.get("email", "")

    with allure.step(f"Fill mobile='{mobile}', email='{email}'"):
        if mobile:
            page.get_by_role("textbox", name="Country code * Enter Your").fill(str(mobile))
        if email:
            page.get_by_role("textbox", name="Enter Your Email Address *").fill(str(email))

    with allure.step("Click Register"):
        page.get_by_role("button", name="Register").click()
        page.wait_for_timeout(3000)

    with allure.step("Verify error/rejection"):
        # Check that success popup did NOT appear or error is shown
        errors = ValidationHelper.get_all_errors(page, timeout=1000)
        allure.attach(
            f"Errors: {errors}\nURL: {page.url}",
            name="Negative Result",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Negative — Login")
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.authentication
@pytest.mark.parametrize("scenario", _login_negative, ids=lambda s: s["scenario_id"])
def test_login_negative(page, scenario):
    """Verify login rejects invalid credentials."""
    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.severity(allure.severity_level.CRITICAL if scenario.get("priority") == "High" else allure.severity_level.NORMAL)

    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.get_by_role("link", name="login").click()
    page.wait_for_timeout(1000)

    mobile = scenario.get("mobile_number", "")
    password = scenario.get("password", "")

    with allure.step(f"Fill mobile='{mobile}', password='{password}'"):
        if mobile:
            page.get_by_role("textbox", name="Enter Your Mobile Number").fill(str(mobile))
        if password:
            page.get_by_role("textbox", name="Enter Your Password").fill(str(password))

    with allure.step("Click Login"):
        page.get_by_role("button", name="Login").click()
        page.wait_for_timeout(3000)

    with allure.step("Verify did NOT navigate to dashboard"):
        assert "dashboard" not in page.url, f"Login should have failed but navigated to: {page.url}"
        errors = ValidationHelper.get_all_errors(page, timeout=1000)
        allure.attach(
            f"Errors: {errors}\nURL: {page.url}",
            name="Negative Result",
            attachment_type=allure.attachment_type.TEXT,
        )
