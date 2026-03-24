# Reference Scripts — Architecture Overview

These scripts are working implementations from a real engagement ([CLIENT_NAME], FY [YEAR]). They are reference code — adapt the structure per client, don't run them verbatim.

Read this file before diving into any script. It tells you what each one does, how they connect, and which parts to customise.

---

## Script Map

| Script | Phase | Input | Output | Lines |
|--------|-------|-------|--------|-------|
| `extract_bank_statements_reference.py` | 1 | Bank PDF files | `bank_transactions_fy[YEAR].csv` + summary | ~350 |
| `classify_transactions_reference.py` | 2 | Extraction CSV | `classified_transactions.csv` + summary | ~330 |
| `build_workpapers_reference.py` | 7 | Classified CSV | `_Working_Papers.xlsx` (12 sheets) | ~1500 |
| `generate_pdf_reference.py` | 7 | Computed data (from workpapers logic) | `_Financial_Statements.pdf` | ~700 |
| `generate_pdf_report_template.py` | 7 | (Alternate template) | PDF report | ~600 |

---

## extract_bank_statements_reference.py

Uses the Reducto API to OCR scanned Maybank Islamic PDFs. **This is the part most likely to change per engagement** — different banks have different table layouts, and you may use a different OCR tool entirely.

Key sections:
- `TableParser` class (line ~34) — HTML table parser for Reducto's output format. Replace if using a different OCR tool.
- `parse_amount()` (line ~121) — Handles Maybank's `+`/`-` suffix format for credits/debits. Other banks may use separate columns or CR/DR labels.
- `process_table_rows()` (line ~155) — The main extraction logic. Skips headers/footers, identifies OPENING/CLOSING balance rows, handles continuation lines (sub-descriptions).
- `main()` — Processes files in order, verifies balance chain, writes CSV.

**What to adapt:** The bank format parsing (amount signs, date format, column layout). The OCR tool invocation. The file list. The output CSV schema stays the same.

---

## classify_transactions_reference.py

Rule-based transaction classifier. The most client-specific script.

Key sections:
- **COA mapping** (line ~19) — Hardcoded dict of account codes and names used for this client. Replace with the COA template JSON for the new client.
- **Known people/entities** (line ~50) — Dict mapping names to account codes. E.g. employee names → 5000, director names → 5035, landlord → 5200. This is the main thing you build per client.
- `classify()` function (line ~93) — The rule engine. Checks in priority order: known people → keyword patterns → amount patterns → suspense. Returns `(account_code, account_name, method)`.
- `main()` — Reads extraction CSV, classifies each row, writes classified CSV + summary.

**What to adapt:** The known people/entities dict (built during Phase 0 from payslips, invoices, entity details). The keyword patterns (most are reusable across Malaysian clients — KWSP, PERKESO, etc., but industry-specific patterns vary). The COA mapping (swap in the right template).

---

## build_workpapers_reference.py

The big one (~1,500 lines). Generates a 12-sheet Excel workbook using openpyxl.

Architecture:
- **`RowTracker` class** (line ~35) — Tracks cell positions across sheets so that cross-sheet formulas (e.g. BS pulling from TB) can be built dynamically. This is reusable as-is.
- **COA + Classification Map** (line ~59) — Maps CSV account codes to GL structure. Adapt per client.
- **Opening Balances** (line ~129) — Hardcoded for this client. For new clients, extract from prior year or set to zero.
- **`load_transactions()`** (line ~176) — Reads the classified CSV into memory, applies reclassifications (e.g. prior year accrual settlements).
- **`main()` block** (line ~203) — Builds all 12 sheets in sequence:
  1. Company Info — entity details, FY, framework
  2. Chart of Accounts — full COA from template
  3. Bank Transactions — extraction data with running balance formula
  4. Payroll Summary — monthly breakdown (if payslips available)
  5. Fixed Asset Register — assets, depreciation, NBV
  6. Journal Entries — all JEs in sequence
  7. General Ledger — JEs posted per account, running balance
  8. Trial Balance — all accounts, DR/CR/Balance columns, SUM formulas
  9. Income Statement — revenue less expenses = profit
  10. Balance Sheet — assets = liabilities + equity, cross-refs to TB
  11. Tax Computation — adjusted income, CA schedule, tax payable
  12. Queries & Notes — suspense items + client questions

**What to adapt:** Opening balances, COA, entity details, payroll structure, fixed asset register. The sheet-building logic and formula patterns are largely reusable.

**Key design principle:** Every total is an Excel SUM formula, every cross-reference is a sheet reference formula (`='Trial Balance'!E15`). No hardcoded totals. This means the workbook self-validates — if a number changes upstream, totals propagate automatically.

---

## generate_pdf_reference.py

Generates the client-facing PDF using reportlab.

Architecture:
- **`compute_all()`** (line ~81) — Duplicates the financial computation from the workpapers script (reads the same classified CSV, builds GL, computes TB/IS/BS). This is intentional — the PDF generator is self-contained and doesn't depend on the Excel file existing.
- **`PageNumberTracker`** (line ~355) — Handles page numbering and TOC page references.
- **`get_styles()`** (line ~386) — Helvetica, black and white, minimal formatting. Firm standard.
- **Builder functions** — `build_cover()`, `build_toc()`, `build_income_statement()`, `build_balance_sheet()`, `build_trial_balance()`, `build_general_ledger()`. Each returns a list of reportlab flowables.
- **Two-pass rendering** — First pass computes page numbers, second pass writes the final PDF with correct TOC references.

**What to adapt:** Entity name, registration number, FY period, cover page text. The financial computation mirrors the workpapers — if you change the COA or classification in the workpapers script, make the same changes here.
