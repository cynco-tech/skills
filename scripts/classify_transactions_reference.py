#!/usr/bin/env python3
"""
Phase 2: Transaction Classification for [CLIENT_NAME] Sdn Bhd
FY: 1 Feb 2024 to 31 Jan 2025

Classifies each bank transaction to the firm's Chart of Accounts.

NOTE: All client names, employee names, and vendor names in this script are
placeholders. Replace with actual client data before use.
"""

import csv, re, os
from pathlib import Path
from collections import defaultdict

BASE = Path(".")
EXTRACTED = BASE / "extracted"
OUTPUT = BASE / "classified_transactions.csv"
SUMMARY = BASE / "classification_summary.md"

# ============================================================
# CHART OF ACCOUNTS MAPPING
# ============================================================
# Revenue
ACCT_EVENT_REVENUE   = "4000"   # Event/Show Revenue
ACCT_CAFE_REVENUE    = "4100"   # F&B/Cafe Revenue
ACCT_OTHER_INCOME    = "4200"   # Other Income

# COGS
ACCT_FB_COST         = "5100"   # Food & Beverage Cost (grocery, coffee, supplies, petty cash)

# Operating Expenses
ACCT_WAGES           = "5000"   # Salary & Wages
ACCT_SUBCONTRACTOR   = "5030"   # Subcontractor / Performer Costs
ACCT_RENTAL          = "5200"   # Rental Expense
ACCT_UTILITIES       = "5210"   # Utilities (electricity)
ACCT_REPAIR          = "5960"   # Repairs & Maintenance
ACCT_BANK_CHARGES    = "5980"   # Bank Charges (card charges)
ACCT_TRANSPORT       = "5900"   # Transport & Travelling
ACCT_ENTERTAINMENT   = "5800"   # Entertainment & Hospitality
ACCT_PRINTING        = "5950"   # Printing & Stationery
ACCT_MISC_EXPENSE    = "5970"   # Miscellaneous Expenses

# Balance Sheet
ACCT_BANK            = "1000"   # Cash at Bank (Maybank)
ACCT_TRADE_PAYABLE   = "2000"   # Trade Payables
ACCT_OTHER_PAYABLE   = "2200"   # Other Payables
ACCT_DUE_DIRECTOR    = "2300"   # Amount Due to Director
ACCT_DUE_SHAREHOLDER = "2400"   # Amount Due to Shareholders
ACCT_SUSPENSE        = "2900"   # Suspense Account

# ============================================================
# KNOWN PEOPLE/ENTITIES
# ============================================================
# EXAMPLE: Replace with actual client data

SALARY_PEOPLE = {
    "EMPLOYEE_1": "wages",
    "EMPLOYEE_2": "wages",
    "EMPLOYEE_3": "wages",
    "EMPLOYEE_4": "wages",
    "EMPLOYEE_5": "part_timer",
    "EMPLOYEE_6": "part_timer",
    "EMPLOYEE_7": "part_timer",
    "EMPLOYEE_8": "subcontractor",  # Example subcontractor
}

# EXAMPLE: List of performers/contractors. Keep only 2-3 actual names, replace rest with CONTRACTOR_N
PERFORMERS = [
    "CONTRACTOR_1", "CONTRACTOR_2", "CONTRACTOR_3",
    "CONTRACTOR_4", "CONTRACTOR_5", "CONTRACTOR_6",
    "CONTRACTOR_7", "CONTRACTOR_8", "CONTRACTOR_9",
    "CONTRACTOR_10", "CONTRACTOR_11", "CONTRACTOR_12",
    "CONTRACTOR_13", "CONTRACTOR_14",
]

# EXAMPLE: List of event clients. Keep only 2-3 actual names, replace rest with EVENT_CLIENT_N
EVENT_CLIENTS = [
    "EVENT_CLIENT_1", "EVENT_CLIENT_2", "EVENT_CLIENT_3",
    "EVENT_CLIENT_4", "EVENT_CLIENT_5", "EVENT_CLIENT_6",
    "EVENT_CLIENT_7", "EVENT_CLIENT_8", "EVENT_CLIENT_9",
    "EVENT_CLIENT_10", "EVENT_CLIENT_11", "EVENT_CLIENT_12",
    "EVENT_CLIENT_13", "EVENT_CLIENT_14",
]

# EXAMPLE: Replace with actual shareholders/directors
SHAREHOLDERS_DIRECTORS = [
    "DIRECTOR_1",  # Example: 60% shareholder
    "DIRECTOR_2",  # Example: 35% shareholder + director
    "DIRECTOR_3",  # Example: director (0% shares)
    "SHAREHOLDER_1",  # Example: related party
]

# EXAMPLE: Replace with actual suppliers. Keep only 2-3 examples.
FOOD_SUPPLIERS = [
    "SUPPLIER_1", "SUPPLIER_2", "SUPPLIER_3",
    "SUPPLIER_4", "SUPPLIER_5", "SUPPLIER_6",
    "SUPPLIER_7", "SUPPLIER_8", "SUPPLIER_9",
]


def classify(desc_raw, credit, debit):
    """
    Classify a transaction based on description and credit/debit amounts.
    Returns (account_code, account_name, category, notes)
    """
    desc = desc_raw.upper()
    is_inflow = credit > 0
    abs_amt = credit if is_inflow else debit

    # ==========================================
    # INFLOWS
    # ==========================================
    if is_inflow:
        # Card Sales (POS terminal) → Cafe Revenue
        # EXAMPLE: Replace terminal ID "[TERMINAL_ID]" with actual POS terminal ID
        if "DR/CARD SALES" in desc or "CR/CARD SALES" in desc or "[TERMINAL_ID] CR/CARD" in desc:
            return ACCT_CAFE_REVENUE, "F&B/Cafe Revenue", "cafe_card_sales", ""

        # QR Sales → Cafe Revenue
        if "QRCASA SALES" in desc:
            return ACCT_CAFE_REVENUE, "F&B/Cafe Revenue", "cafe_qr_sales", ""

        # StoreHub Settlements → Cafe Revenue (POS system settlement)
        if "STOREHUB" in desc:
            return ACCT_CAFE_REVENUE, "F&B/Cafe Revenue", "storehub_settlement", ""

        # CMS Payments from event clients → Event Revenue
        if "CMS" in desc and "PYMT" in desc:
            return ACCT_EVENT_REVENUE, "Event Revenue", "event_cms_payment", ""

        # Known event clients → Event Revenue
        for client in EVENT_CLIENTS:
            if client in desc:
                return ACCT_EVENT_REVENUE, "Event Revenue", "event_client", client

        # Shareholder/Director injections → Amount Due to Shareholder
        # EXAMPLE: Replace DIRECTOR_1, DIRECTOR_2, etc. with actual shareholder/director names
        for person in SHAREHOLDERS_DIRECTORS:
            if person in desc:
                if "DIRECTOR_1" in desc:
                    return ACCT_DUE_SHAREHOLDER, "Amount Due to Shareholders", "shareholder_injection", "DIRECTOR_1"
                elif "DIRECTOR_2" in desc:
                    return ACCT_DUE_DIRECTOR, "Amount Due to Director", "director_injection", "DIRECTOR_2"
                elif "DIRECTOR_3" in desc:
                    return ACCT_DUE_DIRECTOR, "Amount Due to Director", "director_injection", "DIRECTOR_3"
                elif "SHAREHOLDER_1" in desc:
                    return ACCT_DUE_SHAREHOLDER, "Amount Due to Shareholders", "related_party_injection", "SHAREHOLDER_1"

        # Event collaborator inflow → Event Revenue
        # EXAMPLE: Replace with actual collaborator names
        if "[COLLABORATOR_NAME]" in desc:
            return ACCT_EVENT_REVENUE, "Event Revenue", "event_collaborator", "[COLLABORATOR_NAME]"

        # Event-related transfer → Event Revenue
        # EXAMPLE: Replace with actual event coordinator/contact names
        if "[EVENT_COORDINATOR]" in desc:
            return ACCT_EVENT_REVENUE, "Event Revenue", "event_transfer", "[EVENT_COORDINATOR]"

        # DuitNow / Transfer To A/C
        if "TRANSFER TO A/C" in desc or "DUITNOW" in desc:
            # Check for event-related keywords
            event_keywords = ["DINNER", "SHOW", "JAZZ", "TICKET", "TIX", "BOOKING",
                              "DEPOSIT", "PARTY", "EVENT", "CONCERT", "PERFORMANCE",
                              "[EVENT_KEYWORD_1]", "[EVENT_KEYWORD_2]", "[EVENT_KEYWORD_3]", "[EVENT_KEYWORD_4]",
                              "ENGAGEMENT", "[EVENT_KEYWORD_5]"]
            for kw in event_keywords:
                if kw in desc:
                    return ACCT_EVENT_REVENUE, "Event Revenue", "event_transfer", kw

            # Large transfers (> RM200) from individuals → likely event-related
            if abs_amt >= 200:
                return ACCT_EVENT_REVENUE, "Event Revenue", "event_transfer_large", f"RM{abs_amt:.2f}"

            # Small transfers (≤ RM200) → cafe customer payment via DuitNow
            return ACCT_CAFE_REVENUE, "F&B/Cafe Revenue", "cafe_duitnow", ""

        # Inter-bank from known event clients
        if "INTER-BANK" in desc:
            for client in EVENT_CLIENTS:
                if client in desc:
                    return ACCT_EVENT_REVENUE, "Event Revenue", "event_interbank", client
            return ACCT_OTHER_INCOME, "Other Income", "interbank_other", ""

        # Catch-all inflow
        return ACCT_SUSPENSE, "Suspense", "unclassified_inflow", desc_raw[:50]

    # ==========================================
    # OUTFLOWS
    # ==========================================
    else:
        # Salary payments
        for person, role in SALARY_PEOPLE.items():
            if person in desc:
                if "SALARY" in desc or "GAJI" in desc:
                    return ACCT_WAGES, "Salary & Wages", f"salary_{role}", person
                elif "ADVANCE" in desc:
                    return ACCT_WAGES, "Salary & Wages", "advance_salary", person
                elif "GROCERY" in desc:
                    return ACCT_FB_COST, "Food & Beverage Cost", "grocery", person
                elif "PETTY CASH" in desc or "PETTYCASH" in desc:
                    return ACCT_FB_COST, "Food & Beverage Cost", "petty_cash", person
                elif "PART TIME" in desc or "PARTTIME" in desc or "PART TIMER" in desc or "PARTIMER" in desc:
                    return ACCT_WAGES, "Salary & Wages", "part_timer", person

        # Check for salary/wage keywords even without known person
        if "SALARY" in desc or "GAJI" in desc:
            return ACCT_WAGES, "Salary & Wages", "salary_other", ""
        if "ADVANCE SALARY" in desc or ("ADVANCE" in desc and any(p in desc for p in SALARY_PEOPLE)):
            return ACCT_WAGES, "Salary & Wages", "advance_salary", ""
        if "PART TIME" in desc or "PARTTIME" in desc or "PART TIMER" in desc:
            return ACCT_WAGES, "Salary & Wages", "part_timer", ""
        if "WAGES" in desc:
            return ACCT_WAGES, "Salary & Wages", "wages", ""

        # Petty Cash (general)
        if "PETTY CASH" in desc or "PETTYCASH" in desc:
            return ACCT_FB_COST, "Food & Beverage Cost", "petty_cash", ""

        # Grocery (general)
        if "GROCERY" in desc or "GROCERIES" in desc:
            return ACCT_FB_COST, "Food & Beverage Cost", "grocery", ""

        # Rental expense
        # EXAMPLE: Replace "[RENTAL_LOCATION]" and "G06" with actual rental venue location and reference
        if "[RENTAL_LOCATION]" in desc or ("RENTAL" in desc and "G06" in desc) or ("RENT" in desc and "G06" in desc):
            return ACCT_RENTAL, "Rental Expense", "rental_g06", "[RENTAL_LOCATION]"

        # Electricity
        # EXAMPLE: Replace "[UTILITY_PROVIDER]" with actual electricity provider name
        if "[UTILITY_PROVIDER]" in desc:
            return ACCT_UTILITIES, "Utilities", "electricity", "[UTILITY_PROVIDER]"

        # Performers / Show expenses
        for performer in PERFORMERS:
            if performer in desc:
                return ACCT_SUBCONTRACTOR, "Performance & Show Expenses", "performer", performer

        # Jazz/Show keywords
        if any(kw in desc for kw in ["JAZZNIGHT", "JAZZ NIGHT", "JAZNIGHT", "JQZZ NIGHT", "SHOW JAZZ"]):
            return ACCT_SUBCONTRACTOR, "Performance & Show Expenses", "show_expense", ""

        # Event collaborator payment
        # EXAMPLE: Replace with actual collaborator names
        if "[COLLABORATOR_NAME]" in desc:
            return ACCT_SUBCONTRACTOR, "Performance & Show Expenses", "event_collaborator", "[COLLABORATOR_NAME]"

        # Food & Beverage suppliers
        for supplier in FOOD_SUPPLIERS:
            if supplier in desc:
                return ACCT_FB_COST, "Food & Beverage Cost", "supplier", supplier

        # Coffee beans
        if "COFFEE BEANS" in desc or "BEANS" in desc:
            return ACCT_FB_COST, "Food & Beverage Cost", "coffee_beans", ""

        # Specialty ingredient supplier
        # EXAMPLE: Replace with actual ingredient name or supplier
        if "MATCHA" in desc or "[SPECIALTY_SUPPLIER]" in desc:
            return ACCT_FB_COST, "Food & Beverage Cost", "specialty_supply", ""

        # Food payment
        if "FOOD" in desc and ("CAKE" in desc or "MEAL" in desc or "PAYMENT" in desc):
            return ACCT_FB_COST, "Food & Beverage Cost", "food_purchase", ""

        # Repairs & Maintenance
        # EXAMPLE: Replace with actual repair vendor names
        if any(kw in desc for kw in ["REPAIR_VENDOR_1", "REPAIR_VENDOR_2", "[REPAIR_DESCRIPTION]", "REPAIR", "WIRING"]):
            return ACCT_REPAIR, "Repairs & Maintenance", "repair", ""

        # Card charges (small debits from card sales)
        if "DR/CARD SALES" in desc and abs_amt < 5:
            return ACCT_BANK_CHARGES, "Bank Charges", "card_charges", ""

        # Prior year creditor payment
        # EXAMPLE: Replace with actual creditor name
        if "[PRIOR_CREDITOR]" in desc:
            return ACCT_TRADE_PAYABLE, "Trade Payables", "creditor_payment", "[PRIOR_CREDITOR]"

        # Payment to specific person
        # EXAMPLE: Replace with actual person name
        if "[PERSON_NAME]" in desc:
            return ACCT_MISC_EXPENSE, "Miscellaneous Expenses", "payment", "[PERSON_NAME]"

        # Event refund
        # EXAMPLE: Replace with actual event contact name
        if "[EVENT_CONTACT]" in desc and "REFUND" in desc:
            return ACCT_EVENT_REVENUE, "Event Revenue", "refund", "[EVENT_CONTACT]"

        # Director expenses
        # EXAMPLE: Replace with actual director name
        if "DIRECTOR_3" in desc:
            if "DINNER" in desc or "PANEL" in desc:
                return ACCT_ENTERTAINMENT, "Entertainment & Hospitality", "director_dinner", "DIRECTOR_3"
            return ACCT_DUE_DIRECTOR, "Amount Due to Director", "director_repayment", "DIRECTOR_3"

        # Meal purchases
        # EXAMPLE: Replace with actual person name
        if "[MEAL_PURCHASER]" in desc:
            if "MEAL" in desc:
                return ACCT_FB_COST, "Food & Beverage Cost", "meals", "[MEAL_PURCHASER]"
            return ACCT_SUSPENSE, "Suspense", "unclassified", desc_raw[:50]

        # Catch-all outflow
        return ACCT_SUSPENSE, "Suspense", "unclassified_outflow", desc_raw[:50]


def main():
    # Input: bank_transactions_fy[YEAR].csv per DATA_SCHEMAS.md
    INPUT_CSV = BASE / "bank_transactions_fy.csv"

    all_classified = []

    if not INPUT_CSV.exists():
        print(f"ERROR: {INPUT_CSV} not found")
        return

    with open(INPUT_CSV) as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Skip OPENING/CLOSING rows per DATA_SCHEMAS.md
            row_type = r.get("type", "TXN")
            if row_type in ("OPENING", "CLOSING"):
                continue

            desc = r.get("description", "")
            credit = float(r.get("credit", "0") or "0")
            debit = float(r.get("debit", "0") or "0")

            acct_code, acct_name, category, notes = classify(desc, credit, debit)

            all_classified.append({
                "month": r.get("month", ""),
                "date": r.get("date", ""),
                "description": desc,
                "credit": credit,
                "debit": debit,
                "balance": r.get("balance", ""),
                "account_code": acct_code,
                "account_name": acct_name,
                "classification_method": category,
                "notes": notes
            })

    # Write classified CSV per DATA_SCHEMAS.md
    with open(OUTPUT, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "month", "date", "description", "credit", "debit", "balance",
            "account_code", "account_name", "classification_method", "notes"
        ])
        writer.writeheader()
        writer.writerows(all_classified)

    print(f"Classified {len(all_classified)} transactions → {OUTPUT}")

    # Generate summary
    by_account = defaultdict(lambda: {"count": 0, "debit": 0.0, "credit": 0.0})
    suspense_items = []

    for t in all_classified:
        acct = f"{t['account_code']} {t['account_name']}"
        by_account[acct]["count"] += 1
        by_account[acct]["credit"] += t["credit"]
        by_account[acct]["debit"] += t["debit"]

        if t["account_code"] == "2900":
            suspense_items.append(t)

    with open(SUMMARY, 'w') as f:
        f.write("# [CLIENT_NAME] — Transaction Classification Summary\n")
        f.write("## FY: [FY_START] to [FY_END]\n\n")
        f.write(f"**Total transactions classified: {len(all_classified)}**\n")
        f.write(f"**Suspense items: {len(suspense_items)}**\n\n")

        f.write("| Account | # Txns | Credits (In) | Debits (Out) | Net |\n")
        f.write("|---------|-------:|-----------:|-----------:|--------:|\n")

        total_credits = 0
        total_debits = 0
        for acct in sorted(by_account.keys()):
            data = by_account[acct]
            net = data["credit"] - data["debit"]
            f.write(f"| {acct} | {data['count']} | {data['credit']:,.2f} | {data['debit']:,.2f} | {net:,.2f} |\n")
            total_credits += data["credit"]
            total_debits += data["debit"]

        f.write(f"| **TOTAL** | **{len(all_classified)}** | **{total_credits:,.2f}** | **{total_debits:,.2f}** | **{total_credits - total_debits:,.2f}** |\n")

        if suspense_items:
            f.write(f"\n## Suspense Items ({len(suspense_items)} transactions)\n\n")
            f.write("| Date | Description | Credit | Debit | Notes |\n")
            f.write("|------|-------------|-------:|------:|-------|\n")
            for s in suspense_items:
                f.write(f"| {s['date']} | {s['description'][:60]} | {s['credit']:,.2f} | {s['debit']:,.2f} | {s['notes'][:40]} |\n")

    # Print summary to console
    print(f"\n{'='*80}")
    print("CLASSIFICATION SUMMARY")
    print(f"{'='*80}")
    print(f"{'Account':<45} {'#':>5} {'Credits':>12} {'Debits':>12} {'Net':>12}")
    print("-" * 90)
    for acct in sorted(by_account.keys()):
        data = by_account[acct]
        net = data["credit"] - data["debit"]
        print(f"{acct:<45} {data['count']:>5} {data['credit']:>12,.2f} {data['debit']:>12,.2f} {net:>12,.2f}")
    print("-" * 90)
    print(f"{'TOTAL':<45} {len(all_classified):>5} {total_credits:>12,.2f} {total_debits:>12,.2f} {total_credits-total_debits:>12,.2f}")
    print(f"\nSuspense items: {len(suspense_items)}")
    if suspense_items:
        print("\nSUSPENSE DETAILS:")
        for s in suspense_items:
            print(f"  {s['date']} | CR {s['credit']:>10,.2f} DR {s['debit']:>10,.2f} | {s['description'][:60]} | {s['notes']}")


if __name__ == "__main__":
    main()
