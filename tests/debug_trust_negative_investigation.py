"""
Trust Negative Tests — Evidence-Based Investigation
Run: python -m pytest tests/debug_trust_negative_investigation.py -v --headed -s --alluredir=allure-results

Investigates WHY each negative test fails by capturing DOM values
before submit, after submit, and after returning to the page.
"""
import pytest
import os
from datetime import datetime, timedelta


def test_trust_negative_investigation(school_details_ready_page):
    """
    For each negative scenario:
    1. Clear target field
    2. Capture all DOM values BEFORE clicking Next
    3. Click Next
    4. Check navigation + errors
    5. Navigate back
    6. Capture all DOM values AFTER returning
    """
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("TRUST NEGATIVE TESTS — EVIDENCE INVESTIGATION")
    print("=" * 70)

    # Navigate to Trust Details
    page.get_by_text("Trust /Society /Company", exact=False).first.click()
    page.wait_for_timeout(3000)

    from utils.validation_helper import ValidationHelper

    def read_all_trust_values():
        """Read all Trust field DOM values."""
        vals = {}
        vals["ownership"] = page.locator("#ownership_type").input_value()
        vals["owner_name"] = page.locator("#owner_name").input_value()
        vals["establishment_date"] = page.locator("#establishment_date").evaluate("el => el.value")
        vals["registration_date"] = page.locator("#registration_date").evaluate("el => el.value")
        vals["registration_no"] = page.locator("#registration_no").input_value()
        return vals

    def check_navigation():
        try:
            land = page.get_by_text("Certificate of Land", exact=False)
            if land.count() > 0 and land.first.is_visible():
                return True
        except:
            pass
        return False

    def navigate_back():
        page.get_by_text("Trust /Society /Company", exact=False).first.click()
        page.wait_for_timeout(3000)

    # ========================================================================
    # SCENARIO 1: TRUST_FMT_001 — owner_name blank
    # ========================================================================
    print("\n" + "=" * 50)
    print("[TRUST_FMT_001] owner_name blank")
    print("=" * 50)

    # Fill valid baseline
    page.locator("#ownership_type").select_option(label="Trust")
    page.wait_for_timeout(500)
    page.locator("#owner_name").fill("Valid Baseline Trust")
    ValidationHelper.set_readonly_date(page, "#establishment_date", "05/03/2018")
    ValidationHelper.set_readonly_date(page, "#registration_date", "10/04/2019")
    page.locator("#registration_no").fill("VALID-REG-001")
    page.wait_for_timeout(500)

    # Clear target field
    page.locator("#owner_name").fill("")
    page.wait_for_timeout(500)

    # Capture DOM values BEFORE Next
    print("\n  [BEFORE NEXT] DOM values:")
    before = read_all_trust_values()
    for k, v in before.items():
        print(f"    {k}: '{v}'")

    page.screenshot(path="screenshots/debug/trust_fmt001_before_next.png")

    # Click Next
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)

    # Check result
    navigated = check_navigation()
    print(f"\n  [AFTER NEXT] Navigated: {navigated}")

    errors = []
    if not navigated:
        for sel in [".invalid-feedback", ".text-danger", "[class*='invalid']:not(input):not(select):not(textarea)"]:
            try:
                for el in page.locator(sel).all():
                    if el.is_visible():
                        t = el.inner_text().strip()
                        if t and t not in errors:
                            errors.append(t)
            except:
                pass
        print(f"  Errors: {errors}")
    else:
        print("  Form NAVIGATED — no validation blocked it.")

    page.screenshot(path="screenshots/debug/trust_fmt001_after_next.png")

    # Navigate back and check persistence
    navigate_back()
    print("\n  [AFTER RETURNING] DOM values:")
    after = read_all_trust_values()
    for k, v in after.items():
        changed = " ← CHANGED" if before.get(k) != v else ""
        print(f"    {k}: '{v}'{changed}")

    # ========================================================================
    # SCENARIO 2: TRUST_FMT_002 — registration_no blank
    # ========================================================================
    print("\n" + "=" * 50)
    print("[TRUST_FMT_002] registration_no blank")
    print("=" * 50)

    page.locator("#owner_name").fill("Valid Trust Name")
    ValidationHelper.set_readonly_date(page, "#establishment_date", "05/03/2018")
    ValidationHelper.set_readonly_date(page, "#registration_date", "10/04/2019")
    page.locator("#registration_no").fill("")  # Clear target
    page.wait_for_timeout(500)

    print("\n  [BEFORE NEXT] DOM values:")
    before = read_all_trust_values()
    for k, v in before.items():
        print(f"    {k}: '{v}'")

    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)

    navigated = check_navigation()
    print(f"\n  [AFTER NEXT] Navigated: {navigated}")
    if not navigated:
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
        print(f"  Errors: {errors}")

    if navigated:
        navigate_back()
        print("\n  [AFTER RETURNING] DOM values:")
        after = read_all_trust_values()
        for k, v in after.items():
            print(f"    {k}: '{v}'")

    # ========================================================================
    # SCENARIO 3: TRUST_FMT_003 — establishment_date empty
    # ========================================================================
    print("\n" + "=" * 50)
    print("[TRUST_FMT_003] establishment_date empty")
    print("=" * 50)

    if navigated:
        pass  # Already on trust page from navigate_back
    page.locator("#owner_name").fill("Valid Trust Name")
    page.locator("#registration_no").fill("VALID-REG-001")
    ValidationHelper.set_readonly_date(page, "#establishment_date", "")  # Clear
    ValidationHelper.set_readonly_date(page, "#registration_date", "10/04/2019")
    page.wait_for_timeout(500)

    print("\n  [BEFORE NEXT] DOM values:")
    before = read_all_trust_values()
    for k, v in before.items():
        print(f"    {k}: '{v}'")

    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)

    navigated = check_navigation()
    print(f"\n  [AFTER NEXT] Navigated: {navigated}")
    if not navigated:
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
        print(f"  Errors: {errors}")

    if navigated:
        navigate_back()
        print("\n  [AFTER RETURNING] establishment_date value:")
        est_val = page.locator("#establishment_date").evaluate("el => el.value")
        print(f"    establishment_date: '{est_val}'")
        if est_val:
            print("    ⚠️ SERVER RESTORED the date — cleared value was NOT submitted")
        else:
            print("    Date remained blank after return")

    # ========================================================================
    # SCENARIO 4: TRUST_FMT_004 — registration_date empty
    # ========================================================================
    print("\n" + "=" * 50)
    print("[TRUST_FMT_004] registration_date empty")
    print("=" * 50)

    page.locator("#owner_name").fill("Valid Trust Name")
    page.locator("#registration_no").fill("VALID-REG-001")
    ValidationHelper.set_readonly_date(page, "#establishment_date", "05/03/2018")
    ValidationHelper.set_readonly_date(page, "#registration_date", "")  # Clear
    page.wait_for_timeout(500)

    print("\n  [BEFORE NEXT] registration_date DOM value:")
    reg_val = page.locator("#registration_date").evaluate("el => el.value")
    print(f"    registration_date: '{reg_val}'")

    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)

    navigated = check_navigation()
    print(f"\n  [AFTER NEXT] Navigated: {navigated}")

    if navigated:
        navigate_back()
        reg_val_after = page.locator("#registration_date").evaluate("el => el.value")
        print(f"\n  [AFTER RETURNING] registration_date: '{reg_val_after}'")
        if reg_val_after:
            print("    ⚠️ SERVER RESTORED the date")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("INVESTIGATION COMPLETE")
    print("Review screenshots in screenshots/debug/")
    print("=" * 70)

    assert True
