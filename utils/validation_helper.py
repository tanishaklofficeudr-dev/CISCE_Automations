"""
Validation Helper Utility
==========================
Generic reusable utility for capturing and asserting form validation messages
across all modules of the CISCE Preliminary Affiliation automation framework.

Usage:
    from utils.validation_helper import ValidationHelper

    errors = ValidationHelper.get_all_errors(page)
    ValidationHelper.assert_error_present(page, "School name is required")
    ValidationHelper.assert_form_blocked(page, current_url)

Compatible with: Python 3.14, Playwright, Pytest
"""

from typing import List
from playwright.sync_api import Page


class ValidationHelper:
    """
    Reusable validation message utility for form validation testing.

    Supports:
    - Extracting all visible validation errors from a page
    - Asserting specific error messages are present
    - Verifying form submission was blocked (no navigation)
    - Checking if a specific field has an error state

    Designed to work with Bootstrap-style validation feedback elements
    commonly used in the CISCE application.
    """

    # CSS selectors for validation error messages (ordered by specificity)
    ERROR_SELECTORS = [
        ".invalid-feedback:visible",
        ".error-message:visible",
        ".text-danger:visible",
        "[class*='invalid']:visible:not(input):not(select):not(textarea)",
        ".form-error:visible",
        ".validation-error:visible",
        ".field-error:visible",
    ]

    @staticmethod
    def get_all_errors(page: Page, timeout: int = 2000) -> List[str]:
        """
        Collect all visible validation error messages from the current page.

        Scans the page for common validation message patterns and returns
        a deduplicated list of error text strings.

        Args:
            page: Playwright Page instance.
            timeout: Milliseconds to wait for errors to appear after form submission.

        Returns:
            List of visible error message strings, stripped and deduplicated.
        """
        page.wait_for_timeout(timeout)

        errors = []

        for selector in ValidationHelper.ERROR_SELECTORS:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible():
                        text = element.inner_text().strip()
                        if text and text not in errors:
                            errors.append(text)
            except Exception:
                continue

        return errors

    @staticmethod
    def get_error_for_field(page: Page, field_locator: str, timeout: int = 2000) -> str:
        """
        Get the validation error message associated with a specific field.

        Looks for error feedback immediately following the target field element
        (sibling or parent-child relationship typical in Bootstrap forms).

        Args:
            page: Playwright Page instance.
            field_locator: CSS selector or ID of the target field (e.g., "#school_name").
            timeout: Milliseconds to wait for error to appear.

        Returns:
            Error message string if found, empty string otherwise.
        """
        page.wait_for_timeout(timeout)

        # Strategy 1: Look for .invalid-feedback sibling after the field
        sibling_selector = f"{field_locator} ~ .invalid-feedback"
        try:
            sibling = page.locator(sibling_selector)
            if sibling.count() > 0 and sibling.first.is_visible():
                return sibling.first.inner_text().strip()
        except Exception:
            pass

        # Strategy 2: Look for error within the same parent container
        parent_selector = f"{field_locator} >> xpath=.. >> .invalid-feedback"
        try:
            parent_error = page.locator(parent_selector)
            if parent_error.count() > 0 and parent_error.first.is_visible():
                return parent_error.first.inner_text().strip()
        except Exception:
            pass

        # Strategy 3: Check if field itself has validation class and aria-describedby
        try:
            field = page.locator(field_locator)
            if field.count() > 0:
                described_by = field.get_attribute("aria-describedby")
                if described_by:
                    desc_element = page.locator(f"#{described_by}")
                    if desc_element.count() > 0 and desc_element.is_visible():
                        return desc_element.inner_text().strip()
        except Exception:
            pass

        return ""

    @staticmethod
    def assert_error_present(page: Page, expected_error: str, timeout: int = 2000) -> None:
        """
        Assert that a specific validation error message is visible on the page.

        Performs a case-insensitive partial match against all visible errors.

        Args:
            page: Playwright Page instance.
            expected_error: Expected error text (partial match supported).
            timeout: Milliseconds to wait for errors to appear.

        Raises:
            AssertionError: If the expected error is not found among visible errors.
        """
        errors = ValidationHelper.get_all_errors(page, timeout)
        expected_lower = expected_error.lower()

        match_found = any(
            expected_lower in error.lower()
            for error in errors
        )

        assert match_found, (
            f"Expected validation error '{expected_error}' not found.\n"
            f"Visible errors: {errors}"
        )

    @staticmethod
    def assert_no_errors(page: Page, timeout: int = 1000) -> None:
        """
        Assert that no validation errors are visible on the page.

        Useful for positive test scenarios where form submission should succeed.

        Args:
            page: Playwright Page instance.
            timeout: Milliseconds to wait before checking.

        Raises:
            AssertionError: If any validation errors are found.
        """
        errors = ValidationHelper.get_all_errors(page, timeout)

        assert len(errors) == 0, (
            f"Expected no validation errors but found: {errors}"
        )

    @staticmethod
    def assert_form_blocked(page: Page, url_before_submit: str) -> None:
        """
        Assert that the form did not navigate away (submission was blocked).

        For SPA apps: checks that validation errors appeared OR next step did NOT load.

        Args:
            page: Playwright Page instance.
            url_before_submit: Not used for SPA — kept for API compatibility.

        Raises:
            AssertionError: If the form navigated to next step.
        """
        page.wait_for_timeout(1000)
        errors = ValidationHelper.get_all_errors(page, timeout=500)
        if errors:
            return  # Form is blocked — errors visible

        # Check if next step appeared using specific locator
        try:
            address_tab = page.locator("#TabAddressDetails")
            if address_tab.count() > 0 and address_tab.is_visible():
                raise AssertionError(
                    "Form was NOT blocked. Navigated to Address Details step."
                )
        except AssertionError:
            raise
        except Exception:
            pass

    @staticmethod
    def assert_form_submitted(page: Page, url_before_submit: str) -> None:
        """
        Assert that the form navigated to the next step (submission was successful).

        For SPA apps: checks that next step tab became active or next step content appeared.

        Args:
            page: Playwright Page instance.
            url_before_submit: Not used for SPA — kept for API compatibility.

        Raises:
            AssertionError: If the page did NOT navigate to next step.
        """
        page.wait_for_timeout(2000)

        # Check if Address Details tab/content became active using specific locator
        try:
            address_tab = page.locator("#TabAddressDetails")
            if address_tab.count() > 0 and address_tab.is_visible():
                return  # Form submitted — Address Details step visible
        except Exception:
            pass

        # Fallback: check if School Details heading is gone (form moved)
        try:
            school_heading = page.locator("p:has-text('School Details')").first
            if not school_heading.is_visible():
                return  # School Details no longer visible = navigated away
        except Exception:
            pass

        # Check for validation errors
        errors = ValidationHelper.get_all_errors(page, timeout=500)
        raise AssertionError(
            f"Form was NOT submitted. Page did not navigate to next step.\n"
            f"Visible errors: {errors}"
        )

    @staticmethod
    def has_errors(page: Page, timeout: int = 1000) -> bool:
        """
        Check whether any validation errors are currently visible.

        Non-asserting boolean check — useful in conditional logic.

        Args:
            page: Playwright Page instance.
            timeout: Milliseconds to wait before checking.

        Returns:
            True if any validation errors are visible, False otherwise.
        """
        errors = ValidationHelper.get_all_errors(page, timeout)
        return len(errors) > 0

    @staticmethod
    def get_error_count(page: Page, timeout: int = 1000) -> int:
        """
        Return the count of visible validation errors on the page.

        Args:
            page: Playwright Page instance.
            timeout: Milliseconds to wait before checking.

        Returns:
            Integer count of visible error messages.
        """
        errors = ValidationHelper.get_all_errors(page, timeout)
        return len(errors)


    @staticmethod
    def set_readonly_date(page: Page, selector: str, date_value: str) -> None:
        """
        Set value on a readonly datepicker field using JavaScript injection.

        Uses nativeInputValueSetter to bypass readonly restriction and
        dispatches input, change, and blur events so the application
        recognizes the value.

        Verified working with:
        - NOC Details: #noc_date[name='noc_date']
        - Trust Details: #establishment_date, #registration_date
        - Any Bootstrap datepicker with readonly="readonly"

        Args:
            page: Playwright Page instance.
            selector: CSS selector for the date input (e.g., '#noc_date[name="noc_date"]').
            date_value: Date string to set (e.g., '16/05/2025'). Pass '' to clear.
        """
        page.evaluate(f"""
            (dateVal) => {{
                const input = document.querySelector('{selector}');
                if (input) {{
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value').set;
                    nativeInputValueSetter.call(input, dateVal);
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                }}
            }}
        """, date_value)
        page.wait_for_timeout(500)
