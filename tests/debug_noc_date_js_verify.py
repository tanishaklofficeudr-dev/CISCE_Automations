"""
NOC Date — Final JavaScript Injection Verification
Run: python -m pytest tests/debug_noc_date_js_verify.py -v --headed -s --alluredir=allure-results

Objective: Verify whether JS-set date is accepted by the form on Next click.
"""
import pytest
import os


def test_noc_date_js_acceptance(school_details_ready_page):
    """
    1. Navigate to NOC Details
    2. Fill all fields + set date via JavaScript
    3. Click Next
    4. Verify form accepts or rejects
    """
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("NOC DATE — JAVASCRIPT INJECTION FINAL VERIFICATION")
    print("=" * 70)

    # Navigate to NOC Details via tab
    print("\n[STEP 1] Navigate to NOC Details...")
    page.get_by_text("NOC Details", exact=False).first.click()
    page.wait_for_timeout(3000)

    # Verify on NOC page
    noc_date = page.locator("#noc_date[name='noc_date']")
    print(f"  NOC date field visible: {noc_date.is_visible()}")

    if not noc_date.is_visible():
        print("  ERROR: NOC date not visible. Aborting.")
        page.screenshot(path="screenshots/debug/noc_js_verify_not_found.png")
        assert False, "NOC date field not reachable"

    # Fill all NOC mandatory fields
    print("\n[STEP 2] Fill all mandatory fields...")
    page.locator("#noc_authority").fill("District Education Officer")
    page.locator("#noc_designation").fill("Director of Education")
    page.locator("#noc_office_address").fill("Government Education Office, Jaipur")
    page.locator("#noc_country").select_option("2")
    page.wait_for_timeout(1000)
    page.locator("#noc_state").select_option("30")
    page.wait_for_timeout(500)
    page.get_by_role("textbox", name="Select NOC Reference Number").fill("NOC-JS-VERIFY-001")
    print("  All text fields + dropdowns filled.")

    # Set date via JavaScript
    print("\n[STEP 3] Set date via JavaScript injection...")
    page.evaluate("""
        () => {
            const input = document.querySelector('#noc_date[name="noc_date"]');
            if (input) {
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(input, '16/05/2025');
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.dispatchEvent(new Event('blur', { bubbles: true }));
            }
        }
    """)
    page.wait_for_timeout(1000)

    # Read back value
    val_after_js = noc_date.evaluate("el => el.value")
    print(f"  DOM value after JS: '{val_after_js}'")
    page.screenshot(path="screenshots/debug/noc_js_verify_before_next.png")
    print("  Screenshot: noc_js_verify_before_next.png")

    # Click Next
    print("\n[STEP 4] Click Next...")
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(4000)
    page.screenshot(path="screenshots/debug/noc_js_verify_after_next.png")
    print("  Screenshot: noc_js_verify_after_next.png")

    # Check result
    print("\n[STEP 5] Check result...")

    # Check if Trust Details appeared (next step)
    trust_visible = False
    try:
        trust_el = page.get_by_text("Trust/Society/Company", exact=False)
        if trust_el.count() > 0:
            trust_visible = trust_el.first.is_visible()
    except:
        pass

    print(f"  Trust/Society/Company visible (navigated): {trust_visible}")
    print(f"  Current URL: {page.url}")

    # Check for errors
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

    # Determine outcome
    print("\n[STEP 6] CONCLUSION...")
    if trust_visible and not errors:
        print("  ✅ FORM ACCEPTED JS-SET DATE — navigated to Trust Details")
        print("  JavaScript injection is FULLY SUPPORTED.")
        conclusion = "FULLY_SUPPORTED"
    elif errors:
        # Check if date-related error
        date_errors = [e for e in errors if "date" in e.lower() or "noc" in e.lower()]
        if date_errors:
            print(f"  ❌ DATE REJECTED: {date_errors}")
            print("  JavaScript injection sets DOM but app does NOT recognize it.")
            conclusion = "NOT_SUPPORTED"
        else:
            print(f"  ⚠️ ERRORS but not date-related: {errors}")
            print("  Other field validation may be blocking.")
            conclusion = "INCONCLUSIVE"
    else:
        print("  ⚠️ No navigation and no errors — inconclusive")
        print("  May need additional event dispatch or the page didn't respond")
        conclusion = "INCONCLUSIVE"

    # Step 7: If navigated, go back and verify date persistence
    if trust_visible:
        print("\n[STEP 7] Verify date persistence — navigate back to NOC...")
        page.get_by_text("NOC Details", exact=False).first.click()
        page.wait_for_timeout(2000)
        noc_date_again = page.locator("#noc_date[name='noc_date']")
        if noc_date_again.is_visible():
            val_after_return = noc_date_again.evaluate("el => el.value")
            print(f"  Date value after returning: '{val_after_return}'")
            if val_after_return:
                print("  ✅ Date RETAINED after save and return.")
            else:
                print("  ⚠️ Date NOT retained — server may not have saved it.")
        page.screenshot(path="screenshots/debug/noc_js_verify_after_return.png")

    print("\n" + "=" * 70)
    print(f"FINAL CLASSIFICATION: {conclusion}")
    print("=" * 70)

    assert True
