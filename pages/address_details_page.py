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