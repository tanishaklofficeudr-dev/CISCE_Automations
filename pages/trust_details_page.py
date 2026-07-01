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