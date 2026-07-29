"""
PIN Code Field Diagnostic — Address Details Module
Run: python -m pytest tests/debug_pin_code_field.py -v --headed -s --alluredir=allure-results

Verifies:
1. Does .fill() with alphabets retain the value in DOM?
2. Does .fill() with special chars retain the value?
3. Does .press_sequentially() behave differently?
4. What validation message appears for invalid PIN?
5. What validation appears for wrong length?
6. Field HTML attributes (type, maxlength, pattern)
"""
import pytest
import os


def test_pin_code_diagnosis(school_details_ready_page):
    """
    Navigate to Address Details, then diagnose PIN code field.
    Uses school_details_ready_page + fills school details to reach Address.
    """
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("PIN CODE FIELD DIAGNOSTIC — Address Details")
    print("=" * 70)

    # First, submit School Details to reach Address Details
    print("\n[SETUP] Filling School Details to navigate to Address Details...")
    from pages.school_details_page import SchoolDetailsPage
    school_page = SchoolDetailsPage(page)

    school_data = {
        "school_name": "PIN Diagnostic School",
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

    # Verify we're on Address Details
    print(f"  Current URL: {page.url}")
    page.screenshot(path="screenshots/debug/pin_00_address_page.png")

    # Check if ZIP field is visible
    zip_field = page.locator("#zip")
    if not zip_field.is_visible():
        print("  ERROR: ZIP field not visible! May not be on Address Details page.")
        print("  Checking if Address Details tab/content is active...")
        # Try clicking Address Details tab
        page.get_by_text("Address Details", exact=False).first.click()
        page.wait_for_timeout(2000)

    print(f"  ZIP field visible: {zip_field.is_visible()}")

    # ---- FIELD ATTRIBUTES ----
    print("\n[STEP 1] ZIP field HTML attributes...")
    try:
        field_type = zip_field.get_attribute("type")
        field_maxlength = zip_field.get_attribute("maxlength")
        field_pattern = zip_field.get_attribute("pattern")
        field_class = zip_field.get_attribute("class")
        field_placeholder = zip_field.get_attribute("placeholder")
        print(f"  type: {field_type}")
        print(f"  maxlength: {field_maxlength}")
        print(f"  pattern: {field_pattern}")
        print(f"  class: {field_class}")
        print(f"  placeholder: {field_placeholder}")
    except Exception as e:
        print(f"  Error reading attributes: {e}")

    print("\n[STEP 2] ZIP field outer HTML...")
    try:
        outer_html = zip_field.evaluate("el => el.outerHTML")
        print(f"  {outer_html[:300]}")
    except Exception as e:
        print(f"  Error: {e}")

    # ---- TEST .fill() with alphabets ----
    print("\n[STEP 3] .fill('abcdef') — alphabets...")
    zip_field.fill("abcdef")
    page.wait_for_timeout(500)
    val = zip_field.input_value()
    print(f"  Value after .fill('abcdef'): '{val}'")
    print(f"  Conclusion: {'FILTERED' if val != 'abcdef' else 'NOT FILTERED — accepts alphabets'}")

    # ---- TEST .fill() with special chars ----
    print("\n[STEP 4] .fill('12@#56') — special chars...")
    zip_field.fill("12@#56")
    page.wait_for_timeout(500)
    val = zip_field.input_value()
    print(f"  Value after .fill('12@#56'): '{val}'")
    print(f"  Conclusion: {'FILTERED' if val != '12@#56' else 'NOT FILTERED'}")

    # ---- TEST .press_sequentially() with alphabets ----
    print("\n[STEP 5] clear + .press_sequentially('abcdef') — alphabets...")
    zip_field.fill("")
    page.wait_for_timeout(300)
    zip_field.press_sequentially("abcdef")
    page.wait_for_timeout(500)
    val = zip_field.input_value()
    print(f"  Value after .press_sequentially('abcdef'): '{val}'")
    print(f"  Conclusion: {'FILTERED' if val != 'abcdef' else 'NOT FILTERED'}")

    # ---- TEST .press_sequentially() with special chars ----
    print("\n[STEP 6] clear + .press_sequentially('12@#56') — special chars...")
    zip_field.fill("")
    page.wait_for_timeout(300)
    zip_field.press_sequentially("12@#56")
    page.wait_for_timeout(500)
    val = zip_field.input_value()
    print(f"  Value after .press_sequentially('12@#56'): '{val}'")
    print(f"  Conclusion: {'FILTERED' if val != '12@#56' else 'NOT FILTERED'}")

    # ---- TEST with 5 digits (less than 6) ----
    print("\n[STEP 7] .fill('12345') — 5 digits (less than required)...")
    zip_field.fill("12345")
    page.wait_for_timeout(500)
    val = zip_field.input_value()
    print(f"  Value in field: '{val}'")

    # ---- TEST blur behavior ----
    print("\n[STEP 8] Triggering blur on ZIP field...")
    page.locator("#address_1").click()  # Click another field
    page.wait_for_timeout(1000)

    # Check for validation after blur
    errors_after_blur = []
    try:
        error_elements = page.locator("[class*='invalid']:not(input):not(select):not(textarea)").all()
        for el in error_elements:
            if el.is_visible():
                text = el.inner_text().strip()
                if text and "pin" in text.lower() or "zip" in text.lower() or "digit" in text.lower():
                    errors_after_blur.append(text)
    except:
        pass
    print(f"  PIN-related errors after blur: {errors_after_blur}")

    # ---- Fill mandatory fields and click Next with invalid PIN ----
    print("\n[STEP 9] Fill all address fields + invalid PIN, click Next...")

    # Fill address line
    page.locator("#address_1").fill("123 Test Street, Diagnostic Lane")

    # Country
    try:
        page.get_by_role("textbox", name="India").click()
        page.get_by_role("option", name="India").click()
        page.wait_for_timeout(1000)
    except:
        print("  Country already selected or selection failed")

    # State
    try:
        page.locator("#select2-state-container").click()
        page.wait_for_timeout(500)
        page.get_by_role("option", name="Rajasthan").click()
        page.wait_for_timeout(1000)
    except:
        print("  State selection failed or already selected")

    # District
    try:
        page.get_by_role("textbox", name="Select").click()
        page.wait_for_timeout(500)
        page.get_by_role("option").first.click()
        page.wait_for_timeout(1000)
    except:
        print("  District selection failed")

    # City
    try:
        page.get_by_role("textbox", name="Select").click()
        page.wait_for_timeout(500)
        page.get_by_role("option").first.click()
        page.wait_for_timeout(1000)
    except:
        print("  City selection failed")

    # Locality
    try:
        page.locator("#locality").select_option(index=1)
    except:
        print("  Locality selection failed")

    # Set invalid PIN
    zip_field.fill("12345")  # 5 digits — should trigger validation
    page.wait_for_timeout(500)
    page.screenshot(path="screenshots/debug/pin_01_before_next.png")
    print("  Screenshot: pin_01_before_next.png")

    # Click Next
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)
    page.screenshot(path="screenshots/debug/pin_02_after_next.png")
    print("  Screenshot: pin_02_after_next.png")

    # ---- Capture ALL validation messages ----
    print("\n[STEP 10] All validation messages after Next...")
    all_selectors = [
        ".invalid-feedback",
        ".text-danger",
        "[class*='invalid']:not(input):not(select):not(textarea)",
        "small.text-danger",
        "span.text-danger",
        "div.text-danger",
    ]
    all_errors = []
    for selector in all_selectors:
        try:
            elements = page.locator(selector).all()
            for el in elements:
                try:
                    if el.is_visible():
                        text = el.inner_text().strip()
                        if text and text not in [e.split(" → ")[1].strip("'") for e in all_errors]:
                            all_errors.append(f"[{selector}] → '{text}'")
                except:
                    pass
        except:
            pass

    if all_errors:
        print("  ERRORS FOUND:")
        for err in all_errors:
            print(f"    {err}")
    else:
        print("  NO ERRORS FOUND")
        # Check navigation
        noc_visible = page.locator("#TabNOCDetails").is_visible() if page.locator("#TabNOCDetails").count() > 0 else False
        print(f"  NOC Details tab visible (navigated): {noc_visible}")

    print("\n" + "=" * 70)
    print("PIN CODE DIAGNOSTIC COMPLETE")
    print("=" * 70)

    assert True
