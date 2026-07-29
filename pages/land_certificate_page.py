class LandCertificatePage:

    def __init__(self, page):
        self.page = page

    def fill_land_details(self, data):

        # Plot Type
        self.page.get_by_role(
            "radio",
            name=data["plot_type"]
        ).click()

        # Wait for dynamic form to load
        self.page.wait_for_timeout(2000)

        # Type Of Land (Owned / Leased)
        self.page.get_by_role(
            "radio",
            name=data["Type_of_Land"]
        ).click()

        # Wait after selecting ownership type
        self.page.wait_for_timeout(1000)

        # Land Area field wait
        self.page.locator(
            "#land_area_0"
        ).wait_for(
            state="visible",
            timeout=1000
        )

        # Area Unit Dropdown - Try multiple selection approaches
        self.page.locator("#land_unit_0").wait_for(state="visible")
        self.page.wait_for_timeout(1000)

        # Force select "Square Meter" (value="3") directly
        self.page.locator("#land_unit_0").select_option("Square Meter")

        # Land Area
        self.page.locator(
            'input[id^="land_area"]'
        ).nth(0).click()

        self.page.locator(
            'input[id^="land_area"]'
        ).nth(0).fill(
            str(data["land_area"])
        )

        # Situated In
        self.page.locator(
            'input[id^="situate_speci"]'
        ).nth(0).click()

        self.page.locator(
            'input[id^="situate_speci"]'
        ).nth(0).fill(
            data["situated_in"]
        )

        # Situated At
        self.page.locator(
            'input[id^="situated_at"]'
        ).nth(0).click()

        self.page.locator(
            'input[id^="situated_at"]'
        ).nth(0).fill(
            data["situated_at"]
        )

        # Land Owned By
        self.page.locator(
            'input[id^="owned_by"]'
        ).nth(0).click()

        self.page.locator(
            'input[id^="owned_by"]'
        ).nth(0).fill(
            data["land_owned_by"]
        )

        # =================================================
        # Land Title Document
        # =================================================

        self.page.locator(
            "select[id^='land_title_doc']"
        ).first.select_option(
            label=data["land_title_document"]
        )

        # =================================================
        # Sale Deed Condition
        # =================================================

        if data["land_title_document"] == "Sale Deed":

            self.page.locator(
                "select[id^='sale_deed_favor_whom']"
            ).first.wait_for(
                state="visible"
            )

            self.page.locator(
                "select[id^='sale_deed_favor_whom']"
            ).first.select_option(
                label=data["sale_deed_favor"]
            )

        # Registration Details
        self.page.locator(
            'input[id^="land_title"]'
        ).nth(0).click()

        self.page.locator(
            'input[id^="land_title"]'
        ).nth(0).fill(
            data["registration_details"]
        )

        # Seller Name
        self.page.locator(
            'input[id^="executed_by"]'
        ).nth(0).click()

        self.page.locator(
            'input[id^="executed_by"]'
        ).nth(0).fill(
            data["seller_name"]
        )

        # Registration Office Details
        self.page.locator(
            'input[id^="regid_ofc_details"]'
        ).nth(0).click()

        self.page.locator(
            'input[id^="regid_ofc_details"]'
        ).nth(0).fill(
            data["registration_office_details"]
        )

        # Land Document Date
        self.page.get_by_role(
            "textbox",
            name="Select a date"
        ).last.click()

        self.page.get_by_role(
            "textbox",
            name="Select a date"
        ).last.fill(
            data["land_document_date"]
        )

        # Next
        self.page.get_by_role(
            "button",
            name="Next"
        ).click()

    # ===========================================================================
    # REGRESSION TEST METHODS (Additive — Phase 1: Single → Owned)
    # ===========================================================================

    def click_next(self):
        """Click the Next button without filling any fields."""
        self.page.get_by_role("button", name="Next").click()

    def select_plot_type(self, type_name):
        """
        Select plot type radio button (Single/Multiple).
        Waits 2000ms after selection for dynamic form loading.
        """
        self.page.get_by_role("radio", name=type_name).click()
        self.page.wait_for_timeout(2000)

    def select_land_type(self, type_name):
        """
        Select land ownership type radio button (Owned/Leased).
        Waits 1000ms after selection for form sections to load.
        """
        self.page.get_by_role("radio", name=type_name).click()
        self.page.wait_for_timeout(1000)

    def fill_land_area(self, value):
        """Fill or clear the land area field (#land_area_0)."""
        self.page.locator("#land_area_0").click()
        self.page.locator("#land_area_0").fill(str(value) if value is not None else "")

    def fill_document_date(self, date_value):
        """
        Fill the land document date via JavaScript injection.
        Field is readonly (datepicker) — uses ValidationHelper.set_readonly_date().
        Same approach as NOC and Trust date fields.
        """
        from utils.validation_helper import ValidationHelper
        ValidationHelper.set_readonly_date(self.page, '#land_title_date0', date_value)

    def fill_partial_owned_details(self, data, skip_fields=None):
        """
        Fill all Single→Owned path fields, skipping specified fields.
        Then clicks Next to submit.

        Args:
            data: dict with keys matching field names
            skip_fields: list of field keys to leave blank/skip

        Keys in data:
            area_unit, land_area, situated_in, situated_at,
            land_owned_by, land_title_document, sale_deed_favor,
            registration_details, executed_by, registration_office,
            document_date
        """
        if skip_fields is None:
            skip_fields = []

        # Step 1: Select Single plot type + wait for dynamic form
        self.select_plot_type("Single")

        # Step 2: Select Owned land type + wait
        self.select_land_type("Owned")

        # Wait for land_area field to be visible
        self.page.locator("#land_area_0").wait_for(state="visible", timeout=5000)

        # Step 3: Area Unit dropdown
        if "area_unit" not in skip_fields and data.get("area_unit"):
            self.page.locator("#land_unit_0").select_option(label=data["area_unit"])

        # Step 4: Land Area
        if "land_area" not in skip_fields:
            value = data.get("land_area", "")
            self.page.locator("#land_area_0").click()
            self.page.locator("#land_area_0").fill(str(value) if value is not None else "")
        else:
            # Clear field if skipping (for blank validation)
            self.page.locator("#land_area_0").click()
            self.page.locator("#land_area_0").fill("")

        # Step 5: Situated In (specify text field)
        if "situated_in" not in skip_fields:
            value = data.get("situated_in", "")
            self.page.locator("#situate_speci_0").click()
            self.page.locator("#situate_speci_0").fill(str(value) if value else "")
        else:
            self.page.locator("#situate_speci_0").click()
            self.page.locator("#situate_speci_0").fill("")

        # Step 6: Situated At
        if "situated_at" not in skip_fields:
            value = data.get("situated_at", "")
            self.page.locator("#situated_at0").click()
            self.page.locator("#situated_at0").fill(str(value) if value else "")
        else:
            self.page.locator("#situated_at0").click()
            self.page.locator("#situated_at0").fill("")

        # Step 7: Land Owned By
        if "land_owned_by" not in skip_fields:
            value = data.get("land_owned_by", "")
            self.page.locator("#owned_by_0").click()
            self.page.locator("#owned_by_0").fill(str(value) if value else "")
        else:
            self.page.locator("#owned_by_0").click()
            self.page.locator("#owned_by_0").fill("")

        # Step 8: Land Title Document dropdown
        if "land_title_document" not in skip_fields and data.get("land_title_document"):
            self.page.locator("#land_title_doc0").select_option(label=data["land_title_document"])

        # Step 9: Sale Deed conditional — only when Sale Deed selected
        if data.get("land_title_document") == "Sale Deed" and "sale_deed_favor" not in skip_fields:
            self.page.locator("#sale_deed_favor_whom_0").wait_for(state="visible", timeout=3000)
            if data.get("sale_deed_favor"):
                self.page.locator("#sale_deed_favor_whom_0").select_option(label=data["sale_deed_favor"])

        # Step 10: Registration Details
        if "registration_details" not in skip_fields:
            value = data.get("registration_details", "")
            self.page.locator("#land_title0").click()
            self.page.locator("#land_title0").fill(str(value) if value else "")
        else:
            self.page.locator("#land_title0").click()
            self.page.locator("#land_title0").fill("")

        # Step 11: Executed By
        if "executed_by" not in skip_fields:
            value = data.get("executed_by", "")
            self.page.locator("#executed_by0").click()
            self.page.locator("#executed_by0").fill(str(value) if value else "")
        else:
            self.page.locator("#executed_by0").click()
            self.page.locator("#executed_by0").fill("")

        # Step 12: Registration Office
        if "registration_office" not in skip_fields:
            value = data.get("registration_office", "")
            self.page.locator("#regid_ofc_details0").click()
            self.page.locator("#regid_ofc_details0").fill(str(value) if value else "")
        else:
            self.page.locator("#regid_ofc_details0").click()
            self.page.locator("#regid_ofc_details0").fill("")

        # Step 13: Document Date — readonly field, uses JS injection (same as NOC/Trust)
        from utils.validation_helper import ValidationHelper
        if "document_date" not in skip_fields:
            value = data.get("document_date", "")
            ValidationHelper.set_readonly_date(self.page, '#land_title_date0', str(value) if value else "")
        else:
            ValidationHelper.set_readonly_date(self.page, '#land_title_date0', "")

        # Step 14: Click Next
        self.click_next()

    # ===========================================================================
    # REGRESSION TEST METHODS — Phase 1 Extension: Leased + Multiple Paths
    # ===========================================================================

    def select_renewal_clause(self, option):
        """
        Select Renewal Clause radio button (Yes/No) on the Leased path.
        Waits 1000ms after selection for conditional Duration field to load.

        Args:
            option: "Yes" or "No"

        Locators (confirmed by diagnostic):
            Yes: #renewal_yes0 (name='renewal_clause[0]')
            No:  #Renewal_no0 (name='renewal_clause[0]')
        """
        if option == "Yes":
            self.page.locator("#renewal_yes0").click()
        else:
            self.page.locator("#Renewal_no0").click()
        self.page.wait_for_timeout(1000)

    def fill_partial_leased_details(self, data, skip_fields=None):
        """
        Fill all Single→Leased path fields, skipping specified fields.
        Then clicks Next to submit.

        Args:
            data: dict with keys matching field names
            skip_fields: list of field keys to leave blank/skip

        Keys in data:
            area_unit, land_area, lessee_name, lessor_name,
            lease_deed_date, lease_deed_duration,
            registration_date, registration_office,
            renewal_clause, renewal_duration
        """
        from utils.validation_helper import ValidationHelper

        if skip_fields is None:
            skip_fields = []

        # Step 1: Select Single plot type + wait for dynamic form
        self.select_plot_type("Single")

        # Step 2: Select Leased land type + wait
        self.select_land_type("Leased")

        # Wait for lease land area field to be visible
        self.page.locator("#lease_land_area_0").wait_for(state="visible", timeout=5000)

        # Step 3: Lease Area Unit dropdown
        if "area_unit" not in skip_fields and data.get("area_unit"):
            self.page.locator("#lease_area_unit_0").select_option(label=data["area_unit"])

        # Step 4: Lease Land Area
        if "land_area" not in skip_fields:
            value = data.get("land_area", "")
            self.page.locator("#lease_land_area_0").click()
            self.page.locator("#lease_land_area_0").fill(str(value) if value is not None else "")
        else:
            self.page.locator("#lease_land_area_0").click()
            self.page.locator("#lease_land_area_0").fill("")

        # Step 5: Name of Lessee
        if "lessee_name" not in skip_fields:
            value = data.get("lessee_name", "")
            self.page.locator("#leease_name_0").click()
            self.page.locator("#leease_name_0").fill(str(value) if value else "")
        else:
            self.page.locator("#leease_name_0").click()
            self.page.locator("#leease_name_0").fill("")

        # Step 6: Name of Lessor
        if "lessor_name" not in skip_fields:
            value = data.get("lessor_name", "")
            self.page.locator("#leaser_name_0").click()
            self.page.locator("#leaser_name_0").fill(str(value) if value else "")
        else:
            self.page.locator("#leaser_name_0").click()
            self.page.locator("#leaser_name_0").fill("")

        # Step 7: Date of Lease Deed (likely readonly — use JS injection)
        if "lease_deed_date" not in skip_fields:
            value = data.get("lease_deed_date", "")
            ValidationHelper.set_readonly_date(
                self.page, '#lease_deed_date_0', str(value) if value else ""
            )
        else:
            ValidationHelper.set_readonly_date(self.page, '#lease_deed_date_0', "")

        # Step 8: Duration of Lease Deed
        if "lease_deed_duration" not in skip_fields:
            value = data.get("lease_deed_duration", "")
            self.page.locator("#lease_deed_duration_0").click()
            self.page.locator("#lease_deed_duration_0").fill(str(value) if value else "")
        else:
            self.page.locator("#lease_deed_duration_0").click()
            self.page.locator("#lease_deed_duration_0").fill("")

        # Step 9: Date of Registration of Lease Deed (likely readonly)
        if "registration_date" not in skip_fields:
            value = data.get("registration_date", "")
            ValidationHelper.set_readonly_date(
                self.page, '#date_regis_lease_deed0', str(value) if value else ""
            )
        else:
            ValidationHelper.set_readonly_date(self.page, '#date_regis_lease_deed0', "")

        # Step 10: Registration Office Details
        if "registration_office" not in skip_fields:
            value = data.get("registration_office", "")
            self.page.locator("#details_regis_ofc0").click()
            self.page.locator("#details_regis_ofc0").fill(str(value) if value else "")
        else:
            self.page.locator("#details_regis_ofc0").click()
            self.page.locator("#details_regis_ofc0").fill("")

        # Step 11: Renewal Clause (Yes/No radio)
        if "renewal_clause" not in skip_fields and data.get("renewal_clause"):
            self.select_renewal_clause(data["renewal_clause"])

            # Step 12: Duration of Renewal (conditional — only if Renewal=Yes)
            if data["renewal_clause"] == "Yes" and "renewal_duration" not in skip_fields:
                value = data.get("renewal_duration", "")
                # Wait for the renewal duration field to appear
                self.page.locator("#renewal_lease_deed_duration_0").wait_for(
                    state="visible", timeout=3000
                )
                self.page.locator("#renewal_lease_deed_duration_0").click()
                self.page.locator("#renewal_lease_deed_duration_0").fill(
                    str(value) if value else ""
                )

        # Step 13: Re-inject dates (radio clicks may reset JS-injected values)
        # This must be the LAST action before clicking Next
        # Uses enhanced injection that also triggers Bootstrap datepicker update
        if "lease_deed_date" not in skip_fields and data.get("lease_deed_date"):
            self.page.evaluate(f"""
                (dateVal) => {{
                    const input = document.querySelector('#lease_deed_date_0');
                    if (input) {{
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                            window.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(input, dateVal);
                        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        input.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                        // Trigger Bootstrap datepicker update if available
                        if (typeof $ !== 'undefined' && $(input).datepicker) {{
                            $(input).datepicker('update', dateVal);
                        }}
                    }}
                }}
            """, str(data["lease_deed_date"]))
            self.page.wait_for_timeout(500)

        if "registration_date" not in skip_fields and data.get("registration_date"):
            self.page.evaluate(f"""
                (dateVal) => {{
                    const input = document.querySelector('#date_regis_lease_deed0');
                    if (input) {{
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                            window.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(input, dateVal);
                        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        input.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                        if (typeof $ !== 'undefined' && $(input).datepicker) {{
                            $(input).datepicker('update', dateVal);
                        }}
                    }}
                }}
            """, str(data["registration_date"]))
            self.page.wait_for_timeout(500)

        self.page.wait_for_timeout(1000)

        # Step 14: Click Next
        self.click_next()

    def fill_multiple_plot_details(self, data, skip_fields=None):
        """
        Fill Multiple Plot path fields, skipping specified fields.
        Handles the nested conditional chain:
          Contiguous? → (No) → Single Boundary? → (No) → Explanation
        Then clicks Next to submit.

        Args:
            data: dict with keys matching field names
            skip_fields: list of field keys to leave blank/skip

        Keys in data:
            no_of_plots, plot_number, contiguous,
            boundary_wall, explanation
        """
        if skip_fields is None:
            skip_fields = []

        # Step 1: Select Multiple plot type + wait for dynamic form
        self.select_plot_type("Multiple")

        # Wait for number of plots field to be visible
        self.page.locator("#no_of_plots").wait_for(state="visible", timeout=5000)

        # Step 2: Number of Plots
        if "no_of_plots" not in skip_fields:
            value = data.get("no_of_plots", "")
            self.page.locator("#no_of_plots").click()
            self.page.locator("#no_of_plots").fill(str(value) if value is not None else "")
        else:
            self.page.locator("#no_of_plots").click()
            self.page.locator("#no_of_plots").fill("")

        # Step 3: On which plot school building is constructed
        if "plot_number" not in skip_fields:
            value = data.get("plot_number", "")
            self.page.locator("#plot_number_school_building").click()
            self.page.locator("#plot_number_school_building").fill(
                str(value) if value is not None else ""
            )
        else:
            self.page.locator("#plot_number_school_building").click()
            self.page.locator("#plot_number_school_building").fill("")

        # Step 4: Are the plots contiguous? (Yes/No radio)
        # Note: These radios have IDs #renewal_yes / #renewal_no with name='plotTypeyes'
        if "contiguous" not in skip_fields and data.get("contiguous"):
            if data["contiguous"] == "Yes":
                self.page.locator("#renewal_yes").click()
            else:
                self.page.locator("#renewal_no").click()
            self.page.wait_for_timeout(1000)

            # Step 5: If Contiguous=No → Single Boundary Wall? (conditional)
            if data["contiguous"] == "No" and "boundary_wall" not in skip_fields:
                if data.get("boundary_wall"):
                    # Wait for boundary wall radios to appear
                    self.page.wait_for_timeout(500)
                    if data["boundary_wall"] == "Yes":
                        self.page.get_by_role("radio", name="Yes").last.click()
                    else:
                        self.page.get_by_role("radio", name="No").last.click()
                    self.page.wait_for_timeout(1000)

                    # Step 6: If Boundary=No → Explanation textarea (conditional)
                    if data["boundary_wall"] == "No" and "explanation" not in skip_fields:
                        value = data.get("explanation", "")
                        # Wait for explanation textarea to appear
                        self.page.wait_for_timeout(500)
                        explanation_field = self.page.locator("textarea").last
                        try:
                            explanation_field.click(timeout=3000)
                            explanation_field.fill(str(value) if value else "")
                        except Exception:
                            pass

        # Step 7: Click Next
        self.click_next()
