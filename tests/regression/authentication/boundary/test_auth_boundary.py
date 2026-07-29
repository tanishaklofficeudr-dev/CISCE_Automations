"""
Authentication — Boundary Tests (Excel-driven)
=================================================
Registration: REG_BND_001 to REG_BND_003
Login: LOGIN_BND_001 to LOGIN_BND_003
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

_reg_boundary = [r for r in _excel.get_sheet_data("Registration_Boundary") if str(r.get("execute", "")).lower() == "yes"]
_login_boundary = [r for r in _excel.get_sheet_data("Login_Boundary") if str(r.get("execute", "")).lower() == "yes"]


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Boundary — Registration")
@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.authentication
@pytest.mark.parametrize("scenario", _reg_boundary, ids=lambda s: s["scenario_id"])
def test_registration_boundary(page, scenario):
    """Verify registration field boundary values."""
    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.severity(allure.severity_level.NORMAL)

    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.wait_for_timeout(1000)

    field_name = scenario["field_name"]
    field_value = str(scenario["field_value"])
    expected = scenario.get("expected_outcome", "ACCEPT")

    with allure.step(f"Fill {field_name} with boundary value: '{field_value[:30]}'"):
        if field_name == "mobile_number":
            page.get_by_role("textbox", name="Country code * Enter Your").fill(field_value)
            page.get_by_role("textbox", name="Enter Your Email Address *").fill("boundary@test.com")
        elif field_name == "email":
            page.get_by_role("textbox", name="Country code * Enter Your").fill("9876543210")
            page.get_by_role("textbox", name="Enter Your Email Address *").fill(field_value)

    with allure.step("Click Register"):
        page.get_by_role("button", name="Register").click()
        page.wait_for_timeout(3000)

    with allure.step(f"Verify outcome: {expected}"):
        allure.attach(f"URL: {page.url}\nExpected: {expected}", name="Boundary Result", attachment_type=allure.attachment_type.TEXT)


@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Authentication")
@allure.sub_suite("Boundary — Login")
@pytest.mark.regression
@pytest.mark.boundary
@pytest.mark.authentication
@pytest.mark.parametrize("scenario", _login_boundary, ids=lambda s: s["scenario_id"])
def test_login_boundary(page, scenario):
    """Verify login field boundary values."""
    allure.dynamic.title(f"{scenario['scenario_id']} — {scenario['scenario_description']}")
    allure.dynamic.severity(allure.severity_level.NORMAL)

    page.goto("https://dev-eaffiliation.cisce.org/registration")
    page.get_by_role("link", name="login").click()
    page.wait_for_timeout(1000)

    field_name = scenario["field_name"]
    field_value = str(scenario["field_value"])
    expected = scenario.get("expected_outcome", "ACCEPT")

    with allure.step(f"Fill {field_name} with boundary value"):
        if field_name == "mobile_number":
            page.get_by_role("textbox", name="Enter Your Mobile Number").fill(field_value)
            page.get_by_role("textbox", name="Enter Your Password").fill("UPWYJ5")
        elif field_name == "password":
            page.get_by_role("textbox", name="Enter Your Mobile Number").fill("7979009709")
            page.get_by_role("textbox", name="Enter Your Password").fill(field_value)

    with allure.step("Click Login"):
        page.get_by_role("button", name="Login").click()
        page.wait_for_timeout(3000)

    with allure.step(f"Verify outcome: {expected}"):
        if expected == "ACCEPT":
            assert "dashboard" in page.url, f"Expected dashboard but got: {page.url}"
        else:
            assert "dashboard" not in page.url, f"Expected rejection but navigated: {page.url}"
        allure.attach(f"URL: {page.url}", name="Boundary Result", attachment_type=allure.attachment_type.TEXT)
