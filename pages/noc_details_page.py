class NOCDetailsPage:

    def __init__(self, page):
        self.page = page

    def fill_noc_details(self, data):

        # NOC Issuing Authority
        self.page.locator(
            "#noc_authority"
        ).click()

        self.page.locator(
            "#noc_authority"
        ).fill(
            data["noc_issuing_authority"]
        )

        # Designation
        self.page.locator(
            "#noc_designation"
        ).click()

        self.page.locator(
            "#noc_designation"
        ).fill(
            data["designation"]
        )

        # Office Address
        self.page.locator(
            "#noc_office_address"
        ).click()

        self.page.locator(
            "#noc_office_address"
        ).fill(
            data["office_address"]
        )

        # Country Dropdown
        # self.page.locator(
        #     "#noc_country"
        # ).select_option(
        #     label=data["country"]
        # )

        # # State Dropdown
        # self.page.locator(
        #     "#noc_state"
        # ).select_option(
        #     label=data["state"]
        # )

        # # Country Dropdown
        # self.page.locator(
        #     "#noc_country"
        # ).select_option(
        #     str(data["country"])
        # )

        # # State Dropdown
        # self.page.locator(
        #     "#noc_state"
        # ).select_option(
        #     str(data["state"])
        # )


        # Country Dropdown
        self.page.locator("#noc_country").select_option("2")

        # IMPORTANT FIX
        # State Dropdown using VALUE
        self.page.locator("#noc_state").select_option("30")

        # NOC Reference Number
        self.page.get_by_role(
            "textbox",
            name="Select NOC Reference Number"
        ).click()

        self.page.get_by_role(
            "textbox",
            name="Select NOC Reference Number"
        ).fill(
            str(data["noc_reference_number"])
        )

        # NOC Date
        self.page.locator("#noc_date[name='noc_date']").click()

        # Click the back arrow («) to navigate to the previous month (May 2026)
        self.page.get_by_role("columnheader", name="«").click()

        # Select day
        self.page.get_by_role("cell", name="16", exact=True).click()


        # Next Button
        self.page.get_by_role(
            "button",
            name="Next"
        ).click()