# Payment Gateway — Optimized Implementation Plan
## Based on 3-Test Approved Matrix

---

# SCOPE

Implement 3 regression tests — one per payment gateway (HDFC, ICICI, Federal) — verifying each bank's payment flow is accessible up to the bank payment page WITHOUT completing the actual transaction.

---

# CURRENT STATE

| Item | Status |
|------|--------|
| `pages/upload_documents_page.py` — payment flow in E2E | ✅ Exists (READ-ONLY — proven pattern) |
| Payment page object | ❌ Does NOT exist (to create) |
| Payment regression tests | ❌ Do NOT exist (to create) |
| Payment fixture | ❌ Does NOT exist (to create) |
| `pytest.ini` — `payment_gateway` marker | ❌ Does NOT exist (to register) |

---

# PHASE 1 — FRAMEWORK SETUP

## Files to Create

| # | File | Purpose |
|---|------|---------|
| 1 | `pages/payment_gateway_page.py` | Payment Gateway page object |
| 2 | `tests/regression/payment_gateway/__init__.py` | Package root |
| 3 | `tests/regression/payment_gateway/test_payment_gateway.py` | 3 parametrized tests |

## Files to Extend

| # | File | Change |
|---|------|--------|
| 1 | `conftest.py` | Add `payment_ready_page` fixture |
| 2 | `pytest.ini` | Register `payment_gateway` marker |

## New Page Object: `payment_gateway_page.py`

```python
class PaymentGatewayPage:
    def __init__(self, page):
        self.page = page

    def click_pay_button(self):
        """Click the 'Pay ₹' button on Payment Summary page."""

    def verify_payment_details_page(self):
        """Assert 'Payment Details' heading is visible."""

    def select_bank(self, bank_alt_text):
        """Click bank image + JS injection to select radio + enable button."""

    def click_proceed_to_pay(self):
        """Force-enable #pay-button, click, call initiatePayment()."""

    def click_show_qr(self):
        """Switch to iframe, click 'Show QR' button."""

    def click_continue_pay(self):
        """Click fee-bearer-cta inside iframe."""

    def verify_bank_page_reached(self):
        """Verify the bank payment page loaded (iframe content changed)."""
```

**Total methods: 7**

## New Fixture: `payment_ready_page`

| Fixture | Scope | Depends On | Logic |
|---------|-------|-----------|-------|
| `payment_ready_page` | function | `upload_ready_page` | Upload all 5 docs → select affiliation → check declarations → click Proceed → wait for payment URL → return page |

**Alternative approach:** Navigate directly to payment URL if the account already has complete data (faster, avoids re-uploading).

## Marker

```ini
payment_gateway: Payment Gateway module tests
```

---

# PHASE 2 — TEST IMPLEMENTATION

## Test File: `tests/regression/payment_gateway/test_payment_gateway.py`

### Architecture: Parametrized with 3 bank scenarios

```python
BANK_SCENARIOS = [
    {"scenario_id": "PAYMENT_POS_001", "bank_name": "HDFC Collect Now", "bank_alt": "HDFC"},
    {"scenario_id": "PAYMENT_POS_002", "bank_name": "ICICI Bank", "bank_alt": "ICICI"},
    {"scenario_id": "PAYMENT_POS_003", "bank_name": "Federal Bank", "bank_alt": "Federal"},
]

@pytest.mark.parametrize("scenario", BANK_SCENARIOS, ids=lambda s: s["scenario_id"])
def test_payment_gateway_flow(payment_ready_page, scenario):
    # Step 1: Click Pay ₹
    # Step 2: Verify Payment Details
    # Step 3: Select bank
    # Step 4: Proceed to Pay (JS injection)
    # Step 5: Wait for iframe
    # Step 6: Show QR
    # Step 7: Continue/Pay
    # Step 8: Verify bank page — STOP
```

**No Excel sheet needed** — only 3 hardcoded scenarios (same pattern as validation tests).

---

# PHASE 3 — VERIFICATION

| # | Action | Expected |
|---|--------|----------|
| 1 | `python -m pytest tests/regression/payment_gateway/ --collect-only -q` | 3 tests collected |
| 2 | `python -m pytest tests/test_preliminary_form_main.py --collect-only -q` | 1 test (E2E unchanged) |
| 3 | `python -m pytest tests/regression/upload_documents/ --collect-only -q` | 28 tests (unchanged) |
| 4 | Run headed: `python -m pytest tests/regression/payment_gateway/ -v --headed` | Execute + verify |

---

# IMPLEMENTATION DETAILS

## Existing Methods Reused

| Method | From | Used For |
|--------|------|----------|
| `upload_all_documents(file_path)` | upload_documents_page.py | Fixture setup |
| `select_affiliation_type(label)` | upload_documents_page.py | Fixture setup |
| `check_declarations()` | upload_documents_page.py | Fixture setup |
| `click_proceed()` | upload_documents_page.py | Navigate to payment |
| `ScreenshotUtil.take_screenshot()` | utils/screenshot_util.py | Failure capture |

## Existing Methods Left Untouched

| Method | Status |
|--------|--------|
| `upload_documents(data)` | 🔒 E2E — LOCKED |
| All Upload Documents regression methods | 🔒 Unchanged |
| All Land Certificate regression methods | 🔒 Unchanged |
| All other page objects | 🔒 Unchanged |

---

# ESTIMATED EFFORT

| Phase | Task | Effort |
|-------|------|--------|
| 1 | Page object + fixture + folder | 1.5 hrs |
| 2 | Test implementation (3 tests) | 2 hrs |
| 3 | Verification + debugging | 1 hr |
| **TOTAL** | | **~4.5 hrs** |

---

# EXPECTED EXECUTION TIME

| Suite | Tests | Time |
|-------|-------|------|
| Payment Gateway (full) | 3 | ~5–8 min |
| Payment Gateway (single bank) | 1 | ~2–3 min |

**Note:** Each test involves uploading 5 documents + navigating to payment — the fixture setup takes most of the time. If account already has uploads, fixture can skip re-upload.

---

# RISKS

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| 1 | Fixture requires full upload (slow) | Medium | Check if uploads already exist, skip if so |
| 2 | External gateway may be down | High | Add generous timeouts + screenshot on failure |
| 3 | HDFC/Federal alt text may differ from expectation | Medium | Verify on first headed run |
| 4 | Iframe may not load in headless mode | Medium | Test in headed mode first |
| 5 | fee-bearer-cta may not exist for all banks | Medium | Add try/catch with diagnostic |

---

# BACKWARD COMPATIBILITY

| Check | Guaranteed |
|-------|-----------|
| `test_preliminary_form_main.py` unchanged | ✅ |
| `upload_documents(data)` unchanged | ✅ |
| Upload Documents regression tests unchanged | ✅ |
| Certificate of Land tests unchanged | ✅ |
| All other modules unchanged | ✅ |
| All existing fixtures unchanged | ✅ |
| All existing page objects unchanged | ✅ |

**✅ 100% backward compatible — completely independent module.**

---

# FINAL SUMMARY

| Metric | Value |
|--------|-------|
| **Total tests** | 3 |
| **Files to create** | 3 |
| **Files to extend** | 2 |
| **New page methods** | 7 |
| **Existing methods reused** | 5 |
| **Excel sheets needed** | 0 (hardcoded scenarios) |
| **Estimated effort** | ~4.5 hours |
| **Execution time** | ~5–8 min |
| **E2E impact** | Zero |

---

**STATUS:** Implementation plan complete. Ready for phased execution.
