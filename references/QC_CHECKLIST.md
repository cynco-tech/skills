# QUALITY CONTROL CHECKLIST

This checklist is mandatory. Every item must be verified before an engagement is marked complete. Run this checklist programmatically at the end of Phase 6.

---

## SECTION A: MATHEMATICAL INTEGRITY

| # | Check | Pass Criteria | Blocker? |
|---|---|---|---|
| A1 | Trial Balance balances | DR total = CR total, difference = RM0.00 | YES |
| A2 | Balance Sheet balances | Total Assets = Total Liabilities + Total Equity, difference = RM0.00 | YES |
| A3 | P&L ties to BS | Current year profit on P&L = Retained earnings (current year) on BS | YES |
| A4 | All JEs balance | Every individual JE has DR = CR | YES |
| A5 | Bank GL = Bank statement | GL balance for account 1000 = bank statement closing balance exactly | YES |
| A6 | Cash flow ties | Opening cash + net cash flow = closing cash (if cash flow prepared) | YES |

If ANY Section A check fails: **DO NOT PROCEED TO OUTPUT. Fix the error first.**

---

## SECTION B: DATA INTEGRITY

| # | Check | Pass Criteria | Blocker? |
|---|---|---|---|
| B1 | No fabricated data | Every number traces to a source document OR an explicit user decision documented in notes | YES |
| B2 | Bank extraction complete | All 12 months (or applicable months) of bank statements extracted | YES |
| B3 | Bank running balance verified | Running balance in bank transaction sheet matches the bank statement at every point | YES |
| B4 | Opening balances verified | Opening TB matches prior year closing TB (or confirmed first year = zero) | YES |
| B5 | Depreciation accurate | Sample check 3+ assets: cost, useful life, acquisition date, annual charge all correct | NO (flag if fail) |
| B6 | Payroll reconciles | Net pay per payslips = bank salary payments (within timing differences of 1 month) | NO (flag if fail) |
| B7 | Statutory contributions reconcile | EPF/SOCSO/EIS accrued vs paid, timing differences explained | NO (flag if fail) |

---

## SECTION C: COMPLIANCE

| # | Check | Pass Criteria | Blocker? |
|---|---|---|---|
| C1 | Correct framework applied | Sdn Bhd = MPERS, Sole Prop/Partnership = Accrual per S21A ITA | YES |
| C2 | Accrual basis verified | Revenue recognised when earned, expenses when incurred (not just cash basis) | YES |
| C3 | Depreciation policy consistent | Same rates applied across all assets of same category, consistent with FIRM_POLICY.md | YES |
| C4 | Related party transactions disclosed | If any identified, included in notes | NO (flag if missed) |
| C5 | Director remuneration disclosed (Sdn Bhd) | Separate line item on P&L, disclosed in notes | NO (Sdn Bhd only) |
| C6 | SST compliance (if registered) | SST payable correctly computed and disclosed | NO (if applicable) |
| C7 | Tax computation consistent with P&L | Starting point = P&L profit, adjustments traceable | YES (if tax scope) |
| C8 | Capital allowances match FAR | CA schedule ties to fixed asset register | YES (if tax scope) |

---

## SECTION D: COMPLETENESS

| # | Check | Pass Criteria | Blocker? |
|---|---|---|---|
| D1 | All bank transactions classified | No unclassified transactions (all either coded or in Suspense with query) | YES |
| D2 | Suspense account resolved or queried | Balance = 0 OR all items in Queries sheet | YES |
| D3 | Year-end accruals considered | Checked: salary, rent, utilities, audit fee, interest | NO (flag if missed) |
| D4 | Prepayments considered | Checked: insurance, rental, subscriptions paid in advance | NO (flag if missed) |
| D5 | Bad debts reviewed | Receivables ageing reviewed, provision if necessary | NO (flag if missed) |
| D6 | All deliverables produced | Excel workbook + PDF statements + Tax comp (if scope) | YES |
| D7 | Queries sheet complete | All open items documented, numbered, with clear questions | YES |

---

## SECTION E: REPORT FORMAT

| # | Check | Pass Criteria | Blocker? |
|---|---|---|---|
| E1 | PDF is B&W only | No colour in the PDF financial statements | YES |
| E2 | Firm branding correct | "[FIRM_NAME] Chartered Accountants ([CA_REGISTRATION])" on cover and footer | YES |
| E3 | Client name correct | Legal entity name matches SSM registration | YES |
| E4 | FY period correct | Correct financial year end date throughout | YES |
| E5 | Page numbers present | All pages (except cover) have page numbers | NO (flag) |
| E6 | Consistent formatting | Same font, same number format, same alignment throughout | NO (flag) |

---

## SECTION F: EDGE CASES VERIFIED

| # | Check | Pass Criteria | Blocker? |
|---|---|---|---|
| F1 | Personal expenses (sole prop) | Any personal transactions coded to Drawings, not expense | NO (flag) |
| F2 | Mixed business/personal bank | If sole prop with mixed account — personal items = Drawings | NO (flag) |
| F3 | Employer absorbs EE contributions | Payslip checked, correct treatment applied | NO (flag) |
| F4 | Director vs Employee | All persons classified correctly per role | NO (flag) |
| F5 | Capital vs Revenue | Large purchases reviewed — capitalise or expense decision documented | NO (flag) |
| F6 | Inter-entity transactions | Transactions with related entities flagged | NO (flag) |
| F7 | Foreign currency | FCY transactions translated correctly | NO (if applicable) |
| F8 | First year pro-rated depreciation | Assets acquired mid-year: depreciation pro-rated from acquisition date | NO (flag) |

---

## EXECUTION

Generate this checklist as a summary at the end of processing:

```
═══════════════════════════════════════════
QUALITY CONTROL REPORT
Client: [Name]
FY: [Period]
Date: [Processing Date]
═══════════════════════════════════════════

Section A: Mathematical Integrity
  [PASS] A1 Trial Balance: DR 322,144.62 = CR 322,144.62
  [PASS] A2 Balance Sheet: Assets 113,222.52 = L&E 113,222.52
  [PASS] A3 P&L ties to BS: Profit 9,689.11
  [PASS] A4 All 379 JEs balance
  [PASS] A5 Bank GL 85,834.88 = Statement 85,834.88
  [N/A]  A6 Cash flow not prepared

Section B: Data Integrity
  [PASS] B1 No fabricated data
  [PASS] B2 Bank: 11 months extracted (Feb-Dec)
  ...

RESULT: ALL BLOCKER CHECKS PASSED
FLAGS: 2 items flagged for review
  - B6: Dec payroll not verified (payslips not provided for Dec)
  - F3: Employer absorbs SOCSO/EIS employee portion
═══════════════════════════════════════════
```
