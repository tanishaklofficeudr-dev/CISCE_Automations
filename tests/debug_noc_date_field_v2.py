"""
NOC Date Field Diagnostic v2
Run: python -m pytest tests/debug_noc_date_field_v2.py -v --headed -s --alluredir=allure-results

Uses the NOC Details tab directly (skips address district/city issues).
"""
import pytest
import os
from datetime import datetime, timedelta


def test_noc_date_field_v2(school_details_ready_page):
    """Navigate to NOC Details via tab click and diagnose Date field."""
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("NOC DATE FIELD DIAGNOSTIC v2")
    print("=" * 70)

    # ---- SETUP: Navigate to NOC Details via tab ----
    print("\n[SETUP] Navigating to NOC Details via step tab...")

    # Try clicking the NOC Details step tab directly
    try:
        page.get_by_text("NOC Details", exact=False).first.click()
        page.wait_for_timeout(3000)
    except Exception as e:
        print(f"  Could not click NOC tab directly: {e}")
        # Fallback: fill School + Address to reach NOC
        print("  Fallback: filling School Details...")
        from pages.school_details_page import SchoolDetailsPage
        SchoolDetailsPage(page).fill_partial_details({
            "school_name": "NOC Diag School", "school_classification": "Day",
            "school_type": "Co-ed.", "contact_person": "Test",
            "contact_number": "9815311210", "contact_email": "test.9815311210@gmail.com",
            "website": "https://www.test.com", "udise_number": "12345678901",
            "school_category": "Private",
        }, skip_fields=[])
        page.wait_for_timeout(3000)
        print("  Filling Address Details...")
        from pages.address_details_page import AddressDetailsPage
        AddressDetailsPage(page).fill_partial_details({
            "address_line_1": "123 Street", "country": "India",
            "state": "Rajasthan", "district": "Ajmer", "city": "",
            "zip_pin": "302001", "locality_type": "Urban",
        }, skip_fields=["city"])
        page.wait_for_timeout(3000)

    # Verify NOC date field is visible
    noc_date = page.locator("#noc_date[name='noc_date']")
    alt_noc_date = page.locator("#noc_date")

    # Try both locators
    date_field = noc_date if noc_date.count() > 0 else alt_noc_date
    print(f"  #noc_date[name='noc_date'] count: {noc_date.count()}")
    print(f"  #noc_date count: {alt_noc_date.count()}")

    if date_field.count() == 0 or not date_field.is_visible():
        print("  ERROR: Date field not found/visible.")
        page.screenshot(path="screenshots/debug/noc_date_v2_not_found.png")
        # Try tab again
        try:
            page.get_by_text("NOC Details", exact=False).first.click()
            page.wait_for_timeout(2000)
            date_field = page.locator("#noc_date")
            print(f"  After retry - #noc_date visible: {date_field.is_visible()}")
        except:
            pass

    if date_field.count() == 0 or not date_field.is_visible():
        print("  FATAL: Cannot find NOC date field. Taking screenshot and aborting.")
        page.screenshot(path="screenshots/debug/noc_date_v2_fatal.png")
        assert False, "NOC date field not reachable"

    print(f"  Date field visible: {date_field.is_visible()}")

    # ============================================================================
    # CHECK 1: HTML Attributes
    # ============================================================================
    print("\n[CHECK 1] Field HTML attributes...")
    try:
        attrs = date_field.evaluate("""el => ({
            type: el.type, readonly: el.readOnly, disabled: el.disabled,
            maxlength: el.maxLength, placeholder: el.placeholder,
            className: el.className, name: el.name, id: el.id,
            value: el.value, outerHTML: el.outerHTML.substring(0, 400)
        })""")
        for k, v in attrs.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 2: Is field read-only?
    # ============================================================================
    print("\n[CHECK 2] Is the field read-only?")
    try:
        readonly = date_field.evaluate("el => el.readOnly")
        disabled = date_field.evaluate("el => el.disabled")
        print(f"  readOnly: {readonly}")
        print(f"  disabled: {disabled}")
        print(f"  Conclusion: {'READ-ONLY' if readonly else 'EDITABLE'}")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 3: Can .fill() enter a date?
    # ============================================================================
    print("\n[CHECK 3] Can .fill() enter a date?")
    try:
        date_field.fill("16/05/2025")
        page.wait_for_timeout(500)
        val = date_field.input_value()
        print(f"  .fill('16/05/2025') → DOM value: '{val}'")
    except Exception as e:
        print(f"  .fill() FAILED: {e}")

    # ============================================================================
    # CHECK 4: Can .press_sequentially() enter a date?
    # ============================================================================
    print("\n[CHECK 4] Can .press_sequentially() enter a date?")
    try:
        date_field.fill("")
        page.wait_for_timeout(300)
        date_field.click()
        page.wait_for_timeout(300)
        date_field.press_sequentially("16/05/2025")
        page.wait_for_timeout(500)
        val = date_field.input_value()
        print(f"  .press_sequentially('16/05/2025') → DOM value: '{val}'")
    except Exception as e:
        print(f"  FAILED: {e}")

    # ============================================================================
    # CHECK 5: Does clicking open a calendar?
    # ============================================================================
    print("\n[CHECK 5] Does clicking the field open a calendar?")
    try:
        date_field.click()
        page.wait_for_timeout(1000)
        # Look for common datepicker elements
        datepicker_selectors = [
            ".datepicker", ".datepicker-dropdown", ".datepicker-days",
            ".bootstrap-datetimepicker-widget", "table.table-condensed",
            ".flatpickr-calendar", ".daterangepicker"
        ]
        found_calendar = False
        for sel in datepicker_selectors:
            if page.locator(sel).count() > 0:
                visible = page.locator(sel).first.is_visible()
                if visible:
                    print(f"  Calendar found: '{sel}' — VISIBLE")
                    found_calendar = True
                    break
        if not found_calendar:
            print("  No known calendar popup detected")
        page.screenshot(path="screenshots/debug/noc_date_v2_after_click.png")
        print("  Screenshot: noc_date_v2_after_click.png")
        # Close calendar by pressing Escape
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 6: Set past date and check value
    # ============================================================================
    print("\n[CHECK 6] Set past date via .fill('15/03/2024')...")
    try:
        date_field.fill("15/03/2024")
        page.wait_for_timeout(500)
        val = date_field.input_value()
        print(f"  Past date → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 7: Set future date
    # ============================================================================
    print("\n[CHECK 7] Set future date...")
    future = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
    try:
        date_field.fill(future)
        page.wait_for_timeout(500)
        val = date_field.input_value()
        print(f"  Future date ({future}) → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 8: Set today's date
    # ============================================================================
    print("\n[CHECK 8] Set today's date...")
    today = datetime.now().strftime("%d/%m/%Y")
    try:
        date_field.fill(today)
        page.wait_for_timeout(500)
        val = date_field.input_value()
        print(f"  Today ({today}) → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 9: Set invalid date
    # ============================================================================
    print("\n[CHECK 9] Set invalid date '99/99/9999'...")
    try:
        date_field.fill("99/99/9999")
        page.wait_for_timeout(500)
        val = date_field.input_value()
        print(f"  Invalid date → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 10: Set via JavaScript evaluation
    # ============================================================================
    print("\n[CHECK 10] Set date via JavaScript...")
    try:
        page.evaluate("""
            () => {
                const input = document.querySelector('#noc_date[name="noc_date"]') || document.querySelector('#noc_date');
                if (input) {
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value').set;
                    nativeInputValueSetter.call(input, '10/01/2025');
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        """)
        page.wait_for_timeout(500)
        val = date_field.input_value()
        print(f"  JS set '10/01/2025' → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 11: Fill other fields + valid past date + click Next
    # ============================================================================
    print("\n[CHECK 11] Fill all NOC fields + valid past date + click Next...")
    try:
        page.locator("#noc_authority").fill("District Education Officer")
        page.locator("#noc_designation").fill("Director")
        page.locator("#noc_office_address").fill("123 Office Lane")
        page.locator("#noc_country").select_option("2")
        page.wait_for_timeout(1000)
        page.locator("#noc_state").select_option("30")
        page.get_by_role("textbox", name="Select NOC Reference Number").fill("NOC-TEST-001")

        # Set valid past date
        date_field.fill("15/03/2025")
        page.wait_for_timeout(500)
        val = date_field.input_value()
        print(f"  Date before Next: '{val}'")

        page.screenshot(path="screenshots/debug/noc_date_v2_before_next_valid.png")
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshots/debug/noc_date_v2_after_next_valid.png")

        # Check if navigated
        trust_visible = page.get_by_text("Trust/Society/Company", exact=False).first.is_visible() if page.get_by_text("Trust/Society/Company", exact=False).count() > 0 else False
        print(f"  Trust Details visible (navigated): {trust_visible}")

        if not trust_visible:
            # Capture errors
            errors = []
            for sel in [".invalid-feedback", ".text-danger", "[class*='invalid']:not(input):not(select):not(textarea)"]:
                for el in page.locator(sel).all():
                    if el.is_visible():
                        t = el.inner_text().strip()
                        if t:
                            errors.append(t)
            print(f"  Errors: {errors}")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 12: Empty date + click Next
    # ============================================================================
    print("\n[CHECK 12] Empty date + click Next...")
    try:
        # Navigate back to NOC
        page.get_by_text("NOC Details", exact=False).first.click()
        page.wait_for_timeout(2000)

        # Clear date
        date_field_again = page.locator("#noc_date[name='noc_date']") if page.locator("#noc_date[name='noc_date']").count() > 0 else page.locator("#noc_date")
        date_field_again.fill("")
        page.wait_for_timeout(500)
        val = date_field_again.input_value()
        print(f"  Date after clear: '{val}'")

        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshots/debug/noc_date_v2_empty_after_next.png")

        # Capture errors
        errors = []
        for sel in [".invalid-feedback", ".text-danger", "[class*='invalid']:not(input):not(select):not(textarea)"]:
            for el in page.locator(sel).all():
                if el.is_visible():
                    t = el.inner_text().strip()
                    if t:
                        errors.append(t)
        print(f"  Errors with empty date: {errors}")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 13: Future date + click Next
    # ============================================================================
    print("\n[CHECK 13] Future date + click Next...")
    try:
        date_field_again = page.locator("#noc_date[name='noc_date']") if page.locator("#noc_date[name='noc_date']").count() > 0 else page.locator("#noc_date")
        date_field_again.fill(future)
        page.wait_for_timeout(500)
        val = date_field_again.input_value()
        print(f"  Future date set: '{val}'")

        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshots/debug/noc_date_v2_future_after_next.png")

        # Check
        trust_visible = page.get_by_text("Trust/Society/Company", exact=False).first.is_visible() if page.get_by_text("Trust/Society/Company", exact=False).count() > 0 else False
        print(f"  Trust visible (navigated with future date): {trust_visible}")

        if not trust_visible:
            errors = []
            for sel in [".invalid-feedback", ".text-danger", "[class*='invalid']:not(input):not(select):not(textarea)"]:
                for el in page.locator(sel).all():
                    if el.is_visible():
                        t = el.inner_text().strip()
                        if t:
                            errors.append(t)
            print(f"  Future date errors: {errors}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n" + "=" * 70)
    print("NOC DATE DIAGNOSTIC COMPLETE")
    print("=" * 70)

    assert True
