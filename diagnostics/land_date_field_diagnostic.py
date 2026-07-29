"""
Certificate of Land — Date Field Diagnostic
=============================================
Evidence-based investigation of the "Date of Land Title Document" field.

Questions to answer:
1. Is the locator pointing to the correct textbox?
2. How many "Select a date" textboxes exist on the page?
3. Which one is actually the Land Title Date field?
4. Is the field visible and enabled?
5. Is another element covering the textbox?
6. Does the field become editable only after another field is selected?
7. Does the field require clicking elsewhere before typing?
8. Does .fill() fail?
9. Does .type() work?
10. Does .press_sequentially() work?
11. Does JavaScript value injection work?
12. Does the application accept the injected value after clicking Next?
13. Compare this behaviour with the existing E2E implementation.
"""

import sys
import os
import json
from datetime import datetime

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
        # NAVIGATE TO CERTIFICATE OF LAND
        # ====================================================================
        print("=" * 60)
        print("STEP 1: Login and navigate to Certificate of Land")
        print("=" * 60)

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

        # Click Certificate of Land tab
        page.get_by_text("Certificate of Land", exact=False).first.click()
        page.wait_for_timeout(3000)

        # Ensure Single + Owned is selected
        page.get_by_role("radio", name="Single").click()
        page.wait_for_timeout(2000)
        page.get_by_role("radio", name="Owned").click()
        page.wait_for_timeout(1000)
        page.locator("#land_area_0").wait_for(state="visible", timeout=5000)

        print("Successfully navigated to Certificate of Land (Single -> Owned)")
        print()

        # ====================================================================
        # DIAGNOSTIC 1: How many "Select a date" textboxes exist?
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 1: Count of 'Select a date' textboxes")
        print("=" * 60)

        date_textboxes = page.get_by_role("textbox", name="Select a date")
        count = date_textboxes.count()
        print(f"Total 'Select a date' textboxes found: {count}")
        results["total_select_a_date_textboxes"] = count

        # Get details of each one
        for i in range(count):
            el = date_textboxes.nth(i)
            try:
                el_id = el.get_attribute("id")
                el_name = el.get_attribute("name")
                el_placeholder = el.get_attribute("placeholder")
                el_type = el.get_attribute("type")
                el_readonly = el.get_attribute("readonly")
                el_visible = el.is_visible()
                el_enabled = el.is_enabled()
                el_value = el.input_value()
                print(f"  [{i}] id='{el_id}' name='{el_name}' type='{el_type}' "
                      f"placeholder='{el_placeholder}' readonly={el_readonly} "
                      f"visible={el_visible} enabled={el_enabled} value='{el_value}'")
                results[f"textbox_{i}"] = {
                    "id": el_id, "name": el_name, "type": el_type,
                    "placeholder": el_placeholder, "readonly": el_readonly,
                    "visible": el_visible, "enabled": el_enabled, "value": el_value
                }
            except Exception as e:
                print(f"  [{i}] ERROR reading attributes: {e}")
                results[f"textbox_{i}"] = {"error": str(e)}

        print()

        # ====================================================================
        # DIAGNOSTIC 2: Is #land_title_date0 the correct element?
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 2: Direct #land_title_date0 locator check")
        print("=" * 60)

        try:
            direct_el = page.locator("#land_title_date0")
            direct_count = direct_el.count()
            print(f"#land_title_date0 count: {direct_count}")
            if direct_count > 0:
                d_visible = direct_el.is_visible()
                d_enabled = direct_el.is_enabled()
                d_readonly = direct_el.get_attribute("readonly")
                d_type = direct_el.get_attribute("type")
                d_class = direct_el.get_attribute("class")
                d_placeholder = direct_el.get_attribute("placeholder")
                d_value = direct_el.input_value()
                print(f"  visible={d_visible} enabled={d_enabled} readonly='{d_readonly}'")
                print(f"  type='{d_type}' class='{d_class}'")
                print(f"  placeholder='{d_placeholder}' current_value='{d_value}'")
                results["land_title_date0"] = {
                    "count": direct_count, "visible": d_visible, "enabled": d_enabled,
                    "readonly": d_readonly, "type": d_type, "class": d_class,
                    "placeholder": d_placeholder, "value": d_value
                }
            else:
                print("  NOT FOUND on page!")
                results["land_title_date0"] = {"count": 0, "error": "Not found"}
        except Exception as e:
            print(f"  ERROR: {e}")
            results["land_title_date0"] = {"error": str(e)}

        print()

        # ====================================================================
        # DIAGNOSTIC 3: Which textbox is .last pointing to?
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 3: Which textbox does .last resolve to?")
        print("=" * 60)

        try:
            last_el = page.get_by_role("textbox", name="Select a date").last
            last_id = last_el.get_attribute("id")
            last_name = last_el.get_attribute("name")
            last_visible = last_el.is_visible()
            last_enabled = last_el.is_enabled()
            last_readonly = last_el.get_attribute("readonly")
            print(f"  .last resolves to: id='{last_id}' name='{last_name}'")
            print(f"  visible={last_visible} enabled={last_enabled} readonly='{last_readonly}'")
            results["last_textbox"] = {
                "id": last_id, "name": last_name,
                "visible": last_visible, "enabled": last_enabled, "readonly": last_readonly
            }
        except Exception as e:
            print(f"  ERROR: {e}")
            results["last_textbox"] = {"error": str(e)}

        print()

        # ====================================================================
        # DIAGNOSTIC 4: Is another element covering the field?
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 4: Bounding box and overlap check")
        print("=" * 60)

        try:
            target = page.locator("#land_title_date0") if page.locator("#land_title_date0").count() > 0 else last_el
            bbox = target.bounding_box()
            if bbox:
                print(f"  Bounding box: x={bbox['x']}, y={bbox['y']}, w={bbox['width']}, h={bbox['height']}")
                # Check what element is at the center of the bounding box
                center_x = bbox['x'] + bbox['width'] / 2
                center_y = bbox['y'] + bbox['height'] / 2
                element_at_point = page.evaluate(f"""
                    () => {{
                        const el = document.elementFromPoint({center_x}, {center_y});
                        if (el) {{
                            return {{
                                tagName: el.tagName,
                                id: el.id,
                                className: el.className,
                                type: el.type || ''
                            }};
                        }}
                        return null;
                    }}
                """)
                print(f"  Element at center point ({center_x}, {center_y}): {element_at_point}")
                results["bounding_box"] = bbox
                results["element_at_center"] = element_at_point
            else:
                print("  No bounding box (element may be hidden)")
                results["bounding_box"] = None
        except Exception as e:
            print(f"  ERROR: {e}")
            results["bounding_box_error"] = str(e)

        print()

        # ====================================================================
        # DIAGNOSTIC 5: Check if field has datepicker overlay/widget
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 5: Datepicker/overlay detection")
        print("=" * 60)

        try:
            datepicker_info = page.evaluate("""
                () => {
                    const el = document.querySelector('#land_title_date0') || 
                               document.querySelector('[placeholder="Select a date"]');
                    if (!el) return {error: 'Element not found'};
                    
                    const parent = el.parentElement;
                    const siblings = parent ? Array.from(parent.children).map(c => ({
                        tag: c.tagName,
                        class: c.className,
                        id: c.id
                    })) : [];
                    
                    // Check for datepicker classes
                    const hasDatepicker = el.classList.contains('datepicker') || 
                                         el.classList.contains('flatpickr-input') ||
                                         el.classList.contains('datetimepicker-input') ||
                                         el.hasAttribute('data-toggle');
                    
                    const dataAttrs = {};
                    for (const attr of el.attributes) {
                        if (attr.name.startsWith('data-')) {
                            dataAttrs[attr.name] = attr.value;
                        }
                    }
                    
                    return {
                        elementTag: el.tagName,
                        elementId: el.id,
                        elementClass: el.className,
                        readonly: el.readOnly,
                        disabled: el.disabled,
                        hasDatepicker: hasDatepicker,
                        dataAttributes: dataAttrs,
                        parentTag: parent ? parent.tagName : null,
                        parentClass: parent ? parent.className : null,
                        siblings: siblings
                    };
                }
            """)
            print(f"  Element info: {json.dumps(datepicker_info, indent=4)}")
            results["datepicker_info"] = datepicker_info
        except Exception as e:
            print(f"  ERROR: {e}")
            results["datepicker_info_error"] = str(e)

        print()

        # ====================================================================
        # DIAGNOSTIC 6: Does field become editable after selecting another field?
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 6: Field editability after other field interaction")
        print("=" * 60)

        try:
            # First check current readonly state
            readonly_before = page.evaluate("""
                () => {
                    const el = document.querySelector('#land_title_date0');
                    if (!el) return 'NOT FOUND';
                    return {readonly: el.readOnly, disabled: el.disabled, value: el.value};
                }
            """)
            print(f"  Before interaction: {readonly_before}")

            # Fill another field (registration details) then check again
            page.locator("#land_title0").click()
            page.locator("#land_title0").fill("TEST-REG-001")
            page.wait_for_timeout(500)

            readonly_after = page.evaluate("""
                () => {
                    const el = document.querySelector('#land_title_date0');
                    if (!el) return 'NOT FOUND';
                    return {readonly: el.readOnly, disabled: el.disabled, value: el.value};
                }
            """)
            print(f"  After filling another field: {readonly_after}")
            results["editability_check"] = {"before": readonly_before, "after": readonly_after}
        except Exception as e:
            print(f"  ERROR: {e}")
            results["editability_check_error"] = str(e)

        print()

        # ====================================================================
        # DIAGNOSTIC 7: Test .fill() approach
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 7: .fill() test")
        print("=" * 60)

        try:
            # Test with #land_title_date0
            target = page.locator("#land_title_date0")
            if target.count() > 0 and target.is_visible():
                target.click()
                page.wait_for_timeout(500)
                target.fill("15/03/2020")
                page.wait_for_timeout(500)
                val_after_fill = target.input_value()
                print(f"  #land_title_date0 .fill('15/03/2020') -> value='{val_after_fill}'")
                results["fill_by_id"] = {"success": True, "value": val_after_fill}
            else:
                print(f"  #land_title_date0 not visible/found, trying .last approach")
                last_el = page.get_by_role("textbox", name="Select a date").last
                last_el.click()
                page.wait_for_timeout(500)
                last_el.fill("15/03/2020")
                page.wait_for_timeout(500)
                val_after_fill = last_el.input_value()
                print(f"  .last.fill('15/03/2020') -> value='{val_after_fill}'")
                results["fill_by_role_last"] = {"success": True, "value": val_after_fill}
        except Exception as e:
            print(f"  .fill() FAILED: {e}")
            results["fill_test"] = {"success": False, "error": str(e)}

        print()

        # ====================================================================
        # DIAGNOSTIC 8: Clear and test .type() approach
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 8: .type() test")
        print("=" * 60)

        try:
            # Clear first
            target = page.locator("#land_title_date0")
            if target.count() > 0:
                page.evaluate("document.querySelector('#land_title_date0').value = ''")
                page.wait_for_timeout(300)

                target.click()
                page.wait_for_timeout(500)
                target.type("20/06/2019")
                page.wait_for_timeout(500)
                val_after_type = target.input_value()
                print(f"  .type('20/06/2019') -> value='{val_after_type}'")
                results["type_test"] = {"success": True, "value": val_after_type}
            else:
                print("  #land_title_date0 not found for .type() test")
                results["type_test"] = {"success": False, "error": "Element not found"}
        except Exception as e:
            print(f"  .type() FAILED: {e}")
            results["type_test"] = {"success": False, "error": str(e)}

        print()

        # ====================================================================
        # DIAGNOSTIC 9: .press_sequentially() test
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 9: .press_sequentially() test")
        print("=" * 60)

        try:
            target = page.locator("#land_title_date0")
            if target.count() > 0:
                # Clear
                page.evaluate("document.querySelector('#land_title_date0').value = ''")
                page.wait_for_timeout(300)

                target.click()
                page.wait_for_timeout(500)
                # Triple-click to select all, then type
                target.press("Control+a")
                page.wait_for_timeout(200)
                target.press_sequentially("10012018", delay=100)
                page.wait_for_timeout(500)
                val_after_seq = target.input_value()
                print(f"  .press_sequentially('10012018') -> value='{val_after_seq}'")
                results["press_sequentially_test"] = {"success": True, "value": val_after_seq}
            else:
                print("  Element not found")
                results["press_sequentially_test"] = {"success": False, "error": "Not found"}
        except Exception as e:
            print(f"  .press_sequentially() FAILED: {e}")
            results["press_sequentially_test"] = {"success": False, "error": str(e)}

        print()

        # ====================================================================
        # DIAGNOSTIC 10: JavaScript injection test
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 10: JavaScript value injection test")
        print("=" * 60)

        try:
            js_result = page.evaluate("""
                () => {
                    const el = document.querySelector('#land_title_date0');
                    if (!el) return {error: 'Element not found'};
                    
                    // Method 1: Direct value set
                    el.value = '15/03/2020';
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    el.dispatchEvent(new Event('blur', {bubbles: true}));
                    
                    return {value: el.value, success: true};
                }
            """)
            print(f"  Direct JS injection: {js_result}")
            results["js_direct_injection"] = js_result

            # Method 2: nativeInputValueSetter
            js_result2 = page.evaluate("""
                () => {
                    const el = document.querySelector('#land_title_date0');
                    if (!el) return {error: 'Element not found'};
                    
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value').set;
                    nativeInputValueSetter.call(el, '15/03/2020');
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    el.dispatchEvent(new Event('blur', {bubbles: true}));
                    
                    return {value: el.value, success: true};
                }
            """)
            print(f"  nativeInputValueSetter: {js_result2}")
            results["js_native_setter"] = js_result2

        except Exception as e:
            print(f"  JS injection FAILED: {e}")
            results["js_injection_error"] = str(e)

        print()

        # ====================================================================
        # DIAGNOSTIC 11: Does app accept the injected value on Next?
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 11: Fill ALL fields + JS date, then click Next")
        print("=" * 60)

        try:
            # First fill all other mandatory fields
            page.locator("#land_unit_0").select_option(label="Square Meter")
            page.locator("#land_area_0").click()
            page.locator("#land_area_0").fill("5000")
            page.locator("#situate_speci_0").click()
            page.locator("#situate_speci_0").fill("Survey No(s)")
            page.locator("#situated_at0").click()
            page.locator("#situated_at0").fill("Civil Lines, Jaipur")
            page.locator("#owned_by_0").click()
            page.locator("#owned_by_0").fill("Test Trust")
            page.locator("#land_title_doc0").select_option(label="Conveyance Deed")
            page.locator("#land_title0").click()
            page.locator("#land_title0").fill("REG-DIAG-001")
            page.locator("#executed_by0").click()
            page.locator("#executed_by0").fill("Mr. Diagnostic")
            page.locator("#regid_ofc_details0").click()
            page.locator("#regid_ofc_details0").fill("Sub-Registrar Office")

            # Set date via JS
            page.evaluate("""
                () => {
                    const el = document.querySelector('#land_title_date0');
                    if (el) {
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                            window.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(el, '15/03/2020');
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        el.dispatchEvent(new Event('change', {bubbles: true}));
                        el.dispatchEvent(new Event('blur', {bubbles: true}));
                    }
                }
            """)
            page.wait_for_timeout(500)

            # Verify value before click
            val_before_next = page.locator("#land_title_date0").input_value()
            print(f"  Date value before clicking Next: '{val_before_next}'")

            # Click Next
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(3000)

            # Check if navigated
            land_area_visible = page.locator("#land_area_0").is_visible()
            print(f"  After Next: #land_area_0 still visible? {land_area_visible}")

            if land_area_visible:
                # Check for errors
                errors = []
                for selector in [".invalid-feedback:visible", ".text-danger:visible"]:
                    try:
                        els = page.locator(selector).all()
                        for el in els:
                            if el.is_visible():
                                text = el.inner_text().strip()
                                if text:
                                    errors.append(text)
                    except:
                        pass
                print(f"  Form BLOCKED. Errors: {errors}")
                results["next_with_js_date"] = {"navigated": False, "errors": errors}
            else:
                print(f"  Form NAVIGATED (accepted JS date)")
                results["next_with_js_date"] = {"navigated": True}

        except Exception as e:
            print(f"  ERROR: {e}")
            results["next_with_js_date_error"] = str(e)

        print()

        # ====================================================================
        # DIAGNOSTIC 12: E2E comparison - use EXACT E2E approach
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 12: E2E exact approach comparison")
        print("=" * 60)

        try:
            # Navigate back to Certificate of Land
            page.get_by_text("Certificate of Land", exact=False).first.click()
            page.wait_for_timeout(3000)

            # E2E uses: get_by_role("textbox", name="Select a date").last.click() then .fill()
            e2e_target = page.get_by_role("textbox", name="Select a date").last
            e2e_id = e2e_target.get_attribute("id")
            e2e_visible = e2e_target.is_visible()
            e2e_readonly = e2e_target.get_attribute("readonly")
            print(f"  E2E .last target: id='{e2e_id}' visible={e2e_visible} readonly='{e2e_readonly}'")

            # Clear and try E2E approach exactly
            page.evaluate(f"""
                () => {{
                    const el = document.querySelector('#{e2e_id}');
                    if (el) el.value = '';
                }}
            """)
            page.wait_for_timeout(300)

            e2e_target.click()
            page.wait_for_timeout(1000)

            # Check if a datepicker/calendar opened
            calendar_visible = page.evaluate("""
                () => {
                    // Check for common datepicker overlays
                    const flatpickr = document.querySelector('.flatpickr-calendar.open');
                    const bootstrap_dp = document.querySelector('.datepicker.datepicker-dropdown');
                    const jquery_dp = document.querySelector('#ui-datepicker-div:not([style*="display: none"])');
                    const any_picker = document.querySelector('.picker--opened, .daterangepicker');
                    
                    return {
                        flatpickr: !!flatpickr,
                        bootstrap: !!bootstrap_dp,
                        jquery: !!jquery_dp,
                        other: !!any_picker,
                        body_classes: document.body.className
                    };
                }
            """)
            print(f"  After click - calendar/picker visible? {calendar_visible}")
            results["calendar_check_after_click"] = calendar_visible

            # Now try .fill()
            e2e_target.fill("15/03/2020")
            page.wait_for_timeout(500)
            e2e_val = e2e_target.input_value()
            print(f"  After E2E .fill('15/03/2020'): value='{e2e_val}'")
            results["e2e_fill_result"] = e2e_val

            # Check if calendar closed after fill
            calendar_after_fill = page.evaluate("""
                () => {
                    const flatpickr = document.querySelector('.flatpickr-calendar.open');
                    const bootstrap_dp = document.querySelector('.datepicker.datepicker-dropdown');
                    return {flatpickr: !!flatpickr, bootstrap: !!bootstrap_dp};
                }
            """)
            print(f"  Calendar still open after .fill()? {calendar_after_fill}")

        except Exception as e:
            print(f"  ERROR: {e}")
            results["e2e_comparison_error"] = str(e)

        print()

        # ====================================================================
        # DIAGNOSTIC 13: Check all date-related inputs on page with full DOM info
        # ====================================================================
        print("=" * 60)
        print("DIAGNOSTIC 13: Full DOM scan for date-like inputs")
        print("=" * 60)

        try:
            all_date_inputs = page.evaluate("""
                () => {
                    const inputs = document.querySelectorAll('input[type="text"], input[type="date"], input:not([type])');
                    const dateInputs = [];
                    inputs.forEach((el, i) => {
                        const placeholder = el.getAttribute('placeholder') || '';
                        const id = el.id || '';
                        const name = el.name || '';
                        if (placeholder.toLowerCase().includes('date') || 
                            id.toLowerCase().includes('date') ||
                            name.toLowerCase().includes('date') ||
                            placeholder.toLowerCase().includes('select a date')) {
                            dateInputs.push({
                                index: i,
                                id: el.id,
                                name: el.name,
                                type: el.type,
                                placeholder: placeholder,
                                readonly: el.readOnly,
                                disabled: el.disabled,
                                value: el.value,
                                visible: el.offsetParent !== null,
                                className: el.className,
                                parentClass: el.parentElement ? el.parentElement.className : ''
                            });
                        }
                    });
                    return dateInputs;
                }
            """)
            print(f"  Date-like inputs found: {len(all_date_inputs)}")
            for inp in all_date_inputs:
                print(f"    {json.dumps(inp)}")
            results["all_date_inputs"] = all_date_inputs
        except Exception as e:
            print(f"  ERROR: {e}")
            results["all_date_inputs_error"] = str(e)

        print()

        # ====================================================================
        # FINAL: Take screenshot for evidence
        # ====================================================================
        os.makedirs("diagnostics/evidence", exist_ok=True)
        page.screenshot(path="diagnostics/evidence/land_date_field_state.png", full_page=True)
        print("Screenshot saved: diagnostics/evidence/land_date_field_state.png")

        # Save results
        with open("diagnostics/evidence/land_date_diagnostic_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print("Results saved: diagnostics/evidence/land_date_diagnostic_results.json")

        browser.close()

    # ====================================================================
    # GENERATE REPORT
    # ====================================================================
    print()
    print("=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)
    print()
    print("Key findings:")
    print(f"  Total 'Select a date' textboxes: {results.get('total_select_a_date_textboxes', 'unknown')}")
    print(f"  .last resolves to: {results.get('last_textbox', {}).get('id', 'unknown')}")
    print(f"  #land_title_date0 readonly: {results.get('land_title_date0', {}).get('readonly', 'unknown')}")
    print(f"  .fill() result: {results.get('fill_by_id', results.get('fill_by_role_last', 'unknown'))}")
    print(f"  .type() result: {results.get('type_test', 'unknown')}")
    print(f"  .press_sequentially(): {results.get('press_sequentially_test', 'unknown')}")
    print(f"  JS injection: {results.get('js_native_setter', 'unknown')}")
    print(f"  Next with JS date: {results.get('next_with_js_date', 'unknown')}")


if __name__ == "__main__":
    run_diagnostic()
