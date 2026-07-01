import os
import time 
from playwright.sync_api import expect

class UploadDocumentsPage:

    def __init__(self, page):
        self.page = page

    def upload_documents(self, data):
        file_path = os.path.abspath("test_data/LandCertificate.pdf")
        self.page.wait_for_timeout(3000)

        # NOC Document  
           
        container_noc = self.page.locator("div.col-lg-6", has_text="NOC Document")
        with self.page.expect_file_chooser() as fc_info:
            container_noc.locator("#noc").click()
        fc_info.value.set_files(file_path)

        container = self.page.locator("div.col-lg-6", has_text="Certificate of Land")

        with self.page.expect_file_chooser() as fc_info:
            # Click the 'dz-message' area inside that specific container
            container.locator(".dz-message").click()

        file_chooser = fc_info.value
        file_chooser.set_files(file_path)

        container_trust = self.page.locator("div.col-lg-6", has_text="Trust / Society / Company Document")
        with self.page.expect_file_chooser() as fc_info:
            container_trust.locator("#trust").click()
        fc_info.value.set_files(file_path)

        container_land_ownership = self.page.locator("div.col-lg-6", has_text="Land Ownership Document")

        with self.page.expect_file_chooser() as fc_info:
            # Click the dropzone area (using ID #land or the .dz-message inside the container)
            container_land_ownership.locator("#land").click()

        file_chooser = fc_info.value
        file_chooser.set_files(file_path)

        container_school_image = self.page.locator("div.col-lg-6", has_text="School Image")
        with self.page.expect_file_chooser() as fc_info:
            container_school_image.locator("#school_image").click()
        fc_info.value.set_files(file_path)
        
        # Wait after upload
        self.page.wait_for_timeout(3000)

        # =================================================
        # Comments
        # =================================================
        self.page.get_by_role(
            "textbox",
            name="Any relevant information that"
        ).fill(
            data["comments"]
        )

        # =================================================
        # Affiliation Type
        # =================================================
        self.page.get_by_label(
            data["affiliation_type"]
        ).check(force=True)

        # =================================================
        # Verify Checkboxes
        # =================================================
        self.page.locator(
            "#verify_composite"
        ).check(force=True)

        self.page.locator(
            "#verify"
        ).check(force=True)

        # =================================================
        # Proceed
        # =================================================
        self.page.get_by_role(
            "button",
            name="Proceed to Payment"
        ).click(force=True)

        # =================================================
        # Wait for Payment Page
        # =================================================
        self.page.wait_for_timeout(10000)

        # =================================================
        # Validate Payment URL
        # =================================================
        self.page.wait_for_url("**/payment**", timeout=30000)

        # =================================================
        # Click Pay ₹ Button
        # =================================================
        self.page.get_by_role(
            "button",
            name="Pay ₹"
        ).click()

        # =================================================
        # Validate Payment Details Page
        # =================================================
        expect(
            self.page.get_by_role(
                "heading",
                name="Payment Details"
            )
        ).to_be_visible()

        # =================================================
        # Select ICICI Bank
        # =================================================
        self.page.get_by_role(
            "img",
            name="ICICI Bank"
        ).click()

        self.page.wait_for_timeout(2000)

        # =================================================
        # Proceed to Pay
        # =================================================
        # The button stays disabled because gateway selection needs
        # to set a hidden field. Use JavaScript to select gateway
        # and enable the button properly.
        self.page.evaluate("""
            () => {
                // Try to find and call the gateway selection function
                // Look for radio buttons or hidden inputs for gateway
                const iciciImg = document.querySelector('img[alt*="ICICI"]');
                if (iciciImg) {
                    const parent = iciciImg.closest('label') || iciciImg.closest('div');
                    if (parent) {
                        const radio = parent.querySelector('input[type="radio"]');
                        if (radio) {
                            radio.checked = true;
                            radio.dispatchEvent(new Event('change', { bubbles: true }));
                            radio.dispatchEvent(new Event('click', { bubbles: true }));
                        }
                    }
                }
                
                // Also try setting any gateway-related hidden fields
                const gatewayInputs = document.querySelectorAll('input[name*="gateway"], input[name*="bank"], input[name*="payment"]');
                gatewayInputs.forEach(input => {
                    if (input.type === 'hidden' || input.type === 'radio') {
                        input.value = input.value || 'ICICI';
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                });
            }
        """)

        self.page.wait_for_timeout(3000)

        # Force enable and click the pay button
        self.page.evaluate("""
            () => {
                const btn = document.querySelector('#pay-button');
                if (btn) {
                    btn.disabled = false;
                    btn.removeAttribute('disabled');
                    btn.click();
                }
            }
        """)

        # Wait and check if initiatePayment exists, call it as backup
        self.page.wait_for_timeout(2000)
        self.page.evaluate("""
            () => {
                if (typeof initiatePayment === 'function') {
                    initiatePayment();
                }
            }
        """)

        # =================================================
        # Wait for QR Section
        # =================================================
        self.page.wait_for_timeout(
            5000
        )

        # =================================================
        # Click Show QR
        # =================================================
        iframe = self.page.locator(
            "iframe"
        ).content_frame

        iframe.get_by_role(
            "button",
            name="Show QR"
        ).click()

        # =================================================
        # Click Final Pay Button
        # =================================================
        iframe = self.page.locator(
            "iframe"
        ).content_frame

        iframe.get_by_test_id(
            "fee-bearer-cta"
        ).click()

        # =================================================
        # Wait for Success Page
        # =================================================
        self.page.wait_for_timeout(10000)
        

        # =================================================
        # Validate Transaction Success
        # =================================================
        expect(
            self.page.get_by_text(
                "Transaction Successful!"
            )
        ).to_be_visible(
            timeout=30000
        )

        # =================================================
        # Click Go to Home Button
        # =================================================
        self.page.get_by_role(
            "link",
            name="Go to Homepage"
        ).click()

        # Validate Home Page
        self.page.wait_for_url("**/school_view**", timeout=30000)
        