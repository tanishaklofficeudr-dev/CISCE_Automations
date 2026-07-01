from playwright.sync_api import expect


class RegistrationPage:

    def __init__(self, page):
        self.page = page

    def register_school(self, data):

        # Open Registration Page
        self.page.goto(
            "https://dev-eaffiliation.cisce.org/registration"
        )

        # Mobile Number
        self.page.get_by_role(
            "textbox",
            name="Country code * Enter Your"
        ).fill(
            str(data["mobile_number"])
        )

        # Email
        self.page.get_by_role(
            "textbox",
            name="Enter Your Email Address *"
        ).fill(
            data["email"]
        )

        # Register Button
        self.page.get_by_role(
            "button",
            name="Register"
        ).click()

        # =================================================
        # Handle Success Popup if it appears
        # =================================================
        try:

            success_popup = self.page.get_by_text(
                "Registration successful"
            )

            expect(success_popup).to_be_visible(
                timeout=2000
            )

            # Click OK button
            self.page.get_by_role(
                "button",
                name="OK"
            ).click()

        except:
            print(
                "Registration success popup not displayed."
            )