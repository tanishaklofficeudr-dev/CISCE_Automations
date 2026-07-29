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
        

    # ===========================================================================
    # REGRESSION TEST METHODS (Additive — Upload Documents Module)
    # ===========================================================================

    # Dropzone ID mapping for each document type
    UPLOAD_MAP = {
        "NOC Document": "#noc",
        "Certificate of Land": "#land_certificate",
        "Trust / Society / Company Document": "#trust",
        "Land Ownership Document": "#land",
        "School Image": "#school_image",
    }

    def upload_single_file(self, document_label, file_path):
        """
        Upload a single file to a specific dropzone identified by its label.

        Args:
            document_label: Visible label text (e.g., "NOC Document", "School Image")
            file_path: Absolute path to the file to upload

        Returns:
            None. Waits 3000ms after upload for async processing.

        Raises:
            TimeoutError if file chooser doesn't appear within 10s.
        """
        dropzone_id = self.UPLOAD_MAP.get(document_label)
        container = self.page.locator("div.col-lg-6", has_text=document_label)

        with self.page.expect_file_chooser(timeout=10000) as fc_info:
            if dropzone_id:
                container.locator(dropzone_id).click()
            else:
                container.locator(".dz-message").click()

        fc_info.value.set_files(file_path)
        self.page.wait_for_timeout(3000)

    def upload_all_documents(self, file_path):
        """
        Upload the same file to all 5 dropzones in sequence.
        Waits 3000ms between each upload for async processing.

        Args:
            file_path: Absolute path to the file to upload to all dropzones.
        """
        for label in self.UPLOAD_MAP.keys():
            self.upload_single_file(label, file_path)

    def select_affiliation_type(self, label):
        """
        Select an affiliation type radio button by its visible label text.

        Args:
            label: Full or partial label text (e.g., "Provisional Affiliation up to Class X")

        Uses JavaScript to select by value since labels are ambiguous for Switch Over options.
        Retries on context destruction (caused by upload navigation).
        """
        # Map label text to radio value
        value_map = {
            "Provisional Affiliation up to Class X": "2",
            "Composite Affiliation up to Class XII": "3",
            "Affiliation Under Switch Over Category up to class X": "4",
            "Affiliation Under Switch Over Category up to class XII": "5",
        }

        value = value_map.get(label)
        if value:
            for attempt in range(3):
                try:
                    self.page.evaluate(f"""
                        () => {{
                            const radios = document.querySelectorAll('input[name="composite_type"]');
                            for (const r of radios) {{
                                if (r.value === '{value}') {{
                                    r.checked = true;
                                    r.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    r.dispatchEvent(new Event('click', {{ bubbles: true }}));
                                    break;
                                }}
                            }}
                        }}
                    """)
                    break
                except Exception:
                    self.page.wait_for_timeout(2000)
        else:
            # Fallback: try get_by_label for unknown labels
            self.page.get_by_label(label).first.check(force=True)
        self.page.wait_for_timeout(500)

    def check_declarations(self):
        """
        Check both declaration checkboxes (#verify_composite and #verify).
        Uses JavaScript with retry to handle context destruction after uploads.
        """
        for attempt in range(3):
            try:
                self.page.evaluate("""
                    () => {
                        const vc = document.querySelector('#verify_composite');
                        const v = document.querySelector('#verify');
                        if (vc && !vc.checked) { vc.checked = true; vc.dispatchEvent(new Event('change', { bubbles: true })); }
                        if (v && !v.checked) { v.checked = true; v.dispatchEvent(new Event('change', { bubbles: true })); }
                    }
                """)
                break
            except Exception:
                self.page.wait_for_timeout(2000)
        self.page.wait_for_timeout(500)

    def fill_comments(self, text):
        """
        Fill the comments textarea with provided text.
        If text is empty string, clears the textarea.

        Args:
            text: Comment text to fill (supports multiline, unicode, special chars)
        """
        textarea = self.page.get_by_role("textbox", name="Any relevant information that")
        textarea.fill(text)

    def click_proceed(self):
        """
        Click the 'Proceed to Payment' button.
        Uses force=True to handle potential disabled state bypass.
        """
        self.page.get_by_role("button", name="Proceed to Payment").click(force=True)

    def get_upload_status(self, dropzone_id):
        """
        Get the current upload status for a specific dropzone.

        Args:
            dropzone_id: The Dropzone element ID (e.g., 'noc', 'land_certificate')

        Returns:
            dict with keys: fileCount, status, hasError, hasSuccess, errorMessage
        """
        return self.page.evaluate(f"""
            () => {{
                const dz = Dropzone.instances.find(d => d.element.id === '{dropzone_id}');
                if (!dz) return {{error: 'Dropzone not found', fileCount: 0}};
                const files = dz.files || [];
                const lastFile = files[files.length - 1];
                const errorEl = dz.element.querySelector('.dz-error-message');
                return {{
                    fileCount: files.length,
                    status: lastFile ? lastFile.status : 'empty',
                    accepted: lastFile ? lastFile.accepted : null,
                    hasError: !!dz.element.querySelector('.dz-error'),
                    hasSuccess: !!dz.element.querySelector('.dz-success'),
                    errorMessage: errorEl ? errorEl.textContent.trim() : ''
                }};
            }}
        """)
