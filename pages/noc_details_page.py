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

    def click_next(self):
        """Click the Next button without filling any fields."""
        self.page.get_by_role("button", name="Next").click()

    def fill_authority(self, value):
        """Fill/clear the NOC Issuing Authority field."""
        self.page.locator("#noc_authority").fill(str(value))

    def fill_designation(self, value):
        """Fill/clear the Designation field."""
        self.page.locator("#noc_designation").fill(str(value))

    def fill_office_address(self, value):
        """Fill/clear the Office Address field."""
        self.page.locator("#noc_office_address").fill(str(value))

    def fill_reference_number(self, value):
        """Fill/clear the NOC Reference Number field."""
        self.page.get_by_role(
            "textbox", name="Select NOC Reference Number"
        ).fill(str(value))

    def set_date(self, date_value):
        """
        Set the NOC Date using JavaScript injection.
        Reuses ValidationHelper.set_readonly_date().

        Args:
            date_value: Date string (e.g., '16/05/2025') or '' to clear.
        """
        from utils.validation_helper import ValidationHelper
        ValidationHelper.set_readonly_date(
            self.page, '#noc_date[name="noc_date"]', date_value
        )

    def fill_partial_details(self, data, skip_fields=None):
        """
        Fill all NOC fields except those in skip_fields, then click Next.

        Text fields in skip_fields → cleared with .fill("")
        Date in skip_fields → cleared via JS
        Country/State → always set to valid values (cannot blank)

        Args:
            data: Dict with NOC field keys.
            skip_fields: List of field names to skip/clear.
        """
        if skip_fields is None:
            skip_fields = []

        # NOC Authority
        if "noc_authority" not in skip_fields:
            self.page.locator("#noc_authority").fill(
                str(data.get("noc_authority", ""))
            )
        else:
            self.page.locator("#noc_authority").fill("")

        # Designation
        if "designation" not in skip_fields:
            self.page.locator("#noc_designation").fill(
                str(data.get("designation", ""))
            )
        else:
            self.page.locator("#noc_designation").fill("")

        # Office Address
        if "office_address" not in skip_fields:
            self.page.locator("#noc_office_address").fill(
                str(data.get("office_address", ""))
            )
        else:
            self.page.locator("#noc_office_address").fill("")

        # Country (standard <select> — always set, cannot blank)
        country_val = data.get("country_value", "2")
        self.page.locator("#noc_country").select_option(str(country_val))
        self.page.wait_for_timeout(1000)

        # State (dependent <select> — always set, cannot blank)
        state_val = data.get("state_value", "30")
        self.page.locator("#noc_state").select_option(str(state_val))

        # NOC Reference Number
        if "noc_reference_number" not in skip_fields:
            self.page.get_by_role(
                "textbox", name="Select NOC Reference Number"
            ).fill(str(data.get("noc_reference_number", "")))
        else:
            self.page.get_by_role(
                "textbox", name="Select NOC Reference Number"
            ).fill("")

        # Date of NOC (readonly — uses JS injection)
        if "noc_date" not in skip_fields:
            from utils.validation_helper import ValidationHelper
            ValidationHelper.set_readonly_date(
                self.page, '#noc_date[name="noc_date"]',
                str(data.get("noc_date", ""))
            )
        else:
            from utils.validation_helper import ValidationHelper
            ValidationHelper.set_readonly_date(
                self.page, '#noc_date[name="noc_date"]', ""
            )

        # Click Next
        self.page.get_by_role("button", name="Next").click()
