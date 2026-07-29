"""
NOC Country & State Dropdown Diagnostic
Run: python -m pytest tests/debug_noc_country_state.py -v --headed -s --alluredir=allure-results
"""
import pytest
import os


def test_noc_country_state_diagnosis(school_details_ready_page):
    """
    Navigate to NOC Details page and diagnose Country/State dropdown behavior.
    """
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("NOC COUNTRY & STATE DROPDOWN DIAGNOSTIC")
    print("=" * 70)

    # ---- SETUP: Navigate to NOC Details ----
    print("\n[SETUP] Navigating to NOC Details...")

    # Fill School Details
    from pages.school_details_page import SchoolDetailsPage
    SchoolDetailsPage(page).fill_partial_details({
        "school_name": "Country State Diag School",
        "school_classification": "Day",
        "school_type": "Co-ed.",
        "contact_person": "Test",
        "contact_number": "9815311210",
        "contact_email": "test.9815311210@gmail.com",
        "website": "https://www.test.com",
        "udise_number": "12345678901",
        "school_category": "Private",
    }, skip_fields=[])
    page.wait_for_timeout(3000)

    # Fill Address Details — skip district/city to avoid Select2 issue
    from pages.address_details_page import AddressDetailsPage
    AddressDetailsPage(page).fill_partial_details({
        "address_line_1": "123 Diag Street",
        "country": "India",
        "state": "Rajasthan",
        "district": "Ajmer",
        "city": "",
        "zip_pin": "302001",
        "locality_type": "Urban",
    }, skip_fields=["city"])
    page.wait_for_timeout(3000)

    # Verify on NOC Details
    country_field = page.locator("#noc_country")
    if not country_field.is_visible():
        page.get_by_text("NOC Details", exact=False).first.click()
        page.wait_for_timeout(2000)

    print(f"  NOC Country field visible: {country_field.is_visible()}")
    if not country_field.is_visible():
        print("  ERROR: Cannot reach NOC Details. Aborting.")
        assert False, "Cannot reach NOC Details"

    # ============================================================================
    # CHECK 1: Field HTML attributes
    # ============================================================================
    print("\n[CHECK 1] Country field outer HTML...")
    try:
        html = country_field.evaluate("el => el.outerHTML.substring(0, 300)")
        print(f"  {html}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[CHECK 1b] State field outer HTML...")
    state_field = page.locator("#noc_state")
    try:
        html = state_field.evaluate("el => el.outerHTML.substring(0, 300)")
        print(f"  {html}")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 2: select_option(value) — how E2E does it
    # ============================================================================
    print("\n[CHECK 2] select_option(value='2') for Country (India)...")
    try:
        country_field.select_option("2")
        page.wait_for_timeout(500)
        val = country_field.input_value()
        print(f"  Country value after select_option('2'): '{val}'")
        print("  Result: SUCCESS")
    except Exception as e:
        print(f"  FAILED: {e}")

    # ============================================================================
    # CHECK 3: select_option(label) for Country
    # ============================================================================
    print("\n[CHECK 3] select_option(label='India') for Country...")
    try:
        country_field.select_option(label="India")
        page.wait_for_timeout(500)
        val = country_field.input_value()
        print(f"  Country value after select_option(label='India'): '{val}'")
        print("  Result: SUCCESS")
    except Exception as e:
        print(f"  FAILED: {e}")

    # ============================================================================
    # CHECK 4: select_option(index) for Country
    # ============================================================================
    print("\n[CHECK 4] select_option(index=1) for Country...")
    try:
        country_field.select_option(index=1)
        page.wait_for_timeout(500)
        val = country_field.input_value()
        selected_text = country_field.evaluate("el => el.options[el.selectedIndex].text")
        print(f"  Country value: '{val}', text: '{selected_text}'")
        print("  Result: SUCCESS")
    except Exception as e:
        print(f"  FAILED: {e}")

    # Reset to India
    country_field.select_option("2")
    page.wait_for_timeout(1000)

    # ============================================================================
    # CHECK 5: Does State load after Country selection?
    # ============================================================================
    print("\n[CHECK 5] State options after Country = India...")
    try:
        page.wait_for_timeout(1000)
        state_count = state_field.evaluate("el => el.options.length")
        first_state = state_field.evaluate("el => el.options[1] ? el.options[1].text : 'NONE'")
        print(f"  State options count: {state_count}")
        print(f"  First state option: '{first_state}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 6: select_option(value) for State
    # ============================================================================
    print("\n[CHECK 6] select_option(value='30') for State (Rajasthan)...")
    try:
        state_field.select_option("30")
        page.wait_for_timeout(500)
        val = state_field.input_value()
        print(f"  State value: '{val}'")
        print("  Result: SUCCESS")
    except Exception as e:
        print(f"  FAILED: {e}")

    # ============================================================================
    # CHECK 7: select_option(label) for State
    # ============================================================================
    print("\n[CHECK 7] select_option(label='Maharashtra') for State...")
    try:
        state_field.select_option(label="Maharashtra")
        page.wait_for_timeout(500)
        val = state_field.input_value()
        print(f"  State value after label select: '{val}'")
        print("  Result: SUCCESS")
    except Exception as e:
        print(f"  FAILED: {e}")

    # ============================================================================
    # CHECK 8: Can Country be changed to a different value?
    # ============================================================================
    print("\n[CHECK 8] Change Country to different value (index=2)...")
    try:
        country_field.select_option(index=2)
        page.wait_for_timeout(1500)
        val = country_field.input_value()
        country_text = country_field.evaluate("el => el.options[el.selectedIndex].text")
        print(f"  New country value: '{val}', text: '{country_text}'")

        # Check if State reset
        state_count_after = state_field.evaluate("el => el.options.length")
        state_val = state_field.input_value()
        print(f"  State options after Country change: {state_count_after}")
        print(f"  State value after Country change: '{state_val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # Reset back to India
    country_field.select_option("2")
    page.wait_for_timeout(1500)

    # ============================================================================
    # CHECK 9: Can dropdown be cleared (set to blank/Select)?
    # ============================================================================
    print("\n[CHECK 9] Can Country be set to blank/Select?")
    try:
        country_field.select_option(index=0)
        page.wait_for_timeout(500)
        val = country_field.input_value()
        text = country_field.evaluate("el => el.options[el.selectedIndex].text")
        print(f"  Country at index 0: value='{val}', text='{text}'")
        disabled = country_field.evaluate("el => el.options[0].disabled")
        print(f"  Index 0 disabled: {disabled}")
    except Exception as e:
        print(f"  Error: {e}")

    # ============================================================================
    # CHECK 10: Values retained — save and return
    # ============================================================================
    print("\n[CHECK 10] Current values before any save action...")
    try:
        country_val = country_field.input_value()
        state_val = state_field.input_value()
        print(f"  Country: '{country_val}', State: '{state_val}'")
    except Exception as e:
        print(f"  Error: {e}")

    page.screenshot(path="screenshots/debug/noc_country_state_final.png")
    print("  Screenshot: noc_country_state_final.png")

    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)

    assert True
