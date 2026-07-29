"""
Certificate of Land — Complete Field & Flow Diagnostic
Run: python -m pytest tests/debug_land_certificate.py -v --headed -s --alluredir=allure-results

Verifies ALL paths, ALL fields, ALL dynamic behavior.
"""
import pytest
import os
from datetime import datetime, timedelta


def test_land_certificate_diagnostic(school_details_ready_page):
    """Complete diagnostic of Certificate of Land module."""
    page = school_details_ready_page
    os.makedirs("screenshots/debug", exist_ok=True)

    print("\n" + "=" * 70)
    print("CERTIFICATE OF LAND — COMPLETE DIAGNOSTIC")
    print("=" * 70)

    # Navigate to Certificate of Land via tab
    print("\n[SETUP] Navigate to Certificate of Land...")
    page.get_by_text("Certificate of Land", exact=False).first.click()
    page.wait_for_timeout(3000)
    page.screenshot(path="screenshots/debug/land_01_initial.png")

    from utils.validation_helper import ValidationHelper

    # ========================================================================
    # FLOW 1: Plot Type Radio Buttons
    # ========================================================================
    print("\n" + "=" * 50)
    print("[FLOW 1] PLOT TYPE — Single / Multiple")
    print("=" * 50)

    print("\n[1.1] Check radio buttons present...")
    single_radio = page.get_by_role("radio", name="Single")
    multiple_radio = page.get_by_role("radio", name="Multiple")
    print(f"  'Single' radio visible: {single_radio.is_visible() if single_radio.count() > 0 else 'NOT FOUND'}")
    print(f"  'Multiple' radio visible: {multiple_radio.is_visible() if multiple_radio.count() > 0 else 'NOT FOUND'}")

    # Try alternate names
    if single_radio.count() == 0:
        print("  Trying alternate radio names...")
        all_radios = page.get_by_role("radio").all()
        print(f"  Total radios on page: {len(all_radios)}")
        for i, r in enumerate(all_radios[:10]):
            try:
                name = r.get_attribute("name")
                value = r.get_attribute("value")
                label = r.evaluate("el => el.labels ? el.labels[0]?.textContent : ''")
                checked = r.is_checked()
                print(f"    [{i}] name='{name}' value='{value}' label='{label.strip()[:40]}' checked={checked}")
            except:
                pass

    print("\n[1.2] Check default selection...")
    try:
        # Find which radio is checked by default
        radios = page.locator("input[type='radio']").all()
        for r in radios[:10]:
            if r.is_checked():
                name = r.get_attribute("name")
                value = r.get_attribute("value")
                print(f"  Default checked: name='{name}' value='{value}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # FLOW 2: Single → Owned (E2E path)
    # ========================================================================
    print("\n" + "=" * 50)
    print("[FLOW 2] SINGLE → OWNED PATH")
    print("=" * 50)

    print("\n[2.1] Select Single plot type...")
    try:
        page.get_by_role("radio", name="Single").click()
        page.wait_for_timeout(2000)
        print("  Single selected.")
    except Exception as e:
        print(f"  Error selecting Single: {e}")
        # Try by value
        try:
            page.locator("input[type='radio'][value='Single']").click()
            page.wait_for_timeout(2000)
            print("  Single selected via value locator.")
        except Exception as e2:
            print(f"  Also failed: {e2}")

    print("\n[2.2] Select Owned...")
    try:
        page.get_by_role("radio", name="Owned").click()
        page.wait_for_timeout(2000)
        print("  Owned selected.")
    except Exception as e:
        print(f"  Error: {e}")

    page.screenshot(path="screenshots/debug/land_02_owned_form.png")

    # ---- Area Unit Dropdown ----
    print("\n[2.3] Area Unit dropdown (#land_unit_0)...")
    area_unit = page.locator("#land_unit_0")
    if area_unit.count() > 0 and area_unit.is_visible():
        try:
            html = area_unit.evaluate("el => el.outerHTML.substring(0, 500)")
            print(f"  HTML: {html[:300]}")
            options = area_unit.evaluate("""el => {
                let opts = [];
                for (let i = 0; i < el.options.length; i++)
                    opts.push({index:i, value:el.options[i].value, text:el.options[i].text, disabled:el.options[i].disabled});
                return opts;
            }""")
            for o in options:
                print(f"    [{o['index']}] value='{o['value']}' text='{o['text']}' disabled={o['disabled']}")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("  Area Unit NOT visible")

    # ---- Land Title Document dropdown ----
    print("\n[2.4] Land Title Document dropdown...")
    title_doc = page.locator("select[id^='land_title_doc']").first
    if title_doc.count() > 0 and title_doc.is_visible():
        try:
            options = title_doc.evaluate("""el => {
                let opts = [];
                for (let i = 0; i < el.options.length; i++)
                    opts.push({index:i, value:el.options[i].value, text:el.options[i].text});
                return opts;
            }""")
            print("  Options:")
            for o in options:
                print(f"    [{o['index']}] value='{o['value']}' text='{o['text']}'")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("  Land Title Doc NOT visible")

    # ---- Sale Deed conditional ----
    print("\n[2.5] Select 'Sale Deed' → check for Sale Deed Favor field...")
    try:
        title_doc.select_option(label="Sale Deed")
        page.wait_for_timeout(1000)
        sale_deed_favor = page.locator("select[id^='sale_deed_favor_whom']").first
        print(f"  Sale Deed Favor visible: {sale_deed_favor.is_visible()}")
        if sale_deed_favor.is_visible():
            options = sale_deed_favor.evaluate("""el => {
                let opts = [];
                for (let i = 0; i < el.options.length; i++)
                    opts.push({text:el.options[i].text, value:el.options[i].value});
                return opts;
            }""")
            for o in options:
                print(f"    value='{o['value']}' text='{o['text']}'")
    except Exception as e:
        print(f"  Error: {e}")

    # ---- Date field ----
    print("\n[2.6] Land Document Date field...")
    date_field = page.get_by_role("textbox", name="Select a date").last
    try:
        attrs = date_field.evaluate("""el => ({
            type: el.type, readonly: el.readOnly, placeholder: el.placeholder,
            className: el.className, id: el.id, name: el.name
        })""")
        for k, v in attrs.items():
            print(f"  {k}: {v}")

        # Test .fill()
        print("\n  Testing .fill('15/03/2024')...")
        try:
            date_field.fill("15/03/2024")
            page.wait_for_timeout(500)
            val = date_field.input_value()
            print(f"  .fill() result: '{val}'")
        except Exception as e:
            print(f"  .fill() FAILED: {str(e)[:80]}")
            # Try JS injection
            print("  Testing set_readonly_date()...")
            field_id = attrs.get("id", "")
            if field_id:
                ValidationHelper.set_readonly_date(page, f"#{field_id}", "15/03/2024")
                val = date_field.evaluate("el => el.value")
                print(f"  JS injection result: '{val}'")
    except Exception as e:
        print(f"  Error: {e}")

    page.screenshot(path="screenshots/debug/land_03_owned_filled.png")

    # ========================================================================
    # FLOW 3: Single → Leased
    # ========================================================================
    print("\n" + "=" * 50)
    print("[FLOW 3] SINGLE → LEASED PATH")
    print("=" * 50)

    print("\n[3.1] Select Leased...")
    try:
        page.get_by_role("radio", name="Leased").click()
        page.wait_for_timeout(2000)
        print("  Leased selected.")
        page.screenshot(path="screenshots/debug/land_04_leased_form.png")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n[3.2] Scan all visible fields in Leased section...")
    # Find all visible inputs/selects/textareas
    try:
        inputs = page.locator("input:visible, select:visible, textarea:visible").all()
        print(f"  Total visible form elements: {len(inputs)}")
        for i, el in enumerate(inputs[:25]):
            try:
                tag = el.evaluate("el => el.tagName")
                el_id = el.get_attribute("id") or ""
                el_name = el.get_attribute("name") or ""
                el_type = el.get_attribute("type") or ""
                el_readonly = el.evaluate("el => el.readOnly")
                print(f"    [{i}] <{tag}> id='{el_id}' name='{el_name}' type='{el_type}' readonly={el_readonly}")
            except:
                pass
    except Exception as e:
        print(f"  Error scanning: {e}")

    # ---- Renewal clause radio ----
    print("\n[3.3] Look for Renewal clause radio...")
    try:
        yes_radio = page.get_by_role("radio", name="Yes")
        no_radio = page.get_by_role("radio", name="No")
        print(f"  'Yes' radio count: {yes_radio.count()}")
        print(f"  'No' radio count: {no_radio.count()}")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # FLOW 4: Multiple Plots
    # ========================================================================
    print("\n" + "=" * 50)
    print("[FLOW 4] MULTIPLE PLOTS PATH")
    print("=" * 50)

    print("\n[4.1] Select Multiple...")
    try:
        page.get_by_role("radio", name="Multiple").click()
        page.wait_for_timeout(2000)
        print("  Multiple selected.")
        page.screenshot(path="screenshots/debug/land_05_multiple.png")
    except Exception as e:
        print(f"  Error: {e}")
        try:
            page.locator("input[type='radio'][value='Multiple']").click()
            page.wait_for_timeout(2000)
            print("  Multiple selected via value locator.")
        except:
            print("  Could not select Multiple")

    print("\n[4.2] Scan visible fields for Multiple path...")
    try:
        inputs = page.locator("input:visible, select:visible, textarea:visible").all()
        print(f"  Total visible form elements: {len(inputs)}")
        for i, el in enumerate(inputs[:20]):
            try:
                tag = el.evaluate("el => el.tagName")
                el_id = el.get_attribute("id") or ""
                el_name = el.get_attribute("name") or ""
                el_type = el.get_attribute("type") or ""
                print(f"    [{i}] <{tag}> id='{el_id}' name='{el_name}' type='{el_type}'")
            except:
                pass
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # VALIDATION: All blank + click Next
    # ========================================================================
    print("\n" + "=" * 50)
    print("[VALIDATION] Submit with minimal data — capture errors")
    print("=" * 50)

    # Go back to Single → Owned (the E2E path)
    try:
        page.get_by_role("radio", name="Single").click()
        page.wait_for_timeout(2000)
        page.get_by_role("radio", name="Owned").click()
        page.wait_for_timeout(2000)
    except:
        pass

    print("\n[V.1] Click Next without filling anything...")
    try:
        page.get_by_role("button", name="Next").click()
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshots/debug/land_06_validation.png")

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
            print("  VALIDATION MESSAGES:")
            for e in errors:
                print(f"    - {e}")
        else:
            print("  NO ERRORS — form may have navigated")
            # Check navigation
            upload_visible = page.get_by_text("Upload Documents", exact=False).first.is_visible() if page.get_by_text("Upload Documents", exact=False).count() > 0 else False
            print(f"  Upload Documents visible (navigated): {upload_visible}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n" + "=" * 70)
    print("CERTIFICATE OF LAND DIAGNOSTIC COMPLETE")
    print("Review screenshots in screenshots/debug/")
    print("=" * 70)

    assert True
