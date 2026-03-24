# Intermediate Data Schemas

These schemas define the CSV formats passed between pipeline phases. Following them ensures each phase's output is compatible with the next phase's input.

---

## Bank Extraction CSV (Phase 1 output → Phase 2 input)

Filename: `bank_transactions_fy[YEAR].csv`

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `month` | string | yes | Year-month label, e.g. `2024-02` |
| `date` | string | yes | Transaction date as `YYYY-MM-DD`. Empty for OPENING/CLOSING rows. |
| `description` | string | yes | Bank statement description, verbatim. Multi-line descriptions joined with ` \| `. |
| `credit` | decimal | yes | Inflow amount (money in). `0.00` if none. |
| `debit` | decimal | yes | Outflow amount (money out). `0.00` if none. |
| `balance` | decimal | yes | Running balance after this transaction. |
| `type` | string | yes | One of: `TXN` (normal transaction), `OPENING` (month opening balance), `CLOSING` (month closing balance). |

Notes:
- One row per transaction. Opening and closing balance rows have empty `date` and zero credit/debit.
- Amounts are always positive. Direction is indicated by which column (credit vs debit) is non-zero.
- Description should preserve the original bank text — don't clean or abbreviate at this stage.

---

## Classified Transactions CSV (Phase 2 output → Phase 3 input)

Filename: `classified_transactions.csv` or `all_classified_fy[YEAR].csv`

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `month` | string | yes | Year-month label |
| `date` | string | yes | Transaction date as `YYYY-MM-DD` |
| `description` | string | yes | Bank statement description (verbatim from extraction) |
| `credit` | decimal | yes | Inflow amount |
| `debit` | decimal | yes | Outflow amount |
| `balance` | decimal | yes | Running balance |
| `account_code` | integer | yes | COA account code (e.g. `4000`, `5200`, `2900`) |
| `account_name` | string | yes | Human-readable account name (e.g. `Service Revenue`, `Rental Expense`) |
| `classification_method` | string | no | How it was classified: `rule`, `pattern`, `cross-ref`, `manual`, `suspense` |
| `notes` | string | no | Any notes — especially for suspense items (what it looks like, what's needed to resolve) |

Notes:
- OPENING and CLOSING rows from extraction are excluded — only TXN rows appear here.
- Every row must have an `account_code`. Unresolved items use `2900` (Suspense).
- The `notes` column is mandatory for suspense items — it feeds into the Queries & Notes sheet.

---

## Invoice Register (Phase 1 extraction → Phase 2 matching)

Filename: `invoices_fy[YEAR].csv`

Only created when sales invoices are provided. If no invoices, skip this schema.

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `invoice_no` | string | yes | Invoice number |
| `date` | string | yes | Invoice date as `YYYY-MM-DD` |
| `customer_name` | string | yes | Customer / debtor name |
| `description` | string | no | Line item description or summary |
| `amount` | decimal | yes | Total invoice amount (inclusive of SST if applicable) |
| `sst_amount` | decimal | no | SST component (if SST-registered) |
| `status` | string | yes | `matched` (payment found in bank), `outstanding` (unpaid at FY end), `partial` |
| `matched_bank_date` | string | no | Date of matching bank receipt, if matched |
| `matched_bank_amount` | decimal | no | Amount received against this invoice |

---

## Bill Register (Phase 1 extraction → Phase 2 matching)

Filename: `bills_fy[YEAR].csv`

Only created when purchase bills/invoices are provided.

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `bill_no` | string | yes | Bill / supplier invoice number |
| `date` | string | yes | Bill date as `YYYY-MM-DD` |
| `vendor_name` | string | yes | Vendor / supplier name |
| `description` | string | no | Description of goods/services |
| `amount` | decimal | yes | Total bill amount |
| `account_code` | integer | no | Expense account code (if known from classification) |
| `status` | string | yes | `matched` (payment found in bank), `outstanding` (unpaid at FY end), `partial` |
| `matched_bank_date` | string | no | Date of matching bank payment |
| `matched_bank_amount` | decimal | no | Amount paid against this bill |

---

## Accrual Adjustments Schedule (Phase 2 output → Phase 3 input)

Filename: `accrual_adjustments_fy[YEAR].csv`

Captures all accrual entries identified during reconciliation.

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `type` | string | yes | `receivable`, `payable`, `prepayment`, `accrual`, `unearned_revenue` |
| `date` | string | yes | Date of the underlying event (invoice date, bill date, or FY end date for estimates) |
| `counterparty` | string | no | Customer/vendor name if applicable |
| `description` | string | yes | What this adjustment represents |
| `amount` | decimal | yes | Amount of the adjustment |
| `dr_account` | integer | yes | Debit account code |
| `cr_account` | integer | yes | Credit account code |
| `basis` | string | yes | `invoice_match`, `bill_match`, `client_estimate`, `pattern_based`, `interview` — how this figure was determined |
| `document_ref` | string | no | Reference to source document (invoice number, bill number) if available |

---

## Mid-Pipeline Input Requirements

If the user provides their own pre-extracted or pre-classified CSV, it may not match the schemas above exactly. Before proceeding:

1. Read the column headers. Map them to the expected schema.
2. **Minimum required columns for classification (Phase 2 entry):** date, description, and either a single amount column (with +/- sign or a direction indicator) or separate credit/debit columns.
3. **Minimum required columns for journal entries (Phase 3 entry):** everything in the classified CSV schema — date, description, credit, debit, account_code.
4. If columns are missing or ambiguous, ask the user to clarify before proceeding.
