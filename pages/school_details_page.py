class SchoolDetailsPage:
    def __init__(self, page):
        self.page = page

    def fill_school_details(self, data):

        self.page.get_by_role(
            "textbox",
            name="Name of School *"
        ).fill(data["school_name"])

        self.page.get_by_label(
            "School Classification *"
        ).select_option(label=data["school_classification"])

        self.page.locator("#school_type").select_option(
            label=data["school_type"]
        )

        self.page.locator("#contact_person").fill(
            data["contact_person"]
        )

        self.page.locator("#website").fill(
            data["website"]
        )

        self.page.locator("#udise").fill(
            str(data["udise_number"])
        )

        self.page.get_by_label(
            "School Category *"
        ).select_option(label=data["school_category"])

        self.page.get_by_role("button", name="Next").click()