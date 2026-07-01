class LoginPage:
    def __init__(self, page):
        self.page = page

    def login(self, data):
        self.page.get_by_role("link", name="login").click()

        self.page.get_by_role(
            "textbox",
            name="Enter Your Mobile Number"
        ).fill(str(data["mobile_number"]))

        print("Enter password manually and continue...")

        self.page.pause()

        self.page.get_by_role("button", name="Login").click()