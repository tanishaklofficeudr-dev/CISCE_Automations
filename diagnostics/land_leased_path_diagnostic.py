"""
Certificate of Land — Leased Path Complete Diagnostic
========================================================
Evidence-based investigation of the Single Plot → Leased flow.

Verifies every field, conditional behaviour, validation message,
and dynamic UI toggle with execution evidence.
"""

import sys
import os
import json
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from utils.excel_reader import ExcelReader


def run_diagnostic():
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # ====================================================================
        # LOGIN & NAVIGATE
        # ====================================================================
        print("=" * 70)
        print("STEP 1: Login and navigate to Certificate of Land")
        print("=" * 70)

        excel = ExcelReader("test_data/negative/Validation_Data.xlsx")
        login_data = excel.get_sheet_data("Common_Login")[0]

        registration_data = {
            "mobile_number": login_data["mobile_number"],
            "email": "tannu.9879090210@yopmail.com",
        }
        RegistrationPage(page).register_school(registration_data)
        LoginPage(page).login_automated(login_data)

        page.wait_for_url("**/preliminary/school/dashboard", timeout=30000)
        page.wait_for_timeout(3000)

        page.get_by_text("Certificate of Land", exact=False).first.click()
        page.wait_for_timeout(3000)
        print("Navigated to Certificate of Land page.")

        # ====================================================================
        # DIAGNOSTIC 1: Select Single + Leased
        # ====================================================================
        print("\n" + "=" * 70)
        print("DIAGNOSTIC 1: Select Single + Leased — Form Loading")
        print("=" * 70)

        page.get_by_role("radio", name="Single").click()
        page.wait_for_timeout(2000)
        page.get_by_role("radio", name="Leased").click()
        page.wait_for_timeout(2000)

        # Check if Leased fields are visible
        leased_fields_check = page.evaluate("""
            () => {
                const fields = [
                    {id: 'lease_area_unit_0', label: 'Lease Area Unit'},
                    {id: 'lease_land_area_0', label: 'Lease Land Area'},
                    {id: 'leease_name_0', label: 'Name of Lessee'},
                    {id: 'leaser_name_0', label: 'Name of Lessor'},
                    {id: 'lease_deed_date_0', label: 'Date of Lease Deed'},
                    {id: 'lease_deed_duration_0', label: 'Duration of Lease Deed'},
                    {id: 'date_regis_lease_deed0', label: 'Date of Registration'},
                    {id: 'regid_ofc_details0', label: 'Registration Office'},
                ];
                return fields.map(f => {
                    const el = document.querySelector('#' + f.id);
                    return {
                        id: f.id,
                        label: f.label,
                        found: !!el,
                        visible: el ? el.offsetParent !== null : false,
                        type: el ? el.tagName + '/' + (el.type || '') : 'NOT FOUND',
                        readonly: el ? el.readOnly : null,
                        disabled: el ? el.disabled : null,
                        value: el ? el.value : '',
                        placeholder: el ? el.placeholder : '',
                        className: el ? el.className : '',
                    };
                });
            }
        """)
        print("\nLeased Fields Status:")
        for f in leased_fields_check:
            status = "✅ VISIBLE" if f['visible'] else "❌ HIDDEN/NOT FOUND"
            print(f"  [{status}] #{f['id']} ({f['label']}) — {f['type']} readonly={f['readonly']} value='{f['value']}'")
        results["leased_fields"] = leased_fields_check

        # ====================================================================
        # DIAGNOSTIC 2: Renewal Clause Radios
        # ====================================================================
        print("\n" + "=" * 70)
        print("DIAGNOSTIC 2: Renewal Clause Radio Buttons")
        print("=" * 70)

        renewal_radios = page.evaluate("""
            () => {
                const radios = document.querySelectorAll('input[type="radio"]');
                const renewalRadios = [];
                radios.forEach(r => {
                    if (r.id.includes('renewal') || r.name.includes('renewal') ||
                        r.id.includes('plotType') || r.name.includes('plotType')) {
                        renewalRadios.push({
                            id: r.id,
                            name: r.name,
                            value: r.value,
                            checked: r.checked,
                            visible: r.offsetParent !== null,
                            labels: Array.from(r.labels || []).map(l => l.textContent.trim()),
                            parentText: r.parentElement ? r.parentElement.textContent.trim().substring(0, 50) : ''
                        });
                    }
                });
                return renewalRadios;
            }
        """)
        print("\nRenewal/PlotType Radio Buttons Found:")
        for r in renewal_radios:
            status = "✅" if r['visible'] else "❌"
            print(f"  {status} id='{r['id']}' name='{r['name']}' value='{r['value']}' checked={r['checked']} visible={r['visible']}")
            print(f"      labels={r['labels']} parentText='{r['parentText'][:40]}'")
        results["renewal_radios"] = renewal_radios

        # Also check for any "Yes"/"No" radios with get_by_role
        yes_radios = page.get_by_role("radio", name="Yes")
        no_radios = page.get_by_role("radio", name="No")
        yes_count = yes_radios.count()
        no_count = no_radios.count()
        print(f"\n  get_by_role('radio', name='Yes') count: {yes_count}")
        print(f"  get_by_role('radio', name='No') count: {no_count}")
        results["yes_radio_count"] = yes_count
        results["no_radio_count"] = no_count

        # Check visibility of each
        for i in range(yes_count):
            vis = yes_radios.nth(i).is_visible()
            rid = yes_radios.nth(i).get_attribute("id")
            print(f"    Yes[{i}]: id='{rid}' visible={vis}")

        for i in range(no_count):
            vis = no_radios.nth(i).is_visible()
            rid = no_radios.nth(i).get_attribute("id")
            print(f"    No[{i}]: id='{rid}' visible={vis}")

        # ====================================================================
        # DIAGNOSTIC 3: Full DOM scan for ALL visible fields on Leased form
        # ====================================================================
        print("\n" + "=" * 70)
        print("DIAGNOSTIC 3: Full DOM Scan — All Visible Inputs on Leased Form")
        print("=" * 70)

        all_visible_inputs = page.evaluate("""
            () => {
                const inputs = document.querySelectorAll('input, select, textarea');
                const visible = [];
                inputs.forEach((el, i) => {
                    if (el.offsetParent !== null && el.type !== 'hidden') {
                        visible.push({
                            index: i,
                            tag: el.tagName,
                            id: el.id,
                            name: el.name,
                            type: el.type,
                            placeholder: el.placeholder || '',
                            readonly: el.readOnly,
                            disabled: el.disabled,
                            value: el.value,
                            className: el.className.substring(0, 60)
                        });
                    }
                });
                return visible;
            }
        """)
        print(f"\nTotal visible input/select/textarea elements: {len(all_visible_inputs)}")
        for inp in all_visible_inputs:
            print(f"  [{inp['index']}] <{inp['tag'].lower()} id='{inp['id']}' name='{inp['name']}' type='{inp['type']}' readonly={inp['readonly']} value='{inp['value'][:30]}'>")
        results["all_visible_inputs_leased"] = all_visible_inputs

        # ====================================================================
        # DIAGNOSTIC 4: Date Fields — Readonly Check
        # ====================================================================
        print("\n" + "=" * 70)
        print("DIAGNOSTIC 4: Date Fields — Readonly Status")
        print("=" * 70)

        date_fields = ['lease_deed_date_0', 'date_regis_lease_deed0']
        for df_id in date_fields:
            el = page.locator(f"#{df_id}")
            if el.count() > 0:
                readonly_attr = el.get_attribute("readonly")
                el_class = el.get_attribute("class") or ""
                el_placeholder = el.get_attribute("placeholder") or ""
                el_visible = el.is_visible()
                print(f"\n  #{df_id}:")
                print(f"    visible: {el_visible}")
                print(f"    readonly attr: '{readonly_attr}'")
                print(f"    class: '{el_class}'")
                print(f"    placeholder: '{el_placeholder}'")
                print(f"    has datepicker class: {'datepicker' in el_class}")

                # Try .fill()
                if el_visible:
                    try:
                        el.click(timeout=2000)
                        page.wait_for_timeout(500)
                        el.fill("15/03/2020", timeout=5000)
                        val = el.input_value()
                        print(f"    .fill() result: '{val}' ✅")
                        results[f"{df_id}_fill"] = {"success": True, "value": val}
                    except Exception as e:
                        print(f"    .fill() FAILED: {str(e)[:80]}")
                        results[f"{df_id}_fill"] = {"success": False, "error": str(e)[:80]}

                        # Try JS injection
                        page.evaluate(f"""
                            () => {{
                                const el = document.querySelector('#{df_id}');
                                if (el) {{
                                    const setter = Object.getOwnPropertyDescriptor(
                                        window.HTMLInputElement.prototype, 'value').set;
                                    setter.call(el, '15/03/2020');
                                    el.dispatchEvent(new Event('input', {{bubbles: true}}));
                                    el.dispatchEvent(new Event('change', {{bubbles: true}}));
                                    el.dispatchEvent(new Event('blur', {{bubbles: true}}));
                                }}
                            }}
                        """)
                        page.wait_for_timeout(300)
                        val = el.input_value()
                        print(f"    JS injection result: '{val}' {'✅' if val else '❌'}")
                        results[f"{df_id}_js"] = {"success": bool(val), "value": val}
            else:
                print(f"\n  #{df_id}: NOT FOUND on page")
                results[f"{df_id}_found"] = False

        # ====================================================================
        # DIAGNOSTIC 5: Lease Duration Field
        # ====================================================================
        print("\n" + "=" * 70)
        print("DIAGNOSTIC 5: Lease Deed Duration — Text Input Behaviour")
        print("=" * 70)

        duration_el = page.locator("#lease_deed_duration_0")
        if duration_el.count() > 0 and duration_el.is_visible():
            # Clear and test .fill()
            duration_el.click()
            duration_el.fill("30")
            val = duration_el.input_value()
            print(f"  .fill('30') -> value='{val}'")

            # Test alphabets
            duration_el.fill("abcdef")
            val_alpha = duration_el.input_value()
            print(f"  .fill('abcdef') -> value='{val_alpha}' (DOM accepts alphabets? {'YES' if val_alpha == 'abcdef' else 'NO'})")

            # Test negative
            duration_el.fill("-5")
            val_neg = duration_el.input_value()
            print(f"  .fill('-5') -> value='{val_neg}'")

            # Reset to valid
            duration_el.fill("25")
            results["lease_duration"] = {"fill_works": True, "accepts_alpha": val_alpha == "abcdef", "accepts_negative": val_neg == "-5"}
        else:
            print("  #lease_deed_duration_0: NOT VISIBLE")
            results["lease_duration"] = {"visible": False}

        # ====================================================================
        # DIAGNOSTIC 6: Renewal Clause — Toggle Behaviour
        # ====================================================================
        print("\n" + "=" * 70)
        print("DIAGNOSTIC 6: Renewal Clause Toggle — Dynamic Field")
        print("=" * 70)

        # Try clicking the Yes radio for renewal
        try:
            # First find which radio is the renewal one
            renewal_yes = page.locator("#renewal_yes")
            renewal_no = page.locator("#renewal_no")

            if renewal_yes.is_visible():
                print("  #renewal_yes is VISIBLE — clicking...")
                renewal_yes.click()
                page.wait_for_timeout(1500)

                # Check what appeared
                after_yes = page.evaluate("""
                    () => {
                        const inputs = document.querySelectorAll('input, select, textarea');
                        const visible = [];
                        inputs.forEach(el => {
                            if (el.offsetParent !== null && el.type !== 'hidden' &&
                                (el.id.includes('renewal') || el.id.includes('duration') ||
                                 el.name.includes('renewal') || el.name.includes('duration'))) {
                                visible.push({id: el.id, name: el.name, type: el.type, value: el.value, placeholder: el.placeholder || ''});
                            }
                        });
                        return visible;
                    }
                """)
                print(f"  After Renewal=Yes, duration-related fields visible:")
                for f in after_yes:
                    print(f"    id='{f['id']}' name='{f['name']}' type='{f['type']}' placeholder='{f['placeholder']}'")
                results["after_renewal_yes"] = after_yes

                # Now toggle to No
                print("\n  Clicking #renewal_no...")
                renewal_no.click()
                page.wait_for_timeout(1500)

                after_no = page.evaluate("""
                    () => {
                        const inputs = document.querySelectorAll('input, select, textarea');
                        const visible = [];
                        inputs.forEach(el => {
                            if (el.offsetParent !== null && el.type !== 'hidden' &&
                                (el.id.includes('renewal') || el.id.includes('duration') ||
                                 el.name.includes('renewal') || el.name.includes('duration'))) {
                                visible.push({id: el.id, name: el.name, type: el.type, value: el.value});
                            }
                        });
                        return visible;
                    }
                """)
                print(f"  After Renewal=No, duration-related fields visible:")
                for f in after_no:
                    print(f"    id='{f['id']}' name='{f['name']}' type='{f['type']}'")
                results["after_renewal_no"] = after_no
            else:
                print("  #renewal_yes NOT VISIBLE — trying get_by_role approach")
                # Try label-based approach
                yes_btn = page.get_by_role("radio", name="Yes")
                if yes_btn.count() > 0:
                    for i in range(yes_btn.count()):
                        if yes_btn.nth(i).is_visible():
                            print(f"  Found visible Yes radio at index {i}, clicking...")
                            yes_btn.nth(i).click()
                            page.wait_for_timeout(1500)
                            break
        except Exception as e:
            print(f"  ERROR during renewal toggle: {e}")
            results["renewal_toggle_error"] = str(e)

        # ====================================================================
        # DIAGNOSTIC 7: Fill ALL Leased fields + Click Next (Valid Flow)
        # ====================================================================
        print("\n" + "=" * 70)
        print("DIAGNOSTIC 7: Fill ALL Leased Fields + Submit")
        print("=" * 70)

        try:
            # Re-select Leased to reset form state
            page.get_by_role("radio", name="Single").click()
            page.wait_for_timeout(2000)
            page.get_by_role("radio", name="Leased").click()
            page.wait_for_timeout(2000)

            # Fill Area Unit
            area_unit = page.locator("#lease_area_unit_0")
            if area_unit.is_visible():
                area_unit.select_option(label="Square Meter")
                print("  Area Unit: Square Meter ✅")

            # Fill Land Area
            land_area = page.locator("#lease_land_area_0")
            if land_area.is_visible():
                land_area.click()
                land_area.fill("3000")
                print(f"  Land Area: '3000' -> '{land_area.input_value()}' ✅")

            # Fill Lessee Name
            lessee = page.locator("#leease_name_0")
            if lessee.is_visible():
                lessee.click()
                lessee.fill("ABC School Trust")
                print(f"  Lessee: '{lessee.input_value()}' ✅")

            # Fill Lessor Name
            lessor = page.locator("#leaser_name_0")
            if lessor.is_visible():
                lessor.click()
                lessor.fill("State Government")
                print(f"  Lessor: '{lessor.input_value()}' ✅")

            # Fill Lease Deed Date (JS injection)
            page.evaluate("""
                () => {
                    const el = document.querySelector('#lease_deed_date_0');
                    if (el) {
                        const setter = Object.getOwnPropertyDescriptor(
                            window.HTMLInputElement.prototype, 'value').set;
                        setter.call(el, '10/05/2015');
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        el.dispatchEvent(new Event('change', {bubbles: true}));
                        el.dispatchEvent(new Event('blur', {bubbles: true}));
                    }
                }
            """)
            page.wait_for_timeout(300)
            lease_date_val = page.locator("#lease_deed_date_0").input_value()
            print(f"  Lease Deed Date (JS): '{lease_date_val}' ✅")

            # Fill Duration
            duration = page.locator("#lease_deed_duration_0")
            if duration.is_visible():
                duration.click()
                duration.fill("30")
                print(f"  Duration: '{duration.input_value()}' ✅")

            # Fill Registration Date (JS injection)
            page.evaluate("""
                () => {
                    const el = document.querySelector('#date_regis_lease_deed0');
                    if (el) {
                        const setter = Object.getOwnPropertyDescriptor(
                            window.HTMLInputElement.prototype, 'value').set;
                        setter.call(el, '20/06/2015');
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        el.dispatchEvent(new Event('change', {bubbles: true}));
                        el.dispatchEvent(new Event('blur', {bubbles: true}));
                    }
                }
            """)
            page.wait_for_timeout(300)
            reg_date_val = page.locator("#date_regis_lease_deed0").input_value()
            print(f"  Registration Date (JS): '{reg_date_val}' ✅")

            # Fill Registration Office
            reg_office = page.locator("#regid_ofc_details0")
            if reg_office.is_visible():
                reg_office.click()
                reg_office.fill("Sub-Registrar, District Court")
                print(f"  Reg Office: '{reg_office.input_value()}' ✅")

            # Renewal = No
            renewal_no = page.locator("#renewal_no")
            if renewal_no.is_visible():
                renewal_no.click()
                page.wait_for_timeout(500)
                print("  Renewal: No ✅")

            # Click Next
            print("\n  Clicking Next...")
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(3000)

            # Check navigation
            lease_area_visible = page.locator("#lease_land_area_0").is_visible()
            print(f"  After Next: #lease_land_area_0 visible? {lease_area_visible}")
            if not lease_area_visible:
                print("  ✅ FORM NAVIGATED — Valid Leased submission accepted!")
                results["valid_leased_submit"] = {"navigated": True}
            else:
                # Check for errors
                errors = []
                for sel in [".invalid-feedback", ".text-danger"]:
                    els = page.locator(f"{sel}:visible").all()
                    for el in els:
                        txt = el.inner_text().strip()
                        if txt:
                            errors.append(txt)
                print(f"  ❌ FORM BLOCKED — Errors: {errors}")
                results["valid_leased_submit"] = {"navigated": False, "errors": errors}

        except Exception as e:
            print(f"  ERROR: {e}")
            results["valid_leased_submit_error"] = str(e)

        # ====================================================================
        # DIAGNOSTIC 8: Submit BLANK Leased form — Capture Validation Messages
        # ====================================================================
        print("\n" + "=" * 70)
        print("DIAGNOSTIC 8: Submit BLANK Leased Form — Validation Messages")
        print("=" * 70)

        try:
            # Navigate back
            page.get_by_text("Certificate of Land", exact=False).first.click()
            page.wait_for_timeout(3000)

            # Re-select Leased
            page.get_by_role("radio", name="Single").click()
            page.wait_for_timeout(2000)
            page.get_by_role("radio", name="Leased").click()
            page.wait_for_timeout(2000)

            # Clear all fields
            for fid in ["#lease_land_area_0", "#leease_name_0", "#leaser_name_0", "#lease_deed_duration_0", "#regid_ofc_details0"]:
                el = page.locator(fid)
                if el.is_visible():
                    el.click()
                    el.fill("")

            # Clear dates via JS
            page.evaluate("""
                () => {
                    ['#lease_deed_date_0', '#date_regis_lease_deed0'].forEach(sel => {
                        const el = document.querySelector(sel);
                        if (el) {
                            const setter = Object.getOwnPropertyDescriptor(
                                window.HTMLInputElement.prototype, 'value').set;
                            setter.call(el, '');
                            el.dispatchEvent(new Event('input', {bubbles: true}));
                            el.dispatchEvent(new Event('change', {bubbles: true}));
                        }
                    });
                }
            """)

            # Click Next
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(3000)

            # Capture errors
            errors = []
            for sel in [".invalid-feedback:visible", ".text-danger:visible", "[class*='invalid']:visible"]:
                try:
                    els = page.locator(sel).all()
                    for el in els:
                        if el.is_visible():
                            txt = el.inner_text().strip()
                            if txt and txt not in errors:
                                errors.append(txt)
                except:
                    pass

            print(f"  Validation messages captured ({len(errors)}):")
            for e in errors:
                print(f"    • {e}")
            results["blank_leased_errors"] = errors

            # Check if form navigated or blocked
            lease_visible = page.locator("#lease_land_area_0").is_visible()
            print(f"  Form blocked (still on page): {lease_visible}")
            results["blank_leased_blocked"] = lease_visible

        except Exception as e:
            print(f"  ERROR: {e}")
            results["blank_leased_error"] = str(e)

        # ====================================================================
        # SAVE EVIDENCE
        # ====================================================================
        os.makedirs("diagnostics/evidence", exist_ok=True)
        page.screenshot(path="diagnostics/evidence/land_leased_diagnostic.png", full_page=True)

        with open("diagnostics/evidence/land_leased_diagnostic_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)

        print("\n" + "=" * 70)
        print("DIAGNOSTIC COMPLETE")
        print("=" * 70)
        print(f"Screenshot: diagnostics/evidence/land_leased_diagnostic.png")
        print(f"JSON: diagnostics/evidence/land_leased_diagnostic_results.json")

        browser.close()


if __name__ == "__main__":
    run_diagnostic()
