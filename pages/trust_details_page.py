class TrustDetailsPage:

    def __init__(self, page):
        self.page = page

    def fill_trust_details(self, data):

        # Ownership Type
        self.page.wait_for_timeout(2000)

        self.page.locator("#ownership_type").wait_for(
            state="visible"
        )

        self.page.locator("#ownership_type").select_option(
            data["ownership_type"]
        )

        # Trust / Society / Company Name
        self.page.locator(
            "#owner_name"
        ).click()

        self.page.locator(
            "#owner_name"
        ).fill(
            data["trust_name"]
        )

        # Establishment Date - Set value directly via JavaScript
        # (Navigating back 75+ months with the back arrow is impractical)
        self.page.evaluate("""
            (date) => {
                const input = document.querySelector('#establishment_date');
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(input, date);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """, str(data["establishment_date"]))


        # Registration Date - Set value directly via JavaScript
        self.page.evaluate("""
            (date) => {
                const input = document.querySelector('#registration_date');
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(input, date);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """, str(data["registration_date"]))

        # Registration Number
        self.page.locator(
            "#registration_no"
        ).click()

        self.page.locator(
            "#registration_no"
        ).fill(
            str(data["registration_number"])
        )

        # Next Button
        self.page.get_by_role(
            "button",
            name="Next"
        ).click()

    def click_next(self):
        """Click the Next button without filling any fields."""
        self.page.get_by_role("button", name="Next").click()

    def fill_name(self, value):
        """Fill/clear the Trust/Society/Company Name field (textarea)."""
        self.page.locator("#owner_name").fill(str(value))

    def fill_registration_number(self, value):
        """Fill/clear the Registration Number field."""
        self.page.locator("#registration_no").fill(str(value))

    def set_establishment_date(self, date_value):
        """
        Set Date of Establishment using JavaScript injection.
        Reuses ValidationHelper.set_readonly_date().

        Args:
            date_value: Date string (e.g., '05/03/2020') or '' to clear.
        """
        from utils.validation_helper import ValidationHelper
        ValidationHelper.set_readonly_date(self.page, "#establishment_date", date_value)

    def set_registration_date(self, date_value):
        """
        Set Date of Registration using JavaScript injection.
        Reuses ValidationHelper.set_readonly_date().

        Args:
            date_value: Date string (e.g., '10/04/2021') or '' to clear.
        """
        from utils.validation_helper import ValidationHelper
        ValidationHelper.set_readonly_date(self.page, "#registration_date", date_value)

    def fill_partial_details(self, data, skip_fields=None):
        """
        Fill all Trust Details fields except those in skip_fields, then click Next.

        Text fields in skip_fields -> cleared with .fill("")
        Dates in skip_fields -> cleared via set_readonly_date("", "")
        Ownership -> always set to valid value (cannot blank)

        Args:
            data: Dict with trust field keys.
            skip_fields: List of field names to skip/clear.
        """
        if skip_fields is None:
            skip_fields = []

        # Ownership Type (always set — cannot blank)
        self.page.wait_for_timeout(1000)
        self.page.locator("#ownership_type").wait_for(state="visible")
        ownership = data.get("ownership_type", "Trust")
        self.page.locator("#ownership_type").select_option(label=ownership)
        self.page.wait_for_timeout(500)

        # Trust/Society/Company Name (textarea)
        if "owner_name" not in skip_fields:
            self.page.locator("#owner_name").fill(str(data.get("trust_name", "")))
        else:
            self.page.locator("#owner_name").fill("")

        # Establishment Date
        from utils.validation_helper import ValidationHelper
        if "establishment_date" not in skip_fields:
            ValidationHelper.set_readonly_date(
                self.page, "#establishment_date", str(data.get("establishment_date", ""))
            )
        else:
            ValidationHelper.set_readonly_date(self.page, "#establishment_date", "")

        # Registration Date
        if "registration_date" not in skip_fields:
            ValidationHelper.set_readonly_date(
                self.page, "#registration_date", str(data.get("registration_date", ""))
            )
        else:
            ValidationHelper.set_readonly_date(self.page, "#registration_date", "")

        # Registration Number
        if "registration_no" not in skip_fields:
            self.page.locator("#registration_no").fill(
                str(data.get("registration_number", ""))
            )
        else:
            self.page.locator("#registration_no").fill("")

        # Click Next
        self.page.get_by_role("button", name="Next").click()
