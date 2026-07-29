class AddressDetailsPage:

    def __init__(self, page):
        self.page = page

    def fill_address_details(self, data):

        # Address Line
        self.page.locator("#address_1").click()
        self.page.locator("#address_1").fill(
            data["address_line_1"]
        )

        # Country Dropdown
        self.page.get_by_role(
            "textbox",
            name="India"
        ).click()

        self.page.get_by_role(
            "option",
            name=data["country"]
        ).click()

        # State Dropdown
        self.page.locator(
            "#select2-state-container"
        ).click()

        self.page.get_by_role(
            "option",
            name=data["state"]
        ).click()

        # District Dropdown
        self.page.get_by_role(
            "textbox",
            name="Select"
        ).click()

        self.page.get_by_role(
            "option",
            name=data["district"]
        ).click()

        # City Dropdown
        self.page.get_by_role(
            "textbox",
            name="Select"
        ).click()

        self.page.get_by_role(
            "option",
            name=data["city"]
        ).click()

        # ZIP
        self.page.locator("#zip").click()
        self.page.locator("#zip").fill(
            str(data["zip_pin"])
        )

        # Locality Type
        self.page.locator("#locality").select_option(
            label=data["locality_type"]
        )

        # Next
        self.page.get_by_role(
            "button",
            name="Next"
        ).click()

    def click_next(self):
        """Click the Next button without filling any fields."""
        self.page.get_by_role("button", name="Next").click()

    def fill_address_line(self, value):
        """Clear and fill only the address line field."""
        self.page.locator("#address_1").fill(str(value))

    def fill_zip(self, value):
        """Clear and fill only the ZIP/PIN code field."""
        self.page.locator("#zip").fill(str(value))

    def fill_partial_details(self, data, skip_fields=None):
        """
        Fill Address Details fields except those in skip_fields, then click Next.

        Cascade rules:
        - Skipping "country" also skips state, district, city
        - Skipping "state" also skips district, city
        - Skipping "district" also skips city
        - address_line_1, zip_pin, locality_type can be skipped independently

        For text fields in skip_fields: cleared with .fill("")
        For dropdowns in skip_fields: left unchanged (retain saved value)

        Args:
            data: Dict with address field keys.
            skip_fields: List of field names to skip/clear.
        """
        if skip_fields is None:
            skip_fields = []

        # Cascade enforcement
        if "country" in skip_fields:
            skip_fields = list(set(skip_fields + ["state", "district", "city"]))
        if "state" in skip_fields:
            skip_fields = list(set(skip_fields + ["district", "city"]))
        if "district" in skip_fields:
            skip_fields = list(set(skip_fields + ["city"]))

        # Address Line
        if "address_line_1" not in skip_fields:
            self.page.locator("#address_1").fill(str(data.get("address_line_1", "")))
        else:
            self.page.locator("#address_1").fill("")

        # Country (Select2 Autocomplete)
        if "country" not in skip_fields:
            self.page.get_by_role("textbox", name="India").click()
            self.page.get_by_role("option", name=data["country"]).click()
            self.page.wait_for_timeout(1000)

        # State (Select2 Dependent)
        if "state" not in skip_fields:
            self.page.locator("#select2-state-container").click()
            self.page.get_by_role("option", name=data["state"]).click()
            self.page.wait_for_timeout(1000)

        # District (Select2 Dependent)
        if "district" not in skip_fields:
            # Open the District Select2 dropdown
            district_container = self.page.locator("#select2-district-container")
            if district_container.count() > 0 and district_container.is_visible():
                district_container.click()
                self.page.wait_for_timeout(500)
            else:
                self.page.get_by_role("textbox", name="Select").first.click()
                self.page.wait_for_timeout(500)

            # Select an option from the opened dropdown
            if data.get("district"):
                self.page.get_by_role("option", name=data["district"]).click()
            else:
                # Pick first ENABLED option (skip disabled "Select" placeholder)
                self.page.locator(".select2-results__option:not(.select2-results__option--disabled)").first.click()
            self.page.wait_for_timeout(1000)

        # City (Select2 Dependent)
        if "city" not in skip_fields:
            # Open the City Select2 dropdown
            city_container = self.page.locator("#select2-city-container")
            if city_container.count() > 0 and city_container.is_visible():
                city_container.click()
                self.page.wait_for_timeout(500)
            else:
                self.page.get_by_role("textbox", name="Select").first.click()
                self.page.wait_for_timeout(500)

            # Select an option from the opened dropdown
            if data.get("city"):
                self.page.get_by_role("option", name=data["city"]).click()
            else:
                # Pick first ENABLED option (skip disabled "Select" placeholder)
                self.page.locator(".select2-results__option:not(.select2-results__option--disabled)").first.click()
            self.page.wait_for_timeout(1000)

        # ZIP/PIN Code
        if "zip_pin" not in skip_fields:
            self.page.locator("#zip").fill(str(data.get("zip_pin", "")))
        else:
            self.page.locator("#zip").fill("")

        # Locality Type
        if "locality_type" not in skip_fields:
            self.page.locator("#locality").select_option(label=data["locality_type"])

        # Click Next
        self.page.get_by_role("button", name="Next").click()
