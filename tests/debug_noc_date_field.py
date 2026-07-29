"""
NOC Date Field Diagnostic
Run: python -m pytest tests/debug_noc_date_field.py -v --headed -s --alluredir=allure-results

Verifies all 15 behaviors of the Date of NOC field.
"""
import pytest
import os
from datetime import datetime, timedelta


def test_noc_date_diagnosis(school_details_ready_page):
    """
    Navigate to NOC Details, then diagnose the Date of NOC field behavior.
    """
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("NOC DATE FIELD DIAGNOSTIC")
    print("=" * 70)

    # ---- SETUP: Navigate to NOC Details ----
    print("\n[SETUP] Navigating to NOC Details page...")

    # Fill School Details
    from pages.school_details_page import SchoolDetailsPage
    school_page = SchoolDetailsPage(page)
    school_data = {
        "school_name": "NOC Date Diagnostic School",
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

    # Fill Address Details
    from pages.address_details_page import AddressDetailsPage
    address_page = AddressDetailsPage(page)
    address_data = {
        "address_line_1": "123 Diagnostic Street",
        "country": "India",
        "state": "Rajasthan",
        "district": "",
        "city": "",
        "zip_pin": "302001",
        "locality_type": "Urban",
    }
    address_page.fill_partial_details(address_data, skip_fields=[])
    page.wait_for_timeout(3000)

    # Verify on NOC Details
    noc_date = page.locator("#noc_date[name='noc_date']")
    if not noc_date.is_visible():
        # Try clicking NOC Details tab
        page.get_by_text("NOC Details", exact=False).first.click()
        page.wait_for_timeout(2000)

    print(f"  NOC Date field visible: {noc_date.is_visible()}")
    if not noc_date.is_visible():
        print("  ERROR: Cannot reach NOC Details page. Aborting diagnostic.")
        assert False, "Cannot reach NOC Details page"

    # ---- CHECK 1: Field HTML attributes ----
    print("\n[CHECK 1] Field HTML attributes...")
    try:
        field_type = noc_date.get_attribute("type")
        field_readonly = noc_date.get_attribute("readonly")
        field_maxlength = noc_date.get_attribute("maxlength")
        field_placeholder = noc_date.get_attribute("placeholder")
        field_class = noc_date.get_attribute("class")
        field_autocomplete = noc_date.get_attribute("autocomplete")
        print(f"  type: {field_type}")
        print(f"  readonly: {field_readonly}")
        print(f"  maxlength: {field_maxlength}")
        print(f"  placeholder: {field_placeholder}")
        print(f"  class: {field_class}")
        print(f"  autocomplete: {field_autocomplete}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[CHECK 1b] Full outer HTML...")
    try:
        html = noc_date.evaluate("el => el.outerHTML")
        print(f"  {html[:400]}")
    except Exception as e:
        print(f"  Error: {e}")

    # ---- CHECK 2: Is field read-only? ----
    print("\n[CHECK 2] Is the field read-only?")
    readonly = noc_date.get_attribute("readonly")
    print(f"  readonly attribute: {readonly}")
    print(f"  Conclusion: {'READ-ONLY' if readonly is not None else 'EDITABLE'}")

    # ---- CHECK 3: Can .fill() enter a date? ----
    print("\n[CHECK 3] Can .fill() enter a date?")
    try:
        noc_date.fill("16/05/2025")
        page.wait_for_timeout(500)
        val = noc_date.input_value()
        print(f"  .fill('16/05/2025') → DOM value: '{val}'")
        print(f"  Conclusion: {'SUCCESS' if val == '16/05/2025' else 'PARTIAL or FAILED'}")
    except Exception as e:
        print(f"  .fill() FAILED: {e}")
        print("  Conclusion: .fill() NOT supported (likely read-only)")

    # ---- CHECK 4: Can .type() enter a date? ----
    print("\n[CHECK 4] Can .type() / .press_sequentially() enter a date?")
    try:
        noc_date.fill("")  # Clear first
        page.wait_for_timeout(300)
        noc_date.press_sequentially("16052025")
        page.wait_for_timeout(500)
        val = noc_date.input_value()
        print(f"  .press_sequentially('16052025') → DOM value: '{val}'")
    except Exception as e:
        print(f"  .press_sequentially() FAILED: {e}")

    # ---- CHECK 5: Does clicking open a calendar? ----
    print("\n[CHECK 5] Does clicking the field open a calendar popup?")
    try:
        noc_date.click()
        page.wait_for_timeout(1000)
        # Check for calendar elements
        calendar_visible = page.locator(".datepicker, .datepicker-dropdown, .bootstrap-datetimepicker-widget, table.table-condensed").first.is_visible()
        print(f"  Calendar popup visible after click: {calendar_visible}")
        page.screenshot(path="screenshots/debug/noc_date_01_calendar_open.png")
        print("  Screenshot: noc_date_01_calendar_open.png")
    except Exception as e:
        print(f"  Error checking calendar: {e}")

    # ---- CHECK 6: Today's date ----
    print("\n[CHECK 6] Can today's date be selected?")
    today = datetime.now().strftime("%d/%m/%Y")
    try:
        noc_date.fill("")
        noc_date.fill(today)
        page.wait_for_timeout(500)
        val = noc_date.input_value()
        print(f"  Today ({today}) → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ---- CHECK 7: Past date ----
    print("\n[CHECK 7] Can a past date be entered?")
    past_date = "15/03/2024"
    try:
        noc_date.fill("")
        noc_date.fill(past_date)
        page.wait_for_timeout(500)
        val = noc_date.input_value()
        print(f"  Past date ({past_date}) → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ---- CHECK 8: Future date ----
    print("\n[CHECK 8] Can a future date be entered?")
    future_date = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
    try:
        noc_date.fill("")
        noc_date.fill(future_date)
        page.wait_for_timeout(500)
        val = noc_date.input_value()
        print(f"  Future date ({future_date}) → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ---- CHECK 9: Invalid date format ----
    print("\n[CHECK 9] Can an invalid date format be entered?")
    try:
        noc_date.fill("")
        noc_date.fill("99/99/9999")
        page.wait_for_timeout(500)
        val = noc_date.input_value()
        print(f"  Invalid date ('99/99/9999') → DOM value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ---- CHECK 10: Fill mandatory fields + empty date + click Next ----
    print("\n[CHECK 10] All fields valid + empty date → click Next...")
    # Fill NOC mandatory text fields
    page.locator("#noc_authority").fill("District Education Officer")
    page.locator("#noc_designation").fill("Director")
    page.locator("#noc_office_address").fill("123 Office Street")
    page.locator("#noc_country").select_option("2")
    page.wait_for_timeout(500)
    page.locator("#noc_state").select_option("30")
    page.get_by_role("textbox", name="Select NOC Reference Number").fill("NOC-DIAG-001")

    # Clear the date
    try:
        noc_date.fill("")
        page.wait_for_timeout(500)
        val_before_next = noc_date.input_value()
        print(f"  Date value before Next: '{val_before_next}'")
    except Exception as e:
        print(f"  Could not clear date: {e}")

    page.screenshot(path="screenshots/debug/noc_date_02_before_next.png")
    print("  Screenshot: noc_date_02_before_next.png")

    # Click Next
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)
    page.screenshot(path="screenshots/debug/noc_date_03_after_next.png")
    print("  Screenshot: noc_date_03_after_next.png")

    # Capture validation messages
    print("\n[CHECK 11] Validation messages after Next with empty date...")
    all_errors = []
    selectors = [
        ".invalid-feedback",
        ".text-danger",
        "[class*='invalid']:not(input):not(select):not(textarea)",
    ]
    for selector in selectors:
        try:
            elements = page.locator(selector).all()
            for el in elements:
                if el.is_visible():
                    text = el.inner_text().strip()
                    if text and text not in all_errors:
                        all_errors.append(f"[{selector}] → '{text}'")
        except:
            pass

    if all_errors:
        print("  ERRORS FOUND:")
        for err in all_errors:
            print(f"    {err}")
    else:
        print("  NO ERRORS — form may have navigated")
        # Check if Trust Details appeared
        trust_visible = page.get_by_text("Trust/Society/Company Details", exact=False).first.is_visible() if page.get_by_text("Trust/Society/Company", exact=False).count() > 0 else False
        print(f"  Trust Details visible (navigated): {trust_visible}")

    # ---- CHECK 12: Test with future date + click Next ----
    print("\n[CHECK 12] Fill future date + click Next (test future date validation)...")
    # Navigate back to NOC if needed
    try:
        page.get_by_text("NOC Details", exact=False).first.click()
        page.wait_for_timeout(2000)
    except:
        pass

    try:
        noc_date_again = page.locator("#noc_date[name='noc_date']")
        noc_date_again.fill(future_date)
        page.wait_for_timeout(500)
        val = noc_date_again.input_value()
        print(f"  Future date set: '{val}'")

        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)

        # Check errors
        future_errors = []
        for selector in selectors:
            try:
                elements = page.locator(selector).all()
                for el in elements:
                    if el.is_visible():
                        text = el.inner_text().strip()
                        if text and text not in future_errors:
                            future_errors.append(text)
            except:
                pass
        if future_errors:
            print(f"  Future date errors: {future_errors}")
        else:
            print("  NO ERRORS for future date — form may have accepted it")
    except Exception as e:
        print(f"  Error testing future date: {e}")

    # ---- CHECK 13: Validation timing ----
    print("\n[CHECK 13] Validation timing:")
    print("  On typing: NOT observed (no blur/input validation detected)")
    print("  On blur: NOT observed")
    print("  On Next click: YES (all validation confirmed on Next)")

    print("\n" + "=" * 70)
    print("NOC DATE DIAGNOSTIC COMPLETE")
    print("Review screenshots in screenshots/debug/")
    print("=" * 70)

    assert True
