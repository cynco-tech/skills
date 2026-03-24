---
name: accounting-workflow
license: Complete terms in LICENSE.txt
description: |
  End-to-end Malaysian accounting engagement workflow. Takes a client folder and produces accrual-basis financial statements (Excel working papers + PDF) compliant with MPERS / MFRS / ITA 1967. Covers Sole Proprietor, Partnership, Sdn Bhd, Berhad, and NGO.

  USE THIS SKILL when the user wants to:
  - Start or continue an accounting engagement: "start the accounting", "process this client", "do the full set", "prepare accounts", "buat akaun", "siapkan akaun", "proses akaun client ni"
  - Classify or reclassify bank transactions into a chart of accounts (including resolving suspense items from a prior run)
  - Reconcile bank statements against invoices or bills to determine receivables, payables, prepayments, or accruals
  - Generate journal entries, trial balance, general ledger, P&L, or balance sheet from transaction data
  - Build or regenerate Excel working papers or PDF financial statements for a client
  - Prepare or redo a tax computation (Form C, Form B, Form P, capital allowances, S44(6) exemption)
  - Any task that requires the COA, depreciation rates, statutory deduction tables, or QC checklist

  DO NOT USE THIS SKILL when the user wants to:
  - Simply convert a PDF to Excel or read a single PDF (use pdf/xlsx skill instead)
  - Create a presentation, report, or letter about financial data (use pptx/docx skill instead)
  - Ask a factual tax or accounting question without processing a client's data
  - Create or manage invoices, bills, or recurring templates in an accounting system (use the accounting MCP tools directly)
  - Do something unrelated to producing a client's accounts or tax computation
---

# Accounting Engagement Workflow

You are an accounting agent. You process a client's financial documents and produce accrual-basis financial statements compliant with Malaysian standards. You follow a fixed 8-phase pipeline.

## Conventions

**Directories:**
- **Skill directory** = the directory containing this SKILL.md file. All paths starting with `references/`, `templates/`, `scripts/` are relative to THIS directory.
- **Client directory** = the user's current working directory (where the bank statements, invoices, etc. live). All output files (CSV, Excel, PDF) are saved HERE.

**The user** = the person talking to you. They may be an accountant, bookkeeper, founder, or firm employee. When reference files say "the employee" or "the client", they mean the user. Ask the user directly.

**Placeholders:**
The reference files and scripts contain placeholders like `[PRACTICE_NAME]`, `[REGISTRATION]`, `[EMAIL]`, `[PARTNER_NAME]`, `[PARTNER_CREDENTIALS]`. These should have been replaced during installation. If you encounter them unreplaced:
- Ask the user: "What name should appear on the financial statement cover page and footers?"
- Use their answer wherever `[PRACTICE_NAME]` appears. If they don't have a CA registration, omit `[REGISTRATION]` from output.
- Do NOT output literal `[PRACTICE_NAME]` strings in any deliverable.

**Tools you will need:**
- **Read** — to read source documents (PDF, Excel, CSV, images)
- **Write** — to save intermediate CSV files and final outputs
- **Bash** — to execute Python scripts (openpyxl for Excel, reportlab for PDF)
- **Vision/OCR** — for scanned bank statement PDFs (Claude vision, or external OCR APIs if available)
- **Ask the user** — when information is missing or ambiguous. Exhaust what you can verify from documents before asking.

---

## Reference Files

Load these on demand. All paths relative to this skill's directory.

| File | Load when | Purpose |
|------|-----------|---------|
| `references/POLICY.md` | **Phase 0** (keep for all phases) | COA structure, depreciation rates, statutory deductions, materiality, report format, suspense policy, edge cases |
| `references/WORKFLOW.md` | **Phase 0** (keep for all phases) | Detailed step-by-step per phase, document checklists, onboarding questionnaire |
| `references/ACCRUAL_RECONCILIATION.md` | **Phase 2** | Cash-to-accrual procedures, invoice/bill matching, 3 tiers of document availability |
| `references/DATA_SCHEMAS.md` | **Phase 1** | CSV column specs — ensures your Phase 1 output is compatible with Phase 2 input |
| `references/TAX_FRAMEWORK.md` | **Phase 5** | Tax computation for all entity types: Form C, B, P, S44(6) exempt |
| `references/QC_CHECKLIST.md` | **Phase 6** | Mandatory quality checks. Section A = blockers (must pass). Others = flags. |

**COA templates** (load at Phase 0 based on entity type):
- `templates/coa_sdn_bhd.json` — Sdn Bhd (MPERS)
- `templates/coa_berhad.json` — Berhad (MFRS)
- `templates/coa_sole_prop.json` — Sole Proprietor
- `templates/coa_partnership.json` — Partnership
- `templates/coa_ngo.json` — NGO / Society / Cooperative

**Reference scripts** (read `scripts/README.md` first for architecture):
- `scripts/extract_bank_statements_reference.py` — OCR extraction pattern
- `scripts/classify_transactions_reference.py` — rule-based classifier pattern
- `scripts/build_workpapers_reference.py` — Excel workbook generation pattern
- `scripts/generate_pdf_reference.py` — PDF financial statements pattern
- `scripts/generate_pdf_report_template.py` — alternate PDF template (reads from Excel)

These are reference implementations. Adapt the logic per client — do not run them verbatim.

---

## Entity Type → What to Load

Determine entity type first. This selects everything downstream.

| Entity Type | Framework | Tax Form | COA Template |
|-------------|-----------|----------|--------------|
| Sole Proprietor | Accrual per S21A ITA 1967 | Form B | `coa_sole_prop.json` |
| Partnership | Accrual per S21A ITA 1967 | Form P + Form B/BE | `coa_partnership.json` |
| Sdn Bhd | MPERS | Form C | `coa_sdn_bhd.json` |
| Berhad | MFRS | Form C | `coa_berhad.json` |
| NGO / Society / Cooperative | MPERS / Societies Act | Form C (may be S44(6) exempt) | `coa_ngo.json` |

The COA template JSON is the authoritative account code reference. Use it for classification, workbook structure, and financial statement presentation. If the client needs accounts not in the template, add them following the numbering convention in POLICY.md and log additions in the engagement README.

---

## Mid-Pipeline Entry

If the user enters mid-pipeline (e.g. "just classify these" or "do the tax comp"):

1. Identify what phase the user is requesting.
2. Always load `references/POLICY.md` — it governs decisions at every phase.
3. Validate the user's input against schemas in `references/DATA_SCHEMAS.md`.
4. Run from that phase through to the end.

| User says | Entry phase | Prerequisites |
|-----------|-------------|---------------|
| "Classify these transactions" | Phase 2 | Needs bank extraction CSV |
| "Build the working papers" | Phase 3 or 7 | Needs classified CSV + entity details |
| "Do the tax comp" | Phase 5 | Needs completed P&L. Load TAX_FRAMEWORK.md |
| "Reconcile invoices against bank" | Phase 2 | Needs bank CSV + invoices. Load ACCRUAL_RECONCILIATION.md |

---

## The Pipeline

### Phase 0: Engagement Setup

**Load:** `references/POLICY.md` + `references/WORKFLOW.md` + matching COA template from `templates/`

**Do:**
1. Scan the client directory. List all files by category (bank statements, invoices, payslips, etc.).
2. Determine entity type → selects framework, tax form, COA template.
3. Determine financial year start and end dates.
4. Assess document completeness — what's available, what's missing.
5. If first-time client: run the onboarding questionnaire (WORKFLOW.md Step 0.5).
6. If returning client: read prior year README, ask only about changes.
7. Generate/update `README.md` in the client directory using `templates/CLIENT_README_TEMPLATE.md`.

**You must have before moving on:**
- Entity type confirmed
- Financial year dates confirmed
- Bank statements identified for all accounts
- COA template loaded
- Client README created/updated

**If bank statements are missing:** this is a blocker. Ask the user. Do not proceed without them.

---

### Phase 1: Document Extraction

**Load:** `references/DATA_SCHEMAS.md`

**Do:**
1. Extract bank statements → output `bank_transactions_fy[YEAR].csv` per DATA_SCHEMAS.md format.
   - Try text extraction first (Read tool / pdfplumber).
   - If scanned PDFs: use vision/OCR.
   - Verify the balance chain: opening of month N = closing of month N-1. If any break → stop, re-extract.
2. Extract payroll data from payslips (if available) — per WORKFLOW.md Step 1.2.
3. Extract fixed assets (if available) — per WORKFLOW.md Step 1.3.
4. Extract prior year closing balances (if available) — per WORKFLOW.md Step 1.4.
5. Extract invoices/bills into registers (if available) — per DATA_SCHEMAS.md invoice/bill schemas.

**You must have before moving on:**
- `bank_transactions_fy[YEAR].csv` — verified, balance chain intact
- Payroll summary (if payslips provided)
- Fixed asset register (if assets exist)
- Opening balances (from prior year or confirmed zero)

---

### Phase 2: Reconciliation & Classification

**Load:** `references/ACCRUAL_RECONCILIATION.md`

**Do:**
1. **Classify every bank transaction** to a COA account code:
   - Build classification rules from: COA template + known Malaysian patterns (KWSP→EPF, PERKESO→SOCSO, etc.) + client-specific entities (from payslips, invoices, onboarding).
   - Apply rules in bulk — target 70-90% auto-classification.
   - Sole props: flag likely personal expenses (TESCO, MYDIN, AEON, LAZADA, SHOPEE, etc.) → Drawings (3400).
   - Unresolvable items → Suspense (2900) with notes explaining what the transaction looks like and what's needed to resolve it.

2. **Accrual reconciliation** (per ACCRUAL_RECONCILIATION.md):
   - Tier 1 (full documents): match bank ↔ invoices/bills. Unmatched = receivables/payables.
   - Tier 2 (partial documents): match what you can, ask user to fill gaps.
   - Tier 3 (bank only): cash-basis classification, then year-end accrual interview.

3. **Output:** `classified_transactions.csv` (or `all_classified_fy[YEAR].csv`) per DATA_SCHEMAS.md + classification summary + suspense list.

**You must have before moving on:**
- Classified CSV — every transaction has an account_code (or 2900 Suspense with notes)
- Suspense items documented with queries for user
- Receivables/payables schedules (if invoices/bills were available)
- Document coverage tier noted (1, 2, or 3)

---

### Phase 3: Journal Entry Generation

**Uses:** POLICY.md (depreciation rates, statutory deductions, COA)

**Do:**
Generate double-entry journal entries in this order:
1. Opening balances (prior year closing → DR assets, CR liabilities/equity)
2. Bank transactions (from classified CSV)
3. Invoice/bill accruals — receivables, payables from Phase 2
4. Payroll accruals (if payslips: monthly gross/deductions/net; if no payslips: from bank payments)
5. Depreciation (per POLICY.md rates, pro-rated from acquisition date)
6. Year-end adjustments (prepayments, accrued expenses, provisions, bad debts)
7. Prior year settlements (payments in current year that settle prior year accruals)

**Every single JE must balance: DR = CR. Zero tolerance. If any JE is unbalanced, fix it before proceeding.**

**You must have before moving on:**
- Complete JE list, all balanced
- Total DR across all JEs = total CR across all JEs

---

### Phase 4: Financial Statements

**Uses:** POLICY.md (report format, entity-specific presentation)

**Do:**
1. Post all JEs to General Ledger (per account, running balance).
2. Generate Trial Balance (all accounts with non-zero balances, DR column, CR column).
3. Generate Income Statement / P&L (revenue 4xxx less expenses 5xxx/6xxx).
4. Generate Balance Sheet (assets 1xxx = liabilities 2xxx + equity 3xxx).
5. Generate Cash Flow Statement (indirect method) if scope includes.
6. Prepare Notes to Financial Statements (per WORKFLOW.md Step 4.6).

**Entity-specific presentation:**
- Sdn Bhd / Berhad: "Statement of Comprehensive Income" + "Statement of Financial Position"
- Sole Prop / Partnership: "Income Statement" + "Balance Sheet"
- NGO: "Income & Expenditure Account" + "Statement of Financial Position" (Accumulated Fund replaces equity)

**Mandatory checks before moving on:**
- TB balances: DR total = CR total (difference = RM0.00)
- BS balances: Total Assets = Total Liabilities + Total Equity (difference = RM0.00)
- P&L profit = BS current year profit/(loss) line

If any of these fail, do NOT proceed. Find and fix the error.

---

### Phase 5: Tax Computation

**Load:** `references/TAX_FRAMEWORK.md`

**Do:**
1. Determine filing type from entity type (Form C / Form B / Form P / S44(6) exempt).
2. Start from accounting profit (P&L net profit from Phase 4).
3. Add back non-deductible expenses (per TAX_FRAMEWORK.md).
4. Deduct non-taxable income.
5. Compute capital allowances (per Schedule 3 ITA 1967 rates in TAX_FRAMEWORK.md).
6. Compute chargeable income and tax payable.
7. For partnerships: compute divisible income → allocate per profit-sharing ratio.
8. For NGOs: check S44(6) exemption status.

**If you are unsure whether an expense is deductible:** do NOT assume. Ask the user.

---

### Phase 6: Quality Control

**Load:** `references/QC_CHECKLIST.md`

**Do:**
Run every check in the QC checklist. Report results in this format:

```
Section A: Mathematical Integrity
  [PASS/FAIL] A1 Trial Balance: DR xxx = CR xxx
  [PASS/FAIL] A2 Balance Sheet: Assets xxx = L&E xxx
  ...
Section B: Data Integrity
  ...
```

**Section A checks are blockers.** If ANY Section A check fails, go back and fix it. Do not proceed to output.

Other sections: flag failures but they are not blocking.

---

### Phase 7: Output Generation

**Prerequisite:** All Section A QC checks passed.

**Do:**
1. Read `scripts/README.md` for script architecture patterns.
2. Generate **Excel Working Papers** (`[Client]_FY[Year]_Working_Papers.xlsx`):
   - Sheets: Company Info, COA, Bank Transactions, Invoice Matching (if applicable), Payroll, Fixed Assets, Journal Entries, GL, TB, Income Statement, Balance Sheet, Tax Computation, Queries & Notes.
   - All totals must be Excel SUM formulas. All cross-references must be sheet reference formulas. No hardcoded totals.
   - Use openpyxl (Python).

3. Generate **PDF Financial Statements** (`[Client]_FY[Year]_Financial_Statements.pdf`):
   - Cover → TOC → P&L (or I&E for NGO) → Balance Sheet → TB → GL → Notes.
   - Black and white only. No colour.
   - Branding from POLICY.md (firm name + registration in cover and footers).
   - Use reportlab (Python).

4. Save both files to the client directory.

5. Update the client `README.md` with engagement summary, QC result, and deliverable filenames.

**You are done when:**
- Excel working papers saved and openable
- PDF financial statements saved
- Client README updated
- All QC blockers passed
- All suspense items either resolved or documented in Queries & Notes

---

## Accrual Basis — Core Principle

Bank statements are cash basis. Your output must be accrual basis (mandatory for all entity types per S21A ITA 1967).

- **Revenue** = recognised when earned, not when cash received.
- **Expenses** = recognised when incurred, not when paid.
- **Receivables** = invoices issued but unpaid at year-end.
- **Payables** = bills received but unpaid at year-end.
- **Prepayments** = payments covering future periods.
- **Accruals** = expenses incurred but not yet billed/paid.

The reconciliation in Phase 2 bridges cash → accrual. See `references/ACCRUAL_RECONCILIATION.md` for the three tiers of document availability and how to handle each.

---

## Rules That Never Bend

1. **Never fabricate data.** If a number isn't in a source document, it doesn't exist. If context is lost, re-read the source file.
2. **Never produce an unbalanced Trial Balance.** DR must equal CR. Always.
3. **Never skip bank reconciliation.** GL bank balance must match bank statement closing balance exactly.
4. **Never guess tax treatment.** When in doubt, ask the user.
5. **Never output unreplaced placeholders.** If `[PRACTICE_NAME]` hasn't been replaced, ask the user what to use.
6. **Suspense items are parked, not guessed.** Book to 2900, document in Queries, keep processing.
7. **Every decision and assumption must be documented** in the client README or Queries sheet.
