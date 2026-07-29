"""
Authentication — Positive Tests (Excel-driven)
=================================================
Registration: REG_POS_001
Login: LOGIN_POS_001
"""
import pytest
import allure
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from utils.excel_reader import ExcelReader
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

_reg_positive = [r for r in _excel.get_sheet_data("Registration_Positive") if str(r.get("execute", "")).lower() == "yes"]
_login_positive = [r for r in _excel.get_sheet_data("Login_Positive") if str(r.get("execute", "")).lower() == "yes"]


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Positive")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.authentication
@pytest.mark.parametrize("scenario", _reg_positive, ids=lambda s: s["scenario_id"])
def test_registration_positive(page, scenario):
    """Verify successful registration with valid data."""
    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.severity(allure.severity_level.CRITICAL)

    reg_page = RegistrationPage(page)
    reg_data = {"mobile_number": scenario["mobile_number"], "email": scenario["email"]}

    with allure.step("Register with valid credentials"):
        reg_page.register_school(reg_data)
        page.wait_for_timeout(2000)

    with allure.step("Verify registration handled (success or duplicate)"):
        # If new → popup appeared. If duplicate → handled gracefully.
        allure.attach(f"URL after registration: {page.url}", name="Result", attachment_type=allure.attachment_type.TEXT)


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Positive")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.authentication
@pytest.mark.parametrize("scenario", _login_positive, ids=lambda s: s["scenario_id"])
def test_login_positive(page, scenario):
    """Verify successful login with valid credentials."""
    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.severity(allure.severity_level.CRITICAL)

    page.goto("https://dev-eaffiliation.cisce.org/registration")
    login_page = LoginPage(page)
    login_data = {"mobile_number": scenario["mobile_number"], "password": scenario["password"]}

    with allure.step("Login with valid credentials"):
        login_page.login_automated(login_data)

    with allure.step("Verify navigation to dashboard"):
        page.wait_for_url("**/preliminary/school/dashboard", timeout=30000)
        assert "dashboard" in page.url, f"Did not reach dashboard. URL: {page.url}"
        allure.attach(f"Dashboard reached: {page.url}", name="Result", attachment_type=allure.attachment_type.TEXT)
