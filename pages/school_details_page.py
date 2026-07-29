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

    def click_next(self):
        """
        Click the Next button without filling any fields.

        Used by negative tests to trigger validation on blank or
        partially filled forms.
        """
        self.page.get_by_role("button", name="Next").click()

    def fill_partial_details(self, data, skip_fields=None):
        """
        Fill all School Details fields except those in skip_fields, then click Next.

        Reuses the same locators as fill_school_details(). Fields listed in
        skip_fields are left untouched (blank/default), triggering validation.

        Args:
            data: Dict with keys matching School_Details sheet columns.
            skip_fields: List of field names to skip. Valid names:
                         school_name, school_classification, school_type,
                         contact_person, website, udise_number, school_category
        """
        if skip_fields is None:
            skip_fields = []

        if "school_name" not in skip_fields:
            self.page.get_by_role(
                "textbox",
                name="Name of School *"
            ).fill(str(data.get("school_name", "")))
        else:
            # Clear the field to test blank validation
            self.page.get_by_role(
                "textbox",
                name="Name of School *"
            ).fill("")

        if "school_classification" not in skip_fields:
            self.page.get_by_label(
                "School Classification *"
            ).select_option(label=data["school_classification"])

        if "school_type" not in skip_fields:
            self.page.locator("#school_type").select_option(
                label=data["school_type"]
            )

        if "contact_person" not in skip_fields:
            self.page.locator("#contact_person").fill(
                str(data.get("contact_person", ""))
            )
        else:
            self.page.locator("#contact_person").fill("")

        if "website" not in skip_fields:
            self.page.locator("#website").fill(
                str(data.get("website", ""))
            )
        else:
            self.page.locator("#website").fill("")

        if "udise_number" not in skip_fields:
            self.page.locator("#udise").fill(
                str(data.get("udise_number", ""))
            )
        else:
            self.page.locator("#udise").fill("")

        # Contact Number (fetched from registration but may be empty on first run)
        if "contact_number" not in skip_fields:
            contact_num_field = self.page.locator("#contact_no")
            if contact_num_field.is_visible():
                contact_num_field.fill(str(data.get("contact_number", "")))

        # Contact Email (fetched from registration but may be empty on first run)
        if "contact_email" not in skip_fields:
            contact_email_field = self.page.locator("#contact_email")
            if contact_email_field.is_visible():
                contact_email_field.fill(str(data.get("contact_email", "")))

        if "school_category" not in skip_fields:
            self.page.get_by_label(
                "School Category *"
            ).select_option(label=data["school_category"])

        self.page.get_by_role("button", name="Next").click()