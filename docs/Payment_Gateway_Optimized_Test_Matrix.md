# Payment Gateway — Optimized Regression Test Matrix
## Minimal Suite: 3 Tests (Management-Approved)

---

# DESIGN PRINCIPLES

1. **One test per payment gateway** — verifies each bank is functional
2. **Stop before actual payment** — no financial transaction executed
3. **Same flow pattern** for all 3 — only bank selection differs
4. **Verify end-to-end reachability** — from Pay button to bank payment page

---

# OPTIMIZED TEST MATRIX

| TC ID | Bank | Scenario | Priority | Expected Result |
|-------|------|----------|----------|-----------------|
| PAYMENT_POS_001 | HDFC Collect Now | Verify complete payment gateway flow for HDFC — Payment Summary → Pay ₹ → Select HDFC → Proceed → Show QR → Continue → Bank page reached | Critical | User reaches HDFC bank payment page without error |
| PAYMENT_POS_002 | ICICI Bank | Verify complete payment gateway flow for ICICI — Payment Summary → Pay ₹ → Select ICICI → Proceed → Show QR → Pay → Bank page reached | Critical | User reaches ICICI bank payment page without error |
| PAYMENT_POS_003 | Federal Bank | Verify complete payment gateway flow for Federal — Payment Summary → Pay ₹ → Select Federal → Proceed → Show QR → Pay → Bank page reached | Critical | User reaches Federal bank payment page without error |

---

# TEST STEPS (Common to all 3)

Each test verifies the following steps in sequence:

| Step | Action | Assertion |
|------|--------|-----------|
| 1 | Payment Summary page is displayed | URL contains `/payment` |
| 2 | Click "Pay ₹10000.00" button | Payment Details heading visible |
| 3 | Select bank (click image) | Bank image clickable |
| 4 | JS: Enable Proceed button + click | Gateway starts loading |
| 5 | Wait for iframe to load | Iframe element present |
| 6 | Click "Show QR" (inside iframe) | QR section appears |
| 7 | Click "Continue"/"Pay" (fee-bearer-cta) | Bank payment page reached |
| 8 | **STOP** — verify page is accessible | No error, page loaded |

---

# TOTAL: 3 TESTS

| Category | Count |
|----------|-------|
| Positive (Gateway Validation) | 3 |
| **TOTAL** | **3** |

---

# SANITY SUITE

All 3 tests are sanity-critical (each verifies a payment gateway works).

| Sanity ID | TC ID | Why |
|-----------|-------|-----|
| S01 | PAYMENT_POS_001 | HDFC gateway accessible |
| S02 | PAYMENT_POS_002 | ICICI gateway accessible |
| S03 | PAYMENT_POS_003 | Federal gateway accessible |

---

# REGRESSION SUITE

| R-ID | TC ID | Bank |
|------|-------|------|
| R01 | PAYMENT_POS_001 | HDFC Collect Now |
| R02 | PAYMENT_POS_002 | ICICI Bank |
| R03 | PAYMENT_POS_003 | Federal Bank |

---

# EXCLUDED SCENARIOS (Not in scope)

| Scenario | Reason |
|----------|--------|
| Actual payment completion | Management directive — stop before payment |
| Payment success verification | Requires real transaction |
| Payment failure handling | Requires failed transaction |
| Refund flow | Separate module |
| Timeout/retry scenarios | Environment-specific |
| Multiple payment attempts | Edge case |
| Payment amount validation | Static value — verified visually |
| Cancel payment flow | Not in management requirement |

---

# RISK ASSESSMENT

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| 1 | External gateway unavailable (maintenance) | High | Retry logic + graceful failure |
| 2 | Iframe loading timeout | Medium | 30s timeout + screenshot on failure |
| 3 | Bank-specific image alt text differs | Medium | Verify during first run |
| 4 | fee-bearer-cta may not exist for all banks | Medium | Try/catch with diagnostic |
| 5 | Gateway may require CAPTCHA | Low | Document as blocker if found |

---

**STATUS:** Test matrix approved. 3 tests — one per bank. Ready for implementation planning.
