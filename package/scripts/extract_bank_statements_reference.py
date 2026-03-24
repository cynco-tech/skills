#!/usr/bin/env python3
"""
Extract [BANK_NAME] bank statements for [CLIENT_NAME] Sdn Bhd
FY: [FY_START] to [FY_END]
Uses Reducto API for OCR-based extraction from scanned PDFs

IMPORTANT: Set REDUCTO_API_KEY environment variable with your API credentials.
Example: export REDUCTO_API_KEY="your-api-key-here"
"""

import os, json, csv, re, time, sys
from pathlib import Path
import requests
from html.parser import HTMLParser

# API key from environment (example: REDUCTO_API_KEY="your-api-key-here")
API_KEY = os.environ.get("REDUCTO_API_KEY")
BASE_DIR = Path(".")
OUTPUT_CSV = BASE_DIR / "bank_transactions_fy.csv"
OUTPUT_SUMMARY = BASE_DIR / "bank_summary_fy.md"

# Files to process in chronological order
# Format: (month_label, relative_path)
# Add all months for the FY
STATEMENT_FILES = [
    ("[YYYY-MM]", "Bank Statements/[YYYY-MM].pdf"),
    ("[YYYY-MM]", "Bank Statements/[YYYY-MM].pdf"),
    ("[YYYY-MM]", "Bank Statements/[YYYY-MM].pdf"),
    # ... continue for all months in the FY
]

class TableParser(HTMLParser):
    """Parse HTML tables from Reducto output into rows."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.current_cell = ""
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.in_header = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
            self.current_table = []
        elif tag == "tr":
            self.in_row = True
            self.current_row = []
        elif tag in ("td", "th"):
            self.in_cell = True
            self.in_header = (tag == "th")
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
            self.current_table = []
        elif tag == "tr":
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
            self.current_row = []
        elif tag in ("td", "th"):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
            self.current_cell = ""

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data


def upload_file(filepath):
    """Upload a PDF to Reducto and return the file_id."""
    url = "https://platform.reducto.ai/upload"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    with open(filepath, 'rb') as f:
        resp = requests.post(url, headers=headers, files={"file": (filepath.name, f, "application/pdf")})
    resp.raise_for_status()
    return resp.json()["file_id"]


def parse_file(file_id):
    """Parse an uploaded file with Reducto."""
    url = "https://platform.reducto.ai/parse"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "document_url": file_id,
        "advanced_options": {
            "table_output_format": "html"
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()


def extract_tables_from_result(result):
    """Extract HTML tables from Reducto parse result."""
    chunks = result.get("result", {}).get("chunks", [])
    all_tables = []
    for chunk in chunks:
        content = chunk.get("content", "")
        if "<table" in content:
            parser = TableParser()
            parser.feed(content)
            all_tables.extend(parser.tables)
    return all_tables


def parse_amount(amount_str):
    """Parse transaction amount string like '200.00+' or '3,945.00-' into (credit, debit)."""
    if not amount_str:
        return 0.0, 0.0

    amount_str = amount_str.strip().replace(",", "").replace(" ", "")

    # Try to find amount with +/- suffix
    match = re.match(r'^([\d.]+)([+-])$', amount_str)
    if match:
        val = float(match.group(1))
        if match.group(2) == '+':
            return val, 0.0  # credit (inflow)
        else:
            return 0.0, val  # debit (outflow)

    # Try plain number (could be balance)
    try:
        return float(amount_str.replace(",", "")), 0.0
    except ValueError:
        return 0.0, 0.0


def parse_balance(bal_str):
    """Parse balance string like '15,266.41' into float."""
    if not bal_str:
        return None
    bal_str = bal_str.strip().replace(",", "").replace(" ", "")
    try:
        return float(bal_str)
    except ValueError:
        return None


def process_table_rows(tables, month_label):
    """Process extracted table rows into transaction records."""
    transactions = []

    for table in tables:
        for row in table:
            # Skip header rows
            if any("ENTRY DATE" in str(cell) or "TARIKH MASUK" in str(cell) for cell in row):
                continue

            # We expect 5 columns: entry_date, value_date, description, amount, balance
            if len(row) < 5:
                continue

            entry_date = row[0].strip()
            value_date = row[1].strip() if len(row) > 1 else ""
            description = row[2].strip() if len(row) > 2 else ""
            amount_str = row[3].strip() if len(row) > 3 else ""
            balance_str = row[4].strip() if len(row) > 4 else ""

            # Skip rows that are just headers, footers, or empty
            if not description and not amount_str and not balance_str:
                continue
            if "BEGINNING BALANCE" in description:
                bal = parse_balance(balance_str)
                if bal is not None:
                    transactions.append({
                        "month": month_label,
                        "date": "",
                        "description": "BEGINNING BALANCE",
                        "credit": 0.0,
                        "debit": 0.0,
                        "balance": bal,
                        "type": "OPENING"
                    })
                continue
            if "ENDING BALANCE" in description:
                bal = parse_balance(balance_str)
                if bal is not None:
                    transactions.append({
                        "month": month_label,
                        "date": "",
                        "description": "ENDING BALANCE",
                        "credit": 0.0,
                        "debit": 0.0,
                        "balance": bal,
                        "type": "CLOSING"
                    })
                continue
            if any(skip in description for skip in ["LEDGER BALANCE", "TOTAL DEBIT", "TOTAL CREDIT", "PROFIT OUTSTANDING", "BAKI LEGAR", "BAKI AKHIR"]):
                continue

            # Parse the amount
            credit, debit = parse_amount(amount_str)
            balance = parse_balance(balance_str)

            # Only add rows that have actual transaction data
            if (credit > 0 or debit > 0) and balance is not None:
                # Convert date format from DD/MM to YYYY-MM-DD
                full_date = ""
                if entry_date and "/" in entry_date:
                    parts = entry_date.split("/")
                    if len(parts) == 2:
                        day, month = parts
                        year = month_label[:4]
                        full_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

                transactions.append({
                    "month": month_label,
                    "date": full_date,
                    "description": description.replace("\n", " ").strip(),
                    "credit": credit,
                    "debit": debit,
                    "balance": balance,
                    "type": "TXN"
                })
            elif not entry_date and description and not amount_str:
                # This is a continuation line (sub-description)
                # Append to previous transaction's description
                if transactions and transactions[-1]["type"] == "TXN":
                    transactions[-1]["description"] += " | " + description.replace("\n", " ").strip()

    return transactions


def main():
    if not API_KEY:
        print("ERROR: REDUCTO_API_KEY not set")
        sys.exit(1)

    all_transactions = []
    monthly_summary = []

    for month_label, rel_path in STATEMENT_FILES:
        filepath = BASE_DIR / rel_path
        if not filepath.exists():
            print(f"WARNING: {filepath} not found, skipping")
            continue

        print(f"\n{'='*60}")
        print(f"Processing: {month_label} — {filepath.name}")
        print(f"{'='*60}")

        # Upload
        print("  Uploading...", end=" ", flush=True)
        file_id = upload_file(filepath)
        print(f"OK ({file_id[:30]}...)")

        # Parse
        print("  Parsing with OCR...", end=" ", flush=True)
        result = parse_file(file_id)
        print("OK")

        # Extract tables
        tables = extract_tables_from_result(result)
        print(f"  Found {len(tables)} table(s)")

        # Process rows
        txns = process_table_rows(tables, month_label)
        print(f"  Extracted {len(txns)} records")

        # Find opening and closing balances
        opening = next((t for t in txns if t["type"] == "OPENING"), None)
        closing = next((t for t in txns if t["type"] == "CLOSING"), None)
        actual_txns = [t for t in txns if t["type"] == "TXN"]

        total_credit = sum(t["credit"] for t in actual_txns)
        total_debit = sum(t["debit"] for t in actual_txns)

        summary = {
            "month": month_label,
            "opening": opening["balance"] if opening else None,
            "closing": closing["balance"] if closing else None,
            "total_inflow": total_credit,
            "total_outflow": total_debit,
            "txn_count": len(actual_txns)
        }
        monthly_summary.append(summary)

        print(f"  Opening: {summary['opening']}")
        print(f"  Closing: {summary['closing']}")
        print(f"  Inflows: {total_credit:,.2f}")
        print(f"  Outflows: {total_debit:,.2f}")
        print(f"  Transactions: {summary['txn_count']}")

        all_transactions.extend(txns)

        # Small delay between API calls
        time.sleep(1)

    # Write CSV
    print(f"\n{'='*60}")
    print(f"Writing {len(all_transactions)} records to CSV...")
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["month", "date", "description", "credit", "debit", "balance", "type"])
        writer.writeheader()
        writer.writerows(all_transactions)
    print(f"  Saved to: {OUTPUT_CSV}")

    # Write summary
    with open(OUTPUT_SUMMARY, 'w') as f:
        f.write("# [CLIENT_NAME] SDN BHD — Bank Statement Summary\n")
        f.write(f"## FY: [FY_START] to [FY_END]\n")
        f.write(f"## Account: [ACCOUNT_NUMBER] ([BANK_NAME])\n\n")
        f.write("| Month | Opening | Closing | Inflows | Outflows | Txn Count |\n")
        f.write("|-------|---------|---------|---------|----------|-----------|\n")
        for s in monthly_summary:
            f.write(f"| {s['month']} | {s['opening']:,.2f} | {s['closing']:,.2f} | {s['total_inflow']:,.2f} | {s['total_outflow']:,.2f} | {s['txn_count']} |\n")

        # Verify chain
        f.write("\n## Balance Chain Verification\n\n")
        chain_ok = True
        for i in range(1, len(monthly_summary)):
            prev_close = monthly_summary[i-1]["closing"]
            curr_open = monthly_summary[i]["opening"]
            match = "PASS" if abs(prev_close - curr_open) < 0.01 else "FAIL"
            if match == "FAIL":
                chain_ok = False
            f.write(f"- {monthly_summary[i-1]['month']} closing ({prev_close:,.2f}) → {monthly_summary[i]['month']} opening ({curr_open:,.2f}): **{match}**\n")

        f.write(f"\n**Overall chain: {'ALL PASS' if chain_ok else 'FAILURES DETECTED'}**\n")

        # Totals
        total_in = sum(s["total_inflow"] for s in monthly_summary)
        total_out = sum(s["total_outflow"] for s in monthly_summary)
        f.write(f"\n## FY Totals\n")
        f.write(f"- Total inflows: **RM {total_in:,.2f}**\n")
        f.write(f"- Total outflows: **RM {total_out:,.2f}**\n")
        f.write(f"- Net movement: **RM {total_in - total_out:,.2f}**\n")
        f.write(f"- Total transactions: **{sum(s['txn_count'] for s in monthly_summary)}**\n")

    print(f"  Summary saved to: {OUTPUT_SUMMARY}")
    print("\nDONE!")


if __name__ == "__main__":
    main()
