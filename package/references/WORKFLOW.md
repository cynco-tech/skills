# ACCOUNTING ENGAGEMENT WORKFLOW

This document defines the mandatory step-by-step workflow for every client engagement. You MUST follow every phase in sequence. No phase may be skipped.

---

## PHASE 0: ENGAGEMENT SETUP

**Objective**: Understand the client, identify what we're working with, and assess readiness.

### Step 0.1 — Read Firm Instructions
- Read `references/POLICY.md` (firm policies, standards, COA, depreciation rates, etc.)
- Read this file (`WORKFLOW.md`)
- If a client-specific `README.md` exists in the folder, read it (contains prior engagement notes, client preferences, known issues)

### Step 0.2 — Scan Client Folder
Recursively scan the client folder to identify all available documents. Categorise into:

| Category | What to look for | File types |
|---|---|---|
| Corporate details | SSM forms, registration cert, Form 9/13/24/49, constitution | PDF, JPG |
| Bank statements | Monthly statements from all bank accounts | PDF |
| Invoices (Sales) | Sales invoices issued to customers | PDF, JPG, Excel |
| Invoices (Purchase) | Purchase invoices from suppliers | PDF, JPG |
| Receipts | Payment receipts, petty cash vouchers | PDF, JPG |
| Payroll | Payslips, EA forms, EPF/SOCSO statements | PDF, Excel |
| Fixed assets | Asset listing, purchase invoices for equipment | PDF, Excel |
| Contracts & agreements | Tenancy, hire purchase, loan agreements | PDF |
| Prior year | Audit report, management accounts, prior year workbook, tax computation | PDF, Excel |
| Inventory | Stock listing, stock count sheets | PDF, Excel |
| Other | Any other documents | Any |

### Step 0.3 — Identify Entity Details
Extract from corporate documents or ASK the user:
- [ ] Entity name (full legal name)
- [ ] Registration number (SSM / ROB / ROC)
- [ ] Entity type: Sdn Bhd / Sole Proprietor / Partnership
- [ ] Income tax reference number
- [ ] Financial year end date
- [ ] Date of incorporation / commencement
- [ ] Principal business activity
- [ ] Registered address
- [ ] Director(s) / owner(s) / partner(s) names
- [ ] SST registration status (registered / not registered / exempt)
- [ ] Number of employees

### Step 0.4 — Assess Document Completeness
Generate a checklist of what's available vs what's missing:

**MANDATORY documents (cannot proceed without these):**
- [ ] Bank statements for ALL bank accounts for the FULL financial year
- [ ] Entity registration/incorporation details

**IMPORTANT documents (can proceed but with limitations):**
- [ ] Payslips / payroll records
- [ ] Fixed asset listing or purchase invoices for assets
- [ ] Prior year financial statements / audit report
- [ ] Prior year tax computation
- [ ] Tenancy agreement (if rental expense exists)
- [ ] Hire purchase agreements (if HP payments exist)
- [ ] Loan agreements (if loan payments exist)

**NICE-TO-HAVE documents:**
- [ ] Sales invoices (helps verify revenue classification)
- [ ] Purchase invoices (helps verify expense classification)
- [ ] Receipts (supports expense claims)
- [ ] Contracts

### Step 0.5 — Client Onboarding / Smart Questions

**First-time client (no prior README exists):**
Full onboarding questionnaire via AskUserQuestion. Cover:
1. Entity type confirmation (Sdn Bhd / Sole Prop / Partnership)
2. Financial year end date
3. Principal business activity
4. Number of bank accounts and which banks
5. Number of employees
6. Does the client have fixed assets? Approximate count/value?
7. Does the client have inventory/stock?
8. Prior year accounts — audit report or management accounts available?
9. SST registration status
10. Any related entities (other companies/businesses owned by same person)?
11. Any special tax incentives (pioneer status, ITA, RA)?
12. Any hire purchase or loan facilities?
13. Does employer absorb employee statutory contributions?
14. Any specific client preferences or instructions?
15. Missing mandatory documents (bank statements, etc.)

**Returning client (prior README exists):**
Smart mode — read prior year README, then only ask:
1. "Any changes from last year?" (new employees, new bank accounts, entity changes)
2. Missing documents not yet provided
3. Items flagged in prior year's "Notes for Next Year"

**Do NOT ask about things already answered by the documents. Check first, then ask only what's genuinely missing.**

### Step 0.6 — Generate Engagement README
Create/update `README.md` in the client folder with:
- Entity details
- FY period
- Document inventory (what's provided, what's missing)
- Special notes
- Engagement date

---

## PHASE 1: DOCUMENT INGESTION & EXTRACTION

**Objective**: Convert all source documents into structured, machine-readable data.

### Step 1.1 — Extract Bank Statements
**Approach**: Intelligent parsing. Read any Malaysian bank PDF (Maybank, CIMB, Public Bank, RHB, Hong Leong, AmBank, etc.) and extract using your understanding of the format. No bank-specific templates — adapt to whatever format the bank uses.

For each bank account:
1. Read all bank statement PDFs in chronological order
2. Extract into structured format: Date, Description, Credit (In), Debit (Out), Balance
3. Verify: opening balance of month N = closing balance of month N-1
4. Verify: first month's opening balance matches the bank's reported opening
5. Verify: last month's closing balance is the year-end balance
6. Store extracted data with running balance
7. If ANY discrepancy in the chain — STOP and flag. Do not continue with incorrect bank data.

**Critical**: Bank extraction must be 100% accurate. Every single transaction must be captured. Cross-check transaction counts and totals per month against the statement summaries (most bank statements show monthly totals).

### Step 1.2 — Extract Payroll Data
If payslips are available:
1. Extract per employee per month: Gross salary, allowances, overtime, commission, deductions (EPF EE, SOCSO EE, EIS EE, PCB), net pay
2. Verify: employer contributions (EPF ER, SOCSO ER, EIS ER)
3. Cross-reference with bank statement salary payments
4. Flag any discrepancy between payslip net pay and actual bank payment

If payslips are NOT available:
1. Identify salary payments from bank statements (common descriptions: "Gaji", "Salary", names followed by salary-related keywords)
2. Flag: "Payroll data based on bank statements only — not independently verified. Payslips not provided."
3. Ask user to confirm: who are the employees, what are the salary amounts

### Step 1.3 — Extract Fixed Asset Data
If asset listing is available:
1. Extract: Description, Category, Date Acquired, Cost, Location
2. Cross-reference with bank statements for payment verification

If no listing but purchase invoices exist:
1. Identify assets from invoices (items > RM500 that are not consumables)
2. Build the register from invoices

If neither:
1. Check bank statements for large equipment purchases
2. Ask user: "The following payments may be asset purchases. Please confirm: [list]"

### Step 1.4 — Extract Prior Year Data
If audit report / management accounts / prior year workbook exists:
1. Extract closing Balance Sheet balances → these become opening balances
2. Extract closing TB → verify against BS
3. If audit report: check for auditor's adjusting entries (AJEs)
4. If AJEs exist: incorporate them into the opening balances
5. If audit report exists but AJEs are not separately documented: ASK — "Prior year was audited by [auditor name]. Were any audit adjusting entries passed? If so, please provide the AJE list."
6. Extract prior year tax computation: capital allowances b/f, unabsorbed losses, S108 balance

If no prior year data:
1. First-year entity: opening = zero (+ share capital for Sdn Bhd)
2. Existing entity, no data: ASK — "This appears to be an existing business but no prior year accounts are available. Please provide prior year closing balances or confirm this is the first year of accounts preparation."

### Step 1.5 — Extract Other Documents
- **Tenancy agreements**: Monthly rental amount, lease term, deposit amount, commencement date
- **Hire purchase agreements**: Asset description, HP principal, interest rate, monthly instalment, tenure
- **Loan agreements**: Principal, interest rate, repayment schedule
- **Contracts**: Revenue contracts for service revenue recognition basis

---

## PHASE 2: VERIFICATION & RECONCILIATION

**Objective**: Cross-reference all extracted data. Identify discrepancies, gaps, and items needing clarification.

### Step 2.1 — Bank Statement Integrity Check
- Total all monthly inflows and outflows
- Verify: Opening + Total Inflows - Total Outflows = Closing
- This must hold for each month AND for the full year
- If any month fails: re-extract that month's data. Do not proceed until bank data is 100% verified.

### Step 2.2 — Transaction Classification
For each bank transaction, classify into an account code:
1. **Clear transactions** — description clearly indicates the nature (e.g., "KWSP" = EPF, "Sewa" = rental). Classify directly.
2. **Pattern-matched transactions** — recurring same-amount transactions to the same party (e.g., monthly rental). Classify by pattern.
3. **Cross-referenced transactions** — match against invoices/receipts. Classify per document.
4. **Ambiguous transactions** — cannot determine from available information.
   - Park in **Suspense (2900)**
   - Add to Queries list for user/client
5. **Capital vs Revenue** — large payments for equipment/assets: verify if asset purchase (capitalise) or expense. When in doubt, ASK.

### Step 2.3 — Payroll Reconciliation
If payslips are available:
- Total net pay per month from payslips must match bank payments for salaries
- Total employer EPF per payslip must reconcile to EPF payments in bank
- Total SOCSO/EIS per payslip must reconcile to SOCSO/EIS payments in bank
- Flag any timing differences (e.g., Nov salary paid in Dec, Dec EPF paid in Jan — these create accruals/payables)

### Step 2.4 — Fixed Asset Reconciliation
- Verify asset purchases against bank payments
- Check for disposals (any assets in prior year register not carried forward?)
- Verify depreciation calculations: cost, useful life, acquisition date, residual value

### Step 2.5 — Prior Year Reconciliation
- Opening TB must match prior year closing TB exactly
- If any difference: STOP and investigate. Ask user.
- Prior year retained earnings must equal: prior year P&L + accumulated retained earnings

### Step 2.6 — Generate Queries List
Compile all open items into a structured list:

```
QUERIES & OPEN ITEMS
Engagement: [Client Name] FY[Year]
Date Prepared: [Date]
Prepared by: AI Agent / [User Name]

FOR USER (INTERNAL):
1. [Date] — [Amount] — [Description] — [What's needed]

FOR CLIENT (EXTERNAL):
1. [Date] — [Amount] — [Description] — [Plain English question]
```

Present to user for immediate items. Include in final workbook for client items.

---

## PHASE 3: JOURNAL ENTRIES

**Objective**: Record all transactions as double-entry journal entries.

### Step 3.1 — Opening Balance Journal Entry
JE #1: Opening balances
- DR all asset accounts (per prior year closing)
- CR all liability accounts (per prior year closing)
- CR equity accounts (share capital, retained earnings)
- This JE must balance (DR = CR)

### Step 3.2 — Bank Transaction Journal Entries
For each classified bank transaction:

| Transaction Type | Debit | Credit |
|---|---|---|
| Revenue received | 1000 Bank | 4xxx Revenue |
| Expense paid | 5xxx Expense | 1000 Bank |
| Asset purchased | 1300/1310/1320 PPE | 1000 Bank |
| Salary paid (payslip exists) | 2150 Salary Payable | 1000 Bank |
| Salary paid (no payslip) | 5000 Salary & Wages | 1000 Bank |
| EPF payment | 2110 EPF Payable | 1000 Bank |
| SOCSO payment | 2120 SOCSO Payable | 1000 Bank |
| EIS payment | 2130 EIS Payable | 1000 Bank |
| Loan repayment | 2300 Loan (principal) + 5990 Interest | 1000 Bank |
| HP instalment | 2400 HP (principal) + 5990 Interest | 1000 Bank |
| Capital contribution | 1000 Bank | 3000/3100 Capital |
| Drawings (sole prop) | 3400 Drawings | 1000 Bank |
| Suspense item | 2900 Suspense | 1000 Bank (outflow) |
| Suspense item | 1000 Bank | 2900 Suspense (inflow) |

### Step 3.3 — Payroll Accrual Journal Entries (Monthly)
If payslips are available, for each month:
```
DR 5000 Salary & Wages          [gross basic]
DR 5010 Allowances               [allowances]
DR 5020 Commission               [commission]
DR 5100 EPF - Employer           [employer EPF]
DR 5110 SOCSO - Employer         [employer SOCSO]
DR 5120 EIS - Employer           [employer EIS]
  CR 2110 EPF Payable            [employer + employee EPF]
  CR 2120 SOCSO Payable          [employer + employee SOCSO]
  CR 2130 EIS Payable            [employer + employee EIS]
  CR 2150 Salary Payable         [net pay]
```

### Step 3.4 — Depreciation Journal Entries
Annual entry (or monthly if client prefers):
```
DR 5300 Depreciation - Equipment       [annual charge]
DR 5310 Depreciation - Computer        [annual charge]
DR 5320 Depreciation - Motor Vehicle   [annual charge]
  CR 1399 Accum Depr - Equipment       [annual charge]
  CR 1398 Accum Depr - Computer        [annual charge]
  CR 1397 Accum Depr - Motor Vehicle   [annual charge]
```
Pro-rate for assets acquired/disposed during the year.

### Step 3.5 — Year-End Adjustments
Check and record:
- [ ] **Accrued expenses**: expenses incurred but not yet paid (e.g., Dec salary paid in Jan, audit fee, year-end bonuses)
- [ ] **Prepaid expenses**: payments covering next FY period (e.g., insurance, rental paid in advance)
- [ ] **Accrued revenue**: revenue earned but not yet received
- [ ] **Unearned revenue**: payments received for services not yet rendered
- [ ] **Bad debt provision**: review receivables ageing, provide if necessary
- [ ] **Inventory adjustment**: if inventory exists, adjust to closing stock value
- [ ] **Tax provision**: estimated tax payable for the year

### Step 3.6 — Verify All JEs Balance
Run a check: for every JE, sum of debits must equal sum of credits.
Total imbalance across all JEs must be RM0.00.
If not zero: find and fix the error before proceeding.

---

## PHASE 4: FINANCIAL STATEMENTS

**Objective**: Generate the complete set of financial statements from the journal entries.

### Step 4.1 — General Ledger
- Post all JEs to their respective accounts
- Calculate running balance per account
- Sort by account code, then by date within each account

### Step 4.2 — Trial Balance
- List all accounts with non-zero balances
- DR column = sum of all debit-balance accounts
- CR column = sum of all credit-balance accounts
- **DR must equal CR.** If not, do not proceed. Find the error.

### Step 4.3 — Income Statement (Profit & Loss)
- Revenue accounts (4xxx): list all, calculate total revenue
- Expense accounts (5xxx): list all, calculate total expenses
- Profit/(Loss) = Total Revenue - Total Expenses

### Step 4.4 — Balance Sheet (Statement of Financial Position)
**Assets:**
- Current Assets: Cash & Bank, Trade Receivables, Other Receivables, Prepayments, Inventory
- Non-Current Assets: PPE (cost less accumulated depreciation), Intangible Assets

**Liabilities:**
- Current Liabilities: Trade Payables, Statutory Payables, Other Payables, Current portion of loans/HP
- Non-Current Liabilities: Long-term loans, HP non-current, Deferred tax

**Equity:**
- Share Capital / Capital Account
- Capital Contribution
- Retained Earnings (prior years)
- Current Year Profit/(Loss)
- Less: Drawings (sole prop/partnership)

**Total Assets MUST equal Total Liabilities + Equity.**

### Step 4.5 — Cash Flow Statement
Prepare using the indirect method:
- Operating: Profit + depreciation +/- changes in working capital
- Investing: PPE purchases, disposals
- Financing: Capital contributions, drawings, loan proceeds/repayments

### Step 4.6 — Notes to Financial Statements
Include (where material):
1. Basis of preparation and compliance statement
2. Significant accounting policies
3. Revenue breakdown
4. Employee costs breakdown
5. PPE schedule (cost, additions, depreciation, NBV)
6. Related party transactions (if any)
7. Directors' remuneration (Sdn Bhd)
8. Tax expense reconciliation
9. Contingent liabilities (if any)
10. Events after reporting period (if any)

### Step 4.7 — Management Reports (Optional — If Scope Includes)

**Financial Ratios:**
- Profitability: Gross margin, Net margin, ROE, ROA
- Liquidity: Current ratio, Quick ratio
- Efficiency: Receivable days, Payable days, Inventory turnover
- Leverage: Debt-to-equity, Interest coverage

**Cash Flow Analysis:**
- Monthly cash flow trend
- Operating vs investing vs financing breakdown
- Free cash flow

**Comparative Analysis (if prior year data available):**
- Year-on-year comparison for all P&L and BS line items
- Variance analysis (amount and percentage change)
- Highlight significant changes (> 20% or > RM5,000)

---

## PHASE 5: TAX COMPUTATION

**Objective**: Compute the tax liability per LHDN requirements.

### Step 5.1 — Determine Filing Type

| Entity Type | Form | Due Date |
|---|---|---|
| Sdn Bhd | Form C | 7 months after FY end |
| Sole Proprietor | Form B | 30 June (manual) / 15 July (e-filing) |
| Partnership | Form P + individual B/BE | 30 June / 15 July |

### Step 5.2 — Tax Adjustments
Start from accounting profit. Adjust for:

**Add back (non-deductible expenses):**
- Private/personal expenses
- Entertainment (50% unless wholly for business promotion)
- Penalties & fines (6200)
- Donations (unless approved under S44(6))
- Depreciation (accounting) — replaced by capital allowances
- Private motor vehicle expenses in excess of limits
- General provisions (unspecific bad debt provision)
- Capital expenditure incorrectly expensed
- Zakat Perniagaan (claimed as rebate instead)

**Deduct (non-taxable income):**
- Exempt income (4900)
- Income already taxed at source
- Gains on disposal of non-trade assets (capital in nature)
- Prior year's over-provision of expenses now reversed

### Step 5.3 — Capital Allowances
Compute per Schedule 3 ITA 1967:
- Initial Allowance (IA): on cost of asset in year of acquisition
- Annual Allowance (AA): on cost of asset every year
- Balancing Allowance/Charge: on disposal
- Small value assets (< RM2,000): 100% IA
- Prepare a capital allowance schedule: Asset, Cost, IA, AA, Residual, Accumulated CA

### Step 5.4 — Tax Payable Computation

```
Accounting Profit / (Loss)
Add: Non-deductible expenses
Less: Non-taxable income
= Adjusted Income / (Adjusted Loss)
Less: Capital Allowances
= Chargeable Income / Nil (if loss, carry forward)
x Tax Rate
= Tax Payable (before rebates)
Less: Zakat rebate (if applicable, max = tax payable)
Less: S110 tax deducted at source
Less: CP204 instalments paid
= Tax Payable / (Refundable)
```

**Tax Rates (2024 YA):**
- Sdn Bhd: 17% on first RM150,000 (if paid-up capital <= RM2.5m and gross income <= RM50m), 24% on balance
- Sole Prop / Individual: Progressive 0%-30% per Schedule 1 ITA 1967
- Partnership: taxed at individual partner level per profit-sharing ratio

### Step 5.5 — S108 / PCB Reconciliation (if applicable)
- For companies: reconcile PCB deducted against tax payable
- For individuals: reconcile against Form B/BE

---

## PHASE 6: QUALITY CONTROL

**Objective**: Final verification before output generation.

### Mandatory Checks (ALL must pass)

- [ ] Trial Balance balances (DR = CR, difference = RM0.00)
- [ ] Balance Sheet balances (Assets = Liabilities + Equity, difference = RM0.00)
- [ ] Bank closing balance matches bank statement exactly
- [ ] All JEs balance individually (no single JE has DR != CR)
- [ ] Opening balances match prior year closing (if prior year exists)
- [ ] Depreciation calculations are correct (verify sample of 3 assets minimum)
- [ ] Payroll reconciles: total payslip net pay = total salary bank payments (within timing differences)
- [ ] EPF/SOCSO/EIS paid matches accrued (within timing differences)
- [ ] Tax computation: adjusted income traces back to P&L profit
- [ ] Capital allowances: traces back to fixed asset register
- [ ] No fabricated data — every number traces to a source document or explicit user decision
- [ ] Suspense account: zero balance, OR all items documented in Queries sheet
- [ ] Report format: black & white, minimal, clean, [PRACTICE_NAME] branding

### Internal Notes for User
Flag anything that requires professional judgement or client follow-up:
- Unusual transactions
- Potential tax implications
- Compliance risks
- Missing documentation that limits assurance

### Queries for Client
Final compiled list of all outstanding items the client needs to address.

---

## PHASE 7: OUTPUT GENERATION

### Step 7.1 — Excel Working Papers
Generate comprehensive Excel workbook with all sheets as per POLICY.md specifications.
Run formula recalculation (LibreOffice recalc.py if available).

### Step 7.2 — PDF Financial Statements
Generate using reportlab per POLICY.md format standards:
- Cover page
- Table of contents
- P&L, BS, TB, GL
- Notes (if material)
- Queries & Outstanding Items (if any)

### Step 7.3 — Tax Computation (Excel)
Separate workbook or sheet:
- Tax adjustment schedule
- Capital allowance schedule
- Tax payable computation
- Supporting schedules

### Step 7.4 — Final Deliverables Checklist
Before marking engagement as complete:
- [ ] Excel working papers saved to client folder
- [ ] PDF financial statements saved to client folder
- [ ] Tax computation saved to client folder
- [ ] Client README.md updated with engagement summary
- [ ] Queries sheet populated (or confirmed empty = all resolved)
- [ ] All QC checks passed

---

## INITIATING THE WORKFLOW

When the user says any of the following (or similar), begin Phase 0:
- "Start the accounting"
- "Process this client"
- "Begin the engagement"
- "Do the full set"
- "Start processing"

Respond: "Starting engagement. Reading firm policies and scanning client folder..." and proceed through Phase 0.
