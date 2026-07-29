"""
Trust/Society/Company Details — Complete Field Diagnostic
Run: python -m pytest tests/debug_trust_details.py -v --headed -s --alluredir=allure-results
"""
import pytest
import os
from datetime import datetime, timedelta


def test_trust_details_diagnostic(school_details_ready_page):
    """
    Combined diagnostic for all Trust Details fields.
    Navigates to Trust Details via tab, then tests every field behavior.
    """
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("TRUST/SOCIETY/COMPANY DETAILS — COMPLETE DIAGNOSTIC")
    print("=" * 70)

    # Navigate to Trust Details via tab
    print("\n[SETUP] Navigate to Trust Details via tab...")
    page.get_by_text("Trust /Society /Company", exact=False).first.click()
    page.wait_for_timeout(3000)

    ownership = page.locator("#ownership_type")
    if not ownership.is_visible():
        print("  Retry tab click...")
        page.get_by_text("Trust", exact=False).first.click()
        page.wait_for_timeout(3000)

    print(f"  Ownership field visible: {ownership.is_visible()}")
    if not ownership.is_visible():
        page.screenshot(path="screenshots/debug/trust_not_found.png")
        assert False, "Cannot reach Trust Details page"

    # ========================================================================
    # DIAGNOSTIC 1: Ownership Type Dropdown
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 1] OWNERSHIP TYPE DROPDOWN")
    print("=" * 50)

    print("\n[1.1] Outer HTML...")
    try:
        html = ownership.evaluate("el => el.outerHTML.substring(0, 500)")
        print(f"  {html}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[1.2] All options...")
    try:
        options = ownership.evaluate("""el => {
            let opts = [];
            for (let i = 0; i < el.options.length; i++) {
                opts.push({index: i, value: el.options[i].value, text: el.options[i].text, disabled: el.options[i].disabled});
            }
            return opts;
        }""")
        for opt in options:
            print(f"  [{opt['index']}] value='{opt['value']}' text='{opt['text']}' disabled={opt['disabled']}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[1.3] select_option(label='Trust')...")
    try:
        ownership.select_option(label="Trust")
        page.wait_for_timeout(500)
        val = ownership.input_value()
        print(f"  Value after label select: '{val}'")
    except Exception as e:
        print(f"  FAILED: {e}")

    print("\n[1.4] select_option(index=0) — blank/disabled?")
    try:
        ownership.select_option(index=0)
        page.wait_for_timeout(500)
        val = ownership.input_value()
        print(f"  Value at index 0: '{val}'")
    except Exception as e:
        print(f"  FAILED (disabled placeholder): {e}")

    # Reset to a valid option
    try:
        ownership.select_option(index=1)
        page.wait_for_timeout(500)
    except:
        pass

    # ========================================================================
    # DIAGNOSTIC 2: Trust Name Field
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 2] TRUST NAME FIELD (#owner_name)")
    print("=" * 50)

    name_field = page.locator("#owner_name")
    print("\n[2.1] Field attributes...")
    try:
        attrs = name_field.evaluate("""el => ({
            type: el.type, readonly: el.readOnly, maxlength: el.maxLength,
            placeholder: el.placeholder, className: el.className
        })""")
        for k, v in attrs.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[2.2] Fill 'Test Trust Name'...")
    try:
        name_field.fill("Test Trust Name")
        page.wait_for_timeout(300)
        val = name_field.input_value()
        print(f"  Value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # DIAGNOSTIC 3: Establishment Date
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 3] ESTABLISHMENT DATE (#establishment_date)")
    print("=" * 50)

    est_date = page.locator("#establishment_date")

    print("\n[3.1] Field attributes...")
    try:
        attrs = est_date.evaluate("""el => ({
            type: el.type, readonly: el.readOnly, placeholder: el.placeholder,
            className: el.className, value: el.value
        })""")
        for k, v in attrs.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[3.2] .fill() attempt...")
    try:
        est_date.fill("01/01/2020")
        print(f"  .fill() succeeded: '{est_date.input_value()}'")
    except Exception as e:
        print(f"  .fill() FAILED (expected — readonly): {str(e)[:80]}")

    print("\n[3.3] set_readonly_date('05/03/2020')...")
    from utils.validation_helper import ValidationHelper
    try:
        ValidationHelper.set_readonly_date(page, "#establishment_date", "05/03/2020")
        val = est_date.evaluate("el => el.value")
        print(f"  Value after JS: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[3.4] set_readonly_date with future date...")
    future = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
    try:
        ValidationHelper.set_readonly_date(page, "#establishment_date", future)
        val = est_date.evaluate("el => el.value")
        print(f"  Future date ({future}) set: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # DIAGNOSTIC 4: Registration Date
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 4] REGISTRATION DATE (#registration_date)")
    print("=" * 50)

    reg_date = page.locator("#registration_date")

    print("\n[4.1] Field attributes...")
    try:
        attrs = reg_date.evaluate("""el => ({
            type: el.type, readonly: el.readOnly, placeholder: el.placeholder,
            className: el.className, value: el.value
        })""")
        for k, v in attrs.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[4.2] set_readonly_date('10/04/2021')...")
    try:
        ValidationHelper.set_readonly_date(page, "#registration_date", "10/04/2021")
        val = reg_date.evaluate("el => el.value")
        print(f"  Value after JS: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # DIAGNOSTIC 5: Registration Number
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 5] REGISTRATION NUMBER (#registration_no)")
    print("=" * 50)

    reg_no = page.locator("#registration_no")

    print("\n[5.1] Field attributes...")
    try:
        attrs = reg_no.evaluate("""el => ({
            type: el.type, readonly: el.readOnly, maxlength: el.maxLength,
            placeholder: el.placeholder, className: el.className
        })""")
        for k, v in attrs.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[5.2] Fill with alphabets 'ABCXYZ'...")
    try:
        reg_no.fill("ABCXYZ")
        val = reg_no.input_value()
        print(f"  Value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[5.3] Fill with special chars 'REG@#$%'...")
    try:
        reg_no.fill("REG@#$%")
        val = reg_no.input_value()
        print(f"  Value: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # DIAGNOSTIC 6: Submit with valid data — verify form navigates
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 6] SUBMIT WITH VALID DATA")
    print("=" * 50)

    print("\n[6.1] Fill all fields with valid data...")
    ownership.select_option(index=1)
    page.wait_for_timeout(500)
    name_field.fill("Test Diagnostic Trust")
    ValidationHelper.set_readonly_date(page, "#establishment_date", "05/03/2020")
    ValidationHelper.set_readonly_date(page, "#registration_date", "10/04/2021")
    reg_no.fill("TRUST-REG-2021-001")
    page.wait_for_timeout(500)

    page.screenshot(path="screenshots/debug/trust_before_next_valid.png")
    print("  Screenshot: trust_before_next_valid.png")

    print("\n[6.2] Click Next...")
    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)

    # Check if Land Certificate appeared
    land_visible = False
    try:
        land_el = page.get_by_text("Certificate of Land", exact=False)
        if land_el.count() > 0:
            land_visible = land_el.first.is_visible()
    except:
        pass
    print(f"  Certificate of Land visible (navigated): {land_visible}")
    page.screenshot(path="screenshots/debug/trust_after_next_valid.png")

    if not land_visible:
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
        print(f"  ERRORS: {errors}")

    # ========================================================================
    # DIAGNOSTIC 7: Registration Date BEFORE Establishment Date
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 7] BUSINESS RULE: Reg Date < Est Date")
    print("=" * 50)

    # Navigate back
    page.get_by_text("Trust", exact=False).first.click()
    page.wait_for_timeout(3000)

    print("\n[7.1] Set Est=2022, Reg=2019 (reg before est)...")
    ownership.select_option(index=1)
    page.wait_for_timeout(500)
    name_field.fill("Business Rule Test Trust")
    ValidationHelper.set_readonly_date(page, "#establishment_date", "01/06/2022")
    ValidationHelper.set_readonly_date(page, "#registration_date", "15/03/2019")
    reg_no.fill("BR-TEST-001")

    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)

    land_visible_2 = False
    try:
        land_el = page.get_by_text("Certificate of Land", exact=False)
        if land_el.count() > 0:
            land_visible_2 = land_el.first.is_visible()
    except:
        pass
    print(f"  Navigated (accepted): {land_visible_2}")

    if not land_visible_2:
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
        print(f"  ERRORS: {errors}")
    else:
        print("  ⚠️ Form ACCEPTED Reg Date < Est Date — no validation for this rule")

    # ========================================================================
    # DIAGNOSTIC 8: Future Establishment Date
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 8] FUTURE ESTABLISHMENT DATE")
    print("=" * 50)

    page.get_by_text("Trust", exact=False).first.click()
    page.wait_for_timeout(3000)

    print("\n[8.1] Set future establishment date...")
    ownership.select_option(index=1)
    page.wait_for_timeout(500)
    name_field.fill("Future Date Test Trust")
    ValidationHelper.set_readonly_date(page, "#establishment_date", future)
    ValidationHelper.set_readonly_date(page, "#registration_date", "10/04/2021")
    reg_no.fill("FUT-TEST-001")

    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)

    land_visible_3 = False
    try:
        land_el = page.get_by_text("Certificate of Land", exact=False)
        if land_el.count() > 0:
            land_visible_3 = land_el.first.is_visible()
    except:
        pass
    print(f"  Navigated (accepted): {land_visible_3}")

    if not land_visible_3:
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
        print(f"  ERRORS: {errors}")
    else:
        print("  ⚠️ Future establishment date ACCEPTED — potential app defect")

    # ========================================================================
    # DIAGNOSTIC 9: All Fields Blank — Validation Messages
    # ========================================================================
    print("\n" + "=" * 50)
    print("[DIAG 9] ALL FIELDS BLANK — VALIDATION MESSAGES")
    print("=" * 50)

    page.get_by_text("Trust", exact=False).first.click()
    page.wait_for_timeout(3000)

    print("\n[9.1] Clear all text fields + dates...")
    name_field.fill("")
    reg_no.fill("")
    ValidationHelper.set_readonly_date(page, "#establishment_date", "")
    ValidationHelper.set_readonly_date(page, "#registration_date", "")

    page.get_by_role("button", name="Next").click()
    page.wait_for_timeout(3000)

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
        print("  VALIDATION MESSAGES FOUND:")
        for e in errors:
            print(f"    • {e}")
    else:
        print("  NO ERRORS — form may have navigated")

    page.screenshot(path="screenshots/debug/trust_all_blank_errors.png")

    print("\n" + "=" * 70)
    print("TRUST DETAILS DIAGNOSTIC COMPLETE")
    print("=" * 70)

    assert True
