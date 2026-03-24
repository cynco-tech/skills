# TAX COMPUTATION FRAMEWORK

## Scope

This framework covers Malaysian income tax computation for:
- **Form C** — Companies (Sdn Bhd)
- **Form B** — Individuals with business income (Sole Proprietors)
- **Form BE** — Individuals without business income (Salaried employees — relevant for partnership individual filings)
- **Form P** — Partnerships (the partnership entity itself)

---

## PART 1: FORM C — COMPANY TAX COMPUTATION

### 1.1 Structure

```
AINAN MEDIA SDN BHD
TAX COMPUTATION
YEAR OF ASSESSMENT 2024

                                                    RM              RM
Profit before taxation (per accounts)                           XX,XXX.XX

Add: Non-deductible expenses
  Depreciation (accounting)                     XX,XXX.XX
  Entertainment (50% disallowed)                 X,XXX.XX
  Private motor vehicle expenses (excess)        X,XXX.XX
  Penalties & fines                                XXX.XX
  Donations (not S44(6) approved)                  XXX.XX
  General provision for doubtful debts             XXX.XX
  Zakat perniagaan (claimed as rebate)             XXX.XX
  Other non-deductible items                       XXX.XX
                                                               XX,XXX.XX

Less: Non-taxable income
  Exempt income                                    XXX.XX
  Over-provision of expenses (prior year)          XXX.XX
                                                               (X,XXX.XX)

Adjusted Income / (Adjusted Loss)                             XXX,XXX.XX

Less: Capital Allowances (Schedule 3)
  Current year                                  XX,XXX.XX
  Brought forward                                X,XXX.XX
                                                              (XX,XXX.XX)

Chargeable Income                                             XXX,XXX.XX

Tax Payable:
  First RM150,000 @ 17% (SME rate)              XX,XXX.XX
  Balance @ 24%                                  X,XXX.XX
                                                               XX,XXX.XX

Less: Zakat rebate (max = tax payable)                         (X,XXX.XX)
Less: Tax deducted at source (S110)                              (XXX.XX)
Less: CP204 instalments paid                                  (XX,XXX.XX)

Tax Payable / (Refundable)                                     XX,XXX.XX
```

### 1.2 SME Rate Qualification (YA 2024)
A company qualifies for the preferential 17% rate on first RM150,000 if:
- Paid-up capital for ordinary shares <= RM2.5 million at beginning of basis period; AND
- Gross business income <= RM50 million

If not qualified: flat 24% on all chargeable income.

### 1.3 Non-Deductible Expenses — Common Items

| Expense | Treatment | ITA Reference |
|---|---|---|
| Accounting depreciation | Add back entirely. Replaced by capital allowances. | S33(1) |
| Entertainment | 50% disallowed unless wholly for business promotion | S33(1), Public Ruling 3/2008 |
| Private motor vehicle expenses | Restricted. See motor vehicle rules below. | S39(1)(m) |
| Penalties & fines | Not incurred in production of income | S33(1) |
| General bad debt provision | Not specific. Only specific provisions allowed. | S34(2) |
| Donations (general) | Not deductible unless to approved institution S44(6) | S44(6) |
| Zakat perniagaan | Not a deduction — claimed as rebate against tax | S6A(3) |
| Capital expenditure | Not revenue in nature | S33(1) |
| Pre-commencement expenses | Only deductible if incurred within 18 months before commencement | S33(1), Public Ruling 4/2022 |
| Club membership fees | Not deductible | S39(1)(l) |
| Domestic/private expenses | Not incurred in production of income | S39(1)(a) |

### 1.4 Motor Vehicle Restriction

| Vehicle Type | Cost Limit | CA Limit |
|---|---|---|
| Vehicle not on-the-road | RM100,000 | CA based on RM100,000 |
| Vehicle on-the-road, new, Malaysian | RM200,000 | CA based on RM200,000 |
| Vehicle on-the-road, above RM200,000 | RM200,000 cap | CA based on RM200,000 |

Running expenses for company vehicles used privately: 50% disallowed (unless log book kept proving 100% business use).

---

## PART 2: CAPITAL ALLOWANCES — SCHEDULE 3 ITA 1967

### 2.1 Rates

| Asset Category | Initial Allowance (IA) | Annual Allowance (AA) |
|---|---|---|
| Plant & Machinery (general) | 20% | 14% |
| Heavy Machinery | 20% | 20% |
| Motor Vehicle | 20% | 20% |
| Computer & IT Equipment | 20% | 20% (accelerated) |
| Office Equipment & Furniture | 20% | 10% |
| Small Value Assets (< RM2,000 each, per RM20,000 aggregate cap per YA) | 100% | - |
| Industrial Building | 10% | 3% |

### 2.2 Computation Structure

```
CAPITAL ALLOWANCE SCHEDULE
YA 2024

Asset       Cost      IA     Prior AA    Current AA    Accum CA    Residual
─────────────────────────────────────────────────────────────────────────────
Computer    1,523     305       -          305           610         913
Camera      7,300     -       1,460       1,460         5,840       1,460
...
─────────────────────────────────────────────────────────────────────────────
TOTAL       XX,XXX    X,XXX   XX,XXX      XX,XXX       XX,XXX      XX,XXX
```

### 2.3 Rules
- IA: only in the year of acquisition
- AA: every year the asset is in use
- Pro-rate: IA and AA are pro-rated if the asset is acquired/disposed during the year (use months-in-use method)
- Balancing Allowance (BA): if disposal proceeds < residual, the shortfall is a BA (deductible)
- Balancing Charge (BC): if disposal proceeds > residual, the excess is a BC (taxable). Max BC = total CA claimed.
- Unabsorbed CA: carried forward indefinitely (no time limit, but subject to S44(5A) restrictions for dormant companies)

---

## PART 3: FORM B — SOLE PROPRIETOR TAX

### 3.1 Structure
```
Form B — Income Tax Return for Individual with Business Income

Section B: Business Income
  Business Name: [name]
  Business Registration: [ROB number]

  Adjusted Income from Business           XXX,XXX.XX
  Less: Capital Allowances                (XX,XXX.XX)
  Statutory Income from Business           XX,XXX.XX

Section C: Other Income Sources (if any)
  Employment income                        XX,XXX.XX
  Rental income                             X,XXX.XX
  Interest/Dividend income                    XXX.XX

Aggregate Income                          XXX,XXX.XX
Less: Personal reliefs (claimed by taxpayer)
  Self                                      9,000.00
  Medical insurance                         3,000.00
  EPF (voluntary, max)                      4,000.00
  SOCSO                                       350.00
  Education (self)                          7,000.00
  Lifestyle                                 2,500.00
  ...

Chargeable Income                          XX,XXX.XX
Tax on chargeable income (progressive)      X,XXX.XX
Less: Zakat rebate                           (XXX.XX)
Less: Tax deducted at source                 (XXX.XX)
Tax Payable / (Refundable)                  X,XXX.XX
```

### 3.2 Individual Tax Rates (YA 2024)

| Chargeable Income (RM) | Rate | Cumulative Tax (RM) |
|---|---|---|
| 0 - 5,000 | 0% | 0 |
| 5,001 - 20,000 | 1% | 150 |
| 20,001 - 35,000 | 3% | 600 |
| 35,001 - 50,000 | 6% | 1,500 |
| 50,001 - 70,000 | 11% | 3,700 |
| 70,001 - 100,000 | 19% | 9,400 |
| 100,001 - 400,000 | 25% | 84,400 |
| 400,001 - 600,000 | 26% | 136,400 |
| 600,001 - 2,000,000 | 28% | 528,400 |
| Above 2,000,000 | 30% | - |

### 3.3 Key Differences from Form C
- Sole prop business income is combined with ALL other income sources
- Personal reliefs reduce chargeable income (companies don't get personal reliefs)
- Agent prepares the business income section only; personal reliefs are the taxpayer's responsibility
- Note: "Personal reliefs to be claimed by taxpayer on Form B submission. Business income section prepared as above."

---

## PART 4: FORM P — PARTNERSHIP TAX

### 4.1 Partnership Filing
- The partnership files **Form P** declaring total partnership income
- Each partner then files **Form B** (or Form BE if no business income) declaring their share of partnership profit
- Tax is paid at the INDIVIDUAL level, not partnership level

### 4.2 Profit Distribution
```
Partnership Net Profit (per accounts)          XX,XXX.XX

Tax Adjustments (same as Form C method):
  Add back non-deductible                       X,XXX.XX
  Less non-taxable                              (XXX.XX)
Adjusted Income                                XX,XXX.XX
Less: Capital Allowances                       (X,XXX.XX)
Divisible Income                               XX,XXX.XX

Distribution per profit-sharing ratio:
  Partner A (50%):                              X,XXX.XX
  Partner B (50%):                              X,XXX.XX
```

### 4.3 Partners' Salary & Interest on Capital
- If partnership agreement provides for partner salary or interest on capital:
  - These are treated as APPROPRIATIONS (not expenses)
  - Deducted before applying profit-sharing ratio
  - Added to the respective partner's share of income
  - For tax: already included in the divisible income, so no separate add-back needed

---

## PART 4A: FORM C — BERHAD (PUBLIC COMPANY)

### 4A.1 Key Differences from Sdn Bhd
- **No SME rate**: Berhad pays flat 24% on all chargeable income (no 17% tier).
- **Mandatory statutory audit**: All Berhad are audited. Audit adjustments (AJEs) must be incorporated.
- **Transfer pricing**: More likely to have related party transactions subject to S140A transfer pricing rules. Documentation required.
- **Withholding tax**: More likely to have foreign payments subject to S109/S109B withholding tax. Ensure WHT correctly deducted and remitted.
- **Group relief**: If part of a group (70%+ ownership), unabsorbed losses may be surrendered to profitable group companies per S44A.

### 4A.2 Computation Structure
Same as Part 1 (Form C for Sdn Bhd), except:
- Tax rate: flat 24% on all chargeable income
- Additional schedules may be needed: transfer pricing documentation, WHT schedule, group relief computation

---

## PART 4B: FORM C — NGO / TAX-EXEMPT BODIES

### 4B.1 Tax-Exempt Status

| Category | Basis | ITA Reference |
|----------|-------|---------------|
| Approved institution/organisation | Gazetted under S44(6) — donations to this entity are tax-deductible for donors | S44(6) |
| Religious institution | Income from religious activities exempt | S13(1)(a) |
| Charitable body | Exempt if income used solely for charitable objects | S44(6), Public Ruling 3/2019 |
| Trade/professional association | May be partially exempt | S44(6) |

### 4B.2 Computation — Exempt Body
Even if exempt, the NGO still files Form C. The computation shows:

```
Income (per Income & Expenditure Account)        XX,XXX.XX

Less: Exempt income
  Donations received                             (XX,XXX.XX)
  Membership fees                                 (X,XXX.XX)
  Government grants                               (X,XXX.XX)
  Activity income (if within charitable objects)   (X,XXX.XX)
                                                 -----------
Chargeable Income                                       0.00

Tax Payable                                             0.00
Exemption under: S44(6) / S13(1)(a) [as applicable]
```

### 4B.3 When Exemption Does NOT Apply
- **Business income** earned by the NGO (e.g., running a café, selling merchandise) may be taxable even if the entity is S44(6) approved, unless the business is directly related to its charitable objects.
- **Investment income** (dividends, interest, rental) — check the gazette order. Some exempt all income, others only exempt income from charitable objects.
- **If not gazetted**: the NGO is taxed as a normal company (24% flat rate). You must ASK: "Is this NGO gazetted under S44(6)? Please provide the gazette reference number."

### 4B.4 Cooperative-Specific Tax
Cooperatives are taxed under S10(1)(a) at a separate rate schedule:

| Chargeable Income (RM) | Rate |
|------------------------|------|
| First 30,000 | 0% |
| 30,001 – 60,000 | 5% |
| 60,001 – 100,000 | 8% |
| 100,001 – 150,000 | 12% |
| 150,001 – 250,000 | 15% |
| 250,001 – 500,000 | 18% |
| 500,001 – 750,000 | 21% |
| Above 750,000 | 24% |

Cooperatives must also set aside statutory reserves (min 15% of net profit) before computing distributable surplus.

---

## PART 5: COMMON TAX ADJUSTMENTS

### 5.1 Double Deduction Items
Expenses eligible for double deduction (claim 200%):
- Training expenses for disabled employees
- Expenditure on approved research (S34A)
- Export promotion expenses (certain industries)
- Hiring disabled persons

### 5.2 Special Deductions
- Further deduction for employee training (HRDF-approved)
- Environmental protection expenditure
- Approved donations (S44(6)): deductible up to 10% of aggregate income

### 5.3 Tax Incentives (Check Applicability)
- Pioneer Status (S127): 70-100% tax exemption for 5-10 years
- Reinvestment Allowance (Schedule 7A): 60% of qualifying capex
- Investment Tax Allowance (S127): 60-100% of qualifying capex
- MSC Malaysia status: various incentives for tech companies
- Halal industry incentives

**You must ASK the user**: "Does this client have any approved tax incentives (pioneer status, ITA, RA, MSC)?" Do not assume.

---

## PART 6: TAX ESTIMATION (CP204/CP500)

### For Companies (CP204)
- Filed by 30th day of month before FY starts
- Estimate must not be less than 85% of prior year's estimate (revised)
- If underpaid: penalty 10% on the shortfall
- Flag if estimated tax (based on current year computation) differs significantly from CP204 paid

### For Individuals (CP500)
- Issued by LHDN based on prior year assessment
- Payable bi-monthly (6 instalments)
- Agent notes the difference between CP500 paid and actual tax liability

---

## IMPLEMENTATION NOTES

1. **Agent generates tax computation as a separate Excel sheet** within the working papers workbook
2. **Schedules**: Tax adjustment, Capital allowance, S110 reconciliation (if applicable)
3. **PDF**: Tax computation is NOT included in the client-facing PDF financial statements (separate deliverable)
4. **Review**: Tax computation always requires user review before finalisation — flag any uncertain tax treatments
5. **Queries**: If tax treatment is unclear (e.g., is this expense deductible?), park the item and ask the user. Never assume deductibility.
