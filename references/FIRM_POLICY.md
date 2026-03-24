# Firm Policy & Accounting Standards

> **Placeholders:** `[FIRM_NAME]`, `[CA_REGISTRATION]`, `[FIRM_EMAIL]` below should have been replaced during installation. If they still show as placeholders, ask the user what to use for report branding. See SKILL.md Conventions for details.

## Firm Identity

- **Firm**: [FIRM_NAME]
- **Registration**: [CA_REGISTRATION]
- **Services**: Accounting, Tax, Advisory
- **Contact**: [FIRM_EMAIL]

---

## CORE PRINCIPLES

1. **Accuracy above speed.** Never fabricate, estimate, or hallucinate data. Every number must trace to a source document or an explicit decision by the user.
2. **Check first, ask second.** Before asking any question, exhaust what you can verify from the documents provided. Only ask when something is genuinely missing, ambiguous, or contradictory.
3. **Standards compliance is non-negotiable.** All work must comply with the applicable Malaysian accounting framework and LHDN requirements. No shortcuts.
4. **Consistency across engagements.** Every client gets the same rigorous process, same report format, same quality. The workflow does not change based on who runs it.
5. **Document everything.** Every decision, assumption, classification, and query must be logged in the working papers. If it's not documented, it didn't happen.

---

## APPLICABLE FRAMEWORKS

### By Entity Type

| Entity Type | Accounting Framework | Tax Filing | Basis |
|---|---|---|---|
| Sole Proprietor | Accrual basis per S21A ITA 1967 | Form B | Accrual |
| Partnership | Accrual basis per S21A ITA 1967 | Form P + individual Form B/BE | Accrual |
| Sdn Bhd (Private Limited) | MPERS (Malaysian Private Entities Reporting Standards) | Form C | Accrual |
| Berhad (Public Limited) | MFRS (Malaysian Financial Reporting Standards) | Form C | Accrual |
| NGO — Society | MPERS or Societies Act 1966 reporting | Form C (may be exempt under S44(6)) | Accrual |
| NGO — Foundation | MPERS | Form C (may be exempt under S44(6)) | Accrual |
| NGO — Cooperative | Co-operative Societies Act 1993 + MPERS | Form C | Accrual |

### Key Standards References
- **MPERS**: Sections 1-35 (particularly S2 Concepts, S4 Financial Position, S5 Comprehensive Income, S17 PPE, S20 Leases, S23 Revenue, S29 Income Tax). Applies to Sdn Bhd, NGOs (foundations, societies unless regulated otherwise).
- **MFRS**: Full Malaysian Financial Reporting Standards (converged with IFRS). Applies to Berhad and entities required to apply MFRS. Key differences from MPERS: MFRS 15 Revenue from Contracts with Customers (5-step model), MFRS 16 Leases (right-of-use), MFRS 9 Financial Instruments, MFRS 133 Earnings Per Share.
- **ITA 1967**: Income Tax Act 1967 (Malaysia)
- **S21A ITA 1967**: Mandatory accrual basis for ALL entity types
- **Societies Act 1966**: Registered societies must prepare annual accounts showing true and fair view. Income & Expenditure Account + Balance Sheet. Annual return to ROS.
- **Co-operative Societies Act 1993**: Co-ops must maintain proper books per Act requirements. Subject to audit by Suruhanjaya Koperasi Malaysia (SKM) or approved auditor.

### Accrual Basis Enforcement
All entity types use accrual basis. Bank statements are inherently cash basis. You must reconcile cash data against invoices, bills, and receipts to produce accrual-basis financial statements. See `ACCRUAL_RECONCILIATION.md` for detailed procedures. When source documents are incomplete, use AskUserQuestion to fill gaps and flag limitations in the financial statement notes.
- **Schedule 3 ITA 1967**: Capital allowances rates
- **Income Tax (Deduction for Depreciation of Small Value Assets) Rules 2021**: Assets < RM2,000

### Malaysian Statutory Deductions (Employment)

| Item | Employer Rate | Employee Rate | Notes |
|---|---|---|---|
| EPF/KWSP | 13% (salary <= RM5,000) / 12% (salary > RM5,000) | 11% | Mandatory for Malaysian employees. Foreign workers: employer 5 sen only |
| SOCSO/PERKESO | 1.75% | 0.5% | Category 1 (< 60 years). Max insurable earnings RM6,000 |
| EIS/SIP | 0.2% | 0.2% | Max insurable earnings RM6,000 |
| PCB/MTD | Per LHDN Schedule | Employee bears | Monthly tax deduction |
| HRDF/PSMB | 1% | N/A | Only for employers with 10+ employees |

**Important**: Some employers absorb employee statutory contributions. You MUST check payslips to determine actual deduction structure. Do NOT assume standard deductions without verification.

---

## DEPRECIATION POLICY (DEFAULT RATES)

### Accounting Depreciation (Straight-Line)

| Asset Category | Useful Life | Annual Rate |
|---|---|---|
| Building | 50 years | 2% |
| Renovation & Improvements | 10 years | 10% |
| Office Equipment & Furniture | 10 years | 10% |
| Computer Equipment & Software | 3 years | 33.33% |
| Photography/Video Equipment | 5 years | 20% |
| Motor Vehicle | 5 years | 20% |
| Plant & Machinery | 10 years | 10% |
| Signage & Fixtures | 10 years | 10% |

### Tax Capital Allowances (Schedule 3 ITA 1967)

| Asset Category | Initial Allowance | Annual Allowance |
|---|---|---|
| Plant & Machinery (general) | 20% | 14% |
| Motor Vehicle (up to RM100k / RM200k if on-the-road) | 20% | 20% |
| Computer & IT Equipment | 20% | 20% (accelerated) |
| Office Equipment & Furniture | 20% | 10% |
| Small Value Assets (< RM2,000 each) | 100% | - |
| Building (industrial) | 10% | 3% |

**Note**: For first year, depreciation is pro-rated from date of acquisition. You MUST verify acquisition dates from source documents.

---

## STANDARD CHART OF ACCOUNTS

You uses the following base COA structure. It adapts based on entity type and client needs, but the numbering convention is fixed.

### Account Code Structure
```
1xxx - Assets
  1000-1099 : Cash & Bank
  1100-1199 : Trade Receivables
  1200-1299 : Other Receivables, Prepayments, Deposits
  1300-1399 : Property, Plant & Equipment (Cost)
  1390-1399 : Accumulated Depreciation
  1400-1499 : Intangible Assets
  1500-1599 : Inventory

2xxx - Liabilities
  2000-2099 : Trade Payables
  2100-2199 : Statutory Payables (EPF, SOCSO, EIS, PCB)
  2150      : Salary Payable / Accrued Payroll
  2200-2249 : Other Payables & Accruals
  2250      : Unearned Revenue
  2300-2399 : Loans & Borrowings (Current)
  2400-2499 : Hire Purchase (Current Portion)
  2500-2599 : Loans & Borrowings (Non-Current)
  2600-2699 : Hire Purchase (Non-Current)
  2700-2799 : Deferred Tax Liability
  2900      : Suspense Account

3xxx - Equity
  3000      : Share Capital (Sdn Bhd) / Capital Account (Sole Prop/Partnership)
  3100      : Capital Contribution / Additional Paid-in Capital
  3200      : Retained Earnings (Prior Years)
  3300      : Current Year Profit / (Loss)
  3400      : Drawings (Sole Prop/Partnership only)
  3500      : Partners' Current Account (Partnership only)

4xxx - Revenue
  4000      : Service Revenue (Primary)
  4100      : Service Revenue (Secondary)
  4200      : Other Income
  4300      : Interest Income
  4400      : Gain on Disposal of Assets
  4500      : Rental Income
  4900      : Exempt Income

5xxx - Cost of Sales & Expenses
  5050      : Cost of Goods Sold / Purchases (trading/manufacturing only)
  5055      : Opening Stock (trading/manufacturing only)
  5056      : Closing Stock (trading/manufacturing only, CR balance)
  5000      : Salary & Wages
  5010      : Allowances
  5020      : Commission
  5030      : Subcontractor / Freelancer Costs
  5035      : Director Remuneration
  5040      : Bonus
  5100      : EPF - Employer Contribution
  5110      : SOCSO - Employer Contribution
  5120      : EIS - Employer Contribution
  5130      : HRDF Levy
  5200      : Rental Expense
  5210      : Utilities
  5220      : Property Maintenance
  5300      : Depreciation - Equipment
  5310      : Depreciation - Computer
  5320      : Depreciation - Motor Vehicle
  5330      : Depreciation - Building / Renovation
  5400      : Software & Subscriptions
  5500      : Advertising & Marketing
  5510      : Professional & Membership Fees
  5520      : Legal & Audit Fees
  5530      : Secretarial Fees
  5600      : Insurance
  5700      : Office Supplies & Consumables
  5800      : Entertainment & Hospitality
  5900      : Transport & Travelling
  5910      : Motor Vehicle Expenses (Fuel, Toll, Parking)
  5920      : Courier & Postage
  5950      : Printing & Stationery
  5960      : Repairs & Maintenance
  5970      : Miscellaneous Expenses
  5980      : Bank Charges
  5990      : Interest Expense
  6000      : Bad Debts / Doubtful Debts
  6100      : Foreign Exchange Loss
  6200      : Penalties & Fines (Non-Deductible)
  6300      : Donation
  6400      : Zakat Perniagaan

9xxx - Tax
  9000      : Tax Expense (Current Year)
  9100      : Deferred Tax Expense / (Benefit)
```

### Entity-Specific Variations
- **Sole Proprietor**: Use 3000 as Capital Account, add 3400 Drawings. No Share Capital.
- **Partnership**: Use 3000 as Partners' Capital, add 3500 Partners' Current Account (one sub-account per partner). Track profit-sharing ratio.
- **Sdn Bhd**: Standard as above. 3000 = Share Capital (par value x shares).
- **Berhad (Public)**: 3000 = Share Capital. Add 3150 Share Premium, 3160 Other Reserves (revaluation, translation, hedging). Requires EPS disclosure. More extensive note disclosures (segment reporting if applicable, financial instruments per MFRS 7).
- **NGO — Society / Foundation**: Replace 3xxx Equity with: 3000 = Accumulated Fund (replaces Retained Earnings), 3100 = Restricted Fund (donor-imposed conditions), 3200 = Unrestricted Fund. Replace P&L with Income & Expenditure Account. Revenue accounts include: 4000 Membership Fees, 4100 Donations & Grants (Unrestricted), 4150 Donations & Grants (Restricted), 4200 Activity/Programme Income, 4300 Government Grants. Expense accounts include: 5050 Programme/Activity Expenses, 5060 Grant Disbursements.
- **NGO — Cooperative**: 3000 = Share Capital (member shares). Add 3050 Statutory Reserve (min 15% of net profit per Act), 3060 Members' Deposit. Revenue may include: 4000 Trading Revenue, 4100 Service Charges, 4200 Dividend Income. Must comply with SKM reporting requirements.

---

## MATERIALITY & ROUNDING

- **Materiality threshold**: RM100 for line items. Transactions below RM100 may be grouped unless individually significant.
- **Rounding**: All figures to 2 decimal places (sen). Final statements round to nearest RM (whole number) only if client requests.
- **Suspense tolerance**: RM0.00. Trial balance MUST balance to zero. No tolerance for imbalance.
- **Bank reconciliation tolerance**: RM0.00. Bank closing balance from GL must match bank statement exactly.

---

## REPORT FORMAT STANDARDS

### All Reports
- **Colour**: Black and white only. No colour.
- **Font**: Helvetica (PDF) / Arial (Excel)
- **Style**: Minimal, clean, professional. No unnecessary decoration.
- **Format**: PDF for final client-facing reports. Excel for working papers and detailed schedules.

### PDF Financial Statements (Client Deliverable)
Using reportlab (Python). Always include:
1. **Cover Page**: Client name, registration number, "Financial Statements", FY period, "Prepared by [FIRM_NAME] Chartered Accountants ([CA_REGISTRATION])"
2. **Table of Contents**: Page-numbered
3. **Statement of Comprehensive Income** (Profit & Loss)
4. **Statement of Financial Position** (Balance Sheet)
5. **Trial Balance**
6. **General Ledger**
7. **Notes & Queries** (if any open items exist)

Footer on every page (except cover): "[FIRM_NAME] Chartered Accountants ([CA_REGISTRATION])" left, "Page X" right.

### Excel Working Papers (Internal)
Always include these sheets:
1. Company Info
2. Chart of Accounts
3. Bank Transactions (with running balance)
4. Payroll Summary (if applicable)
5. Fixed Asset Register (if applicable)
6. Journal Entries
7. General Ledger
8. Trial Balance
9. Income Statement
10. Balance Sheet
11. Queries & Notes (if any)

---

## SUSPENSE ACCOUNT POLICY

When a bank transaction cannot be identified and no supporting document exists:

1. **Book to Account 2900 (Suspense Account)** — never guess.
2. **Flag for user** — add to internal notes: what the transaction looks like, possible classifications, and what document is needed to resolve it.
3. **Flag for client** — add to the Queries & Notes sheet with:
   - Transaction date
   - Amount
   - Bank description
   - Question: "Please advise the nature of this transaction and provide supporting documentation."
4. **Continue processing** — do not halt the entire engagement for one missing item. Park it and move on.
5. **Reconcile at end** — the Queries & Notes sheet serves as the client query list. All suspense items must be resolved before finalising.

---

## OPENING BALANCE POLICY

### First-Year Client (New Incorporation)
- Opening balances = zero (or share capital if Sdn Bhd)
- For companies converted from sole prop/partnership: opening = assets/liabilities transferred. You MUST ask for the transfer details if not provided.

### Existing Client (Prior Year Available)
You MUST follow this sequence:
1. **Scan for prior year files** — look for audit reports, management accounts, prior year workbooks, tax computations in the client folder.
2. **Extract closing balances** — from the most authoritative source: signed audit report > management accounts > prior year working papers.
3. **Check for auditor's adjustments (AJE)** — if an audit was done, the auditor may have passed adjusting entries. These MUST be incorporated. If audit report exists but AJEs are not separately provided, ASK the user to obtain the AJE list from the auditor.
4. **Verify opening = prior closing** — every opening balance must match the prior year's closing balance exactly. Any discrepancy must be flagged and explained.
5. **If prior year data is incomplete or missing** — ASK. Do not assume. The user must provide or obtain the opening balances.

### Prior Year Tax Computation
- Extract: capital allowances brought forward, unabsorbed losses, S108 balance.
- These carry forward into the current year's tax computation. Verify continuity.

---

## WORKFLOW REFERENCE

The detailed step-by-step workflow is in `WORKFLOW.md`. You MUST follow this workflow for every engagement. No steps may be skipped.

Summary of phases:
1. **PHASE 0**: Engagement Setup — scan folder, identify entity, identify FY, assess document completeness
2. **PHASE 1**: Document Ingestion — extract bank statements, invoices, payslips, fixed assets, prior year data
3. **PHASE 2**: Verification & Reconciliation — cross-reference, identify gaps, flag suspense items, ask questions
4. **PHASE 3**: Journal Entries — opening balances, bank transactions, payroll, depreciation, accruals, adjustments
5. **PHASE 4**: Financial Statements — TB, P&L, BS, GL, Cash Flow, management reports (optional)
6. **PHASE 5**: Tax Computation — adjustments, capital allowances, tax payable
7. **PHASE 6**: Quality Control — verification checklist, balance checks, notes, queries
8. **PHASE 7**: Output — generate Excel working papers + PDF financial statements

---

## COMMUNICATION STANDARDS

### To User (Internal / Technical Notes)
- Technical accounting language is acceptable
- Be specific: "Account 2110 EPF Payable shows DR balance of RM4,164. This means EPF was overpaid. Please verify against KWSP statement."
- When flagging issues, always provide: what's wrong, what you checked, what you need

### To Client (via Queries & Notes sheet)
- Plain English. No jargon.
- Concise. One question per item.
- Actionable: tell them exactly what document or information is needed.
- Format: numbered list with date, amount, and clear question.
- Example: "1. 15/06/2024 — RM3,800 payment to KENZ DIGITAL. Please provide the invoice or confirm the nature of this purchase (equipment/expense)."

### Notes to Financial Statements
- Only include notes that have material impact.
- Keep concise. No boilerplate filler.
- Standard notes: Basis of preparation, Significant accounting policies, Revenue recognition, PPE & depreciation, Related party transactions (if any), Contingent liabilities (if any), Events after reporting period (if any).

---

## EDGE CASES & SPECIAL HANDLING

### 1. Employer Absorbs Employee Statutory Contributions
Some employers pay both employer AND employee portions of SOCSO/EIS (not deducted from salary). You MUST check payslips:
- If net salary = gross salary (no deductions), employer is absorbing.
- Book: DR 5110/5120 (full amount), CR 2120/2130 (full amount). No employee deduction line.

### 2. Director Remuneration vs Salary
- Director payments may not follow standard payroll.
- If a person appears in bank statements receiving payments but is NOT on payslips, ask: "Is [name] a director or employee?"
- Directors: use 5035 (Director Remuneration). Not subject to SOCSO/EIS if not under contract of service.

### 3. Related Party Transactions
- Payments to/from entities with similar names (e.g., "AINAN WEDDING" payments for a company called "AINAN MEDIA") — flag as potential related party.
- You MUST disclose in notes if material.

### 4. Capital vs Revenue Expenditure
- Equipment purchases > RM2,000: capitalise as PPE (1300/1310/1320).
- Equipment < RM2,000: expense (per small value asset rules) OR capitalise — ask user for policy preference on first occurrence, then apply consistently.
- Renovation/fit-out: capitalise and depreciate over lease term or 10 years, whichever is shorter.

### 5. Mixed Personal & Business (Sole Prop)
- Common in sole proprietorships. You must ask if any bank transactions appear personal (e.g., grocery, personal insurance).
- Personal expenses paid from business account: DR 3400 Drawings, CR 1000 Bank.

### 6. GST/SST Considerations
- SST abolished 01/09/2018, reinstated as SST.
- Check if client is SST-registered (threshold: RM500k for taxable services).
- If SST-registered: separate SST payable (2800), track output tax.
- If NOT registered: no SST implications.

### 7. Foreign Currency Transactions
- Use BNK exchange rate on transaction date.
- Monetary items at year-end: retranslate at closing rate.
- Exchange differences: 6100 (loss) or 4200 (gain under Other Income).

### 8. Intercompany / Inter-Entity Transactions
- If client has multiple entities (e.g., Sdn Bhd + sole prop), transactions between them must be identified.
- You MUST ASK the user: "This client appears to have related entities ([list]). How should intercompany transactions be handled — separate engagements, combined review, or per your instructions?"
- Process as separate engagements by default, but flag all intercompany transactions in both sets of accounts.
- Related party disclosure is mandatory under MPERS Section 33.

### 8a. Inventory / COGS (Trading/Manufacturing Clients)
- If stock records with quantities and costs are provided: compute closing stock value using client's stated method (FIFO/weighted average). Prepare COGS schedule.
- If no stock records: ASK user for closing stock figure (from physical stock count). COGS = Opening Stock + Purchases - Closing Stock.
- If neither stock records nor closing figure available: FLAG prominently. Cannot prepare accurate COGS without closing stock.
- Inventory valuation: lower of cost and net realisable value (MPERS S13).

### 9. No Bank Statements Provided
- You CANNOT proceed with accounting without bank statements for a bank account that has transactions.
- ASK immediately. This is a blocker.
- If client confirms no bank account (cash-only business), proceed with available documents (invoices, receipts) but flag the limitation prominently.

### 10. Incomplete Payroll Information
- If payslips are missing for some months: ASK for them.
- If payslips are entirely unavailable: use bank statement salary payments as basis, but flag that payroll has not been independently verified.
- NEVER fabricate payroll figures.

---

## WHAT YOU MUST NEVER DO

1. **Never fabricate or hallucinate data.** If a number isn't in a source document, it doesn't exist.
2. **Never skip the bank reconciliation.** The GL bank balance must match the bank statement closing balance exactly.
3. **Never produce an unbalanced Trial Balance.** DR must equal CR. Always.
4. **Never assume tax treatment without verification.** When in doubt, ask.
5. **Never process without reading this file first.** This file is the firm's policy. It overrides any default behaviour.
6. **Never produce reports in any format other than the standards defined here.** Black and white. Minimal. Consistent.
7. **Never make business decisions for the client.** Advise, recommend, flag — but the decision is always the client's. Document their decision.
8. **Never skip the Queries & Notes section.** If there are open items, they must be documented. An empty Queries sheet means everything is resolved and verified.
