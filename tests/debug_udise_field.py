"""
Diagnostic script: UDISE field behavior verification.
Run with: python -m pytest tests/debug_udise_field.py -v --headed -s
"""
import pytest
from pages.school_details_page import SchoolDetailsPage


def test_udise_field_diagnosis(school_details_ready_page):
    """
    Diagnose UDISE field behavior:
    1. Use .fill() with alphabets → read DOM value
    2. Use .type() with alphabets → read DOM value
    3. Capture actual validation message text
    """
    page = school_details_ready_page
    udise_field = page.locator("#udise")

    print("\n" + "=" * 60)
    print("UDISE FIELD DIAGNOSTIC")
    print("=" * 60)

    # --- TEST 1: .fill() with alphabets ---
    print("\n--- TEST 1: page.fill('abcdefghijk') ---")
    udise_field.fill("abcdefghijk")
    page.wait_for_timeout(500)
    value_after_fill = udise_field.input_value()
    print(f"  Value after .fill(): '{value_after_fill}'")
    print(f"  Length: {len(value_after_fill)}")
    print(f"  Conclusion: {'FILTERED (input mask active)' if value_after_fill != 'abcdefghijk' else 'NOT FILTERED (.fill bypassed mask)'}")

    # --- TEST 2: .fill() with special chars ---
    print("\n--- TEST 2: page.fill('123@#$456!!') ---")
    udise_field.fill("123@#$456!!")
    page.wait_for_timeout(500)
    value_after_fill_special = udise_field.input_value()
    print(f"  Value after .fill(): '{value_after_fill_special}'")
    print(f"  Length: {len(value_after_fill_special)}")

    # --- TEST 3: Clear and use .press_sequentially() ---
    print("\n--- TEST 3: clear + press_sequentially('abcdefghijk') ---")
    udise_field.fill("")  # Clear
    page.wait_for_timeout(300)
    udise_field.press_sequentially("abcdefghijk")
    page.wait_for_timeout(500)
    value_after_type = udise_field.input_value()
    print(f"  Value after .press_sequentially(): '{value_after_type}'")
    print(f"  Length: {len(value_after_type)}")
    print(f"  Conclusion: {'FILTERED (input mask works with typing)' if value_after_type != 'abcdefghijk' else 'NOT FILTERED'}")

    # --- TEST 4: Clear and use .press_sequentially() with special chars ---
    print("\n--- TEST 4: clear + press_sequentially('123@#$456!!') ---")
    udise_field.fill("")
    page.wait_for_timeout(300)
    udise_field.press_sequentially("123@#$456!!")
    page.wait_for_timeout(500)
    value_after_type_special = udise_field.input_value()
    print(f"  Value after .press_sequentially(): '{value_after_type_special}'")
    print(f"  Length: {len(value_after_type_special)}")

    # --- TEST 5: Click Next with invalid value and capture validation ---
    print("\n--- TEST 5: Click Next and capture validation messages ---")
    # Fill other mandatory fields first
    page.get_by_role("textbox", name="Name of School *").fill("Diagnostic School")
    page.locator("#contact_person").fill("Test Person")
    page.locator("#contact_no").fill("9815311210")
    page.locator("#contact_email").fill("test@test.com")

    # Set UDISE to short value (should trigger length validation)
    udise_field.fill("")
    udise_field.press_sequentially("12345")  # Only 5 digits
    page.wait_for_timeout(500)
    value_before_next = udise_field.input_value()
    print(f"  UDISE value before Next: '{value_before_next}'")

    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(2000)

    # Capture ALL visible errors
    print("\n--- VALIDATION MESSAGES FOUND ---")
    error_selectors = [
        ".invalid-feedback",
        ".text-danger",
        "[class*='invalid']:not(input):not(select)",
        ".form-error",
        ".validation-error",
    ]
    all_errors = []
    for selector in error_selectors:
        try:
            elements = page.locator(selector).all()
            for el in elements:
                if el.is_visible():
                    text = el.inner_text().strip()
                    if text:
                        all_errors.append(f"  [{selector}] → '{text}'")
        except Exception:
            pass

    if all_errors:
        for err in all_errors:
            print(err)
    else:
        print("  NO VALIDATION MESSAGES FOUND")
        # Check if form navigated
        if page.locator("#TabAddressDetails").is_visible():
            print("  FORM NAVIGATED TO ADDRESS DETAILS (no validation)")
        else:
            print("  Form stayed but no error elements visible")

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    # Force pass — this is diagnostic only
    assert True
