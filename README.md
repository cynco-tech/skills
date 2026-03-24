```
                                          _   _                                 _     __ _
   __ _  ___ ___ ___  _   _ _ __ | |_(_)_ __   __ _     __      _____  _ __| | __/ _| | _____      __
  / _` |/ __/ __/ _ \| | | | '_ \| __| | '_ \ / _` |____\ \ /\ / / _ \| '__| |/ / |_| |/ _ \ \ /\ / /
 | (_| | (_| (_| (_) | |_| | | | | |_| | | | | (_| |_____\ V  V / (_) | |  |   <|  _| | (_) \ V  V /
  \__,_|\___\___\___/ \__,_|_| |_|\__|_|_| |_|\__, |      \_/\_/ \___/|_|  |_|\_\_| |_|\___/ \_/\_/
                                               |___/
```

**a claude code skill that does your malaysian accounting.
the whole thing. bank statements in, financial statements out.**

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │   bank statements     ──►  trial balance                        │
  │   invoices & bills    ──►  income statement (P&L)               │
  │   payslips            ──►  balance sheet                        │
  │   fixed asset list    ──►  general ledger                       │
  │   prior year accounts ──►  tax computation                      │
  │                            working papers (.xlsx)               │
  │                            financial statements (.pdf)          │
  │                                                                 │
  │   accrual basis. MPERS / MFRS / ITA 1967 compliant.            │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
```

---

## who is this for

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │   accounting firms    automate your engagement workflow.          │
  │                       same process, every client, every time.    │
  │                       brand the output with your firm name.      │
  │                                                                  │
  │   bookkeepers         get proper accrual-basis accounts          │
  │                       from bank statements. no more manual       │
  │                       spreadsheets.                              │
  │                                                                  │
  │   founders / owners   do your own company accounts.              │
  │                       sdn bhd, sole prop, partnership —          │
  │                       all supported. hand the output to          │
  │                       your auditor or tax agent.                 │
  │                                                                  │
  │   solo accountants    one-person practice? this is your          │
  │                       second pair of hands.                      │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

---

## what is a claude code skill?

a skill is a structured set of instructions and reference files that teaches claude how to do a specific task. think of it like a runbook — but instead of a human following steps, claude follows them.

this skill lives in your `.claude/skills/` directory. when you tell claude to "process the accounts" or "start the accounting", it reads the skill, loads the right reference files at each phase, and walks through the full accounting pipeline.

you need [claude code](https://docs.anthropic.com/en/docs/claude-code) (anthropic's CLI agent) or a compatible agent runner that supports the skills format.

---

## the pipeline

8 phases. every engagement, every time. no shortcuts.

```
  ╔═══════════════════════════════════════════════════════════╗
  ║                                                           ║
  ║   PHASE 0   engagement setup                              ║
  ║   ───────   scan folder, detect entity type & FY,         ║
  ║             inventory what documents are available         ║
  ║                          │                                ║
  ║   PHASE 1   document extraction                           ║
  ║   ───────   OCR bank statements, parse invoices,          ║
  ║             extract payslips & bills                       ║
  ║                          │                                ║
  ║   PHASE 2   reconciliation & classification               ║
  ║   ───────   classify every transaction against COA,       ║
  ║             match bank ↔ invoices for accrual basis       ║
  ║                          │                                ║
  ║   PHASE 3   journal entries                               ║
  ║   ───────   opening balances, bank txns, payroll,         ║
  ║             depreciation, accruals, adjustments           ║
  ║                          │                                ║
  ║   PHASE 4   financial statements                          ║
  ║   ───────   GL → TB → P&L → balance sheet                ║
  ║                          │                                ║
  ║   PHASE 5   tax computation                               ║
  ║   ───────   Form C / Form B / Form P / S44(6) exempt     ║
  ║                          │                                ║
  ║   PHASE 6   quality control                               ║
  ║   ───────   mandatory checklist — math, data,             ║
  ║             compliance, completeness                      ║
  ║                          │                                ║
  ║   PHASE 7   output                                        ║
  ║   ───────   Excel working papers (openpyxl)               ║
  ║             PDF financial statements (reportlab)          ║
  ║                                                           ║
  ╚═══════════════════════════════════════════════════════════╝
```

---

## entity types

```
  ┌────────────────────────┬──────────────────────────┬──────────────────────┐
  │ entity                 │ framework                │ tax form             │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │ sole proprietor        │ accrual per S21A ITA '67 │ Form B               │
  │ partnership            │ accrual per S21A ITA '67 │ Form P + Form B/BE   │
  │ sdn bhd               │ MPERS                    │ Form C               │
  │ berhad                 │ MFRS                     │ Form C               │
  │ NGO / society / co-op  │ MPERS / Societies Act    │ Form C (maybe S44(6))│
  └────────────────────────┴──────────────────────────┴──────────────────────┘
```

---

## how it works

three layers. the agent only loads what it needs, when it needs it.

```
  layer 1 ─ trigger
  ─────────────────
  YAML frontmatter in SKILL.md.
  matches: "start the accounting", "process this client",
           "buat akaun", "siapkan akaun", etc.
            │
            ▼
  layer 2 ─ orchestration
  ────────────────────────
  the body of SKILL.md tells the agent:
  what to do, in what order, and which
  reference to load at each phase.
            │
            ▼
  layer 3 ─ references (on demand)
  ────────────────────────────────
  heavy policy files, schemas, checklists.
  only loaded when that phase is reached.
  keeps the context window lean.
```

---

## what's in the box

```
  accounting-workflow/
  │
  ├── SKILL.md ·························· the brain (trigger + pipeline)
  ├── LICENSE.txt ······················· MIT
  │
  ├── references/
  │   ├── FIRM_POLICY.md ················ COA, depreciation, statutory deductions, report format
  │   ├── WORKFLOW.md ··················· step-by-step for all 8 phases
  │   ├── ACCRUAL_RECONCILIATION.md ···· cash-to-accrual, invoice/bill matching
  │   ├── DATA_SCHEMAS.md ·············· CSV column specs for data handoff between phases
  │   ├── TAX_FRAMEWORK.md ············· Form C / B / P / exempt computation
  │   └── QC_CHECKLIST.md ·············· mandatory quality control checks
  │
  ├── scripts/
  │   ├── README.md ···················· architecture overview
  │   ├── requirements.txt ············ python dependencies
  │   ├── extract_bank_statements_reference.py
  │   ├── classify_transactions_reference.py
  │   ├── build_workpapers_reference.py
  │   ├── generate_pdf_reference.py
  │   └── generate_pdf_report_template.py
  │
  └── templates/
      ├── CLIENT_README_TEMPLATE.md ···· per-client engagement readme
      ├── coa_sdn_bhd.json ············· chart of accounts — sdn bhd (MPERS)
      ├── coa_berhad.json ·············· chart of accounts — berhad (MFRS)
      ├── coa_sole_prop.json ··········· chart of accounts — sole prop
      ├── coa_partnership.json ········· chart of accounts — partnership
      └── coa_ngo.json ················· chart of accounts — NGO
```

---

## getting started

**you need:**
- [claude code](https://docs.anthropic.com/en/docs/claude-code) or a compatible agent runner that supports skills
- python 3.10+ with `openpyxl`, `reportlab`, `pdfplumber` (`pip install -r scripts/requirements.txt`)
- a vision model for scanned bank statements (claude vision, openai, mistral, etc.)

**install:**

1. copy `accounting-workflow/` into your `.claude/skills/` directory.

2. personalise the output — find-and-replace these placeholders:

```
  ┌──────────────────────────┬─────────────────────────────────────────────┐
  │ placeholder              │ what to put                                 │
  ├──────────────────────────┼─────────────────────────────────────────────┤
  │ [FIRM_NAME]              │ your name, company, or practice name        │
  │ [CA_REGISTRATION]        │ CA reg number — or delete if not applicable │
  │ [FIRM_EMAIL]             │ your contact email                          │
  │ [PARTNER_NAME]           │ your name or the person signing off         │
  │ [PARTNER_CREDENTIALS]    │ credentials (CA(M), CPA) — or delete       │
  └──────────────────────────┴─────────────────────────────────────────────┘
```

   these control the branding on your PDF cover pages, Excel headers, and footers. fill in what applies, delete what doesn't. there's no wrong answer here — a founder can put their company name, a bookkeeper can put their practice name, a firm can put their CA registration.

   quickest way: `grep -r "\[FIRM_NAME\]" .` then find-and-replace.

3. review `references/FIRM_POLICY.md` — adjust depreciation rates, materiality thresholds, report format if yours differ from the defaults.

4. review `templates/coa_*.json` — standard malaysian COA structure, but you might want to add or rename accounts for your industry.

**prepare your folder:**

```
  my-client/
  ├── Bank Statements/
  │   ├── 2024-01.pdf
  │   ├── 2024-02.pdf
  │   └── ... (all months for the FY)
  ├── Payslips/          (optional — if employees exist)
  ├── Invoices/          (optional — helps with accrual accuracy)
  ├── Bills/             (optional — helps with accrual accuracy)
  ├── Fixed Assets/      (optional — asset register or purchase invoices)
  └── Prior Year/        (optional — last year's accounts or audit report)
```

bank statements are the only hard requirement. everything else improves accuracy but isn't blocking.

**run it:**

point claude at a folder with bank statements and say:

```
  "process the accounts for this client"
```

or if it's your own company:

```
  "do the accounts for my company"
```

the skill activates and walks you through the pipeline, phase by phase.

---

## customise

```
  ┌──────────────────────────────────┬──────────────────────────────────────┐
  │ what to change                   │ where                                │
  ├──────────────────────────────────┼──────────────────────────────────────┤
  │ accounting policies, rates,      │ references/FIRM_POLICY.md            │
  │ materiality, report format       │                                      │
  │                                  │                                      │
  │ chart of accounts                │ templates/coa_*.json                 │
  │                                  │                                      │
  │ python scripts (adapt per client)│ scripts/                             │
  │                                  │                                      │
  │ trigger phrases                  │ SKILL.md description field           │
  └──────────────────────────────────┴──────────────────────────────────────┘
```

the pipeline phases and QC checklist follow MPERS, MFRS, and ITA 1967. you generally don't need to touch those unless the regulations change.

---

## privacy & data

- **all processing is local.** your data stays on your machine. nothing is sent anywhere except OCR API calls if you use an external OCR service for scanned PDFs.
- **client data is excluded from git.** the `.gitignore` blocks `.xlsx`, `.pdf`, `.csv`, and other data files. never commit client data.
- **no telemetry.** no analytics, no tracking, no phoning home.

---

## faq

**what is this exactly?**
a claude code skill — a structured prompt + reference files that teaches claude how to do a full malaysian accounting engagement. you drop it in, point claude at a client folder, and it does the work.

**do i need to be an accountant to use this?**
you need enough accounting knowledge to review the output and answer the skill's questions (it will ask about things it can't classify). you don't need to be a chartered accountant. founders doing their own books, bookkeepers, and accounting students can all use this — but someone with accounting knowledge should review the final output.

**do i need to be a programmer to use this?**
nope. if you can use claude code, you can use this. the scripts in `scripts/` are reference code for when you want to understand how something works under the hood — you don't need to run them manually.

**do i need a CA registration to use this?**
no. the `[CA_REGISTRATION]` placeholder is optional. if you're a firm, fill it in. if you're a founder or bookkeeper doing your own accounts, leave it blank or remove it from the templates.

**i'm a founder — can i use this for my own sdn bhd?**
yes. point it at your bank statements, answer its questions, and you'll get working papers + financial statements you can hand to your auditor or tax agent.

**will this work for my sole prop / partnership / sdn bhd / berhad / NGO?**
yes. all five entity types are supported, each with the correct framework (S21A / MPERS / MFRS / Societies Act) and tax form (Form B / P / C / exempt).

**is it accrual basis or cash basis?**
accrual. always. bank statements are cash-basis data — the skill reconciles them against invoices and bills to produce proper accrual-basis financials. this is mandatory under S21A ITA 1967 for all entity types.

**what if i only have bank statements, no invoices?**
the skill handles three tiers: full documents (bank + invoices + bills), partial documents (bank + some supporting docs), and bank-only (with an interview process to fill in the gaps). it works with what you have and flags what's missing.

**what if something can't be classified?**
it goes to account 2900 (suspense) and gets flagged in the queries & notes sheet. the skill never guesses. it parks unknowns and keeps going.

**does it handle EPF, SOCSO, EIS, PCB?**
yes. employer and employee rates are built into FIRM_POLICY.md. it even checks whether the employer absorbs employee contributions (some do — the skill reads payslips to determine the actual structure).

**what about capital allowances and depreciation?**
both. accounting depreciation (straight-line, per MPERS/MFRS) and tax capital allowances (per Schedule 3 ITA 1967) are separate computations. the skill handles them independently.

**does it handle trading businesses with inventory?**
yes. COA templates include COGS/Purchases and stock accounts. if stock records are provided, it computes closing stock. if not, it asks for the figure from a physical count. see edge case 8a in FIRM_POLICY.md.

**will this replace my auditor?**
no. this produces management accounts and working papers. it doesn't audit. it does, however, produce accounts clean enough that your auditor will have a much easier time.

**can i use this for my own firm's branding?**
that's what the placeholders are for. replace `[FIRM_NAME]` and friends with your details, and every output — Excel, PDF, cover pages — carries your branding.

**can i modify and redistribute this?**
yes. MIT license. do what you want with it.

**is this production-tested?**
it was built from a real engagement workflow at a malaysian chartered accounting firm. the pipeline, COA structure, tax computations, and QC checklist have all been used on actual client work.

**what about e-invoicing / MyInvois?**
not yet built in. contributions welcome.

**will this make me a better accountant?**
legally we cannot guarantee that it will, but...

---

## contributing

contributions welcome. open an issue or PR.

areas where help would be particularly valuable: SST handling, e-invoicing (MyInvois) integration, MFRS 16 lease accounting, COA templates for specialised industries (construction, F&B, manufacturing), and adapting the skill for non-Malaysian jurisdictions.

---

```
  MIT License
  Copyright (c) 2025 Cynco Sdn. Bhd. (1588139-X)
  https://cynco.ai
```
