"""
NOC Future Date Verification
Run: python -m pytest tests/debug_noc_future_date.py -v --headed -s --alluredir=allure-results
"""
import pytest
import os
from datetime import datetime, timedelta


def test_noc_future_date_verification(school_details_ready_page):
    """Verify whether future date is accepted or rejected by NOC form."""
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("NOC FUTURE DATE VERIFICATION")
    print("=" * 70)

    # Navigate to NOC Details via tab
    print("\n[STEP 1] Navigate to NOC Details...")
    page.get_by_text("NOC Details", exact=False).first.click()
    page.wait_for_timeout(3000)

    # Fill all mandatory fields
    print("\n[STEP 2] Fill all mandatory fields with valid data...")
    page.locator("#noc_authority").fill("District Education Officer")
    page.locator("#noc_designation").fill("Director of Education")
    page.locator("#noc_office_address").fill("State Education Office, Jaipur")
    page.locator("#noc_country").select_option("2")
    page.wait_for_timeout(1000)
    page.locator("#noc_state").select_option("30")
    page.wait_for_timeout(500)
    page.get_by_role("textbox", name="Select NOC Reference Number").fill("NOC-FUTURE-TEST-001")
    print("  All text fields and dropdowns filled.")

    # Set FUTURE date via JavaScript
    future_date = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
    print(f"\n[STEP 3] Set FUTURE date: '{future_date}' via JavaScript...")

    from utils.validation_helper import ValidationHelper
    ValidationHelper.set_readonly_date(page, '#noc_date[name="noc_date"]', future_date)

    # Verify DOM value
    noc_date = page.locator("#noc_date[name='noc_date']")
    val = noc_date.evaluate("el => el.value")
    print(f"  DOM value after JS: '{val}'")
    page.screenshot(path="screenshots/debug/noc_future_date_before_next.png")
    print("  Screenshot: noc_future_date_before_next.png")

    # Click Next
    print("\n[STEP 4] Click Next...")
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(4000)
    page.screenshot(path="screenshots/debug/noc_future_date_after_next.png")
    print("  Screenshot: noc_future_date_after_next.png")

    # Check result
    print("\n[STEP 5] Check result...")
    print(f"  Current URL: {page.url}")

    # Check if Trust Details appeared
    trust_visible = False
    try:
        trust_el = page.get_by_text("Trust/Society/Company", exact=False)
        if trust_el.count() > 0:
            trust_visible = trust_el.first.is_visible()
    except:
        pass

    print(f"  Trust/Society visible (navigated): {trust_visible}")

    # Capture errors
    errors = []
    for sel in [".invalid-feedback", ".text-danger", "[class*='invalid']:not(input):not(select):not(textarea)"]:
        try:
            for el in page.locator(sel).all():
                if el.is_visible():
                    t = el.inner_text().strip()
                    if t and t not in errors:
                        errors.append(t)
        except:
            pass

    if errors:
        print(f"  VALIDATION ERRORS: {errors}")
    else:
        print("  NO ERRORS found.")

    # Classification
    print("\n[STEP 6] CLASSIFICATION...")
    print(f"  Future date used: {future_date}")
    print(f"  Form navigated: {trust_visible}")
    print(f"  Errors shown: {errors}")

    if not trust_visible and errors:
        date_errors = [e for e in errors if "date" in e.lower() or "future" in e.lower() or "noc" in e.lower()]
        if date_errors:
            print(f"\n  ✅ CORRECTLY REJECTED — Future date validation exists.")
            print(f"  Validation message: {date_errors}")
            print("  Classification: NEGATIVE TEST VALID")
        else:
            print(f"\n  ⚠️ Form blocked but not for date: {errors}")
            print("  Classification: OTHER VALIDATION BLOCKING")
    elif trust_visible:
        print(f"\n  ⚠️ FUTURE DATE ACCEPTED — Form navigated to Trust Details.")
        print("  Classification: POTENTIAL APPLICATION DEFECT – Future Date Accepted")
        print("  Recommendation: Keep NOC_FMT_006 in matrix as xfail documenting the gap.")
    else:
        print("\n  ❓ INCONCLUSIVE — No navigation and no errors.")
        print("  Classification: NEEDS INVESTIGATION")

    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)

    assert True
