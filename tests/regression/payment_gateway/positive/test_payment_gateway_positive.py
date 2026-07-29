#python -m pytest tests/regression/payment_gateway/ -v --headed -k "POS_001"
"""
Payment Gateway — Positive Regression Tests
==============================================
Verifies each payment gateway (HDFC, ICICI, Federal) is accessible
and functional up to the bank payment page.

DOES NOT complete any actual payment transaction.

Data Source: test_data/negative/Validation_Data.xlsx → "Payment_Gateway_Positive"
Page Object: pages/payment_gateway_page.py
Fixture: payment_ready_page (conftest.py)
"""

import pytest
import allure

from pages.payment_gateway_page import PaymentGatewayPage
from utils.excel_reader import ExcelReader
from utils.screenshot_util import ScreenshotUtil


# ============================================================================
# AUTO SCREENSHOT ON FAILURE
# ============================================================================

@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request):
    """Capture and attach screenshot to Allure on test failure."""
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page = request.node.funcargs.get("payment_ready_page")
        if page:
            try:
                path = ScreenshotUtil.take_screenshot(page, request.node.name[:50])
                if path:
                    allure.attach.file(
                        path,
                        name=f"Screenshot_{request.node.name[:50]}",
                        attachment_type=allure.attachment_type.PNG,
                    )
            except Exception:
                pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the request node for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ============================================================================
# DATA LOADING
# ============================================================================

_excel = ExcelReader("test_data/negative/Validation_Data.xlsx")

_payment_scenarios = [
    row for row in _excel.get_sheet_data("Payment_Gateway_Positive")
    if str(row.get("execute", "")).lower() == "yes"
]


# ============================================================================
# PAYMENT GATEWAY POSITIVE TESTS
# ============================================================================

@allure.parent_suite("CISCE E-Affiliation")
@allure.suite("Payment Gateway")
@allure.sub_suite("Positive")
@allure.feature("Payment Gateway Accessibility")
@allure.story("Bank Payment Flow Verification")
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.payment_gateway
@pytest.mark.parametrize(
    "scenario",
    _payment_scenarios,
    ids=lambda s: s["scenario_id"],
)
def test_payment_gateway_flow(payment_ready_page, scenario):
    """
    Verify complete payment gateway flow for a specific bank.
    Stops at the bank payment page — does NOT complete payment.

    Flow: Payment Summary → Pay ₹ → Select Bank → Proceed → Show QR → Continue → Bank Page
    """
    page = payment_ready_page
    payment_page = PaymentGatewayPage(page)

    bank_name = scenario["bank_name"]
    bank_alt = scenario["bank_alt_text"]

    allure.dynamic.title(f"{scenario['scenario_id']} — {bank_name}")
    allure.dynamic.description(
        f"Bank: {bank_name}\n"
        f"Alt text: {bank_alt}\n"
        f"Amount: ₹{scenario['payment_amount']}\n"
        f"Expected: {scenario['expected_result']}"
    )
    allure.dynamic.severity(allure.severity_level.CRITICAL)
    allure.dynamic.tag("regression", "positive", "payment_gateway", bank_name.lower().replace(" ", "_"))

    with allure.step("Step 1: Verify Payment Summary page"):
        assert "payment" in page.url.lower(), (
            f"Not on Payment page. Current URL: {page.url}"
        )
        allure.attach(
            f"Payment Summary URL confirmed: {page.url}",
            name="Payment Summary",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Step 2: Click 'Pay ₹' button"):
        payment_page.click_pay_button()

    with allure.step("Step 3: Verify Payment Details page"):
        payment_page.verify_payment_details_page()
        allure.attach(
            "Payment Details heading is visible.",
            name="Payment Details Verified",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f"Step 4: Select bank — {bank_name}"):
        payment_page.select_bank(bank_alt)
        allure.attach(
            f"Bank selected: {bank_name} (alt='{bank_alt}')",
            name="Bank Selection",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Step 5: Click 'Proceed to Pay'"):
        payment_page.click_proceed_to_pay()

    with allure.step("Step 6: Click 'Show QR' (inside payment iframe)"):
        payment_page.click_show_qr()
        allure.attach(
            "Show QR button clicked successfully inside iframe.",
            name="Show QR",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Step 7: Click 'Continue/Pay' (fee-bearer-cta)"):
        payment_page.click_continue_pay()

    with allure.step(f"Step 8: Verify {bank_name} payment page reached — STOP"):
        reached = payment_page.verify_bank_page_reached()
        allure.attach(
            f"Bank page reached: {reached}\n"
            f"Bank: {bank_name}\n"
            f"STOP — Payment NOT completed (by design).",
            name="Final Verification",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert reached, (
            f"Failed to reach {bank_name} payment page. "
            f"Iframe may not have loaded or bank page did not appear."
        )
