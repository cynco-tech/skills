# Accrual Reconciliation Procedures

Bank statements are cash basis. The accounts must be accrual basis. This reference defines how to bridge the gap — matching cash movements to their underlying economic events, and recognising revenue/expenses in the correct period.

---

## The Core Problem

A bank statement tells you *when cash moved*. Accrual accounting requires you to know *when the economic event occurred*. These often differ:

- Invoice issued 15 Dec, customer pays 10 Jan → revenue belongs in Dec (accrual), cash arrives in Jan.
- Supplier bill dated 20 Dec, paid 5 Jan → expense belongs in Dec, cash leaves in Jan.
- Rent paid 1 Dec for Dec-Feb → 1/3 is Dec expense, 2/3 is prepayment.
- Audit fee for FY2024, invoice received March 2025 → accrue in FY2024.

The reconciliation process identifies these timing differences and creates the journal entries to shift from cash basis to accrual basis.

---

## Document Availability Tiers

Not every client provides the same level of documentation. The approach adapts:

### Tier 1: Full Documents Available
Sales invoices, purchase bills, receipts, delivery orders, contracts.

**Approach:** Invoice-level matching. Precise receivables and payables. Highest confidence.

1. Build an invoice register (all sales invoices issued during the FY).
2. Build a bill register (all purchase bills received during the FY).
3. Match bank receipts to invoices. Match bank payments to bills.
4. Unmatched invoices at year-end = Trade Receivables (1100).
5. Unmatched bills at year-end = Trade Payables (2000).
6. Review for prepayments and accruals (see sections below).

### Tier 2: Partial Documents
Some invoices/bills available, but not a complete set.

**Approach:** Match what you can. Fill gaps with smart questioning.

1. Match available invoices/bills to bank transactions.
2. For unmatched bank transactions, classify from description/pattern (same as cash-only approach).
3. Use AskUserQuestion to fill critical gaps:
   - "At year-end [date], did you have any outstanding invoices that customers hadn't paid yet? Approximate total?"
   - "Were there any supplier bills you hadn't paid by year-end? Who were the main ones?"
   - "Had you paid for anything in advance that covers the next financial year? (rent, insurance, subscriptions)"
4. Book accrual entries based on responses. Document the basis clearly.
5. Flag: "Receivables/payables based on [matched invoices / client-provided estimates]. Not all source documents independently verified."

### Tier 3: Bank Statements Only
No invoices, no bills, no receipts. Cash data is all you have.

**Approach:** Cash-basis extraction as foundation. Year-end accrual adjustments via interview. This is the minimum viable approach.

1. Classify all bank transactions per Phase 2 rules. This gives a cash-basis P&L.
2. At year-end, conduct an accrual adjustment interview via AskUserQuestion:
   - **Receivables**: "Were there any amounts owed to you by customers at [FY end date] that hadn't been paid yet?"
   - **Payables**: "Were there any amounts you owed to suppliers at [FY end date] that you hadn't paid yet?"
   - **Prepayments**: "Did you make any payments before [FY end date] that cover services after that date? (e.g., rent, insurance, subscriptions)"
   - **Accrued expenses**: "Were there any expenses you'd incurred by [FY end date] but hadn't received a bill for yet? (e.g., utilities, audit fee, bonuses)"
   - **Unearned revenue**: "Did you receive any payments from customers before [FY end date] for services you hadn't delivered yet?"
3. Book accrual entries based on responses.
4. Flag prominently in Queries & Notes and in the financial statement notes: "Financial statements prepared from bank statements and client-provided information. Accrual adjustments based on management representations, not independently verified against source documents."

---

## Matching Procedures

### Sales: Bank Receipts ↔ Invoices

For each bank receipt (credit/inflow):
1. Match by amount + customer name. Exact match = confirmed.
2. If multiple invoices exist for one customer, match by date proximity (invoice closest to but before receipt date).
3. Partial payments: if receipt < invoice amount, allocate to oldest invoice first (FIFO). Remaining invoice balance stays in receivables.
4. Overpayments: if receipt > invoice total, the excess may be advance payment (unearned revenue 2200) or deposit — ask.
5. Receipts with no matching invoice: likely cash sales (no invoice issued) or a missing invoice. If the client is expected to issue invoices for all sales, flag it.

At year-end:
- Open invoices (issued but no matching receipt) = **Trade Receivables (1100)**
- Book: DR 1100 Trade Receivables / CR 4000 Revenue (if not already booked via bank)

### Purchases: Bank Payments ↔ Bills

For each bank payment (debit/outflow):
1. Match by amount + vendor name.
2. Partial payments: allocate to oldest bill.
3. Payments with no matching bill: likely cash purchases or missing bill. Classify from bank description. Flag if material.

At year-end:
- Open bills (received but no matching payment) = **Trade Payables (2000)**
- Book: DR 5xxx Expense (per nature) / CR 2000 Trade Payables

### Timing Differences: Which Period?

The key question: does this transaction belong in the current FY or the next?

| Situation | Current FY Treatment |
|-----------|---------------------|
| Invoice issued Dec, paid Jan | Revenue in Dec (DR Receivables / CR Revenue). Cash receipt in Jan settles receivable. |
| Bill received Dec, paid Jan | Expense in Dec (DR Expense / CR Payables). Cash payment in Jan settles payable. |
| Rent paid Dec for Dec–Feb | 1/3 expense, 2/3 prepayment (DR Prepaid 1200 / CR Bank). Release monthly. |
| Insurance paid Oct for 12 months | Pro-rate: months in current FY = expense, remainder = prepayment. |
| Audit fee for current FY, bill not yet received | Accrue estimate (DR 5520 Audit Fee / CR 2200 Accrued Expenses). |
| Deposit received for future event | Unearned revenue (DR Bank / CR 2250 Unearned Revenue). Recognise when event occurs. |

---

## Prepayments — Identification Checklist

Scan for these common prepayments at year-end:
- **Rent**: paid monthly/quarterly in advance? Check if the last payment covers the next period.
- **Insurance**: annual premium — pro-rate based on policy period vs FY.
- **Software subscriptions**: annual plans (e.g., accounting software, Microsoft 365) — pro-rate.
- **Road tax / vehicle insurance**: annual, pro-rate.
- **Deposits**: rental deposits, utility deposits — these are assets (1200), not expenses.

### Journal Entry Pattern
```
DR 1200 Prepaid Expenses           [future portion]
DR 5xxx Relevant Expense           [current FY portion]
  CR 1000 Bank                     [total amount paid]
```

---

## Accruals — Identification Checklist

Scan for these common accruals at year-end:
- **Salary**: last month salary if paid in the following month.
- **EPF/SOCSO/EIS**: statutory contributions for the last month.
- **Utilities**: last month's bill if not yet received/paid.
- **Audit fee**: if the client is audited, accrue the audit fee.
- **Bonus**: if approved/committed but not yet paid.
- **Interest**: on loans/HP, accrued daily.
- **Rent**: if paying in arrears.

### Journal Entry Pattern
```
DR 5xxx Relevant Expense           [amount incurred]
  CR 2200 Accrued Expenses         [amount unpaid]
```

---

## Revenue Recognition Principles

Revenue is recognised when the performance obligation is satisfied — not when cash is received.

| Revenue Type | Recognition Point | Common Entity Types |
|-------------|-------------------|-------------------|
| Service revenue (one-off) | When service is delivered / completed | All |
| Service revenue (ongoing/retainer) | Over the service period (straight-line or milestone) | Sdn Bhd, Berhad |
| Product sales | When goods are delivered and control transfers | Trading entities |
| Subscription / membership fees | Over the subscription period | NGO, Sdn Bhd |
| Event revenue | When the event takes place | All |
| Rental income | Over the rental period (straight-line) | All |
| Donations / grants (NGO) | When conditions are met, or immediately if unconditional | NGO |
| Government grants | Per MPERS S24 / MFRS 120 — depends on conditions | Sdn Bhd, Berhad, NGO |

For NGOs: distinguish between **restricted funds** (donor-imposed conditions on use) and **unrestricted funds** (available for general purposes). Restricted fund income is recognised only when the restriction is met.

---

## Reconciliation Output

At the end of Phase 2, you should have:
1. **Classified bank transactions** (all transactions mapped to COA codes)
2. **Invoice matching schedule** (if invoices were available) — showing matched and unmatched
3. **Receivables schedule** — open invoices at year-end
4. **Payables schedule** — open bills at year-end
5. **Prepayments schedule** — with pro-ration calculations
6. **Accruals schedule** — with basis for each estimate
7. **Suspense items** — unresolvable items with queries
8. **Document coverage flag** — Tier 1, 2, or 3, noted in engagement README and financial statement notes
