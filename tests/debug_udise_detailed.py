"""
Detailed UDISE field diagnostic with screenshots.
Run: python -m pytest tests/debug_udise_detailed.py -v --headed -s --alluredir=allure-results
"""
import pytest
import os
from datetime import datetime


def test_udise_detailed_diagnosis(school_details_ready_page):
    """
    Step-by-step diagnosis of UDISE field with alphabets.
    Captures screenshots at each stage.
    """
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("DETAILED UDISE DIAGNOSIS - SCH_NEG_07 (alphabets)")
    print("=" * 70)

    # Fill all other fields with valid data first
    print("\n[STEP 1] Filling all mandatory fields with valid data...")
    page.get_by_role("textbox", name="Name of School *").fill("Diagnostic School")
    page.get_by_label("School Classification *").select_option(label="Day")
    page.locator("#school_type").select_option(label="Co-ed.")
    page.locator("#contact_person").fill("Test Person")
    page.locator("#contact_no").fill("9815311210")
    page.locator("#contact_email").fill("test.9815311210@gmail.com")
    page.locator("#website").fill("https://www.test.com")
    page.get_by_label("School Category *").select_option(label="Private")
    page.wait_for_timeout(500)

    # Now handle UDISE
    udise = page.locator("#udise")

    print("\n[STEP 2] Clearing UDISE field...")
    udise.fill("")
    page.wait_for_timeout(500)
    val_after_clear = udise.input_value()
    print(f"  Value after clear: '{val_after_clear}'")

    print("\n[STEP 3] Filling UDISE with 'abcdefghijk' using .fill()...")
    udise.fill("abcdefghijk")
    page.wait_for_timeout(1000)
    val_after_fill = udise.input_value()
    print(f"  DOM value after .fill(): '{val_after_fill}'")
    page.screenshot(path="screenshots/debug/01_after_fill_alphabets.png")
    print("  Screenshot: 01_after_fill_alphabets.png")

    print("\n[STEP 4] Triggering blur/focus-out on UDISE field...")
    # Click somewhere else to trigger blur
    page.locator("#contact_person").click()
    page.wait_for_timeout(1000)
    val_after_blur = udise.input_value()
    print(f"  DOM value after blur: '{val_after_blur}'")
    page.screenshot(path="screenshots/debug/02_after_blur.png")
    print("  Screenshot: 02_after_blur.png")

    # Check if validation appeared after blur
    print("\n[STEP 5] Checking for validation messages after blur (before Next)...")
    errors_after_blur = []
    error_elements = page.locator("[class*='invalid']:not(input):not(select):not(textarea)").all()
    for el in error_elements:
        if el.is_visible():
            text = el.inner_text().strip()
            if text:
                errors_after_blur.append(text)
    print(f"  Errors visible after blur: {errors_after_blur}")
    page.screenshot(path="screenshots/debug/03_before_next_click.png")
    print("  Screenshot: 03_before_next_click.png")

    print("\n[STEP 6] Clicking Next button...")
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)  # Wait longer for server validation
    page.screenshot(path="screenshots/debug/04_after_next_click.png")
    print("  Screenshot: 04_after_next_click.png")

    # Check current state
    val_after_next = udise.input_value() if not page.locator("#TabAddressDetails").is_visible() else "N/A (navigated)"
    print(f"  DOM value after Next: '{val_after_next}'")

    # Check if navigated
    address_visible = page.locator("#TabAddressDetails").is_visible()
    print(f"  Address Details visible (navigated): {address_visible}")

    # Collect ALL error messages
    print("\n[STEP 7] Collecting all validation messages after Next...")
    all_selectors = [
        ".invalid-feedback",
        ".text-danger",
        "[class*='invalid']:not(input):not(select):not(textarea)",
        "[class*='error']",
        ".form-text.text-danger",
        "small.text-danger",
        "span.text-danger",
        "div.text-danger",
        "p.text-danger",
    ]
    all_errors = []
    for selector in all_selectors:
        try:
            elements = page.locator(selector).all()
            for el in elements:
                try:
                    if el.is_visible():
                        text = el.inner_text().strip()
                        if text and text not in all_errors:
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
        print("  NO ERRORS FOUND IN DOM")

    # Check if form navigated using multiple indicators
    print("\n[STEP 8] Navigation check...")
    print(f"  #TabAddressDetails visible: {page.locator('#TabAddressDetails').is_visible()}")
    try:
        address_heading = page.locator("p:has-text('Address Details')")
        print(f"  'Address Details' <p> count: {address_heading.count()}")
    except:
        print("  Could not check Address Details heading")

    # Final screenshot
    page.screenshot(path="screenshots/debug/05_final_state.png")
    print("  Screenshot: 05_final_state.png")

    print("\n[STEP 9] UDISE field HTML attributes...")
    try:
        field_type = udise.get_attribute("type")
        field_maxlength = udise.get_attribute("maxlength")
        field_pattern = udise.get_attribute("pattern")
        field_class = udise.get_attribute("class")
        print(f"  type: {field_type}")
        print(f"  maxlength: {field_maxlength}")
        print(f"  pattern: {field_pattern}")
        print(f"  class: {field_class}")
    except Exception as e:
        print(f"  Error reading attributes: {e}")

    # Get full outer HTML of the field
    print("\n[STEP 10] UDISE field outer HTML...")
    try:
        outer_html = udise.evaluate("el => el.outerHTML")
        print(f"  {outer_html[:300]}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n" + "=" * 70)
    print("DIAGNOSIS COMPLETE — Review screenshots in screenshots/debug/")
    print("=" * 70)

    assert True
