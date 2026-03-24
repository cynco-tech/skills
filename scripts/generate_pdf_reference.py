#!/usr/bin/env python3
"""
[CLIENT_NAME] — FY[YEAR] Financial Statements PDF Generator
Generates a professional PDF with:
  - Cover page
  - Table of Contents
  - Statement of Comprehensive Income
  - Statement of Financial Position
  - Trial Balance
  - General Ledger
"""

import sys
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict, OrderedDict
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, NextPageTemplate,
)
from reportlab.lib import colors

# Import data from build_workpapers.py
from build_workpapers import (
    COA, OPENING_BALANCES, CLASSIFICATION_MAP, PRIOR_YEAR_SETTLEMENTS,
    load_transactions, d, D, BASE,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OUTPUT = BASE / "[CLIENT]_FY[YEAR]_Financial_Statements.pdf"
PAGE_W, PAGE_H = A4  # 595.27 x 841.89 points
MARGIN = 2.5 * cm    # ~71 points
FRAME_W = PAGE_W - 2 * MARGIN
FRAME_H = PAGE_H - 2 * MARGIN

COMPANY_NAME = "[CLIENT_NAME]"
REG_NO = "[SSM_REGISTRATION]"
FY_PERIOD = "FOR THE FINANCIAL YEAR ENDED 31 JANUARY 2025"
FY_PERIOD_LONG = "FOR THE FINANCIAL YEAR\n1 FEBRUARY 2024 TO 31 JANUARY 2025"


# ---------------------------------------------------------------------------
# Number formatting
# ---------------------------------------------------------------------------
def fmt(n, show_zero=False):
    """Format number: comma-separated, 2dp, brackets for negatives."""
    if isinstance(n, Decimal):
        val = float(n)
    else:
        val = float(n)
    if abs(val) < 0.005 and not show_zero:
        return "-"
    if val < 0:
        return f"({abs(val):,.2f})"
    return f"{val:,.2f}"


def fmt_or_blank(n):
    """Format number, return empty string for zero."""
    if isinstance(n, Decimal):
        val = float(n)
    else:
        val = float(n)
    if abs(val) < 0.005:
        return ""
    if val < 0:
        return f"({abs(val):,.2f})"
    return f"{val:,.2f}"


# ---------------------------------------------------------------------------
# Computation — duplicated from build_workpapers.py __main__ block
# ---------------------------------------------------------------------------
def compute_all():
    """Run full computation: JEs, GL, TB, IS, BS. Return all data."""
    all_txns = load_transactions()

    # --- Journal Entry Generation ---
    journal_entries = []
    je_num = 0

    # JE-001: Opening Balances
    je_num += 1
    for acct, bal in OPENING_BALANCES.items():
        if bal == d("0"):
            continue
        acct_info = COA[acct]
        if bal > 0:
            journal_entries.append({
                "je_num": je_num, "date": "2024-02-01",
                "acct": acct, "acct_name": acct_info["name"],
                "description": "Opening balance",
                "dr": bal, "cr": d("0"),
            })
        else:
            journal_entries.append({
                "je_num": je_num, "date": "2024-02-01",
                "acct": acct, "acct_name": acct_info["name"],
                "description": "Opening balance",
                "dr": d("0"), "cr": abs(bal),
            })

    # JE-002 to JE-N: Bank Transactions
    for txn in all_txns:
        je_num += 1
        gl_acct = CLASSIFICATION_MAP.get(txn["acct_code"], txn["acct_code"])
        gl_info = COA.get(gl_acct, {"name": f"Unknown ({gl_acct})", "type": "Unknown"})
        amt = d(txn["amount"])
        desc = txn["description"][:80]

        if amt > 0:
            journal_entries.append({
                "je_num": je_num, "date": txn["date"],
                "acct": "1000", "acct_name": COA["1000"]["name"],
                "description": desc, "dr": amt, "cr": d("0"),
            })
            journal_entries.append({
                "je_num": je_num, "date": txn["date"],
                "acct": gl_acct, "acct_name": gl_info["name"],
                "description": desc, "dr": d("0"), "cr": amt,
            })
        elif amt < 0:
            abs_amt = abs(amt)
            journal_entries.append({
                "je_num": je_num, "date": txn["date"],
                "acct": gl_acct, "acct_name": gl_info["name"],
                "description": desc, "dr": abs_amt, "cr": d("0"),
            })
            journal_entries.append({
                "je_num": je_num, "date": txn["date"],
                "acct": "1000", "acct_name": COA["1000"]["name"],
                "description": desc, "dr": d("0"), "cr": abs_amt,
            })

    # JE: Depreciation Music
    je_num += 1
    journal_entries.append({
        "je_num": je_num, "date": "2025-01-31",
        "acct": "5300", "acct_name": COA["5300"]["name"],
        "description": "Annual depreciation - Music System & Equipment @ 20% SL",
        "dr": d("12070.78"), "cr": d("0"),
    })
    journal_entries.append({
        "je_num": je_num, "date": "2025-01-31",
        "acct": "1399", "acct_name": COA["1399"]["name"],
        "description": "Annual depreciation - Music System & Equipment @ 20% SL",
        "dr": d("0"), "cr": d("12070.78"),
    })

    # JE: Depreciation Computer
    je_num += 1
    journal_entries.append({
        "je_num": je_num, "date": "2025-01-31",
        "acct": "5310", "acct_name": COA["5310"]["name"],
        "description": "Annual depreciation - Computer & POS @ 20% SL",
        "dr": d("713.60"), "cr": d("0"),
    })
    journal_entries.append({
        "je_num": je_num, "date": "2025-01-31",
        "acct": "1398", "acct_name": COA["1398"]["name"],
        "description": "Annual depreciation - Computer & POS @ 20% SL",
        "dr": d("0"), "cr": d("713.60"),
    })

    # JE: Prepayment Consumed
    je_num += 1
    journal_entries.append({
        "je_num": je_num, "date": "2024-05-31",
        "acct": "5970", "acct_name": COA["5970"]["name"],
        "description": "Prepayment consumed - Secretarial fee Feb-May 24",
        "dr": d("333.33"), "cr": d("0"),
    })
    journal_entries.append({
        "je_num": je_num, "date": "2024-05-31",
        "acct": "1210", "acct_name": COA["1210"]["name"],
        "description": "Prepayment consumed - Secretarial fee Feb-May 24",
        "dr": d("0"), "cr": d("333.33"),
    })

    # JE: Accrued Audit Fee
    je_num += 1
    journal_entries.append({
        "je_num": je_num, "date": "2025-01-31",
        "acct": "5520", "acct_name": COA["5520"]["name"],
        "description": "Accrued audit fee FY ending [FY_END]",
        "dr": d("3000.00"), "cr": d("0"),
    })
    journal_entries.append({
        "je_num": je_num, "date": "2025-01-31",
        "acct": "2100", "acct_name": COA["2100"]["name"],
        "description": "Accrued audit fee FY ending [FY_END]",
        "dr": d("0"), "cr": d("3000.00"),
    })

    # JE: Accrued Accounting Fee
    je_num += 1
    journal_entries.append({
        "je_num": je_num, "date": "2025-01-31",
        "acct": "5510", "acct_name": COA["5510"]["name"],
        "description": "Accrued accounting fee FY ending [FY_END]",
        "dr": d("2000.00"), "cr": d("0"),
    })
    journal_entries.append({
        "je_num": je_num, "date": "2025-01-31",
        "acct": "2100", "acct_name": COA["2100"]["name"],
        "description": "Accrued accounting fee FY ending [FY_END]",
        "dr": d("0"), "cr": d("2000.00"),
    })

    # --- General Ledger ---
    gl = defaultdict(list)
    gl_balance = defaultdict(lambda: d("0"))
    for je in journal_entries:
        acct = je["acct"]
        net = je["dr"] - je["cr"]
        gl_balance[acct] += net
        gl[acct].append({
            "je_num": je["je_num"],
            "date": je["date"],
            "description": je["description"],
            "dr": je["dr"],
            "cr": je["cr"],
            "balance": gl_balance[acct],
        })

    # --- Trial Balance ---
    tb = OrderedDict()
    for acct in sorted(gl_balance.keys()):
        bal = gl_balance[acct]
        if abs(bal) < Decimal("0.01"):
            continue
        acct_info = COA.get(acct, {"name": f"Unknown ({acct})", "type": "Unknown"})
        dr_val = bal if bal > 0 else d("0")
        cr_val = abs(bal) if bal < 0 else d("0")
        tb[acct] = {
            "name": acct_info["name"],
            "type": acct_info["type"],
            "dr": dr_val,
            "cr": cr_val,
            "balance": bal,
        }

    tb_total_dr = sum(v["dr"] for v in tb.values())
    tb_total_cr = sum(v["cr"] for v in tb.values())

    # --- Income Statement ---
    revenue_accts = {k: v for k, v in tb.items() if k.startswith("4")}
    expense_accts = {k: v for k, v in tb.items() if k.startswith("5") or k.startswith("6")}
    total_revenue = sum(v["cr"] - v["dr"] for v in revenue_accts.values())
    cogs = tb.get("5050", {"dr": d("0"), "cr": d("0")})
    cogs_amt = cogs["dr"] - cogs["cr"]
    gross_profit = total_revenue - cogs_amt
    total_opex = sum(v["dr"] - v["cr"] for k, v in expense_accts.items() if k != "5050")
    net_profit = gross_profit - total_opex

    # --- Balance Sheet ---
    cash_bank = gl_balance.get("1000", d("0"))
    cash_hand = gl_balance.get("1010", d("0"))
    trade_recv = gl_balance.get("1100", d("0"))
    prepayments = gl_balance.get("1210", d("0"))
    deposits = gl_balance.get("1220", d("0"))
    total_ca = cash_bank + cash_hand + trade_recv + prepayments + deposits

    ppe_music_cost = gl_balance.get("1300", d("0"))
    ppe_comp_cost = gl_balance.get("1310", d("0"))
    accum_dep_music = gl_balance.get("1399", d("0"))
    accum_dep_comp = gl_balance.get("1398", d("0"))
    ppe_music_net = ppe_music_cost + accum_dep_music
    ppe_comp_net = ppe_comp_cost + accum_dep_comp
    total_nca = ppe_music_net + ppe_comp_net
    total_assets = total_ca + total_nca

    trade_pay = abs(gl_balance.get("2000", d("0")))
    other_pay = abs(gl_balance.get("2100", d("0")))
    epf_pay = abs(gl_balance.get("2110", d("0")))
    socso_pay = abs(gl_balance.get("2120", d("0")))
    eis_pay = abs(gl_balance.get("2130", d("0")))
    due_director = abs(gl_balance.get("2350", d("0")))
    due_shareholders = abs(gl_balance.get("2360", d("0")))
    suspense = abs(gl_balance.get("2900", d("0")))
    total_cl = (trade_pay + other_pay + epf_pay + socso_pay + eis_pay
                + due_director + due_shareholders + suspense)

    share_cap = abs(gl_balance.get("3000", d("0")))
    retained = gl_balance.get("3200", d("0"))  # DR balance = positive (loss)
    accum_loss = retained - net_profit  # total accumulated loss (net_profit is negative => loss adds)
    # Actually: accumulated loss = prior loss (retained, positive = loss) + current year loss
    # net_profit is negative when loss, so accum_loss_total = retained + abs(net_profit) if loss
    # But for BS: Total Equity = Share Capital - Accumulated Loss
    # retained is DR 58547.35 (prior accumulated loss)
    # net_profit is negative (loss)
    # accumulated_loss_total = retained - net_profit  (since net_profit is negative, this adds)
    # But let's compute total equity directly:
    total_equity = share_cap - retained + net_profit
    # Accumulated loss for display = retained - net_profit (when net_profit < 0, this is retained + |net_profit|)
    accum_loss_display = retained - net_profit  # positive = loss to show in brackets

    total_eq_liab = total_equity + total_cl

    return {
        "journal_entries": journal_entries,
        "gl": gl,
        "gl_balance": gl_balance,
        "tb": tb,
        "tb_total_dr": tb_total_dr,
        "tb_total_cr": tb_total_cr,
        "revenue_accts": revenue_accts,
        "expense_accts": expense_accts,
        "total_revenue": total_revenue,
        "cogs_amt": cogs_amt,
        "gross_profit": gross_profit,
        "total_opex": total_opex,
        "net_profit": net_profit,
        "cash_bank": cash_bank,
        "cash_hand": cash_hand,
        "trade_recv": trade_recv,
        "prepayments": prepayments,
        "deposits": deposits,
        "total_ca": total_ca,
        "ppe_music_cost": ppe_music_cost,
        "ppe_comp_cost": ppe_comp_cost,
        "accum_dep_music": accum_dep_music,
        "accum_dep_comp": accum_dep_comp,
        "ppe_music_net": ppe_music_net,
        "ppe_comp_net": ppe_comp_net,
        "total_nca": total_nca,
        "total_assets": total_assets,
        "trade_pay": trade_pay,
        "other_pay": other_pay,
        "epf_pay": epf_pay,
        "socso_pay": socso_pay,
        "eis_pay": eis_pay,
        "due_director": due_director,
        "due_shareholders": due_shareholders,
        "suspense": suspense,
        "total_cl": total_cl,
        "share_cap": share_cap,
        "retained": retained,
        "accum_loss_display": accum_loss_display,
        "total_equity": total_equity,
        "total_eq_liab": total_eq_liab,
    }


# ---------------------------------------------------------------------------
# Page number tracking
# ---------------------------------------------------------------------------
class PageNumberTracker:
    """Track page numbers during document build."""
    def __init__(self):
        self.page_count = 0
        self.section_pages = {}  # section_name -> starting page

    def on_page(self, canvas, doc):
        """Called for every page (content pages, not cover)."""
        self.page_count = doc.page
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        # Left footer
        canvas.drawString(
            MARGIN, 1.2 * cm,
            "[FIRM_NAME] Chartered Accountants ([CA_REGISTRATION])"
        )
        # Right footer - page number
        canvas.drawRightString(
            PAGE_W - MARGIN, 1.2 * cm,
            f"Page {doc.page}"
        )
        canvas.restoreState()

    def on_cover_page(self, canvas, doc):
        """No footer on cover page."""
        pass


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "CoverTitle", fontName="Helvetica-Bold", fontSize=16,
        alignment=TA_CENTER, leading=22, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "CoverSubtitle", fontName="Helvetica", fontSize=12,
        alignment=TA_CENTER, leading=16, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "CoverBody", fontName="Helvetica", fontSize=11,
        alignment=TA_CENTER, leading=15, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "CoverFooter", fontName="Helvetica", fontSize=10,
        alignment=TA_CENTER, leading=14, spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        "SectionTitle", fontName="Helvetica-Bold", fontSize=12,
        alignment=TA_CENTER, leading=16, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "SectionSubtitle", fontName="Helvetica", fontSize=10,
        alignment=TA_CENTER, leading=14, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "CategoryHeader", fontName="Helvetica-Bold", fontSize=10,
        alignment=TA_LEFT, leading=14, spaceAfter=2, spaceBefore=8,
    ))
    styles.add(ParagraphStyle(
        "NormalLeft", fontName="Helvetica", fontSize=9,
        alignment=TA_LEFT, leading=12,
    ))
    styles.add(ParagraphStyle(
        "NormalRight", fontName="Helvetica", fontSize=9,
        alignment=TA_RIGHT, leading=12,
    ))
    styles.add(ParagraphStyle(
        "SmallLeft", fontName="Helvetica", fontSize=8,
        alignment=TA_LEFT, leading=10,
    ))
    styles.add(ParagraphStyle(
        "SmallRight", fontName="Helvetica", fontSize=8,
        alignment=TA_RIGHT, leading=10,
    ))
    styles.add(ParagraphStyle(
        "TOCEntry", fontName="Helvetica", fontSize=11,
        alignment=TA_LEFT, leading=20,
    ))
    styles.add(ParagraphStyle(
        "GLHeader", fontName="Helvetica-Bold", fontSize=9,
        alignment=TA_LEFT, leading=12, spaceBefore=10, spaceAfter=4,
    ))
    return styles


# ---------------------------------------------------------------------------
# Helper: create a financial table row for IS/BS
# ---------------------------------------------------------------------------
def _underline_style():
    """Single underline under the amount column."""
    return ('LINEBELOW', (-1, -1), (-1, -1), 0.5, colors.black)


def _double_underline_style():
    """Double underline under the amount column."""
    return ('LINEBELOW', (-1, -1), (-1, -1), 1.0, colors.black)


# ---------------------------------------------------------------------------
# Build Cover Page
# ---------------------------------------------------------------------------
def build_cover(styles):
    """Return flowables for cover page."""
    elements = []
    # Vertical spacer to center content
    elements.append(Spacer(1, 6 * cm))

    elements.append(Paragraph(COMPANY_NAME, styles["CoverTitle"]))
    elements.append(Paragraph(
        f"Registration No. {REG_NO}", styles["CoverSubtitle"]
    ))
    elements.append(Paragraph("(Incorporated in Malaysia)", styles["CoverSubtitle"]))
    elements.append(Spacer(1, 2.5 * cm))
    elements.append(Paragraph("REPORT AND FINANCIAL STATEMENTS", styles["CoverTitle"]))
    elements.append(Paragraph(FY_PERIOD_LONG, styles["CoverSubtitle"]))

    # Push footer to bottom
    elements.append(Spacer(1, 8 * cm))

    elements.append(Paragraph("Prepared by:", styles["CoverFooter"]))
    elements.append(Paragraph("<b>[FIRM_NAME]</b>", styles["CoverFooter"]))
    elements.append(Paragraph("Chartered Accountants ([CA_REGISTRATION])", styles["CoverFooter"]))
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph("Partner: [PARTNER_NAME]", styles["CoverFooter"]))
    elements.append(Paragraph(
        "[PARTNER_CREDENTIALS]", styles["CoverFooter"]
    ))
    elements.append(Paragraph("[FIRM_EMAIL]", styles["CoverFooter"]))

    elements.append(NextPageTemplate("content"))
    elements.append(PageBreak())
    return elements


# ---------------------------------------------------------------------------
# Build Table of Contents
# ---------------------------------------------------------------------------
def build_toc(styles, page_map):
    """Return flowables for TOC."""
    elements = []
    elements.append(Spacer(1, 1 * cm))
    elements.append(Paragraph("TABLE OF CONTENTS", styles["SectionTitle"]))
    elements.append(Spacer(1, 1.5 * cm))

    toc_data = [
        ["", "", "Page"],
        ["1.", "Statement of Comprehensive Income", str(page_map.get("is", 3))],
        ["2.", "Statement of Financial Position", str(page_map.get("bs", 4))],
        ["3.", "Trial Balance", str(page_map.get("tb", 5))],
        ["4.", "General Ledger", f"{page_map.get('gl', 6)}"],
    ]

    col_widths = [1.2 * cm, 10 * cm, 2 * cm]
    toc_table = Table(toc_data, colWidths=col_widths)
    toc_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
    ]))
    elements.append(toc_table)
    elements.append(PageBreak())
    return elements


# ---------------------------------------------------------------------------
# Build Title Block (reused for IS, BS, TB)
# ---------------------------------------------------------------------------
def build_title_block(styles, statement_title, subtitle=None):
    """Company name, reg no, statement title."""
    elements = []
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph(COMPANY_NAME, styles["SectionTitle"]))
    elements.append(Paragraph(
        f"(Registration No. {REG_NO})", styles["SectionSubtitle"]
    ))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph(statement_title, styles["SectionTitle"]))
    if subtitle:
        elements.append(Paragraph(subtitle, styles["SectionSubtitle"]))
    elements.append(Spacer(1, 0.8 * cm))
    return elements


# ---------------------------------------------------------------------------
# Build Income Statement
# ---------------------------------------------------------------------------
def build_income_statement(styles, data):
    """Return flowables for the Statement of Comprehensive Income."""
    elements = build_title_block(
        styles,
        "STATEMENT OF COMPREHENSIVE INCOME",
        FY_PERIOD
    )

    # Build the IS as a table with: [Label, Sub-amount, Total-amount]
    # Column widths: label=10cm, sub_amount=3cm, total_amount=3cm
    col_widths = [10 * cm, 3.5 * cm, 3.5 * cm]

    rows = []
    style_commands = []
    row_idx = 0

    def add_row(label, sub_amt="", total_amt="", bold=False, indent=0,
                underline=False, double_underline=False, label_font_size=9):
        nonlocal row_idx
        prefix = "    " * indent
        font = "Helvetica-Bold" if bold else "Helvetica"
        rows.append([f"{prefix}{label}", sub_amt, total_amt])
        style_commands.append(('FONTNAME', (0, row_idx), (0, row_idx), font))
        style_commands.append(('FONTNAME', (1, row_idx), (2, row_idx), 'Helvetica'))
        if underline:
            style_commands.append(('LINEBELOW', (2, row_idx), (2, row_idx), 0.5, colors.black))
        if double_underline:
            # Two lines for double underline effect
            style_commands.append(('LINEBELOW', (2, row_idx), (2, row_idx), 0.5, colors.black))
            style_commands.append(('LINEABOVE', (2, row_idx), (2, row_idx), 0.5, colors.black))
        row_idx += 1

    # Header row
    add_row("", "", "RM", bold=True)

    # Spacer
    add_row("")

    # REVENUE
    add_row("REVENUE", bold=True)
    for acct, info in data["revenue_accts"].items():
        amt = info["cr"] - info["dr"]
        add_row(f"  {info['name']}", "", fmt(amt))

    add_row("", "", "", underline=True)
    add_row("TOTAL REVENUE", "", fmt(data["total_revenue"]), bold=True)

    add_row("")

    # COST OF SALES
    add_row("COST OF SALES", bold=True)
    add_row("  Food & Beverage Cost", "", fmt(-data["cogs_amt"]))
    add_row("", "", "", underline=True)
    add_row("GROSS PROFIT", "", fmt(data["gross_profit"]), bold=True)

    add_row("")

    # ADMINISTRATIVE & OPERATING EXPENSES
    add_row("ADMINISTRATIVE & OPERATING EXPENSES", bold=True)
    for acct, info in data["expense_accts"].items():
        if acct == "5050":
            continue
        amt = info["dr"] - info["cr"]
        add_row(f"  {info['name']}", "", fmt(-amt))

    add_row("", "", "", underline=True)
    add_row("TOTAL EXPENSES", "", fmt(-data["total_opex"]), bold=True)

    add_row("")
    # Double underline before net profit
    style_commands.append(('LINEABOVE', (2, row_idx), (2, row_idx), 0.5, colors.black))
    add_row(
        "NET LOSS FOR THE FINANCIAL YEAR", "",
        fmt(data["net_profit"]), bold=True, double_underline=True
    )

    # Build the table
    is_table = Table(rows, colWidths=col_widths)
    is_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ] + style_commands))

    elements.append(is_table)
    elements.append(PageBreak())
    return elements


# ---------------------------------------------------------------------------
# Build Balance Sheet
# ---------------------------------------------------------------------------
def build_balance_sheet(styles, data):
    """Return flowables for the Statement of Financial Position."""
    elements = build_title_block(
        styles,
        "STATEMENT OF FINANCIAL POSITION",
        "AS AT 31 JANUARY 2025"
    )

    # Three columns: [Label, Sub-amount, Total-amount]
    col_widths = [10 * cm, 3.5 * cm, 3.5 * cm]

    rows = []
    style_commands = []
    row_idx = 0

    def add_row(label, sub_amt="", total_amt="", bold=False,
                underline_sub=False, underline_total=False,
                double_underline_total=False):
        nonlocal row_idx
        font = "Helvetica-Bold" if bold else "Helvetica"
        rows.append([label, sub_amt, total_amt])
        style_commands.append(('FONTNAME', (0, row_idx), (0, row_idx), font))
        style_commands.append(('FONTNAME', (1, row_idx), (2, row_idx), 'Helvetica'))
        if underline_sub:
            style_commands.append(('LINEBELOW', (1, row_idx), (1, row_idx), 0.5, colors.black))
        if underline_total:
            style_commands.append(('LINEBELOW', (2, row_idx), (2, row_idx), 0.5, colors.black))
        if double_underline_total:
            style_commands.append(('LINEBELOW', (2, row_idx), (2, row_idx), 0.5, colors.black))
            style_commands.append(('LINEABOVE', (2, row_idx), (2, row_idx), 0.5, colors.black))
        row_idx += 1

    # Header
    add_row("", "", "RM", bold=True)
    add_row("")

    # NON-CURRENT ASSETS
    add_row("NON-CURRENT ASSETS", bold=True)
    add_row("Property, plant and equipment", bold=True)
    add_row("  Music System & Equipment", fmt(data["ppe_music_cost"]))
    add_row("  Less: Accumulated Depreciation", fmt(data["accum_dep_music"]), underline_sub=True)
    add_row("", "", fmt(data["ppe_music_net"]))
    add_row("  Computer & POS", fmt(data["ppe_comp_cost"]))
    add_row("  Less: Accumulated Depreciation", fmt(data["accum_dep_comp"]), underline_sub=True)
    add_row("", "", fmt(data["ppe_comp_net"]))
    add_row("", "", "", underline_total=True)
    add_row("TOTAL NON-CURRENT ASSETS", "", fmt(data["total_nca"]), bold=True)

    add_row("")

    # CURRENT ASSETS
    add_row("CURRENT ASSETS", bold=True)
    add_row("  Trade Receivables", "", fmt(data["trade_recv"]))
    add_row("  Deposits", "", fmt(data["deposits"]))
    add_row("  Cash at Bank", "", fmt(data["cash_bank"]))
    add_row("  Cash in Hand", "", fmt(data["cash_hand"]))
    add_row("", "", "", underline_total=True)
    add_row("TOTAL CURRENT ASSETS", "", fmt(data["total_ca"]), bold=True)

    add_row("")
    style_commands.append(('LINEABOVE', (2, row_idx), (2, row_idx), 0.5, colors.black))
    add_row("TOTAL ASSETS", "", fmt(data["total_assets"]), bold=True,
            double_underline_total=True)

    add_row("")

    # EQUITY AND LIABILITIES
    add_row("EQUITY AND LIABILITIES", bold=True)
    add_row("")

    add_row("EQUITY", bold=True)
    add_row("  Share Capital", "", fmt(data["share_cap"]))
    add_row("  Accumulated Loss", "", fmt(-data["accum_loss_display"]))
    add_row("", "", "", underline_total=True)
    add_row("TOTAL EQUITY", "", fmt(data["total_equity"]), bold=True)

    add_row("")

    # CURRENT LIABILITIES
    add_row("CURRENT LIABILITIES", bold=True)
    add_row("  Trade Payables", "", fmt(data["trade_pay"]))
    add_row("  Other Payables & Accruals", "", fmt(data["other_pay"]))
    if data["epf_pay"] > 0:
        add_row("  EPF Payable", "", fmt(data["epf_pay"]))
    if data["socso_pay"] > 0:
        add_row("  SOCSO Payable", "", fmt(data["socso_pay"]))
    if data["eis_pay"] > 0:
        add_row("  EIS Payable", "", fmt(data["eis_pay"]))
    add_row("  Amount Due to Director", "", fmt(data["due_director"]))
    add_row("  Amount Due to Shareholders", "", fmt(data["due_shareholders"]))
    if data["suspense"] > 0:
        add_row("  Suspense Account", "", fmt(data["suspense"]))
    add_row("", "", "", underline_total=True)
    add_row("TOTAL CURRENT LIABILITIES", "", fmt(data["total_cl"]), bold=True)

    add_row("")
    style_commands.append(('LINEABOVE', (2, row_idx), (2, row_idx), 0.5, colors.black))
    add_row("TOTAL EQUITY AND LIABILITIES", "", fmt(data["total_eq_liab"]), bold=True,
            double_underline_total=True)

    # Build table
    bs_table = Table(rows, colWidths=col_widths)
    bs_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ] + style_commands))

    elements.append(bs_table)
    elements.append(PageBreak())
    return elements


# ---------------------------------------------------------------------------
# Build Trial Balance
# ---------------------------------------------------------------------------
def build_trial_balance(styles, data):
    """Return flowables for the Trial Balance."""
    elements = build_title_block(
        styles,
        "TRIAL BALANCE",
        "AS AT 31 JANUARY 2025"
    )

    # Column widths: Code, Account Name, Debit, Credit
    col_widths = [1.5 * cm, 8.5 * cm, 3.5 * cm, 3.5 * cm]

    # Header row
    header = ["Code", "Account", "Debit (RM)", "Credit (RM)"]
    rows = [header]

    for acct, info in data["tb"].items():
        dr_str = fmt_or_blank(info["dr"])
        cr_str = fmt_or_blank(info["cr"])
        rows.append([acct, info["name"], dr_str, cr_str])

    # Total row
    rows.append(["", "TOTAL", fmt(data["tb_total_dr"]), fmt(data["tb_total_cr"])])

    style_commands = [
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        # Underline before total
        ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.black),
        # Double underline after total
        ('LINEBELOW', (2, -1), (3, -1), 0.5, colors.black),
    ]

    tb_table = Table(rows, colWidths=col_widths, repeatRows=1)
    tb_table.setStyle(TableStyle(style_commands))

    elements.append(tb_table)
    elements.append(PageBreak())
    return elements


# ---------------------------------------------------------------------------
# Build General Ledger
# ---------------------------------------------------------------------------
def build_general_ledger(styles, data):
    """Return flowables for the General Ledger."""
    elements = []
    elements.extend(build_title_block(
        styles,
        "GENERAL LEDGER",
        FY_PERIOD
    ))

    gl = data["gl"]

    # Column widths: Date, JE#, Description, Debit, Credit, Balance
    col_widths = [1.8 * cm, 1.3 * cm, 6.4 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]

    def make_gl_header_row():
        return ["Date", "JE#", "Description", "Debit", "Credit", "Balance"]

    # Iterate through COA in order
    first_account = True
    for acct_code in COA:
        if acct_code not in gl:
            continue
        entries = gl[acct_code]
        acct_name = COA[acct_code]["name"]

        # Account header
        acct_header = Paragraph(
            f"<b>{acct_code} &mdash; {acct_name}</b>", styles["GLHeader"]
        )

        # Build rows for this account
        rows = [make_gl_header_row()]
        for entry in entries:
            rows.append([
                entry["date"],
                f"JE-{entry['je_num']:04d}",
                entry["description"][:50],
                fmt_or_blank(entry["dr"]),
                fmt_or_blank(entry["cr"]),
                fmt(entry["balance"], show_zero=True),
            ])

        # Closing balance row
        closing_bal = entries[-1]["balance"]
        rows.append(["", "", "Closing Balance", "", "", fmt(closing_bal, show_zero=True)])

        num_rows = len(rows)
        style_commands = [
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (2, -1), 'LEFT'),
            ('ALIGN', (3, 0), (5, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
            ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ]

        gl_table = Table(rows, colWidths=col_widths, repeatRows=1)
        gl_table.setStyle(TableStyle(style_commands))

        if not first_account:
            elements.append(Spacer(1, 0.4 * cm))

        elements.append(acct_header)
        elements.append(gl_table)
        first_account = False

    return elements


# ---------------------------------------------------------------------------
# Two-pass PDF generation
# ---------------------------------------------------------------------------
def generate_pdf():
    """Generate the PDF using a two-pass approach for accurate page numbers."""
    print("Computing financial data...")
    data = compute_all()

    # Verify key figures
    print(f"  Total Revenue:    {fmt(data['total_revenue'])}")
    print(f"  Gross Profit:     {fmt(data['gross_profit'])}")
    print(f"  Net Profit:       {fmt(data['net_profit'])}")
    print(f"  Total Assets:     {fmt(data['total_assets'])}")
    print(f"  Total Eq+Liab:    {fmt(data['total_eq_liab'])}")
    print(f"  TB DR:            {fmt(data['tb_total_dr'])}")
    print(f"  TB CR:            {fmt(data['tb_total_cr'])}")

    bs_diff = abs(data["total_assets"] - data["total_eq_liab"])
    tb_diff = abs(data["tb_total_dr"] - data["tb_total_cr"])
    assert bs_diff < Decimal("0.01"), f"Balance sheet does not balance! Diff={bs_diff}"
    assert tb_diff < Decimal("0.01"), f"Trial balance does not balance! Diff={tb_diff}"
    print("  BS and TB verified balanced.")

    styles = get_styles()

    # --- Pass 1: render to count pages per section ---
    print("\nPass 1: Counting pages...")
    tracker1 = PageNumberTracker()

    def on_page_pass1(canvas, doc):
        tracker1.on_page(canvas, doc)

    def on_cover_pass1(canvas, doc):
        tracker1.on_cover_page(canvas, doc)

    import tempfile, os
    tmp_path = os.path.join(tempfile.gettempdir(), "[client_temp]_pass1.pdf")

    doc1 = BaseDocTemplate(
        tmp_path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )

    cover_frame = Frame(MARGIN, MARGIN, FRAME_W, FRAME_H, id="cover_frame")
    content_frame = Frame(MARGIN, MARGIN + 0.8 * cm, FRAME_W, FRAME_H - 0.8 * cm,
                          id="content_frame")

    cover_template = PageTemplate(id="cover", frames=[cover_frame],
                                  onPage=on_cover_pass1)
    content_template = PageTemplate(id="content", frames=[content_frame],
                                    onPage=on_page_pass1)

    doc1.addPageTemplates([cover_template, content_template])

    # Use placeholder page numbers for pass 1
    page_map_placeholder = {"is": 3, "bs": 4, "tb": 5, "gl": 6}

    # We need to track which page each section starts on
    # Use a custom action flowable
    from reportlab.platypus import Flowable

    class SectionMarker(Flowable):
        """Zero-height flowable that records the current page number."""
        def __init__(self, section_name, page_tracker):
            Flowable.__init__(self)
            self.section_name = section_name
            self.page_tracker = page_tracker
            self.width = 0
            self.height = 0

        def draw(self):
            page_num = self.canv._doctemplate.page
            self.page_tracker[self.section_name] = page_num

    section_pages_pass1 = {}

    all_elements = []
    all_elements.extend(build_cover(styles))
    all_elements.extend(build_toc(styles, page_map_placeholder))

    all_elements.append(SectionMarker("is", section_pages_pass1))
    all_elements.extend(build_income_statement(styles, data))

    all_elements.append(SectionMarker("bs", section_pages_pass1))
    all_elements.extend(build_balance_sheet(styles, data))

    all_elements.append(SectionMarker("tb", section_pages_pass1))
    all_elements.extend(build_trial_balance(styles, data))

    all_elements.append(SectionMarker("gl", section_pages_pass1))
    all_elements.extend(build_general_ledger(styles, data))

    doc1.build(all_elements)
    print(f"  Pass 1 complete. Total pages: {tracker1.page_count}")
    print(f"  Section pages: {section_pages_pass1}")

    # Clean up temp file
    try:
        os.remove(tmp_path)
    except:
        pass

    # --- Pass 2: render with correct page numbers ---
    print("\nPass 2: Generating final PDF...")
    tracker2 = PageNumberTracker()

    def on_page_pass2(canvas, doc):
        tracker2.on_page(canvas, doc)

    def on_cover_pass2(canvas, doc):
        tracker2.on_cover_page(canvas, doc)

    doc2 = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )

    cover_frame2 = Frame(MARGIN, MARGIN, FRAME_W, FRAME_H, id="cover_frame")
    content_frame2 = Frame(MARGIN, MARGIN + 0.8 * cm, FRAME_W, FRAME_H - 0.8 * cm,
                           id="content_frame")

    cover_template2 = PageTemplate(id="cover", frames=[cover_frame2],
                                   onPage=on_cover_pass2)
    content_template2 = PageTemplate(id="content", frames=[content_frame2],
                                     onPage=on_page_pass2)

    doc2.addPageTemplates([cover_template2, content_template2])

    # Build with correct page numbers
    all_elements2 = []
    all_elements2.extend(build_cover(styles))
    all_elements2.extend(build_toc(styles, section_pages_pass1))

    # No section markers needed in pass 2
    all_elements2.extend(build_income_statement(styles, data))
    all_elements2.extend(build_balance_sheet(styles, data))
    all_elements2.extend(build_trial_balance(styles, data))
    all_elements2.extend(build_general_ledger(styles, data))

    doc2.build(all_elements2)
    print(f"\nPDF generated: {OUTPUT}")
    print(f"Total pages: {tracker2.page_count}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    generate_pdf()
