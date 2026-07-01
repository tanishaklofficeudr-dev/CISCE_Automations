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

        