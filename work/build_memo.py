from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

root = Path(__file__).resolve().parents[1]
out = root / "artifacts" / "operations-memo.pdf"
user_out = root / "outputs" / "operations-memo.pdf"
out.parent.mkdir(exist_ok=True); user_out.parent.mkdir(exist_ok=True)

navy = colors.HexColor("#153A5B"); pale = colors.HexColor("#E8F1F8"); ink = colors.HexColor("#17212B")
styles = getSampleStyleSheet()
title = ParagraphStyle("Title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=19, leading=22, textColor=ink, alignment=TA_LEFT, spaceAfter=8)
deck = ParagraphStyle("Deck", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=13, textColor=colors.HexColor("#526878"), spaceAfter=14)
h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=ink, spaceBefore=10, spaceAfter=5)
body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.3, leading=13.2, textColor=ink, spaceAfter=7)
small = ParagraphStyle("Small", parent=body, fontSize=8, leading=10)

def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor("#D9E1E8")); canvas.line(0.65*inch,0.55*inch,7.85*inch,0.55*inch)
    canvas.setFont("Helvetica",7.5); canvas.setFillColor(colors.HexColor("#667A89"))
    canvas.drawString(0.65*inch,0.36*inch,"Synthetic portfolio project - not Coinbase policy or production evidence")
    canvas.drawRightString(7.85*inch,0.36*inch,f"{doc.page}")
    canvas.restoreState()

story = [
    Paragraph("Settlement exception desk decision memo", title),
    Paragraph("Prepared 20 September 2026 | Simulated Base Sepolia and x402 exact workflow | Decision owner Finance Operations", deck),
    Paragraph("Recommendation", h1),
    Paragraph("Retain FIFO for the initial scenario. The deadline-first rule reduced value-weighted delay but did not reduce the number of overdue cases. It therefore fails the predeclared adoption gate of at least 15% fewer overdue cases with zero control failures and no more than 10% deterioration in value-weighted overdue time.", body),
    Table([
        ["Metric", "FIFO", "Deadline-first", "Decision relevance"],
        ["Overdue cases", "6", "6", "No count improvement"],
        ["Median resolution delay", "66.1 min", "55.1 min", "Improved"],
        ["P95 resolution delay", "107.1 min", "107.1 min", "Unchanged"],
        ["Value-weighted overdue", "4.43bn", "1.58bn", "Improved in this scenario"],
        ["Control failures", "0", "0", "Constraint preserved"],
    ], colWidths=[1.65*inch,0.9*inch,1.15*inch,2.85*inch], repeatRows=1, style=TableStyle([
        ("BACKGROUND",(0,0),(-1,0),navy),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),8.2),("LEADING",(0,0),(-1,-1),10),
        ("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#D9E1E8")),("BACKGROUND",(0,2),(-1,2),pale),("BACKGROUND",(0,4),(-1,4),pale),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)
    ])),
    Paragraph("What the decision protects", h1),
    Paragraph("A settlement timeout is an unknown outcome, not a failure. The operator reconciles the original attempt before considering any retry. When late payment evidence arrives, the desk recovers the persisted report and never initiates a second charge or entitlement. Payment, delivery, and refund states remain independent until their evidence reconciles.", body),
    Paragraph("The build enforces three non-negotiable controls: one payment claim cannot close two orders; completed refunds plus active reservations cannot exceed the capture; and an unknown refund outcome keeps its reservation. The event log is append-only so late evidence and corrections remain visible.", body),
    Paragraph("Operating design", h1),
    Paragraph("A deterministic reducer derives case state from 65 synthetic events across 16 incidents. Actionable cases enter a single-operator simulation. FIFO orders by opening time. The alternative orders by deadline, then opening time. Both policies receive the same workload fingerprint, evidence timing, duration assumptions, capacity, and control rules.", body),
    PageBreak(),
    Paragraph("Adverse view and limits", title),
    Paragraph("The headline result is not robust enough for adoption", h1),
    Paragraph("Deadline-first looks better on weighted delay because it serves earlier deadlines before some older cases. Yet it leaves the same number overdue. With only nine actionable cases and project-selected durations, that result could reverse under another arrival pattern. The correct conclusion is narrower: the rule behaved as designed, preserved controls, and did not beat FIFO on the chosen primary metric.", body),
    Paragraph("Strongest argument against FIFO", h1),
    Paragraph("FIFO ignores deadline and value. In the initial workload it produced nearly three times the value-weighted overdue minutes. A team whose loss function emphasizes economic exposure could reasonably prefer deadline-first. That would be a different objective, however, and should be declared before looking at results rather than substituted after the primary gate fails.", body),
    Paragraph("Decision conditions", h1),
    Table([
        ["Condition", "Required evidence", "Fallback"],
        ["Retry payment", "Conclusive failure on original attempt and operator approval", "Keep unknown and reconcile"],
        ["Recover delivery", "Matching payment claim and persisted resource digest", "Keep obligation open"],
        ["Approve refund", "Original payer, captured amount, available refundable balance", "Reserve nothing and escalate"],
        ["Close case", "Payment disposition, delivery disposition, and refund disposition", "Leave open with named evidence gap"],
    ], colWidths=[1.4*inch,3.35*inch,1.8*inch], repeatRows=1, style=TableStyle([
        ("BACKGROUND",(0,0),(-1,0),navy),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),8.2),("LEADING",(0,0),(-1,-1),10),
        ("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#D9E1E8")),("BACKGROUND",(0,2),(-1,2),pale),("BACKGROUND",(0,4),(-1,4),pale),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)
    ])),
    Paragraph("Next test", h1),
    Paragraph("Keep FIFO as the working baseline. Before reconsidering, run a larger frozen scenario grid with observed or practitioner-reviewed handling-time ranges and a held-out workload. Evaluate a narrow hybrid that applies deadline-first only when a case is actionable and within a specified SLA window. Preserve the same control rules and report unfinished count and value.", body),
    Paragraph("Evidence and claim boundary", h1),
    Spacer(1,8),
    Paragraph("Source register: x402 v2 specification; Base transaction finality; Coinbase CDP SDK x402 examples; synthetic corpus and pre-authored oracle in the project package.", small),
]

for target in (out, user_out):
    doc = SimpleDocTemplate(str(target), pagesize=LETTER, rightMargin=0.65*inch, leftMargin=0.65*inch, topMargin=0.58*inch, bottomMargin=0.7*inch, title="Settlement exception desk decision memo", author="Portfolio project")
    doc.build(list(story), onFirstPage=footer, onLaterPages=footer)
