# Payment Gateway Module — Complete Analysis Report

---

# 1. MODULE OVERVIEW

The Payment Gateway module handles the financial transaction flow that occurs after the Upload Documents step is completed. It involves cross-domain navigation through an external payment gateway (Razorpay/similar), bank selection, QR code generation, and payment confirmation.

**This regression suite verifies ONLY that each payment gateway is accessible and functional — it does NOT complete actual payments.**

---

# 2. NAVIGATION FLOW

```
┌────────────────────────────────────┐
│ Upload Documents Page              │
│ [Proceed to Payment] clicked       │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│ Payment Summary Page               │
│ URL: /preliminary/school/payment-  │
│      gateway                       │
│                                    │
│ [Pay ₹10000.00] button             │
└──────────────┬─────────────────────┘
               │ click
               ▼
┌────────────────────────────────────┐
│ Payment Details Page               │
│ Heading: "Payment Details"         │
│                                    │
│ Bank Selection:                    │
│   ○ HDFC Collect Now (img)         │
│   ○ ICICI Bank (img)              │
│   ○ Federal Bank (img)            │
│                                    │
│ [Proceed to Pay Rs. 10000.00]      │
│ (button, initially disabled)       │
└──────────────┬─────────────────────┘
               │ click (after bank selection + JS enable)
               ▼
┌────────────────────────────────────┐
│ External Payment Gateway           │
│ (IFRAME — cross-domain)            │
│                                    │
│ Bank-specific payment page         │
│                                    │
│ [Show QR] button                   │
└──────────────┬─────────────────────┘
               │ click
               ▼
┌────────────────────────────────────┐
│ QR Code / Final Payment            │
│ (still in IFRAME)                  │
│                                    │
│ [Continue] or [Pay] button         │
│ (test-id: "fee-bearer-cta")        │
└──────────────┬─────────────────────┘
               │ click
               ▼
┌────────────────────────────────────┐
│ Bank Payment Page                  │
│ (external redirect OR QR scan)     │
│                                    │
│ ← STOP HERE — Do NOT complete      │
│    actual payment                  │
└────────────────────────────────────┘
```

---

# 3. PAGE OBJECTS & LOCATORS (From E2E Evidence)

## 3.1 Payment Summary Page

| Element | Locator | Type |
|---------|---------|------|
| Page URL | `**/payment**` or `/preliminary/school/payment-gateway` | URL |
| Pay button | `get_by_role("button", name="Pay ₹")` | Button |

## 3.2 Payment Details Page

| Element | Locator | Type |
|---------|---------|------|
| Heading | `get_by_role("heading", name="Payment Details")` | Heading |
| HDFC Collect Now | `get_by_role("img", name="HDFC Collect Now")` | Image (clickable) |
| ICICI Bank | `get_by_role("img", name="ICICI Bank")` | Image (clickable) |
| Federal Bank | `get_by_role("img", name="Federal Bank")` | Image (clickable) |
| Pay button | `#pay-button` | Button (initially disabled) |
| Hidden radio inputs | `input[type="radio"]` inside bank label/div | Hidden |

## 3.3 External Payment Gateway (IFRAME)

| Element | Locator | Type |
|---------|---------|------|
| Iframe | `page.locator("iframe").content_frame` | Iframe |
| Show QR button | `iframe.get_by_role("button", name="Show QR")` | Button (inside iframe) |
| Continue/Pay button | `iframe.get_by_test_id("fee-bearer-cta")` | Button (inside iframe) |

---

# 4. CROSS-DOMAIN BEHAVIOUR

| Step | Domain | Behaviour |
|------|--------|-----------|
| 1. Payment Summary | `dev-eaffiliation.cisce.org` | Same domain |
| 2. Payment Details | `dev-eaffiliation.cisce.org` | Same domain |
| 3. Bank selection + Proceed | `dev-eaffiliation.cisce.org` → external | Redirect to payment gateway |
| 4. Payment gateway | External (e.g., `api.razorpay.com` or similar) | Loaded in IFRAME |
| 5. Show QR / Pay | External iframe | Still in iframe |
| 6. Final bank page | External redirect | May leave iframe |

**Key insight:** The payment gateway loads in an IFRAME, not a new tab. All interactions within the gateway use `page.locator("iframe").content_frame`.

---

# 5. BANK SELECTION MECHANISM

The E2E reveals that bank selection is **non-trivial**:

1. Click the bank image → visually selects
2. But the `#pay-button` remains **disabled**
3. Must use JavaScript to:
   - Find the radio input inside the bank's parent element
   - Set `radio.checked = true` + dispatch events
   - Force-enable `#pay-button` by removing `disabled` attribute
   - Call `initiatePayment()` as backup

**This is the same pattern for ALL 3 banks** — only the image `alt` attribute differs.

---

# 6. AUTOMATION RISKS

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| 1 | Iframe cross-domain restrictions | High | Use `content_frame` property (Playwright handles) |
| 2 | `#pay-button` disabled — requires JS injection | High | Reuse E2E pattern (force-enable + click) |
| 3 | External gateway may timeout | Medium | Generous timeouts (30s+) |
| 4 | Gateway page may change without notice | Medium | Keep assertions minimal (existence, not content) |
| 5 | `initiatePayment()` function may not exist | Low | Try/catch approach (E2E pattern) |
| 6 | QR code generation may take time | Medium | Wait 5000ms before Show QR |
| 7 | Bank-specific redirect URLs may vary | Low | Only verify page loads, not specific URL |
| 8 | Payment amount may change | Low | Use partial match for "Pay ₹" |

---

# 7. POTENTIAL APPLICATION DEFECTS

| # | Defect | Evidence |
|---|--------|----------|
| 1 | Pay button disabled after bank selection (requires JS workaround) | E2E uses force-enable |
| 2 | Bank radio inputs hidden (not programmatically selectable via click) | E2E uses JS injection |
| 3 | No visual feedback that bank is selected (relies on hidden radio) | UX issue |

---

# 8. RECOMMENDED AUTOMATION APPROACH

For each bank (HDFC, ICICI, Federal):
1. Navigate to Payment Summary page (via Upload Documents fixture or direct URL)
2. Click "Pay ₹" button
3. Verify "Payment Details" heading
4. Click bank image
5. JS: Find radio, check it, dispatch events
6. JS: Force-enable `#pay-button`, click it
7. JS: Call `initiatePayment()` as backup
8. Wait for iframe to load
9. Switch to iframe: `page.locator("iframe").content_frame`
10. Click "Show QR" button
11. Click "fee-bearer-cta" (Continue/Pay)
12. Verify bank payment page is reached (iframe content changed OR new page loaded)
13. **STOP** — do not complete payment

---

**STATUS:** Analysis complete. Ready for diagnostics.
