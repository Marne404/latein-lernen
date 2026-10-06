# ============================================================
# LATEIN-KLAUSUR-TURBO  ·  OVID: DAEDALUS & IKARUS
# Komplette PDF-Sammlung zum Lernen am iPad (Apple Pencil)
#
# Erzeugt einen Ordner "Latein_Lernpaket" mit:
#   00_Komplettpaket.pdf        alles in einem (mit Lesezeichen)
#   01 ... 08 Einzelkapitel     jeweils mit eigenen Lösungen
#   09_Loesungen.pdf            alle Lösungen
#   10_Spickzettel.pdf          1 Seite für morgen früh
#
# Besonderheiten:
#   - antippbare Checkboxen (PDF-Formularfelder) nach jeder Aufgabe
#   - Schreiblinien mit Apple-Pencil-freundlichem Abstand
#   - Übersetzung in 3 Stufen (vereinfacht -> Original mit Hilfen -> Klausurmodus)
#   - Zeitformen, Kasus, Partizipien, Konjunktiv, Metrik, Stilmittel
#   - Kreuzworträtsel, Wortgitter, Zuordnungsspiele
#   - Probeklausur mit Bewertungsraster, Fehlerprotokoll
#   - falls vocab.js (Web-App) daneben liegt: Anhang mit 500 Grundwörtern
#
# Funktioniert in jeder normalen Python-Umgebung
# (VS Code, PyCharm, IDLE, Thonny, Jupyter, Google Colab usw.)
#
# Voraussetzung:
#     pip install reportlab
# ============================================================

import random
import re
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle,
        PageBreak, Spacer, Flowable, KeepTogether, CondPageBreak,
    )
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.units import cm
except ImportError:
    print("\n❌ Das Modul 'reportlab' ist nicht installiert.")
    print("\nInstalliere es mit:")
    print("    pip install reportlab")
    print("\nDanach dieses Programm erneut starten.")
    raise SystemExit


# ------------------------------------------------------------
# Ausgabeordner
# ------------------------------------------------------------

try:
    script_folder = Path(__file__).resolve().parent
except NameError:
    script_folder = Path.cwd()

OUT = script_folder / "Latein_Lernpaket"
OUT.mkdir(exist_ok=True)

DOC_TITLE = "Latein-Klausur-Turbo · Ovid: Daedalus & Ikarus"


# ------------------------------------------------------------
# Farben & Schriften
# ------------------------------------------------------------
# Nur die PDF-Standardschriften (Helvetica, Times) -> läuft überall,
# ohne Schriftdateien. Darum: keine Sonderzeichen wie Pfeile oder Haken
# im Text; solche Symbole werden als Grafik gezeichnet.

BORDEAUX = colors.HexColor("#7a1f2b")
GOLD = colors.HexColor("#c99a3b")
INK = colors.HexColor("#2b2420")
MUTED = colors.HexColor("#7a6f63")
PAPER = colors.HexColor("#f7f2e8")
PAPER2 = colors.HexColor("#efe6d4")
LINE = colors.HexColor("#d6ccb8")
WRITE = colors.HexColor("#c9d3e0")
BLUE = colors.HexColor("#2d5f8a")
GREEN = colors.HexColor("#2f7d54")
ORANGE = colors.HexColor("#c0622b")
WHITE = colors.white

PAGE_W, PAGE_H = A4
MARGIN_X = 1.7 * cm
MARGIN_TOP = 2.0 * cm
MARGIN_BOTTOM = 1.7 * cm
CONTENT_W = PAGE_W - 2 * MARGIN_X

ss = getSampleStyleSheet()


def style(name, parent="BodyText", **kw):
    base = dict(fontName="Helvetica", fontSize=10, leading=14, textColor=INK)
    base.update(kw)
    return ParagraphStyle(name, parent=ss[parent], **base)


ST = {
    "body": style("body", spaceAfter=5),
    "small": style("small", fontSize=8.5, leading=11.5, textColor=MUTED),
    "cell": style("cell", fontSize=9, leading=11.8, spaceAfter=0),
    "cellb": style("cellb", fontName="Helvetica-Bold", fontSize=9, leading=11.8),
    "cellh": style("cellh", fontName="Helvetica-Bold", fontSize=8.8, leading=11, textColor=WHITE),
    "celll": style("celll", fontName="Times-Italic", fontSize=10.5, leading=12.5),
    "cellc": style("cellc", fontSize=9, leading=11.8, alignment=TA_CENTER),
    "h1": style("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=BORDEAUX,
                spaceBefore=10, spaceAfter=6),
    "h2": style("h2", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=INK,
                spaceBefore=8, spaceAfter=4),
    "boxt": style("boxt", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceAfter=2),
    "box": style("box", fontSize=9.5, leading=13.2, spaceAfter=2),
    "verse": style("verse", fontName="Times-Roman", fontSize=12.5, leading=17.5),
    "versebig": style("versebig", fontName="Times-Roman", fontSize=13.5, leading=26),
    "lat": style("lat", fontName="Times-Roman", fontSize=12, leading=17, spaceAfter=4),
    "task": style("task", fontSize=10, leading=14, spaceAfter=4, textColor=INK),
    "sol": style("sol", fontSize=9.3, leading=12.8, spaceAfter=3),
    "center": style("center", alignment=TA_CENTER),
    "title": style("title", fontName="Times-Bold", fontSize=34, leading=40, textColor=BORDEAUX,
                   alignment=TA_CENTER),
    "subtitle": style("subtitle", fontName="Helvetica", fontSize=13, leading=18, textColor=MUTED,
                      alignment=TA_CENTER),
}


def P(text, st="body"):
    return Paragraph(text, ST[st] if isinstance(st, str) else st)


def L(text):
    """Lateinischer Text inline (kursiv, Times)."""
    return f'<font name="Times-Italic" size="11">{text}</font>'


def H1(text):
    """Zwischenüberschrift, die nie allein unten auf der Seite steht."""
    return [CondPageBreak(4.5 * cm), P(text, "h1")]


def sp(h=0.25):
    return Spacer(1, h * cm)


# ------------------------------------------------------------
# Laufende Sammlung: Aufgaben, Lösungen, Formularfeld-Namen
# ------------------------------------------------------------

class Ctx:
    def __init__(self):
        self.tasks = []        # (kapitel, nr, titel, stufe)
        self.solutions = []    # (kapitel, nr, titel, [flowables])
        self.chapter = ""
        self.field = 0


CTX = Ctx()


def field_name(prefix="cb"):
    CTX.field += 1
    return f"{prefix}{CTX.field}"


# ------------------------------------------------------------
# Eigene Bausteine (Flowables)
# ------------------------------------------------------------

def draw_check(c, x, y, s, color=GREEN, width=2):
    """Gezeichneter Haken (statt Sonderzeichen)."""
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.setLineCap(1)
    c.setLineJoin(1)
    p = c.beginPath()
    p.moveTo(x + s * 0.15, y + s * 0.5)
    p.lineTo(x + s * 0.42, y + s * 0.2)
    p.lineTo(x + s * 0.88, y + s * 0.85)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def draw_arrow(c, x1, y, x2, color=BORDEAUX, width=1.4):
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2 - 4, y)
    p = c.beginPath()
    p.moveTo(x2, y)
    p.lineTo(x2 - 6, y + 3.5)
    p.lineTo(x2 - 6, y - 3.5)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def acro_checkbox(c, x, y, size, tooltip="erledigt"):
    """Antippbare Checkbox (PDF-Formularfeld) – funktioniert in
    Apple Books/Dateien, GoodNotes-Import, Notability, Acrobat, Preview."""
    c.acroForm.checkbox(
        name=field_name(), tooltip=tooltip, x=x, y=y, size=size,
        relative=True, buttonStyle="check", shape="square",
        borderColor=BORDEAUX, fillColor=WHITE, textColor=GREEN,
        borderWidth=1.2, checked=False,
    )


class CheckBox(Flowable):
    """Einzelne Checkbox, z. B. in Tabellenzellen."""

    def __init__(self, size=12, tooltip="erledigt"):
        super().__init__()
        self.size = size
        self.tooltip = tooltip

    def wrap(self, aw, ah):
        return self.size, self.size

    def draw(self):
        acro_checkbox(self.canv, 0, 0, self.size, self.tooltip)


def level_dots(c, x, y, level, r=3.2, gap=9):
    for i in range(3):
        c.setStrokeColor(BORDEAUX)
        c.setFillColor(BORDEAUX if i < level else WHITE)
        c.setLineWidth(0.9)
        c.circle(x + i * gap, y, r, stroke=1, fill=1)


LEVEL_NAME = {1: "Basis", 2: "Aufbau", 3: "Profi"}


class TaskHeader(Flowable):
    """Kopfzeile jeder Aufgabe: Nummer · Titel · Schwierigkeit · Checkbox."""

    def __init__(self, nr, title, level=1, minutes=None):
        super().__init__()
        self.nr, self.title, self.level, self.minutes = nr, title, level, minutes
        self.h = 0.95 * cm

    def wrap(self, aw, ah):
        self.w = aw
        return aw, self.h

    def draw(self):
        c = self.canv
        w, h = self.w, self.h
        c.setFillColor(PAPER)
        c.roundRect(0, 0, w, h, 6, stroke=0, fill=1)
        # Nummer-Badge
        bw = 1.25 * cm
        c.setFillColor(BORDEAUX)
        c.roundRect(0, 0, bw, h, 6, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(bw / 2, h / 2 - 4, self.nr)
        # Titel
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        title = self.title
        while c.stringWidth(title, "Helvetica-Bold", 11) > w - bw - 6.8 * cm and len(title) > 8:
            title = title[:-2]
        if title != self.title:
            title = title.rstrip() + "..."
        c.drawString(bw + 8, h / 2 - 4, title)
        # Stufe
        x = w - 6.3 * cm
        level_dots(c, x, h / 2, self.level)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        lab = LEVEL_NAME[self.level]
        if self.minutes:
            lab += f" · {self.minutes} min"
        c.drawString(x + 24, h / 2 - 3, lab)
        # Checkbox
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(BORDEAUX)
        c.drawRightString(w - 0.95 * cm, h / 2 - 3, "erledigt")
        acro_checkbox(c, w - 0.75 * cm, h / 2 - 7, 14, f"Aufgabe {self.nr} erledigt")
        # Lesezeichen
        key = f"task_{self.nr}_{id(self)}"
        c.bookmarkPage(key)
        c.addOutlineEntry(f"{self.nr} {self.title}", key, level=1, closed=True)


class Lines(Flowable):
    """Schreiblinien für den Apple Pencil."""

    def __init__(self, n=3, gap=0.95 * cm, label=None, indent=0):
        super().__init__()
        self.n, self.gap, self.label, self.indent = n, gap, label, indent

    def wrap(self, aw, ah):
        self.w = aw
        return aw, self.n * self.gap + 0.15 * cm

    def split(self, aw, ah):
        # Lange Schreibflächen dürfen auf die nächste Seite umbrechen
        k = int((ah - 0.15 * cm) // self.gap)
        if k >= self.n:
            return []
        k = min(k, self.n - 3)  # keine einzelnen Restlinien auf der nächsten Seite
        if k < 3:
            return []
        return [Lines(k, self.gap, self.label, self.indent),
                Lines(self.n - k, self.gap, None, self.indent)]

    def draw(self):
        c = self.canv
        c.setStrokeColor(WRITE)
        c.setLineWidth(0.7)
        for i in range(self.n):
            y = (self.n - i - 1) * self.gap + 0.1 * cm
            c.line(self.indent, y, self.w, y)
        if self.label:
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 7.5)
            c.drawString(self.indent, (self.n - 1) * self.gap + 0.1 * cm + 3, self.label)


class Banner(Flowable):
    """Kapitelbanner + Lesezeichen + Kapitelname für die Kopfzeile."""

    def __init__(self, num, title, subtitle=""):
        super().__init__()
        self.num, self.title, self.subtitle = num, title, subtitle
        self.h = 2.6 * cm

    def wrap(self, aw, ah):
        self.w = aw
        return aw, self.h

    def draw(self):
        c = self.canv
        c._chapter = f"Kapitel {self.num}: {self.title}" if self.num else self.title
        key = f"chap_{self.num}_{id(self)}"
        c.bookmarkPage(key)
        c.addOutlineEntry(c._chapter, key, level=0, closed=False)
        c.setFillColor(BORDEAUX)
        c.roundRect(0, 0, self.w, self.h, 10, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, 0.42 * cm, self.w, 0.06 * cm, stroke=0, fill=1)
        x = 0.6 * cm
        if self.num:
            c.setFillColor(GOLD)
            c.setFont("Times-Bold", 46)
            c.drawString(x, 0.85 * cm, str(self.num))
            x += c.stringWidth(str(self.num), "Times-Bold", 46) + 0.45 * cm
        c.setFillColor(WHITE)
        c.setFont("Times-Bold", 22)
        c.drawString(x, 1.45 * cm, self.title)
        if self.subtitle:
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#f3dfc0"))
            c.drawString(x, 0.85 * cm, self.subtitle)


class StepChain(Flowable):
    """Die 5-Schritte-Methode als Kette von Kästen mit Pfeilen."""

    def __init__(self, steps):
        super().__init__()
        self.steps = steps

    def wrap(self, aw, ah):
        self.w = aw
        return aw, 2.3 * cm

    def draw(self):
        c = self.canv
        n = len(self.steps)
        gap = 0.55 * cm
        bw = (self.w - gap * (n - 1)) / n
        for i, (head, sub) in enumerate(self.steps):
            x = i * (bw + gap)
            c.setFillColor(PAPER)
            c.setStrokeColor(BORDEAUX)
            c.setLineWidth(1)
            c.roundRect(x, 0, bw, 2.3 * cm, 7, stroke=1, fill=1)
            c.setFillColor(BORDEAUX)
            c.circle(x + bw / 2, 1.75 * cm, 0.33 * cm, stroke=0, fill=1)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(x + bw / 2, 1.75 * cm - 4, str(i + 1))
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 9.5)
            c.drawCentredString(x + bw / 2, 0.95 * cm, head)
            c.setFont("Helvetica", 7.6)
            c.setFillColor(MUTED)
            c.drawCentredString(x + bw / 2, 0.45 * cm, sub)
            if i < n - 1:
                draw_arrow(c, x + bw + 2, 1.15 * cm, x + bw + gap - 2)


class RatingRow(Flowable):
    """Selbsteinschätzung am Kapitelende: sitzt / fast / nochmal."""

    def __init__(self, text="Wie sicher bist du jetzt?"):
        super().__init__()
        self.text = text

    def wrap(self, aw, ah):
        self.w = aw
        return aw, 1.1 * cm

    def draw(self):
        c = self.canv
        c.setFillColor(PAPER2)
        c.roundRect(0, 0, self.w, 1.1 * cm, 7, stroke=0, fill=1)
        c.setFillColor(INK)
        opts = [("sitzt", GREEN), ("fast", GOLD), ("nochmal üben", ORANGE)]
        x = self.w - 8.0 * cm
        size = 10
        while c.stringWidth(self.text, "Helvetica-Bold", size) > x - 0.8 * cm and size > 7:
            size -= 0.5
        c.setFont("Helvetica-Bold", size)
        c.drawString(0.4 * cm, 0.42 * cm, self.text)
        for lab, col in opts:
            acro_checkbox(c, x, 0.33 * cm, 13, lab)
            c.setFillColor(col)
            c.setFont("Helvetica-Bold", 9.5)
            c.drawString(x + 18, 0.42 * cm, lab)
            x += 2.1 * cm if lab == "sitzt" else 1.9 * cm


class MatchGame(Flowable):
    """Zuordnungsspiel: Punkte mit dem Stift verbinden."""

    def __init__(self, left, right, row_h=0.95 * cm):
        super().__init__()
        self.left, self.right, self.row_h = left, right, row_h

    def wrap(self, aw, ah):
        self.w = aw
        return aw, len(self.left) * self.row_h + 0.2 * cm

    def draw(self):
        c = self.canv
        n = len(self.left)
        colw = self.w * 0.36
        for i in range(n):
            y = (n - i - 0.5) * self.row_h
            for j, (txt, xbox) in enumerate([(self.left[i], 0), (self.right[i], self.w - colw)]):
                c.setFillColor(PAPER)
                c.setStrokeColor(LINE)
                c.roundRect(xbox, y - 0.36 * cm, colw, 0.72 * cm, 5, stroke=1, fill=1)
                c.setFillColor(INK)
                font = "Times-Italic" if j == 0 else "Helvetica"
                c.setFont(font, 11 if j == 0 else 9.5)
                c.drawString(xbox + 0.3 * cm, y - 3.5, txt)
                dotx = xbox + colw + 0.35 * cm if j == 0 else xbox - 0.35 * cm
                c.setFillColor(BORDEAUX)
                c.circle(dotx, y, 3.2, stroke=0, fill=1)


class Scansion(Flowable):
    """Vers groß und gesperrt, mit Platz darüber für Längen/Kürzen."""

    def __init__(self, verse, nr=""):
        super().__init__()
        self.verse, self.nr = verse, nr

    def wrap(self, aw, ah):
        self.w = aw
        return aw, 2.1 * cm

    def draw(self):
        c = self.canv
        c.setFillColor(PAPER)
        c.roundRect(0, 0, self.w, 2.1 * cm, 6, stroke=0, fill=1)
        c.setStrokeColor(WRITE)
        c.setLineWidth(0.6)
        c.line(0.9 * cm, 1.45 * cm, self.w - 0.3 * cm, 1.45 * cm)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(0.2 * cm, 0.55 * cm, str(self.nr))
        c.setFillColor(INK)
        size = 15
        while c.stringWidth(self.verse, "Times-Roman", size) + len(self.verse) * 2.2 > self.w - 1.3 * cm:
            size -= 0.5
        c.setFont("Times-Roman", size)
        t = c.beginText(0.9 * cm, 0.5 * cm)
        t.setFont("Times-Roman", size)
        t.setCharSpace(2.2)
        t.textOut(self.verse)
        c.drawText(t)


class Cover(Flowable):
    """Titelseite."""

    def wrap(self, aw, ah):
        self.w, self.hh = aw, 11.5 * cm
        return aw, self.hh

    def draw(self):
        c = self.canv
        c._nohdr = c.getPageNumber()
        w, h = self.w, self.hh
        c.setFillColor(BORDEAUX)
        c.roundRect(0, h - 9.5 * cm, w, 9.5 * cm, 16, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, h - 9.5 * cm + 1.1 * cm, w, 0.09 * cm, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#f3dfc0"))
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(w / 2, h - 1.6 * cm, "LATEIN  ·  KLAUSUR-TURBO  ·  LERNPAKET")
        c.setFillColor(WHITE)
        c.setFont("Times-Bold", 40)
        c.drawCentredString(w / 2, h - 4.0 * cm, "Daedalus & Ikarus")
        c.setFont("Times-Italic", 18)
        c.drawCentredString(w / 2, h - 5.1 * cm, "Ovid, Metamorphosen 8, 183–235")
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#f3dfc0"))
        c.drawCentredString(w / 2, h - 6.4 * cm,
                            "Übersetzen in 3 Stufen · Zeitformen · Kasus · Vokabeln · Stilmittel")
        c.drawCentredString(w / 2, h - 7.0 * cm,
                            "Rätsel · Probeklausur · Lösungen · Spickzettel")
        # Name / Datum
        c.setFillColor(INK)
        c.setFont("Helvetica", 9.5)
        c.drawString(0, h - 10.7 * cm, "Name:")
        c.drawString(w / 2 + 0.5 * cm, h - 10.7 * cm, "Klausur am:")
        c.setStrokeColor(WRITE)
        c.line(1.3 * cm, h - 10.75 * cm, w / 2 - 0.5 * cm, h - 10.75 * cm)
        c.line(w / 2 + 2.6 * cm, h - 10.75 * cm, w, h - 10.75 * cm)


# ------------------------------------------------------------
# Kästen & Tabellen
# ------------------------------------------------------------

BOX_KINDS = {
    "merke": (BORDEAUX, "MERKE"),
    "tipp": (BLUE, "TIPP"),
    "achtung": (ORANGE, "ACHTUNG"),
    "info": (GOLD, "INFO"),
    "ziel": (GREEN, "DEIN ZIEL"),
    "trick": (BLUE, "KLAUSUR-TRICK"),
}


def box(kind, body, title=None):
    col, label = BOX_KINDS[kind]
    head = f'<font color="{col.hexval().replace("0x", "#")}">{label}</font>'
    if title:
        head += f"  {title}"
    parts = [P(head, "boxt")]
    if isinstance(body, str):
        body = [body]
    for b in body:
        parts.append(P(b, "box") if isinstance(b, str) else b)
    t = Table([["", parts]], colWidths=[0.18 * cm, CONTENT_W - 0.18 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), col),
        ("BACKGROUND", (1, 0), (1, 0), PAPER),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [sp(0.15), t, sp(0.25)]


def cellify(v, st="cell"):
    if isinstance(v, Flowable) or isinstance(v, list):
        return v
    return P(str(v), st)


def table(rows, widths, header=True, lat_cols=(), bold_cols=(), font_st="cell",
          zebra=True, row_h=None, center_cols=()):
    """Tabelle mit Kopfzeile, Zebra-Streifen, Zeilenumbruch in Zellen."""
    data = []
    for r_i, row in enumerate(rows):
        out = []
        for c_i, v in enumerate(row):
            if header and r_i == 0:
                out.append(cellify(v, "cellh"))
            elif c_i in lat_cols:
                out.append(cellify(v, "celll"))
            elif c_i in bold_cols:
                out.append(cellify(v, "cellb"))
            elif c_i in center_cols:
                out.append(cellify(v, "cellc"))
            else:
                out.append(cellify(v, font_st))
        data.append(out)
    heights = None
    if row_h:
        heights = [None if (header and i == 0) else row_h for i in range(len(data))]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, rowHeights=heights)
    cmds = [
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE" if row_h else "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), BORDEAUX))
    if zebra:
        start = 1 if header else 0
        for i in range(start, len(data)):
            if (i - start) % 2 == 1:
                cmds.append(("BACKGROUND", (0, i), (-1, i), PAPER))
    t.setStyle(TableStyle(cmds))
    return t


def fill_table(head, rows, widths, row_h=0.95 * cm, lat_cols=(0,)):
    """Übungstabelle: vorgegebene Spalten + leere Felder zum Ausfüllen."""
    n = len(head)
    full = [head] + [list(r) + [""] * (n - len(r)) for r in rows]
    return table(full, widths, lat_cols=lat_cols, row_h=row_h, zebra=False)


def verse_block(lines_with_nr, hl=None):
    """Lateinischer Originaltext mit Verszahlen."""
    data = []
    for nr, text in lines_with_nr:
        data.append([P(f'<font color="#7a6f63" size="8">{nr}</font>', "cell"), P(text, "verse")])
    t = Table(data, colWidths=[1.15 * cm, CONTENT_W - 1.15 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PAPER),
        ("RIGHTPADDING", (0, 0), (0, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, -1), 8),
        ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
    ]))
    return t


# ------------------------------------------------------------
# Aufgaben & Lösungen registrieren
# ------------------------------------------------------------

def task(nr, title, level=1, minutes=None, intro=None):
    CTX.tasks.append((CTX.chapter, nr, title, level))
    out = [CondPageBreak(4.5 * cm), sp(0.2), TaskHeader(nr, title, level, minutes), sp(0.2)]
    if intro:
        out.append(P(intro, "task"))
    return out


def solution(nr, title, *items):
    flows = []
    for it in items:
        if isinstance(it, str):
            flows.append(P(it, "sol"))
        else:
            flows.append(it)
    CTX.solutions.append((CTX.chapter, nr, title, flows))


def chapter(num, title, subtitle=""):
    CTX.chapter = f"Kapitel {num}: {title}" if num else title
    return [Banner(num, title, subtitle), sp(0.35)]


# ------------------------------------------------------------
# Rätsel-Generatoren (reproduzierbar dank fester Zufallszahl)
# ------------------------------------------------------------

def clean_word(w):
    return re.sub(r"[^A-Z]", "", w.upper().replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE"))


def make_crossword(entries, seed=7, tries=150, max_size=15):
    """entries: [(lösungswort, hinweis)] -> Gitter mit Nummern."""
    rng = random.Random(seed)
    words = [(clean_word(a), clue) for a, clue in entries]
    best = None
    for _ in range(tries):
        order = sorted(words, key=lambda w: (-len(w[0]), rng.random()))
        first, rest = order[0], order[1:]
        rng.shuffle(rest)
        rest.sort(key=lambda w: -len(w[0]) + rng.random() * 4)
        grid = {}
        placed = []

        def can_place(word, r, c, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            br, bc = r - dr, c - dc
            if (br, bc) in grid:
                return -1
            er, ec = r + dr * len(word), c + dc * len(word)
            if (er, ec) in grid:
                return -1
            inter = 0
            for i, ch in enumerate(word):
                rr, cc = r + dr * i, c + dc * i
                if (rr, cc) in grid:
                    if grid[(rr, cc)] != ch:
                        return -1
                    inter += 1
                else:
                    n1 = (rr + dc, cc + dr)
                    n2 = (rr - dc, cc - dr)
                    if n1 in grid or n2 in grid:
                        return -1
            return inter

        def bounds(extra=()):
            cells = list(grid.keys()) + list(extra)
            rs = [p[0] for p in cells]
            cs = [p[1] for p in cells]
            return min(rs), max(rs), min(cs), max(cs)

        def put(word, clue, r, c, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            for i, ch in enumerate(word):
                grid[(r + dr * i, c + dc * i)] = ch
            placed.append((word, clue, r, c, d))

        put(first[0], first[1], 0, 0, "A")
        for word, clue in rest:
            options = []
            for (gr, gc), ch in list(grid.items()):
                for i, wc in enumerate(word):
                    if wc != ch:
                        continue
                    for d in "AD":
                        r, c = (gr, gc - i) if d == "A" else (gr - i, gc)
                        inter = can_place(word, r, c, d)
                        if inter <= 0:
                            continue
                        dr, dc = (0, 1) if d == "A" else (1, 0)
                        cells = [(r + dr * k, c + dc * k) for k in range(len(word))]
                        r0, r1, c0, c1 = bounds(cells)
                        if r1 - r0 + 1 > max_size or c1 - c0 + 1 > max_size:
                            continue
                        area = (r1 - r0 + 1) * (c1 - c0 + 1)
                        options.append((inter * 10 - area * 0.02 + rng.random(), r, c, d))
            if options:
                options.sort(reverse=True)
                _, r, c, d = options[0]
                put(word, clue, r, c, d)
        r0, r1, c0, c1 = bounds()
        score = len(placed) * 100 - (r1 - r0 + 1) * (c1 - c0 + 1) * 0.1
        if best is None or score > best[0]:
            best = (score, dict(grid), list(placed), (r0, r1, c0, c1))
    _, grid, placed, (r0, r1, c0, c1) = best
    grid = {(r - r0, c - c0): ch for (r, c), ch in grid.items()}
    placed = [(w, cl, r - r0, c - c0, d) for (w, cl, r, c, d) in placed]
    starts = sorted({(r, c) for (_, _, r, c, _) in placed})
    num = {pos: i + 1 for i, pos in enumerate(starts)}
    across = sorted([(num[(r, c)], cl, w) for (w, cl, r, c, d) in placed if d == "A"])
    down = sorted([(num[(r, c)], cl, w) for (w, cl, r, c, d) in placed if d == "D"])
    missing = [w for w, _ in words if w not in {p[0] for p in placed}]
    return dict(grid=grid, rows=r1 - r0 + 1, cols=c1 - c0 + 1, num=num,
                across=across, down=down, missing=missing)


class CrosswordGrid(Flowable):
    def __init__(self, cw, solved=False, max_cell=0.8 * cm, max_w=None):
        super().__init__()
        self.cw, self.solved, self.max_cell, self.max_w = cw, solved, max_cell, max_w

    def wrap(self, aw, ah):
        w = self.max_w or aw
        self.cell = min(self.max_cell, w / self.cw["cols"])
        self.w = aw
        return aw, self.cell * self.cw["rows"] + 2

    def draw(self):
        c = self.canv
        s = self.cell
        cw = self.cw
        x0 = (self.w - s * cw["cols"]) / 2
        top = s * cw["rows"]
        for (r, col), ch in cw["grid"].items():
            x = x0 + col * s
            y = top - (r + 1) * s
            c.setFillColor(WHITE)
            c.setStrokeColor(INK)
            c.setLineWidth(0.8)
            c.rect(x, y, s, s, stroke=1, fill=1)
            if (r, col) in cw["num"]:
                c.setFillColor(BORDEAUX)
                c.setFont("Helvetica-Bold", max(5, s * 0.28))
                c.drawString(x + 1.5, y + s - s * 0.3, str(cw["num"][(r, col)]))
            if self.solved:
                c.setFillColor(GREEN)
                c.setFont("Helvetica-Bold", s * 0.55)
                c.drawCentredString(x + s / 2, y + s * 0.25, ch)


def crossword_flows(nr, title, entries, seed, level=2, intro=None):
    for s_ in range(seed, seed + 40):
        cw = make_crossword(entries, seed=s_)
        if not cw["missing"]:
            break
    flows = task(nr, title, level, 15, intro or
                 "Trage die <b>lateinischen</b> Wörter ein (ohne Längenzeichen, Großbuchstaben). "
                 "Ä/Ö/Ü gibt es im Lateinischen nicht.")
    def clue_list(lst, head):
        out = [P(f"<b>{head}</b>", "cellb")]
        for n, cl, w in lst:
            out.append(P(f'<font color="#7a1f2b"><b>{n}</b></font>  {cl} <font color="#7a6f63">({len(w)})</font>', "cell"))
        return out
    t = Table([[clue_list(cw["across"], "Waagerecht"), clue_list(cw["down"], "Senkrecht")]],
              colWidths=[CONTENT_W / 2, CONTENT_W / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2)]))
    # Überschrift, Gitter und Hinweise immer zusammen auf einer Seite
    flows = flows[:2] + [KeepTogether(flows[2:] + [CrosswordGrid(cw), sp(0.3), t])]
    solution(nr, title, CrosswordGrid(cw, solved=True, max_cell=0.55 * cm),
             "Waagerecht: " + ", ".join(f"{n} {w}" for n, _, w in cw["across"]) +
             " · Senkrecht: " + ", ".join(f"{n} {w}" for n, _, w in cw["down"]))
    return flows


def make_wordsearch(words, size=13, seed=3, hard=False):
    rng = random.Random(seed)
    dirs = [(0, 1), (1, 0)]
    if hard:
        dirs += [(1, 1), (-1, 1), (0, -1), (-1, 0)]
    for attempt in range(400):
        grid = [[None] * size for _ in range(size)]
        placed = []
        ok = True
        for w in sorted((clean_word(x) for x in words), key=len, reverse=True):
            done = False
            for _ in range(400):
                dr, dc = rng.choice(dirs)
                r = rng.randrange(size)
                c = rng.randrange(size)
                er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                if not (0 <= er < size and 0 <= ec < size):
                    continue
                if all(grid[r + dr * i][c + dc * i] in (None, w[i]) for i in range(len(w))):
                    for i in range(len(w)):
                        grid[r + dr * i][c + dc * i] = w[i]
                    placed.append((w, r, c, er, ec))
                    done = True
                    break
            if not done:
                ok = False
                break
        if ok:
            letters = "ABCDEFGILMNOPQRSTUVX"
            for r in range(size):
                for c in range(size):
                    if grid[r][c] is None:
                        grid[r][c] = rng.choice(letters)
            return grid, placed
        rng.seed(seed + attempt + 1)
    raise RuntimeError("Wortgitter konnte nicht erzeugt werden")


class WordSearchGrid(Flowable):
    def __init__(self, grid, placed, solved=False, cell=0.82 * cm):
        super().__init__()
        self.grid, self.placed, self.solved, self.cell0 = grid, placed, solved, cell

    def wrap(self, aw, ah):
        self.w = aw
        self.cell = min(self.cell0, aw / len(self.grid))
        return aw, self.cell * len(self.grid) + 4

    def draw(self):
        c = self.canv
        n = len(self.grid)
        s = self.cell
        x0 = (self.w - s * n) / 2
        top = s * n + 2
        c.setFillColor(PAPER)
        c.roundRect(x0 - 4, -2, s * n + 8, s * n + 8, 8, stroke=0, fill=1)
        if self.solved:
            c.setStrokeColor(colors.HexColor("#9fd3b4"))
            c.setLineWidth(s * 0.62)
            c.setLineCap(1)
            for w, r, cc, er, ec in self.placed:
                c.line(x0 + cc * s + s / 2, top - r * s - s / 2, x0 + ec * s + s / 2, top - er * s - s / 2)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", s * 0.5)
        for r in range(n):
            for cc in range(n):
                c.drawCentredString(x0 + cc * s + s / 2, top - r * s - s * 0.68, self.grid[r][cc])


def wordsearch_flows(nr, title, pairs, seed, hard=False, size=13):
    """pairs: [(latein, deutsch)] – gesucht wird das lateinische Wort,
    gegeben ist nur die deutsche Bedeutung (= Vokabeltraining!)."""
    grid, placed = make_wordsearch([p[0] for p in pairs], size=size, seed=seed, hard=hard)
    how = ("Wörter stehen waagerecht, senkrecht, diagonal und auch rückwärts."
           if hard else "Wörter stehen nur waagerecht (von links) und senkrecht (von oben).")
    flows = task(nr, title, 3 if hard else 1, 10,
                 f"Finde zu jeder deutschen Bedeutung das <b>lateinische</b> Wort im Gitter, kreise es ein und "
                 f"schreibe es daneben. {how}")
    flows = flows[:2] + [KeepTogether(flows[2:] + [WordSearchGrid(grid, placed)]), sp(0.3)]
    rows = []
    half = (len(pairs) + 1) // 2
    for i in range(half):
        row = []
        for j in (i, i + half):
            if j < len(pairs):
                row += [CheckBox(11, "gefunden"), P(pairs[j][1], "cell"), ""]
            else:
                row += ["", "", ""]
        rows.append(row)
    t = Table(rows, colWidths=[0.6 * cm, 3.6 * cm, 4.2 * cm] * 2, rowHeights=[0.8 * cm] * len(rows))
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (2, 0), (2, -1), 0.6, WRITE),
        ("LINEBELOW", (5, 0), (5, -1), 0.6, WRITE),
    ]))
    flows.append(t)
    solution(nr, title, WordSearchGrid(grid, placed, solved=True, cell=0.5 * cm),
             ", ".join(f"{d} = <i>{l}</i>" for l, d in pairs))
    return flows


# ============================================================
# INHALT: OVID-TEXT (Met. 8, 183-235)
# ============================================================

OVID = {
    183: "Daedalus interea Creten longumque perosus",
    184: "exilium tactusque loci natalis amore",
    185: "clausus erat pelago. „terras licet“ inquit „et undas",
    186: "obstruat: at caelum certe patet; ibimus illac:",
    187: "omnia possideat, non possidet aera Minos.“",
    188: "dixit et ignotas animum dimittit in artes",
    189: "naturamque novat. nam ponit in ordine pennas",
    190: "a minima coeptas, longam breviore sequenti,",
    191: "ut clivo crevisse putes: sic rustica quondam",
    192: "fistula disparibus paulatim surgit avenis;",
    193: "tum lino medias et ceris alligat imas",
    194: "atque ita conpositas parvo curvamine flectit,",
    195: "ut veras imitetur aves. puer Icarus una",
    196: "stabat et, ignarus sua se tractare pericla,",
    197: "ore renidenti modo, quas vaga moverat aura,",
    198: "captabat plumas, flavam modo pollice ceram",
    199: "mollibat lusuque suo mirabile patris",
    200: "impediebat opus. postquam manus ultima coepto",
    201: "inposita est, geminas opifex libravit in alas",
    202: "ipse suum corpus motaque pependit in aura;",
    203: "instruit et natum „medio“que „ut limite curras,",
    204: "Icare,“ ait „moneo, ne, si demissior ibis,",
    205: "unda gravet pennas, si celsior, ignis adurat:",
    206: "inter utrumque vola. nec te spectare Booten",
    207: "aut Helicen iubeo strictumque Orionis ensem:",
    208: "me duce carpe viam!“ pariter praecepta volandi",
    209: "tradit et ignotas umeris accommodat alas.",
    210: "inter opus monitusque genae maduere seniles,",
    211: "et patriae tremuere manus; dedit oscula nato",
    212: "non iterum repetenda suo pennisque levatus",
    213: "ante volat comitique timet, velut ales, ab alto",
    214: "quae teneram prolem produxit in aera nido,",
    215: "hortaturque sequi damnosasque erudit artes",
    216: "et movet ipse suas et nati respicit alas.",
    217: "hos aliquis tremula dum captat harundine pisces,",
    218: "aut pastor baculo stivave innixus arator",
    219: "vidit et obstipuit, quique aethera carpere possent,",
    220: "credidit esse deos. et iam Iunonia laeva",
    221: "parte Samos (fuerant Delosque Parosque relictae)",
    222: "dextra Lebinthos erat fecundaque melle Calymne,",
    223: "cum puer audaci coepit gaudere volatu",
    224: "deseruitque ducem caelique cupidine tractus",
    225: "altius egit iter. rapidi vicinia solis",
    226: "mollit odoratas, pennarum vincula, ceras;",
    227: "tabuerant cerae: nudos quatit ille lacertos,",
    228: "remigioque carens non ullas percipit auras,",
    229: "oraque caerulea patrium clamantia nomen",
    230: "excipiuntur aqua, quae nomen traxit ab illo.",
    231: "at pater infelix, nec iam pater, „Icare,“ dixit,",
    232: "„Icare,“ dixit „ubi es? qua te regione requiram?“",
    233: "„Icare“ dicebat: pennas aspexit in undis",
    234: "devovitque suas artes corpusque sepulcro",
    235: "condidit, et tellus a nomine dicta sepulti.",
}


def verses(a, b):
    return [(n, OVID[n]) for n in range(a, b + 1)]


# Jeder Abschnitt: Verse, Überschrift, Stufe-1-Text (vereinfacht) +
# Übersetzung, Hilfen für Stufe 2, Original-Übersetzung, Grammatik-Check.
SECTIONS = [
    dict(
        nr=1, v=(183, 187), title="Gefangen auf Kreta – der Plan",
        easy="Daedalus in Creta insula erat. Cretam et longum exilium oderat, nam patriam amabat. "
             "Sed mare eum claudebat. Tum Daedalus dixit: „Minos terras et undas obstruit. "
             "Sed caelum patet! Per caelum ibimus. Minos omnia possidet, sed aerem non possidet.“",
        easy_de="Dädalus war auf der Insel Kreta. Er hasste Kreta und das lange Exil, denn er liebte seine "
                "Heimat. Aber das Meer schloss ihn ein. Da sagte Dädalus: „Minos versperrt die Länder und die "
                "Wellen. Aber der Himmel steht offen! Durch den Himmel werden wir gehen. Minos besitzt alles, "
                "aber die Luft besitzt er nicht.“",
        easy_voc="oderat: er hasste · claudere: einschließen · obstruere: versperren · patere: offenstehen · "
                 "ibimus: wir werden gehen · possidere: besitzen · aer, aeris: Luft",
        help=[("interea", "inzwischen"), ("Creten", "Akk. (griech.) von Crete: Kreta"),
              ("perosus (+ Akk.)", "hassend"), ("exilium", "Verbannung, Exil"),
              ("tactus", "PPP von tangere: berührt, ergriffen"),
              ("loci natalis amore", "von Liebe zum Geburtsort (Abl.)"),
              ("clausus erat", "Plusquamperfekt Passiv: war eingeschlossen"),
              ("pelagus, -i n.", "Meer (pelago = Abl.)"),
              ("licet ... obstruat", "mag er auch ... versperren (Konj.!)"),
              ("inquit", "sagt(e) er"), ("at", "aber"), ("certe", "sicherlich"),
              ("illac", "dort entlang"), ("possideat", "Konj.: mag er besitzen"),
              ("aera", "Akk. (griech.) von aer: Luft")],
        build="Daedalus interea [<i>Creten longumque exilium perosus</i>] [<i>tactusque loci natalis amore</i>] "
              "<b>clausus erat</b> pelago.",
        de="Inzwischen war Dädalus, der Kreta und das lange Exil hasste und von Sehnsucht nach seinem "
           "Geburtsort ergriffen war, vom Meer eingeschlossen. „Mag er auch Länder und Wellen versperren“, "
           "sagte er, „der Himmel aber steht sicherlich offen; dort werden wir entlanggehen. Mag Minos alles "
           "besitzen, die Luft besitzt er nicht.“",
        check=[("Bestimme <i>clausus erat</i>.", "3. Sg. Plusquamperfekt Passiv: er war eingeschlossen."),
               ("Welche Form ist <i>ibimus</i>?", "Futur I, 1. Pl. von ire: wir werden gehen."),
               ("Warum stehen <i>obstruat</i> und <i>possideat</i> im Konjunktiv?",
                "Konzessiv (einräumend): „mag er auch ...“. Dädalus gibt zu, dass Minos Land und Meer "
                "beherrscht – aber nicht die Luft.")],
    ),
    dict(
        nr=2, v=(188, 195), title="Dädalus baut die Flügel",
        easy="Dixit et animum ad novas artes vertit. Naturam mutat: pennas in ordine ponit, primo minimas, "
             "deinde longiores. Sic pennae crescere videntur. Tum medias pennas lino, imas cera alligat et "
             "paulum flectit. Ita alae veras aves imitantur.",
        easy_de="Er sprach und wandte seinen Geist neuen Künsten zu. Er verändert die Natur: Er legt die Federn "
                "in eine Reihe, zuerst die kleinsten, dann längere. So scheinen die Federn zu wachsen. Dann "
                "bindet er die mittleren Federn mit Faden, die untersten mit Wachs zusammen und biegt sie ein "
                "wenig. So ahmen die Flügel echte Vögel nach.",
        easy_voc="animum vertere ad: den Geist richten auf · mutare: verändern · penna: Feder · ordo: Reihe · "
                 "minimus: der kleinste · linum: Faden · cera: Wachs · alligare: festbinden · imus: der unterste · "
                 "flectere: biegen · imitari: nachahmen",
        help=[("animum dimittit in", "richtet den Geist auf"), ("ignotus", "unbekannt"),
              ("novare", "erneuern, verändern"), ("ordo, ordinis m.", "Reihe"),
              ("a minima coeptas", "mit der kleinsten beginnend (PPP zu pennas)"),
              ("longam breviore sequenti", "Abl. abs.: wobei auf eine kürzere eine längere folgt"),
              ("clivus", "Hang, Anhöhe"), ("crevisse", "Inf. Perf. von crescere: gewachsen (zu sein)"),
              ("putes", "Konj.: man könnte glauben"), ("rusticus", "ländlich"),
              ("fistula", "Hirtenflöte, Panflöte"), ("dispar, -paris", "ungleich"),
              ("paulatim", "allmählich"), ("avena", "Halm, Rohr"), ("linum", "Faden"),
              ("alligare", "festbinden"), ("imus", "der unterste"),
              ("conpositas", "PPP: die zusammengesetzten (Federn)"), ("curvamen", "Krümmung"),
              ("flectere", "biegen"), ("imitetur", "Konj. von imitari: nachahmen")],
        build="Nam <b>ponit</b> in ordine pennas [<i>a minima coeptas</i>], [<i>longam breviore sequenti</i>], "
              "ut clivo crevisse <b>putes</b>.",
        de="Er sprach's und richtet seinen Geist auf unbekannte Künste und verändert die Natur. Denn er legt "
           "Federn in eine Reihe, angefangen mit der kleinsten, sodass jeweils auf eine kürzere eine längere "
           "folgt, so dass man glauben könnte, sie seien an einem Hang gewachsen: So wächst einst die ländliche "
           "Hirtenflöte allmählich aus ungleichen Rohrhalmen empor. Dann bindet er die mittleren mit Faden und "
           "die untersten mit Wachs zusammen und biegt die so zusammengesetzten mit einer kleinen Krümmung, "
           "damit sie echte Vögel nachahmen.",
        check=[("Tempus von <i>dixit</i> und von <i>dimittit</i>?",
                "dixit = Perfekt (er sagte); dimittit = Präsens (historisches Präsens, im Deutschen ruhig "
                "Präteritum)."),
               ("Welches Stilmittel ist <i>sic rustica quondam fistula ... surgit</i>?",
                "Ein Vergleich: Die Flügel sehen aus wie eine Panflöte mit ungleich langen Rohren."),
               ("Worauf bezieht sich <i>conpositas</i>?", "Auf (pennas): die so zusammengesetzten Federn.")],
    ),
    dict(
        nr=3, v=(195, 200), title="Ikarus spielt mit der Gefahr",
        easy="Icarus puer cum patre stabat. Periculum non intellegebat. Ridebat et plumas captabat, quas "
             "ventus moverat. Ceram pollice mollibat. Sic opus patris ludo suo impediebat.",
        easy_de="Der Junge Ikarus stand bei dem Vater. Er verstand die Gefahr nicht. Er lachte und haschte nach "
                "den Federn, die der Wind bewegt hatte. Mit dem Daumen knetete er das Wachs weich. So behinderte "
                "er durch sein Spiel das Werk des Vaters.",
        easy_voc="intellegere: verstehen · ridere: lachen · pluma: Feder · captare: zu fangen versuchen · "
                 "moverat: hatte bewegt · pollex: Daumen · mollire: weich machen · ludus: Spiel · "
                 "impedire: behindern",
        help=[("una (Adv.)", "zusammen, dabei"), ("ignarus", "ohne zu wissen"),
              ("se tractare", "AcI: dass er ... berühre, damit hantiere"),
              ("sua pericla (= pericula)", "seine eigene Gefahr"),
              ("ore renidenti", "mit strahlendem Gesicht (Abl.)"), ("modo ... modo", "bald ... bald"),
              ("vagus", "umherschweifend"), ("aura", "Luftzug"), ("moverat", "Plusquamperfekt"),
              ("captare", "zu fangen suchen, haschen"), ("pluma", "Flaumfeder"),
              ("flavus", "goldgelb"), ("pollex, -icis", "Daumen"),
              ("mollibat = molliebat", "Imperfekt: knetete weich"), ("lusus, -us", "Spiel"),
              ("mirabilis", "wunderbar"), ("impediebat", "Imperfekt: behinderte")],
        build="puer Icarus una <b>stabat</b> et, [<i>ignarus sua se tractare pericla</i>], ore renidenti modo "
              "[<i>quas vaga moverat aura</i>] <b>captabat</b> plumas, ...",
        de="Der Knabe Ikarus stand dabei und, ohne zu wissen, dass er mit seiner eigenen Gefahr hantierte, "
           "haschte er mit strahlendem Gesicht bald nach den Federn, die ein umherstreifender Lufthauch bewegt "
           "hatte, bald knetete er mit dem Daumen das gelbe Wachs weich und behinderte durch sein Spiel das "
           "wunderbare Werk des Vaters.",
        check=[("Welches Tempus dominiert hier und warum?",
                "Imperfekt (stabat, captabat, mollibat, impediebat): andauernde Hintergrundhandlung – Ikarus "
                "spielt die ganze Zeit."),
               ("Was ist <i>pericla</i>?", "= pericula: Akk. Pl. n. (Verskürzung)."),
               ("<i>ignarus sua se tractare pericla</i> – welche Konstruktion?",
                "AcI (se ... tractare) abhängig von ignarus: ohne zu wissen, dass er ...")],
    ),
    dict(
        nr=4, v=(200, 209), title="Probeflug und Ermahnung",
        easy="Postquam opus finitum est, Daedalus ipse corpus suum in alis libravit et in aura pependit. "
             "Tum filium monuit: „Icare, medio caelo vola! Si nimis humilis volabis, unda pennas gravabit; "
             "si nimis altus volabis, ignis solis eas uret. Inter utrumque vola! Me duce viam carpe!“ "
             "Deinde alas umeris filii accommodavit.",
        easy_de="Nachdem das Werk vollendet worden war, brachte Dädalus selbst seinen Körper auf den Flügeln ins "
                "Gleichgewicht und schwebte in der Luft. Dann ermahnte er den Sohn: „Ikarus, fliege in der "
                "Mitte des Himmels! Wenn du zu niedrig fliegen wirst, wird die Welle die Federn beschweren; wenn "
                "du zu hoch fliegen wirst, wird das Feuer der Sonne sie verbrennen. Fliege zwischen beidem! Mit "
                "mir als Führer nimm deinen Weg!“ Dann passte er die Flügel an die Schultern des Sohnes an.",
        easy_voc="finire: beenden · librare: im Gleichgewicht halten · pependit: er schwebte · monere: ermahnen · "
                 "humilis: niedrig · gravare: beschweren · urere: verbrennen · dux: Führer · "
                 "carpere viam: den Weg nehmen · umerus: Schulter · accommodare: anpassen",
        help=[("manus ultima", "die letzte Hand"), ("coeptum, -i", "das begonnene Werk (hier Dat.)"),
              ("inposita est", "Perf. Passiv: wurde angelegt"), ("geminus", "doppelt, beide"),
              ("opifex, -ficis", "Künstler, Handwerker"), ("librare", "im Gleichgewicht halten"),
              ("mota ... in aura", "in der bewegten Luft"), ("pependit", "Perf. von pendere: schwebte"),
              ("instruit", "unterweist"), ("natus, -i", "Sohn"),
              ("medio ... ut limite curras", "dass du auf der mittleren Bahn fliegst"),
              ("ait", "sagt er"), ("ne", "damit nicht"),
              ("demissior / celsior", "Komparativ: (zu) niedrig / (zu) hoch"),
              ("gravet / adurat", "Konj.: beschwere / versenge"),
              ("Booten, Helicen, Orionis ensem", "Sternbilder: Bootes, Großer Bär, Schwert des Orion"),
              ("strictus", "gezückt"), ("me duce", "Abl. abs.: mit mir als Führer"),
              ("carpe viam", "nimm den Weg"), ("pariter", "zugleich"),
              ("praecepta volandi", "die Regeln des Fliegens"), ("umerus", "Schulter"),
              ("accommodare", "anpassen")],
        build="„Medio<b>que</b> ut limite <b>curras</b>, Icare,“ <b>ait</b> „<b>moneo</b>, ne, [si demissior "
              "<b>ibis</b>], unda <b>gravet</b> pennas, [si celsior], ignis <b>adurat</b>.“",
        de="Nachdem die letzte Hand an das begonnene Werk gelegt worden war, brachte der Künstler selbst seinen "
           "Körper auf den beiden Flügeln ins Gleichgewicht und schwebte in der bewegten Luft. Er unterweist "
           "auch den Sohn und sagt: „Ich ermahne dich, Ikarus, auf der mittleren Bahn zu fliegen, damit nicht, "
           "wenn du zu tief fliegst, die Welle die Federn beschwert, und wenn zu hoch, das Feuer sie versengt. "
           "Fliege zwischen beidem! Und ich befehle dir nicht, auf den Bootes oder die Helike oder das gezückte "
           "Schwert des Orion zu schauen: Mit mir als Führer nimm deinen Weg!“ Zugleich übergibt er ihm die "
           "Regeln des Fliegens und passt ihm die ungewohnten Flügel an die Schultern an.",
        check=[("<i>vola</i>, <i>carpe</i> – welche Form?", "Imperativ Singular: flieg! nimm!"),
               ("<i>me duce</i> – welche Konstruktion?",
                "Ablativus absolutus ohne Partizip (nominaler Abl. abs.): mit mir als Führer / unter meiner Führung."),
               ("<i>demissior – celsior</i>, <i>unda – ignis</i>: Stilmittel und Wirkung?",
                "Antithese: zwei Gefahren (Wasser unten, Sonne oben) – die Mitte ist der sichere Weg.")],
    ),
    dict(
        nr=5, v=(210, 216), title="Abschied und Aufbruch",
        easy="Dum Daedalus laborat et filium monet, genae eius madidae erant et manus tremebant. Filio "
             "oscula dedit – ultima oscula! Deinde ante filium volavit et pro eo timuit, sicut avis, quae "
             "pullos e nido in aerem ducit. Filium hortabatur: „Sequere me!“ Suas alas movebat et alas filii "
             "respiciebat.",
        easy_de="Während Dädalus arbeitet und den Sohn ermahnt, waren seine Wangen nass und die Hände zitterten. "
                "Er gab dem Sohn Küsse – die letzten Küsse! Dann flog er vor dem Sohn her und fürchtete um ihn, "
                "so wie ein Vogel, der seine Jungen aus dem Nest in die Luft führt. Er ermunterte den Sohn: "
                "„Folge mir!“ Er bewegte seine Flügel und blickte auf die Flügel des Sohnes zurück.",
        easy_voc="gena: Wange · madidus: nass · tremere: zittern · osculum: Kuss · pro eo timere: um ihn fürchten · "
                 "pullus: das Junge (Tier) · nidus: Nest · hortari: ermuntern · sequere: folge! · "
                 "respicere: zurückblicken auf",
        help=[("monitus, -us", "Ermahnung"), ("gena", "Wange"), ("senilis", "eines Alten, greisenhaft"),
              ("maduere = maduerunt", "Perf. von madere: wurden nass"),
              ("tremuere = tremuerunt", "Perf. von tremere: zitterten"), ("patrius", "väterlich"),
              ("osculum", "Kuss"), ("non iterum repetenda", "die nicht wiederholt werden sollten"),
              ("levatus", "PPP: emporgehoben"), ("comes, -itis", "Begleiter"),
              ("comiti timere", "um den Begleiter fürchten (Dat.)"), ("velut ales", "wie ein Vogel"),
              ("tener", "zart"), ("proles, -is f.", "Nachwuchs"),
              ("produxit", "Perf. von producere: hinausführen"), ("nidus", "Nest"),
              ("hortari", "ermuntern"), ("damnosus", "verderblich"), ("erudire", "unterrichten"),
              ("respicere", "zurückblicken auf")],
        build="... ante <b>volat</b> comitique <b>timet</b>, velut ales, [<i>quae teneram prolem "
              "<b>produxit</b> in aera ab alto nido</i>]",
        de="Während der Arbeit und der Ermahnungen wurden die Wangen des alten Mannes feucht, und die "
           "väterlichen Hände zitterten. Er gab seinem Sohn Küsse, die er nicht wiederholen sollte, und von den "
           "Federn emporgehoben fliegt er voraus und fürchtet um seinen Begleiter, wie ein Vogel, der seine "
           "zarte Brut aus dem hohen Nest in die Luft hinausgeführt hat; und er ermuntert ihn zu folgen und "
           "unterweist ihn in der verderblichen Kunst, und er bewegt selbst seine Flügel und blickt auf die "
           "des Sohnes zurück.",
        check=[("<i>maduere</i>, <i>tremuere</i> – welche Form?",
                "3. Pl. Perfekt in der Kurzform: = maduerunt, tremuerunt."),
               ("Welches Stilmittel steht in v. 213 f.?", "Vergleich (velut ales): Dädalus als fürsorglicher Vogel."),
               ("Warum wirkt <i>non iterum repetenda</i> so bedrückend?",
                "Vorausdeutung: Es sind die letzten Küsse – der Leser ahnt den Tod des Ikarus.")],
    ),
    dict(
        nr=6, v=(217, 222), title="Die Zuschauer staunen",
        easy="Piscator, pastor et arator eos viderunt et obstupuerunt. Putaverunt eos deos esse, quia per "
             "caelum volabant. Iam a sinistra parte erat insula Samos – Delos et Paros iam relictae erant –, "
             "a dextra parte erant Lebinthos et Calymne, quae melle abundat.",
        easy_de="Ein Fischer, ein Hirte und ein Pflüger sahen sie und erstarrten vor Staunen. Sie glaubten, dass "
                "sie Götter seien, weil sie durch den Himmel flogen. Schon war auf der linken Seite die Insel "
                "Samos – Delos und Paros waren schon zurückgelassen worden –, auf der rechten Seite waren Lebinthos "
                "und Kalymne, das reich an Honig ist.",
        easy_voc="piscator: Fischer · pastor: Hirte · arator: Pflüger · obstupescere: erstarren, staunen · "
                 "putare: glauben · sinister: links · dexter: rechts · relinquere: zurücklassen · "
                 "mel, mellis: Honig · abundare: reich sein an",
        help=[("hos", "diese (Vater und Sohn, Akk.)"), ("aliquis", "irgendjemand"),
              ("tremula harundine", "mit zitternder Angelrute"), ("captare", "zu fangen suchen"),
              ("baculum", "Stab"), ("stiva", "Pflugsterz (Griff des Pflugs)"),
              ("innixus (+ Abl.)", "gestützt auf"), ("arator", "Pflüger"),
              ("obstipuit", "Perf. von obstupescere: erstarrte"),
              ("qui ... possent", "die ... konnten (Konj.)"), ("aethera", "Akk. (griech.) von aether: Himmel"),
              ("credidit esse deos", "AcI"), ("Iunonius", "der Juno heilig"), ("laevus", "links"),
              ("fuerant ... relictae", "= relictae erant: Plqpf. Passiv"), ("dexter", "rechts"),
              ("fecundus melle", "reich an Honig")],
        build="Hos aliquis, [<i>dum tremula captat harundine pisces</i>], aut pastor ... aut arator <b>vidit</b> et "
              "<b>obstipuit</b> et [<i>quique aethera carpere possent</i>] <b>credidit</b> esse deos.",
        de="Diese sah irgendjemand, während er mit zitternder Rute Fische zu fangen sucht, oder ein Hirte, auf "
           "seinen Stab gestützt, oder ein Pflüger, auf den Pflugsterz gestützt, und er erstarrte vor Staunen und "
           "glaubte, dass sie, die durch den Äther fliegen konnten, Götter seien. Und schon war auf der linken "
           "Seite das der Juno heilige Samos (Delos und Paros waren zurückgelassen worden), auf der rechten "
           "Lebinthos und das honigreiche Kalymne,",
        check=[("<i>credidit esse deos</i> – welche Konstruktion?", "AcI: er glaubte, dass sie Götter seien."),
               ("<i>(fuerant Delosque Parosque relictae)</i> – Stilmittel?",
                "Parenthese (Einschub) und Polysyndeton (-que ... -que)."),
               ("Welches berühmte Gemälde zeigt Fischer, Hirte und Pflüger?",
                "Pieter Bruegel d. Ä.: „Landschaft mit dem Sturz des Ikarus“ – dort bemerkt fast niemand den Sturz.")],
    ),
    dict(
        nr=7, v=(223, 230), title="Der Absturz",
        easy="Tum puer volatu audaci gaudere coepit. Ducem deseruit et altius volavit, quia caelum cupiebat. "
             "Sol ceras mollivit; cerae tabuerunt. Icarus bracchia nuda movit, sed alas non iam habebat. Nomen "
             "patris clamavit et in mare cecidit. Hoc mare nunc nomen eius habet.",
        easy_de="Da begann der Junge, sich über den kühnen Flug zu freuen. Er verließ seinen Führer und flog höher, "
                "weil er nach dem Himmel verlangte. Die Sonne machte das Wachs weich; das Wachs schmolz. Ikarus "
                "bewegte die nackten Arme, aber er hatte keine Flügel mehr. Er rief den Namen des Vaters und fiel "
                "ins Meer. Dieses Meer hat jetzt seinen Namen.",
        easy_voc="audax: kühn · volatus: Flug · gaudere: sich freuen · coepit: er begann · deserere: verlassen · "
                 "altius: höher · cupere: verlangen · tabescere: schmelzen · bracchium: Arm · nudus: nackt · "
                 "cadere: fallen",
        help=[("cum ... coepit", "als (plötzlich) ... begann (cum inversum)"), ("audax, -acis", "kühn"),
              ("volatus, -us", "Flug"), ("deserere", "verlassen, im Stich lassen"),
              ("cupidine tractus", "von Begierde gezogen"), ("altius", "höher"),
              ("iter agere", "den Weg nehmen"), ("rapidus", "reißend, verzehrend"),
              ("vicinia", "Nähe"), ("mollit", "macht weich"), ("odoratus", "duftend"),
              ("vinculum", "Fessel, Band"), ("tabuerant", "Plqpf. von tabescere: war geschmolzen"),
              ("nudus", "nackt"), ("quatere", "schütteln, schlagen"), ("lacertus", "Arm"),
              ("remigium", "Ruderwerk (Metapher für die Flügel)"), ("carere (+ Abl.)", "nicht haben"),
              ("percipere", "fassen"), ("ora", "Mund (poetischer Plural)"), ("caeruleus", "blau"),
              ("clamantia", "PPA: rufend"), ("excipiuntur", "werden aufgenommen"),
              ("nomen traxit ab illo", "erhielt den Namen von ihm (Ikarisches Meer)")],
        build="[<b>cum</b> puer audaci <b>coepit</b> gaudere volatu] <b>deseruit</b>que ducem [<i>caelique "
              "cupidine tractus</i>] altius <b>egit</b> iter.",
        de="... als der Junge begann, sich über den kühnen Flug zu freuen, seinen Führer verließ und, vom "
           "Verlangen nach dem Himmel gezogen, seinen Weg höher nahm. Die Nähe der verzehrenden Sonne macht das "
           "duftende Wachs, die Fesseln der Federn, weich; das Wachs war geschmolzen: Er schlägt mit den nackten "
           "Armen, und ohne Ruderwerk fasst er keine Luft mehr, und sein Mund, der den Namen des Vaters rief, "
           "wird vom blauen Wasser aufgenommen, das von ihm seinen Namen erhielt.",
        check=[("<i>cum ... coepit</i> – welche Art von cum-Satz?",
                "cum inversum (mit Indikativ): „als plötzlich ...“ – die überraschende Wendung."),
               ("<i>pennarum vincula</i> – Stilmittel?",
                "Apposition mit Metapher: Das Wachs ist das „Band/die Fessel“ der Federn."),
               ("Warum steht <i>tabuerant</i> im Plusquamperfekt?",
                "Vorzeitigkeit und Tempo: Das Wachs ist schon geschmolzen, bevor er reagieren kann.")],
    ),
    dict(
        nr=8, v=(231, 235), title="Die Klage des Vaters",
        easy="Pater infelix clamavit: „Icare, ubi es? Ubi te quaeram?“ Tum pennas in undis vidit. Artes suas "
             "devovit et corpus filii in sepulcro condidit. Terra nomen filii accepit.",
        easy_de="Der unglückliche Vater rief: „Ikarus, wo bist du? Wo soll ich dich suchen?“ Dann sah er die "
                "Federn in den Wellen. Er verfluchte seine Künste und bestattete den Körper des Sohnes in einem "
                "Grab. Das Land erhielt den Namen des Sohnes.",
        easy_voc="infelix: unglücklich · quaerere: suchen · unda: Welle · devovere: verfluchen · "
                 "sepulcrum: Grab · condere: bestatten · accipere: erhalten",
        help=[("at", "aber"), ("infelix, -icis", "unglücklich"), ("nec iam pater", "und schon kein Vater mehr"),
              ("qua regione", "in welcher Gegend"), ("requiram", "Konj. (deliberativ): soll ich suchen?"),
              ("dicebat", "Imperfekt: sagte immer wieder"), ("aspexit", "erblickte"),
              ("devovere", "verfluchen"), ("sepulcrum", "Grab"), ("condere", "bergen, bestatten"),
              ("tellus, -uris f.", "Land, Erde"), ("dicta (est)", "wurde benannt"),
              ("sepultus", "der Begrabene (von sepelire)")],
        build="At pater infelix, [<i>nec iam pater</i>], „Icare,“ <b>dixit</b> ...",
        de="Aber der unglückliche Vater, der schon kein Vater mehr war, sagte: „Ikarus!“, sagte: „Ikarus, wo bist "
           "du? In welcher Gegend soll ich dich suchen?“ „Ikarus!“, rief er immer wieder: Da erblickte er die "
           "Federn in den Wellen, verfluchte seine Künste und barg den Körper in einem Grab, und das Land wurde "
           "nach dem Namen des Begrabenen benannt.",
        check=[("„Icare ... Icare ... Icare“ – Stilmittel und Wirkung?",
                "Anapher/Wiederholung (Geminatio): verzweifeltes Rufen, Klage, Hilflosigkeit."),
               ("<i>pater ... nec iam pater</i> – Stilmittel?",
                "Paradoxon: Ohne Sohn ist er kein Vater mehr."),
               ("Unterschied <i>dixit</i> – <i>dicebat</i>?",
                "dixit (Perfekt): einmalig; dicebat (Imperfekt): wiederholt, immer wieder.")],
    ),
]


# ============================================================
# INHALT: WORTSCHATZ
# ============================================================

# (Latein, Formen, Deutsch)
VOCAB_GROUPS = [
    ("Personen", [
        ("Daedalus", "Daedali m.", "Dädalus (Erfinder)"),
        ("Icarus", "Icari m.", "Ikarus (Vok.: Icare!)"),
        ("Minos", "Minois m.", "Minos, König von Kreta"),
        ("pater", "patris m.", "Vater"),
        ("natus", "nati m.", "Sohn"),
        ("filius", "filii m.", "Sohn"),
        ("puer", "pueri m.", "Junge, Knabe"),
        ("opifex", "opificis m.", "Künstler, Handwerker"),
        ("dux", "ducis m.", "Führer"),
        ("comes", "comitis m./f.", "Begleiter(in)"),
        ("pastor", "pastoris m.", "Hirte"),
        ("arator", "aratoris m.", "Pflüger"),
        ("deus", "dei m.", "Gott"),
    ]),
    ("Himmel, Meer & Natur", [
        ("caelum", "caeli n.", "Himmel"),
        ("aer", "aeris m. (Akk. aera)", "Luft"),
        ("aether", "aetheris m. (Akk. aethera)", "Himmel, Äther"),
        ("aura", "aurae f.", "Luft, Lufthauch"),
        ("sol", "solis m.", "Sonne"),
        ("ignis", "ignis m.", "Feuer"),
        ("unda", "undae f.", "Welle, Wasser"),
        ("pelagus", "pelagi n.", "Meer, offene See"),
        ("aqua", "aquae f.", "Wasser"),
        ("terra", "terrae f.", "Land, Erde"),
        ("tellus", "telluris f.", "Erde, Land"),
        ("avis", "avis f.", "Vogel"),
        ("ales", "alitis m./f.", "Vogel"),
        ("nidus", "nidi m.", "Nest"),
        ("proles", "prolis f.", "Nachwuchs"),
        ("regio", "regionis f.", "Gegend"),
        ("piscis", "piscis m.", "Fisch"),
        ("mel", "mellis n.", "Honig"),
    ]),
    ("Flügel, Körper & Handwerk", [
        ("ala", "alae f.", "Flügel"),
        ("penna", "pennae f.", "Feder"),
        ("pluma", "plumae f.", "Flaumfeder"),
        ("cera", "cerae f.", "Wachs"),
        ("linum", "lini n.", "Faden, Leinen"),
        ("ars", "artis f.", "Kunst, Fertigkeit"),
        ("opus", "operis n.", "Werk, Arbeit"),
        ("ordo", "ordinis m.", "Reihe, Ordnung"),
        ("vinculum", "vinculi n.", "Band, Fessel"),
        ("volatus", "volatus m.", "Flug"),
        ("iter", "itineris n.", "Weg, Reise"),
        ("limes", "limitis m.", "Grenze, Bahn"),
        ("remigium", "remigii n.", "Ruderwerk"),
        ("umerus", "umeri m.", "Schulter"),
        ("lacertus", "lacerti m.", "Oberarm"),
        ("pollex", "pollicis m.", "Daumen"),
        ("os", "oris n.", "Mund, Gesicht"),
        ("gena", "genae f.", "Wange"),
        ("osculum", "osculi n.", "Kuss"),
        ("corpus", "corporis n.", "Körper"),
        ("sepulcrum", "sepulcri n.", "Grab"),
        ("nomen", "nominis n.", "Name"),
        ("cupido", "cupidinis f.", "Begierde, Verlangen"),
        ("amor", "amoris m.", "Liebe"),
        ("exilium", "exilii n.", "Verbannung, Exil"),
        ("periculum", "periculi n.", "Gefahr"),
        ("praeceptum", "praecepti n.", "Vorschrift, Lehre"),
        ("monitus", "monitus m.", "Ermahnung"),
    ]),
    ("Verben", [
        ("claudere", "claudo, clausi, clausum", "(ein)schließen"),
        ("patere", "pateo, patui", "offenstehen"),
        ("obstruere", "obstruo, obstruxi, obstructum", "versperren"),
        ("possidere", "possideo, possedi, possessum", "besitzen"),
        ("dimittere", "dimitto, dimisi, dimissum", "entlassen; (animum) richten auf"),
        ("novare", "novo, novavi, novatum", "erneuern, verändern"),
        ("ponere", "pono, posui, positum", "setzen, legen"),
        ("alligare", "alligo, alligavi, alligatum", "festbinden"),
        ("flectere", "flecto, flexi, flexum", "biegen"),
        ("imitari", "imitor, imitatus sum", "nachahmen"),
        ("tractare", "tracto, tractavi, tractatum", "behandeln, berühren"),
        ("captare", "capto, captavi, captatum", "zu fangen suchen"),
        ("mollire", "mollio, mollivi, mollitum", "weich machen"),
        ("impedire", "impedio, impedivi, impeditum", "behindern"),
        ("librare", "libro, libravi, libratum", "im Gleichgewicht halten"),
        ("pendere", "pendeo, pependi", "hängen, schweben"),
        ("instruere", "instruo, instruxi, instructum", "ausrüsten, unterweisen"),
        ("monere", "moneo, monui, monitum", "(er)mahnen, warnen"),
        ("gravare", "gravo, gravavi, gravatum", "beschweren"),
        ("adurere", "aduro, adussi, adustum", "versengen"),
        ("volare", "volo, volavi, volatum", "fliegen"),
        ("carpere", "carpo, carpsi, carptum", "pflücken; (viam) nehmen"),
        ("tradere", "trado, tradidi, traditum", "übergeben, überliefern"),
        ("accommodare", "accommodo, accommodavi, accommodatum", "anpassen"),
        ("madere", "madeo, madui", "nass sein"),
        ("tremere", "tremo, tremui", "zittern"),
        ("levare", "levo, levavi, levatum", "heben"),
        ("timere", "timeo, timui", "(sich) fürchten"),
        ("hortari", "hortor, hortatus sum", "ermuntern, auffordern"),
        ("sequi", "sequor, secutus sum", "folgen"),
        ("erudire", "erudio, erudivi, eruditum", "unterrichten"),
        ("respicere", "respicio, respexi, respectum", "zurückblicken (auf)"),
        ("obstupescere", "obstupesco, obstipui", "erstarren, staunen"),
        ("credere", "credo, credidi, creditum", "glauben"),
        ("gaudere", "gaudeo, gavisus sum", "sich freuen"),
        ("deserere", "desero, deserui, desertum", "verlassen, im Stich lassen"),
        ("trahere", "traho, traxi, tractum", "ziehen"),
        ("agere", "ago, egi, actum", "treiben; (iter) nehmen"),
        ("tabescere", "tabesco, tabui", "schmelzen"),
        ("quatere", "quatio, -, quassum", "schütteln, schlagen"),
        ("percipere", "percipio, percepi, perceptum", "wahrnehmen, fassen"),
        ("excipere", "excipio, excepi, exceptum", "aufnehmen"),
        ("requirere", "requiro, requisivi, requisitum", "suchen, vermissen"),
        ("aspicere", "aspicio, aspexi, aspectum", "erblicken"),
        ("devovere", "devoveo, devovi, devotum", "verfluchen"),
        ("condere", "condo, condidi, conditum", "gründen; bestatten"),
        ("relinquere", "relinquo, reliqui, relictum", "zurücklassen, verlassen"),
        ("cadere", "cado, cecidi, casum", "fallen"),
        ("inquit / ait", "(nur einzelne Formen)", "sagt(e) er"),
    ]),
    ("Adjektive", [
        ("longus", "longa, longum", "lang"),
        ("natalis", "natalis, natale", "Geburts-"),
        ("ignotus", "ignota, ignotum", "unbekannt"),
        ("rusticus", "rustica, rusticum", "ländlich"),
        ("dispar", "disparis", "ungleich"),
        ("medius", "media, medium", "der mittlere"),
        ("imus", "ima, imum", "der unterste"),
        ("verus", "vera, verum", "wahr, echt"),
        ("ignarus", "ignara, ignarum", "unwissend"),
        ("vagus", "vaga, vagum", "umherschweifend"),
        ("flavus", "flava, flavum", "goldgelb, blond"),
        ("mirabilis", "mirabilis, mirabile", "wunderbar"),
        ("geminus", "gemina, geminum", "doppelt, Zwillings-"),
        ("celsus", "celsa, celsum", "hoch"),
        ("demissus", "demissa, demissum", "niedrig, tief"),
        ("damnosus", "damnosa, damnosum", "verderblich"),
        ("tremulus", "tremula, tremulum", "zitternd"),
        ("audax", "audacis", "kühn"),
        ("rapidus", "rapida, rapidum", "reißend, verzehrend"),
        ("odoratus", "odorata, odoratum", "duftend"),
        ("nudus", "nuda, nudum", "nackt"),
        ("caeruleus", "caerulea, caeruleum", "blau"),
        ("infelix", "infelicis", "unglücklich"),
        ("tener", "tenera, tenerum", "zart"),
        ("fecundus", "fecunda, fecundum", "fruchtbar, reich an"),
    ]),
]

SMALL_WORDS = [
    ("interea", "inzwischen"), ("certe", "sicher(lich)"), ("illac", "dort entlang"),
    ("quondam", "einst"), ("paulatim", "allmählich"), ("una", "zusammen, mit dabei"),
    ("modo ... modo", "bald ... bald"), ("pariter", "zugleich, gleichermaßen"), ("velut", "wie"),
    ("iterum", "wieder"), ("altius", "höher"), ("qua", "wo, auf welchem Weg"),
    ("nec iam", "nicht mehr"), ("at", "aber"), ("sic", "so"), ("ita", "so, auf diese Weise"),
    ("ut + Indikativ", "wie"), ("ut + Konjunktiv", "dass, damit, sodass"), ("ne + Konj.", "damit nicht"),
    ("dum", "während"), ("cum + Ind.", "als, wenn"), ("cum + Konj.", "als, weil, obwohl"),
    ("postquam", "nachdem"), ("si", "wenn"), ("nam", "denn"), ("tum", "dann, da"),
    ("ante (Adv.)", "vorn, voraus"), ("inter + Akk.", "zwischen"), ("-que", "und (angehängt)"),
    ("aut", "oder"),
]


# ============================================================
# STARTSEITEN: Deckblatt, Gebrauchsanweisung, Fahrpläne
# ============================================================

def plan_table(rows):
    data = [["", "Zeit", "Was du machst", "Kapitel"]]
    for t, what, where in rows:
        data.append([CheckBox(13, "geschafft"), t, what, where])
    return table(data, [0.9 * cm, 2.1 * cm, 11.0 * cm, 3.6 * cm], center_cols=(0,), bold_cols=(1,))


def front_matter():
    CTX.chapter = "Start"
    f = [Cover(), sp(0.6), P("Inhalt", "h1")]
    f.append(table([
        ["", "Kapitel", "Was drin ist"],
        ["0", "So holst du morgen das Beste raus", "Fahrpläne (2 h / 4–5 h) zum Abhaken, Fortschritts-Tracker"],
        ["1", "Die Übersetzungsmethode", "5-Schritte-Routine, Notfall-Regel, Satzkern finden"],
        ["2", "Verben & Zeitformen", "Endungen, alle 6 Zeiten, Perfektstämme, Partizipien, Konjunktiv"],
        ["3", "Kasus & Satzbau", "Kasus-Fragen, Ablativ-Funktionen, Endungstabelle, Hyperbaton"],
        ["4", "Vokabeln zum Ovid-Text", "ca. 130 Wörter + Kleinwörter, zwei Tests, Rätsel"],
        ["5", "Übersetzen in 3 Stufen", "8 Abschnitte: vereinfacht > Original mit Hilfen > Klausurmodus"],
        ["6", "Stilmittel, Interpretation & Metrik", "14 Stilmittel, Hybris, Schuldfrage, Hexameter"],
        ["7", "Probeklausur", "90 Minuten mit Bewertungsraster, Fehlerprotokoll"],
        ["", "Spickzettel · Lösungen · Anhang", "1 Seite für morgen früh · alle Lösungen · 500 Grundwörter"],
    ], [0.9 * cm, 6.2 * cm, 10.5 * cm], bold_cols=(0, 1)))
    f.append(PageBreak())
    f += chapter(0, "So holst du morgen das Beste raus", "Erst lesen (3 Minuten), dann loslegen")
    f += box("ziel", [
        "Du musst morgen vor allem <b>drei Dinge</b> können:",
        "<b>1.</b> Verb finden und Person/Zeit bestimmen. "
        "<b>2.</b> Satzbau erkennen: Wer macht was mit wem? "
        "<b>3.</b> Vokabeln schnell erkennen und daraus sinnvolles Deutsch bauen.",
        "Nicht: sämtliche Grammatikregeln auswendig können. Du lernst nicht „Latein von vorn“, "
        "sondern trainierst gezielt das, was in der Übersetzung Punkte bringt.",
    ])
    f += H1("So benutzt du das Paket am iPad")
    f += [P(
        "• Öffne die PDF in einer App mit Stift-Funktion (z. B. GoodNotes, Notability, Apple Dateien/"
        "Markierungen, Acrobat). Die <b>Kästchen</b> hinter jeder Aufgabe kannst du <b>antippen</b> – "
        "so siehst du deinen Fortschritt.<br/>"
        "• Die <b>blauen Linien</b> sind zum Schreiben mit dem Apple Pencil gedacht.<br/>"
        "• Jede Aufgabe hat eine <b>Stufe</b>: ein Punkt = Basis, zwei = Aufbau, drei = Profi. "
        "Wenig Zeit? Mach zuerst alle Basis-Aufgaben.<br/>"
        "• Die <b>Lösungen</b> stehen hinten (bzw. in jeder Kapitel-PDF am Ende). Erst selbst probieren!<br/>"
        "• Über die <b>Lesezeichen</b> (Inhaltsverzeichnis deiner PDF-App) springst du direkt zu Kapiteln "
        "und Aufgaben.")]
    f += H1("Wähle deinen Fahrplan – und hake ab")
    f.append(P("<b>A) Notfallplan: nur noch 2 Stunden</b>", "h2"))
    f.append(plan_table([
        ("20 min", "Grammatik-Signale: Endungen und Zeiten erkennen (Merkkästen + Aufgabe 2.1, 2.2)", "Kap. 1 + 2"),
        ("20 min", "Vokabeln: die Ovid-Liste Latein > Deutsch abdecken, Unbekanntes ankreuzen", "Kap. 4"),
        ("70 min", "Übersetzen: Abschnitte 1–8 in Stufe 2 (Original mit Hilfen), Methode anwenden", "Kap. 5"),
        ("10 min", "Fehlerprotokoll + Spickzettel durchlesen, dann schlafen", "Kap. 7 + 10"),
    ]))
    f.append(P("<b>B) Gründlich: 4–5 Stunden (z. B. auf zwei Tage verteilt)</b>", "h2"))
    f.append(plan_table([
        ("30 min", "Methode + Verben/Zeitformen inkl. Zeitmaschine und Zuordnen", "Kap. 1 + 2"),
        ("30 min", "Kasus & Satzbau, Ablativ-Funktionen, Wortgitter", "Kap. 3"),
        ("40 min", "Vokabeln lernen + beide Tests + Kreuzworträtsel", "Kap. 4"),
        ("90 min", "Übersetzung: jeder Abschnitt Stufe 1, dann Stufe 2; am Ende Stufe 3", "Kap. 5"),
        ("30 min", "Stilmittel, Interpretation, Metrik", "Kap. 6"),
        ("45 min", "Probeklausur unter Zeitdruck, danach mit Lösung korrigieren", "Kap. 7"),
        ("15 min", "Fehlerprotokoll + Spickzettel", "Kap. 7 + 10"),
    ]))
    f += box("achtung", "Morgen vor der Arbeit <b>keine neue Grammatik</b> mehr reinprügeln. Lieber 10–15 Minuten "
                        "deine Fehler und die Vokabeln anschauen. Und: Ausschlafen bringt mehr Punkte als eine "
                        "Stunde Pauken um Mitternacht.")
    f.append(PageBreak())
    return f


def tracker():
    CTX.chapter = "Fortschritt"
    f = chapter(0, "Fortschritts-Tracker", "Alle Aufgaben auf einen Blick – antippen, wenn geschafft")
    f.append(P("Hake hier jede Aufgabe ab, die du geschafft hast. Die Punkte zeigen die Stufe "
               "(Basis / Aufbau / Profi).", "body"))
    by_chap = {}
    for chap, nr, title, level in CTX.tasks:
        by_chap.setdefault(chap, []).append((nr, title, level))
    for chap, items in by_chap.items():
        data = [["", "Nr.", chap, "Stufe"]]
        for nr, title, level in items:
            data.append([CheckBox(12, f"Aufgabe {nr}"), nr, title, LEVEL_NAME[level]])
        f.append(KeepTogether([table(data, [0.9 * cm, 1.2 * cm, 12.7 * cm, 2.8 * cm],
                                     center_cols=(0,), bold_cols=(1,)), sp(0.3)]))
    f.append(PageBreak())
    return f


# ============================================================
# KAPITEL 1: DIE ÜBERSETZUNGSMETHODE
# ============================================================

def kap1():
    f = chapter(1, "Die Übersetzungsmethode", "Verb > Wer? > Wen/was? > Rest > Deutsch")
    f += box("ziel", "Bei jedem lateinischen Satz innerhalb von 5 Sekunden das <b>Prädikat</b> finden – und "
                     "danach systematisch statt Wort für Wort übersetzen.")
    f += H1("Die 5-Schritte-Routine")
    f.append(StepChain([("Verb", "einkreisen, bestimmen"), ("Wer?", "Nominativ suchen"),
                        ("Wen/was?", "Akkusativ, Dativ"), ("Rest", "Abl., Gen., Adverbien"),
                        ("Deutsch", "erst jetzt glätten")]))
    f.append(sp(0.3))
    f.append(table([
        ["Schritt", "Was du tust", "Frage"],
        ["1  Prädikat", "Alle Verben einkreisen. Person und Zeit an der Endung bestimmen.", "Was passiert?"],
        ["2  Subjekt", "Nominativ suchen, der zur Person des Verbs passt. Steckt oft schon im Verb!", "Wer?"],
        ["3  Objekte", "Akkusativ = direktes Objekt, Dativ = Empfänger.", "Wen/was? Wem?"],
        ["4  Rest", "Ablativ (womit? wodurch? woher? wann?), Genitiv (wessen?), Adverbien, Nebensätze.",
         "Wie, wo, wann, warum?"],
        ["5  Glätten", "Erst grammatisch korrekt, dann natürliches Deutsch. Wortstellung umbauen erlaubt!",
         "Klingt das deutsch?"],
    ], [2.6 * cm, 11.2 * cm, 3.8 * cm], bold_cols=(0,)))
    f += box("trick", [
        "Nicht: <i>Lateinwort > deutsches Wort > nächstes Lateinwort ...</i>",
        "Sondern: <b>Verb > Wer? > Wen/was? > Zusatzinfos > deutscher Satz.</b>",
        "Bei Ovid stehen zusammengehörige Wörter oft weit auseinander (Hyperbaton). "
        "Suche zu jedem Adjektiv sein Nomen – gleiche Endung bzw. gleicher Kasus, Numerus, Genus (KNG).",
    ])
    f += H1("Vorgemacht: Schritt für Schritt")
    f.append(verse_block(verses(231, 231)))
    f.append(sp(0.2))
    f.append(table([
        ["Schritt", "Ergebnis"],
        ["1  Verb", "<i>dixit</i> – 3. Sg. Perfekt von dicere: <b>er sagte</b>"],
        ["2  Wer?", "<i>pater</i> (Nom. Sg.) + <i>infelix</i> (passt in KNG): <b>der unglückliche Vater</b>"],
        ["3  Wen/was?", "Kein Akkusativ – stattdessen direkte Rede: <i>„Icare“</i> = Vokativ: <b>„Ikarus!“</b>"],
        ["4  Rest", "<i>at</i> = aber; <i>nec iam pater</i> = und schon nicht mehr Vater"],
        ["5  Deutsch", "<b>„Aber der unglückliche Vater, der schon kein Vater mehr war, sagte: ‚Ikarus!‘“</b>"],
    ], [2.6 * cm, 15.0 * cm], bold_cols=(0,)))
    f += box("merke", [
        "<b>Notfall-Regel – sie rettet dir morgen viele Punkte:</b> Wenn du einen Satz nicht komplett verstehst, "
        "gib NICHT auf. Schreib das, was du sicher weißt.",
        "Beispiel: <i>At pater infelix ... dixit ...</i> – du kennst pater, infelix, dixit. Also schreibst du schon: "
        "„Aber der unglückliche Vater sagte ...“. Eine halbwegs sinnvolle Teilübersetzung bringt deutlich mehr "
        "als eine leere Stelle. Unbekannte Stelle markieren, weitergehen, am Ende zurückkommen.",
    ])

    f += task("1.1", "Satzkern finden: Prädikat – Subjekt – Objekt", 1, 10,
              "Trage für jeden Satz Prädikat, Subjekt und Objekt ein und übersetze dann.")
    sents = [
        ("Daedalus pennas in ordine ponit.", "ponit", "Daedalus", "pennas",
         "Dädalus legt die Federn in eine Reihe."),
        ("Puer Icarus plumas captabat.", "captabat", "puer Icarus", "plumas",
         "Der Junge Ikarus haschte nach den Federn."),
        ("Pater filio oscula dedit.", "dedit", "pater", "oscula (Akk.), filio (Dat.)",
         "Der Vater gab dem Sohn Küsse."),
        ("Rapidus sol ceras mollit.", "mollit", "rapidus sol", "ceras",
         "Die verzehrende Sonne macht das Wachs weich."),
        ("Pastor patrem et filium vidit.", "vidit", "pastor", "patrem et filium",
         "Der Hirte sah den Vater und den Sohn."),
        ("Icarus monita patris neglegit.", "neglegit", "Icarus", "monita (patris = Gen.)",
         "Ikarus missachtet die Ermahnungen des Vaters."),
        ("Unda corpus pueri excepit.", "excepit", "unda", "corpus (pueri = Gen.)",
         "Die Welle nahm den Körper des Jungen auf."),
        ("Daedalus artes suas devovit.", "devovit", "Daedalus", "artes suas",
         "Dädalus verfluchte seine Künste."),
    ]
    rows = [[s[0]] for s in sents]
    f.append(fill_table(["Satz", "Prädikat", "Subjekt", "Objekt(e)"], rows,
                        [6.4 * cm, 3.2 * cm, 3.6 * cm, 4.4 * cm], row_h=1.0 * cm))
    f.append(sp(0.2))
    f.append(P("Übersetzungen (Satz 1–8):", "small"))
    f.append(Lines(8))
    solution("1.1", "Satzkern finden",
             table([["Satz", "Prädikat", "Subjekt", "Objekt(e)", "Übersetzung"]] +
                   [[s[0], s[1], s[2], s[3], s[4]] for s in sents],
                   [4.1 * cm, 2.0 * cm, 2.4 * cm, 3.2 * cm, 5.9 * cm], lat_cols=(0, 1)))

    f += task("1.2", "Teilübersetzung retten (Notfall-Training)", 2, 8,
              "Du kennst nicht jedes Wort – macht nichts. Schreib zu jedem Satz auf, was du <b>sicher</b> "
              "verstehst, und mach daraus einen deutschen Satz(anfang).")
    f.append(verse_block([(225, "... rapidi vicinia solis"), (226, OVID[226])]))
    f.append(Lines(2, label="Was ich sicher weiß / mein Satz:"))
    f.append(verse_block(verses(229, 230)))
    f.append(Lines(2, label="Was ich sicher weiß / mein Satz:"))
    solution("1.2", "Teilübersetzung retten",
             "v. 225 f.: Sicher erkennbar: <i>solis</i> = der Sonne, <i>mollit</i> = macht weich, "
             "<i>ceras</i> = das Wachs. Notfallsatz: „(Die Nähe) der Sonne macht das Wachs weich.“ – "
             "Vollständig: „Die Nähe der verzehrenden Sonne macht das duftende Wachs, die Fesseln der Federn, weich.“",
             "v. 229 f.: Sicher: <i>patrium nomen</i> = den Namen des Vaters, <i>clamantia</i> = rufend, "
             "<i>aqua</i> = Wasser, <i>nomen traxit</i> = hat den Namen bekommen. Notfallsatz: „... rufend den "
             "Namen des Vaters ... vom Wasser ..., das den Namen erhielt.“ – Vollständig: „Sein Mund, der den "
             "Namen des Vaters rief, wird vom blauen Wasser aufgenommen, das von ihm seinen Namen erhielt.“")

    f += task("1.3", "Farbmarkierung direkt im Text", 2, 8,
              "Markiere mit dem Pencil: <b>Verben rot</b>, <b>Subjekte blau</b>, <b>Akkusativ-Objekte grün</b>. "
              "Verbinde zusammengehörige Adjektive und Nomen mit einem Bogen.")
    f.append(Table([[verse_block(verses(200, 203))]], colWidths=[CONTENT_W]))
    f.append(sp(0.2))
    f.append(Lines(2, label="Notizen:"))
    solution("1.3", "Farbmarkierung",
             "Verben: <i>inposita est, libravit, pependit, instruit, curras</i>. "
             "Subjekte: <i>manus ultima</i> (zu inposita est), <i>opifex ipse</i> (zu libravit, pependit, instruit). "
             "Akkusative: <i>suum corpus</i> (zu libravit), <i>natum</i> (zu instruit). "
             "Bögen: <i>manus ultima</i>, <i>geminas ... alas</i>, <i>mota ... aura</i>, <i>medio ... limite</i>.")
    f.append(sp(0.3))
    f.append(RatingRow("Wie sicher sitzt die Methode?"))
    f.append(PageBreak())
    return f


# ============================================================
# KAPITEL 2: VERBEN & ZEITFORMEN
# ============================================================

def kap2():
    f = chapter(2, "Verben & Zeitformen", "Endung > Person · Tempuszeichen > Zeit")
    f += box("ziel", "Du musst die Zeiten nicht theoretisch erklären können – du musst sie beim Übersetzen "
                     "<b>erkennen</b>. Die Endung verrät die Person, das Zeichen davor die Zeit.")
    f += H1("1. Personalendungen")
    f.append(table([
        ["Person", "Aktiv (Präsens-Stamm)", "Perfekt aktiv", "Passiv", "Deutsch"],
        ["1. Sg.", "-o / -m", "-i", "-r", "ich"],
        ["2. Sg.", "-s", "-isti", "-ris", "du"],
        ["3. Sg.", "-t", "-it", "-tur", "er / sie / es"],
        ["1. Pl.", "-mus", "-imus", "-mur", "wir"],
        ["2. Pl.", "-tis", "-istis", "-mini", "ihr"],
        ["3. Pl.", "-nt", "-erunt (dichterisch auch -ere!)", "-ntur", "sie"],
    ], [2.0 * cm, 4.0 * cm, 4.8 * cm, 2.6 * cm, 4.2 * cm], bold_cols=(0,)))
    f += box("achtung", "Bei Ovid: <i>maduere</i> = maduerunt, <i>tremuere</i> = tremuerunt. "
                        "Die Endung <b>-ere</b> nach einem Perfektstamm ist die Kurzform der 3. Pl. Perfekt – "
                        "kein Infinitiv!")
    f += H1("2. Die sechs Zeiten – woran du sie erkennst")
    f.append(table([
        ["Tempus", "Kennzeichen", "vocare (a-Konj.)", "esse", "Deutsch", "In Erzählungen"],
        ["Präsens", "Präsensstamm + Endung", "vocat", "est", "er ruft", "oft „historisches Präsens“: lebendig"],
        ["Imperfekt", "<b>-ba-</b> (esse: era-)", "vocabat", "erat", "er rief", "Hintergrund, Dauer, Wiederholung"],
        ["Futur I", "<b>-b-</b> (a/e-Konj.), <b>-a-/-e-</b> (andere)", "vocabit", "erit", "er wird rufen",
         "in wörtlicher Rede"],
        ["Perfekt", "Perfektstamm + -i, -isti, -it ...", "vocavit", "fuit", "er rief / hat gerufen",
         "Handlungskette: dann ... dann"],
        ["Plusquamperf.", "Perfektstamm + <b>-era-</b>", "vocaverat", "fuerat", "er hatte gerufen",
         "Vorzeitigkeit: war schon passiert"],
        ["Futur II", "Perfektstamm + <b>-er-/-eri-</b>", "vocaverit", "fuerit", "er wird gerufen haben",
         "selten, meist in si-Sätzen"],
    ], [2.4 * cm, 3.8 * cm, 2.4 * cm, 1.5 * cm, 3.3 * cm, 4.2 * cm], bold_cols=(0,), lat_cols=(2, 3)))
    f += box("tipp", "Im Deutschen darfst du das historische Präsens (<i>ponit, novat, flectit</i>) ins Präteritum "
                     "setzen, wenn der Rest der Erzählung im Präteritum steht – Hauptsache einheitlich!")

    f.append(CondPageBreak(9 * cm))
    f += H1("3. Volle Konjugation: vocare und esse")
    pers = ["1. Sg.", "2. Sg.", "3. Sg.", "1. Pl.", "2. Pl.", "3. Pl."]
    voc = {
        "Präsens": ["voco", "vocas", "vocat", "vocamus", "vocatis", "vocant"],
        "Imperfekt": ["vocabam", "vocabas", "vocabat", "vocabamus", "vocabatis", "vocabant"],
        "Futur I": ["vocabo", "vocabis", "vocabit", "vocabimus", "vocabitis", "vocabunt"],
        "Perfekt": ["vocavi", "vocavisti", "vocavit", "vocavimus", "vocavistis", "vocaverunt"],
        "Plusqpf.": ["vocaveram", "vocaveras", "vocaverat", "vocaveramus", "vocaveratis", "vocaverant"],
        "Futur II": ["vocavero", "vocaveris", "vocaverit", "vocaverimus", "vocaveritis", "vocaverint"],
    }
    es = {
        "Präsens": ["sum", "es", "est", "sumus", "estis", "sunt"],
        "Imperfekt": ["eram", "eras", "erat", "eramus", "eratis", "erant"],
        "Futur I": ["ero", "eris", "erit", "erimus", "eritis", "erunt"],
        "Perfekt": ["fui", "fuisti", "fuit", "fuimus", "fuistis", "fuerunt"],
        "Plusqpf.": ["fueram", "fueras", "fuerat", "fueramus", "fueratis", "fuerant"],
        "Futur II": ["fuero", "fueris", "fuerit", "fuerimus", "fueritis", "fuerint"],
    }
    for name, d in (("vocare – rufen", voc), ("esse – sein", es)):
        rows = [[name] + list(d.keys())]
        for i, p_ in enumerate(pers):
            rows.append([p_] + [d[k][i] for k in d])
        f.append(table(rows, [2.6 * cm] + [2.5 * cm] * 6, bold_cols=(0,), lat_cols=(1, 2, 3, 4, 5, 6)))
        f.append(sp(0.25))

    f += H1("4. Perfekt erkennen – die Perfektstämme")
    f.append(P("Das Perfekt ist DIE Erzählzeit. Der Stamm verändert sich oft – lerne die Typen:", "body"))
    f.append(table([
        ["Typ", "Bildung", "Beispiele aus dem Ovid-Text"],
        ["v-Perfekt", "Stamm + v", "libra-v-it (er hielt im Gleichgewicht), devo-v-it (verfluchte)"],
        ["u-Perfekt", "Stamm + u", "obstip-u-it (staunte), tab-u-erant (waren geschmolzen), mad-u-ere"],
        ["s-Perfekt", "Stamm + s (c/g + s = x)", "dixit (dic-s-it), traxit, produxit, aspexit"],
        ["Dehnung", "Stammvokal wird lang/verändert", "vidit (videre), egit (agere), cepit (capere), fecit"],
        ["Reduplikation", "Anfangssilbe verdoppelt", "dedit (dare), pependit (pendere), cecidit (cadere)"],
        ["Stammperfekt", "Stamm bleibt fast gleich", "condidit (condere), credidit (credere), deseruit"],
    ], [3.0 * cm, 4.4 * cm, 10.2 * cm], bold_cols=(0,)))

    f += H1("5. Was sonst noch im Text vorkommt")
    f.append(table([
        ["Form", "Erkennen", "Übersetzen", "Beispiele aus dem Text"],
        ["Infinitiv", "-re (Präs.), -isse (Perf.), -ri/-i (Passiv)", "„zu ...“ oder nach Verben",
         "gaudere coepit, sequi hortatur, crevisse"],
        ["Imperativ", "Stamm (Sg.), -te (Pl.)", "Befehl: flieg!", "vola, carpe"],
        ["PPP", "-tus/-sus, -a, -um", "„(nachdem er) ... worden war“, „ge-...“",
         "clausus, tactus, levatus, relictae, conpositas"],
        ["PPA", "-ns, -ntis", "„...end“, „während er ...“", "renidenti, sequenti, clamantia, carens"],
        ["Abl. abs.", "Nomen + Partizip im Ablativ", "„während / nachdem / wobei ...“",
         "breviore sequenti, me duce"],
        ["AcI", "Akkusativ + Infinitiv nach Verben des Sagens/Glaubens", "„dass ...“",
         "credidit esse deos; se tractare"],
        ["Konjunktiv", "-e- (a-Konj.), -a- (andere), -re-, -isse-", "je nach Satzart: „möge“, „damit“, „dass“",
         "obstruat, possideat, gravet, adurat, requiram"],
    ], [2.2 * cm, 4.6 * cm, 4.6 * cm, 6.2 * cm], bold_cols=(0,), lat_cols=(3,)))

    # ---------- Übungen ----------
    f += task("2.1", "Endungs-Blitz: Person und Numerus", 1, 5,
              "Bestimme Person und Numerus und übersetze. Tempo! Ziel: unter 3 Minuten.")
    forms = [("timet", "3. Sg.", "er fürchtet"), ("timent", "3. Pl.", "sie fürchten"),
             ("timeo", "1. Sg.", "ich fürchte"), ("times", "2. Sg.", "du fürchtest"),
             ("volamus", "1. Pl.", "wir fliegen"), ("volatis", "2. Pl.", "ihr fliegt"),
             ("dixit", "3. Sg.", "er sagte"), ("dixerunt", "3. Pl.", "sie sagten"),
             ("dixi", "1. Sg.", "ich sagte"), ("dixisti", "2. Sg.", "du sagtest"),
             ("monebat", "3. Sg.", "er ermahnte"), ("monebant", "3. Pl.", "sie ermahnten"),
             ("ibimus", "1. Pl.", "wir werden gehen"), ("ibis", "2. Sg.", "du wirst gehen"),
             ("excipiuntur", "3. Pl.", "sie werden aufgenommen"), ("hortatur", "3. Sg.", "er ermuntert")]
    half = len(forms) // 2
    rows = []
    for i in range(half):
        rows.append([forms[i][0], "", "", forms[i + half][0], "", ""])
    f.append(table([["Form", "Person", "Übersetzung", "Form", "Person", "Übersetzung"]] + rows,
                   [2.4 * cm, 1.8 * cm, 4.6 * cm, 2.4 * cm, 1.8 * cm, 4.6 * cm],
                   lat_cols=(0, 3), row_h=0.9 * cm, zebra=False))
    solution("2.1", "Endungs-Blitz",
             table([["Form", "Person", "Übersetzung"]] + [list(x) for x in forms],
                   [3.5 * cm, 2.5 * cm, 6 * cm], lat_cols=(0,)))

    f += task("2.2", "Tempus-Detektiv: Formen aus dem Ovid-Text", 1, 12,
              "Alle Formen stammen aus Met. 8, 183–235. Bestimme Tempus und Person und übersetze.")
    det = [
        ("erat", "Imperfekt", "3. Sg.", "er war"), ("ibimus", "Futur I", "1. Pl.", "wir werden gehen"),
        ("dixit", "Perfekt", "3. Sg.", "er sagte"), ("dimittit", "Präsens", "3. Sg.", "er richtet"),
        ("stabat", "Imperfekt", "3. Sg.", "er stand"), ("moverat", "Plusquamperfekt", "3. Sg.", "er hatte bewegt"),
        ("captabat", "Imperfekt", "3. Sg.", "er haschte"), ("libravit", "Perfekt", "3. Sg.", "er hielt im Gleichgewicht"),
        ("pependit", "Perfekt", "3. Sg.", "er schwebte"), ("ibis", "Futur I", "2. Sg.", "du wirst gehen/fliegen"),
        ("maduere", "Perfekt", "3. Pl.", "sie wurden nass"), ("dedit", "Perfekt", "3. Sg.", "er gab"),
        ("produxit", "Perfekt", "3. Sg.", "er hat hinausgeführt"), ("obstipuit", "Perfekt", "3. Sg.", "er staunte"),
        ("fuerant relictae", "Plqpf. Passiv", "3. Pl.", "sie waren zurückgelassen worden"),
        ("coepit", "Perfekt", "3. Sg.", "er begann"), ("tabuerant", "Plusquamperfekt", "3. Pl.", "sie waren geschmolzen"),
        ("excipiuntur", "Präsens Passiv", "3. Pl.", "sie werden aufgenommen"),
        ("dicebat", "Imperfekt", "3. Sg.", "er sagte (immer wieder)"), ("condidit", "Perfekt", "3. Sg.", "er bestattete"),
    ]
    f.append(fill_table(["Form", "Tempus", "Person", "Übersetzung"], [[d[0]] for d in det],
                        [3.6 * cm, 3.6 * cm, 2.2 * cm, 8.2 * cm], row_h=0.92 * cm))
    solution("2.2", "Tempus-Detektiv",
             table([["Form", "Tempus", "Person", "Übersetzung"]] + [list(d) for d in det],
                   [3.5 * cm, 3.5 * cm, 2 * cm, 8.5 * cm], lat_cols=(0,)))

    f += task("2.3", "Zeitmaschine: Setze die Form in die anderen Zeiten", 2, 12,
              "Gleiche Person, gleicher Numerus – nur die Zeit ändert sich.")
    tm = [("volat", "volabat", "volavit", "volaverat", "volabit"),
          ("timet", "timebat", "timuit", "timuerat", "timebit"),
          ("dicit", "dicebat", "dixit", "dixerat", "dicet"),
          ("capit", "capiebat", "cepit", "ceperat", "capiet"),
          ("est", "erat", "fuit", "fuerat", "erit"),
          ("it", "ibat", "iit", "ierat", "ibit"),
          ("ponunt", "ponebant", "posuerunt", "posuerant", "ponent"),
          ("vident", "videbant", "viderunt", "viderant", "videbunt")]
    f.append(fill_table(["Präsens", "Imperfekt", "Perfekt", "Plusquamperfekt", "Futur I"],
                        [[t[0]] for t in tm], [3.0 * cm, 3.6 * cm, 3.6 * cm, 3.8 * cm, 3.6 * cm], row_h=1.0 * cm))
    solution("2.3", "Zeitmaschine",
             table([["Präsens", "Imperfekt", "Perfekt", "Plusquamperfekt", "Futur I"]] + [list(t) for t in tm],
                   [3.0 * cm, 3.4 * cm, 3.4 * cm, 3.8 * cm, 3.4 * cm], lat_cols=(0, 1, 2, 3, 4)))

    f += task("2.4", "Stammformen-Match: Verbinde Perfekt und Infinitiv", 1, 5,
              "Zieh mit dem Pencil eine Linie vom Punkt links zum passenden Punkt rechts.")
    pairs = [("dixit", "dicere – sagen"), ("cepit", "capere – nehmen"), ("reliquit", "relinquere – verlassen"),
             ("condidit", "condere – bestatten"), ("vidit", "videre – sehen"), ("traxit", "trahere – ziehen"),
             ("egit", "agere – treiben"), ("dedit", "dare – geben"), ("cecidit", "cadere – fallen"),
             ("produxit", "producere – hinausführen")]
    rng = random.Random(11)
    right = [p[1] for p in pairs]
    rng.shuffle(right)
    f[-3:] = [KeepTogether(f[-3:] + [MatchGame([p[0] for p in pairs], right)])]
    solution("2.4", "Stammformen-Match", " · ".join(f"<i>{a}</i> = {b}" for a, b in pairs))

    f += task("2.5", "Partizipien jagen", 3, 12,
              "Bestimme bei jedem Partizip die Art (PPP/PPA), das Bezugswort und übersetze passend.")
    pt = [("tactus (184)", "PPP", "Daedalus", "ergriffen (von Liebe)"),
          ("coeptas (190)", "PPP", "pennas", "begonnen (mit der kleinsten)"),
          ("renidenti (197)", "PPA", "ore", "strahlend"),
          ("mota (202)", "PPP", "aura", "bewegt"),
          ("levatus (212)", "PPP", "Daedalus", "emporgehoben"),
          ("tractus (224)", "PPP", "puer", "gezogen"),
          ("carens (228)", "PPA", "ille (Icarus)", "ohne ... (entbehrend)"),
          ("clamantia (229)", "PPA", "ora", "rufend")]
    f.append(fill_table(["Partizip (Vers)", "Art", "Bezugswort", "Übersetzung"], [[p[0]] for p in pt],
                        [3.8 * cm, 2.0 * cm, 4.0 * cm, 7.8 * cm], row_h=0.95 * cm))
    solution("2.5", "Partizipien jagen",
             table([["Partizip", "Art", "Bezugswort", "Übersetzung"]] + [list(p) for p in pt],
                   [3.8 * cm, 1.8 * cm, 3.6 * cm, 8.4 * cm], lat_cols=(0, 2)))

    f += task("2.6", "Konjunktiv-Radar: Warum steht hier ein Konjunktiv?", 3, 10,
              "Ordne jeder Stelle die passende Erklärung zu (Buchstabe eintragen) und übersetze die Form.")
    kj = [("obstruat (186)", "A", "mag er versperren"), ("putes (191)", "B", "man könnte glauben"),
          ("imitetur (195)", "C", "damit/sodass er nachahmt"), ("curras (203)", "D", "dass du fliegst"),
          ("gravet (205)", "E", "damit nicht ... beschwert"), ("requiram (232)", "F", "soll ich suchen?")]
    f.append(P("<b>A</b> einräumend: „mag auch“ · <b>B</b> Möglichkeit: „man könnte“ · "
               "<b>C</b> ut-Satz: Zweck/Folge · <b>D</b> ut-Satz nach „ermahnen“ (Begehrsatz) · "
               "<b>E</b> ne-Satz: „damit nicht“ · <b>F</b> Überlegungsfrage: „soll ich ...?“", "box"))
    f.append(fill_table(["Stelle", "Erklärung", "Übersetzung"], [[k[0]] for k in kj],
                        [4.0 * cm, 2.6 * cm, 11.0 * cm], row_h=0.95 * cm))
    solution("2.6", "Konjunktiv-Radar",
             table([["Stelle", "Erklärung", "Übersetzung"]] + [list(k) for k in kj],
                   [4 * cm, 2.5 * cm, 11 * cm], lat_cols=(0,)))

    f += crossword_flows("2.7", "Kreuzworträtsel: Verbformen", [
        ("DIXIT", "er sagte"), ("CEPIT", "er nahm"), ("VIDIT", "er sah"), ("ERAT", "er war"),
        ("IBIMUS", "wir werden gehen"), ("VOLAT", "er fliegt"), ("TIMET", "er fürchtet"),
        ("DEDIT", "er gab"), ("TRAXIT", "er zog"), ("CECIDIT", "er fiel"), ("CONDIDIT", "er bestattete"),
        ("RELIQUIT", "er verließ"), ("MOVERAT", "er hatte bewegt"), ("STABAT", "er stand (gerade)"),
        ("COEPIT", "er begann"), ("ASPEXIT", "er erblickte"), ("FUERAT", "er war gewesen"),
    ], seed=21, level=1)
    f.append(sp(0.3))
    f.append(RatingRow("Wie sicher erkennst du die Zeiten?"))
    f.append(PageBreak())
    return f


# ============================================================
# KAPITEL 3: KASUS & SATZBAU
# ============================================================

def kap3():
    f = chapter(3, "Kasus & Satzbau", "Nicht auswendig, sondern praktisch: Welche Frage beantwortet das Wort?")
    f += box("ziel", "Der größte Hebel für deine Übersetzung: Zu jedem Nomen sofort die passende <b>Frage</b> "
                     "stellen – Wer? Wen? Wem? Wessen? Womit/wodurch/woher?")
    f += H1("1. Die Kasus und ihre Aufgaben")
    f.append(table([
        ["Kasus", "Frage", "Funktion im Satz", "Beispiel aus dem Text"],
        ["Nominativ", "Wer? Was?", "Subjekt – führt die Handlung aus", "<i>Daedalus</i> clausus erat"],
        ["Genitiv", "Wessen?", "Zugehörigkeit, Attribut", "opus <i>patris</i> – das Werk des Vaters"],
        ["Dativ", "Wem?", "indirektes Objekt, Empfänger", "dedit oscula <i>nato</i> – dem Sohn"],
        ["Akkusativ", "Wen? Was? Wohin?", "direktes Objekt, Richtung", "ponit <i>pennas</i> – die Federn"],
        ["Ablativ", "Womit? Wodurch? Woher? Wo? Wann?", "Umstände: Mittel, Grund, Ort, Art", "<i>lino</i> alligat – mit Faden"],
        ["Vokativ", "(Anrede)", "jemand wird angesprochen", "<i>Icare</i> – Ikarus!"],
    ], [2.4 * cm, 3.8 * cm, 5.0 * cm, 6.4 * cm], bold_cols=(0,)))
    f += H1("2. Der Ablativ – viele Gesichter")
    f.append(table([
        ["Funktion", "Frage", "Übersetzung mit ...", "Beispiel"],
        ["instrumenti (Mittel)", "Womit? Wodurch?", "mit, durch", "lino, ceris (mit Faden, mit Wachs); pollice"],
        ["causae (Grund)", "Weshalb? Wodurch?", "aus, vor, wegen, von", "amore tactus (von Liebe ergriffen)"],
        ["modi (Art und Weise)", "Wie?", "mit", "ore renidenti (mit strahlendem Gesicht)"],
        ["separativus (Trennung)", "Woher? Wovon?", "von, aus", "ab alto nido (aus dem hohen Nest); remigio carens"],
        ["loci (Ort)", "Wo?", "in, auf, an", "in undis (in den Wellen); medio limite"],
        ["Abl. absolutus", "Unter welchen Umständen?", "während, nachdem, wobei, mit", "me duce (mit mir als Führer)"],
    ], [3.8 * cm, 3.4 * cm, 3.6 * cm, 6.8 * cm], bold_cols=(0,)))
    f.append(CondPageBreak(8 * cm))
    f += H1("3. Endungen auf einen Blick")
    f.append(table([
        ["Kasus", "a-Dekl. (f)", "o-Dekl. (m)", "o-Dekl. (n)", "3. Dekl. (m/f)", "3. Dekl. (n)", "u-Dekl.", "e-Dekl."],
        ["Nom. Sg.", "ala", "nidus", "caelum", "sol", "nomen", "volatus", "res"],
        ["Gen. Sg.", "alae", "nidi", "caeli", "solis", "nominis", "volatus", "rei"],
        ["Dat. Sg.", "alae", "nido", "caelo", "soli", "nomini", "volatui", "rei"],
        ["Akk. Sg.", "alam", "nidum", "caelum", "solem", "nomen", "volatum", "rem"],
        ["Abl. Sg.", "ala", "nido", "caelo", "sole", "nomine", "volatu", "re"],
        ["Nom. Pl.", "alae", "nidi", "caela", "soles", "nomina", "volatus", "res"],
        ["Gen. Pl.", "alarum", "nidorum", "caelorum", "solum", "nominum", "volatuum", "rerum"],
        ["Dat./Abl. Pl.", "alis", "nidis", "caelis", "solibus", "nominibus", "volatibus", "rebus"],
        ["Akk. Pl.", "alas", "nidos", "caela", "soles", "nomina", "volatus", "res"],
    ], [2.4 * cm] + [2.15 * cm] * 7, bold_cols=(0,), lat_cols=(1, 2, 3, 4, 5, 6, 7)))
    f += box("achtung", [
        "Mehrdeutige Endungen nicht raten – den <b>Satz</b> entscheiden lassen:",
        "<b>-ae</b> = Gen./Dat. Sg. oder Nom. Pl. · <b>-is</b> = Dat./Abl. Pl. (oder Gen. Sg. 3. Dekl.) · "
        "<b>-um</b> = Akk. Sg. oder Gen. Pl. (3. Dekl.) oder Nom./Akk. n. · <b>-a</b> = Nom./Abl. Sg. oder "
        "Nom./Akk. Pl. n. · Griechische Formen bei Ovid: <i>Creten, aera, aethera, Booten, Helicen</i> = Akkusative!",
    ])
    f += box("trick", [
        "<b>KNG-Regel gegen das Ovid-Chaos:</b> Ein Adjektiv gehört zu dem Nomen, das in Kasus, Numerus und "
        "Genus passt – egal, wie weit es entfernt steht.",
        "<i><b>longum</b>que perosus / <b>exilium</b></i> · <i><b>ignotas</b> animum dimittit in <b>artes</b></i> · "
        "<i><b>flavam</b> modo pollice <b>ceram</b></i>",
    ])

    f += task("3.1", "Kasus bestimmen", 1, 10,
              "Bestimme Kasus und Numerus und schreib die Frage bzw. Funktion dazu.")
    ks = [("pelago (185)", "Abl. Sg.", "wo/wodurch? vom Meer (eingeschlossen)"),
          ("Creten (183)", "Akk. Sg.", "wen? Kreta (griech. Endung)"),
          ("amore (184)", "Abl. Sg.", "wodurch? von Liebe"),
          ("undas (185)", "Akk. Pl.", "wen/was? die Wellen"),
          ("pennas (189)", "Akk. Pl.", "wen/was? die Federn"),
          ("lino (193)", "Abl. Sg.", "womit? mit Faden"),
          ("patris (199)", "Gen. Sg.", "wessen? des Vaters"),
          ("umeris (209)", "Dat. Pl.", "wem/woran? an die Schultern"),
          ("nato (211)", "Dat. Sg.", "wem? dem Sohn"),
          ("harundine (217)", "Abl. Sg.", "womit? mit der Rute"),
          ("solis (225)", "Gen. Sg.", "wessen? der Sonne"),
          ("aqua (230)", "Abl. Sg.", "wodurch? vom Wasser"),
          ("Icare (231)", "Vokativ", "Anrede: Ikarus!")]
    f.append(fill_table(["Form (Vers)", "Kasus + Numerus", "Frage / Funktion"], [[k[0]] for k in ks],
                        [4.2 * cm, 4.0 * cm, 9.4 * cm], row_h=0.9 * cm))
    solution("3.1", "Kasus bestimmen",
             table([["Form", "Kasus", "Frage / Funktion"]] + [list(k) for k in ks],
                   [4.2 * cm, 3 * cm, 10.4 * cm], lat_cols=(0,)))

    f += task("3.2", "Hyperbaton-Detektiv: Wer gehört zu wem?", 2, 8,
              "Finde in jeder Stelle das Adjektiv (bzw. Partizip) und sein Nomen und schreib beide auf.")
    hb = [("Creten longumque perosus / exilium (183 f.)", "longum ... exilium"),
          ("ignotas animum dimittit in artes (188)", "ignotas ... artes"),
          ("sic rustica quondam / fistula (191 f.)", "rustica ... fistula"),
          ("flavam modo pollice ceram (198)", "flavam ... ceram"),
          ("mirabile patris / impediebat opus (199 f.)", "mirabile ... opus"),
          ("geminas opifex libravit in alas (201)", "geminas ... alas"),
          ("ab alto / quae teneram prolem produxit in aera nido (213 f.)", "alto ... nido; teneram prolem"),
          ("audaci coepit gaudere volatu (223)", "audaci ... volatu"),
          ("odoratas, pennarum vincula, ceras (226)", "odoratas ... ceras")]
    f.append(fill_table(["Stelle", "Adjektiv + Nomen"], [[h[0]] for h in hb],
                        [10.0 * cm, 7.6 * cm], row_h=0.95 * cm))
    solution("3.2", "Hyperbaton-Detektiv", " · ".join(f"<i>{h[1]}</i>" for h in hb),
             "Wirkung: Das Hyperbaton spannt einen Bogen und hebt die getrennten Wörter hervor; bei "
             "<i>ab alto ... nido</i> „umschließt“ das Nest sogar die Brut – Wortstellung bildet den Inhalt ab.")

    f += task("3.3", "Ablativ-Funktionen bestimmen", 2, 8,
              "Welche Ablativ-Funktion liegt vor? (instrumenti / causae / modi / separativus / loci / Abl. abs.)")
    ab = [("lino ... alligat (193)", "instrumenti", "mit Faden"),
          ("ore renidenti (197)", "modi", "mit strahlendem Gesicht"),
          ("ab alto nido (213 f.)", "separativus", "aus dem hohen Nest"),
          ("in undis (233)", "loci", "in den Wellen"),
          ("amore tactus (184)", "causae", "von Liebe ergriffen"),
          ("me duce (208)", "Abl. abs.", "mit mir als Führer"),
          ("caeli cupidine tractus (224)", "causae", "vom Verlangen nach dem Himmel gezogen"),
          ("remigio carens (228)", "separativus", "ohne Ruderwerk")]
    f.append(fill_table(["Stelle", "Funktion", "Übersetzung"], [[a[0]] for a in ab],
                        [5.4 * cm, 3.6 * cm, 8.6 * cm], row_h=0.95 * cm))
    solution("3.3", "Ablativ-Funktionen",
             table([["Stelle", "Funktion", "Übersetzung"]] + [list(a) for a in ab],
                   [5.4 * cm, 3 * cm, 9.2 * cm], lat_cols=(0,)))

    f += task("3.4", "Satzanalyse wie ein Profi (Einrückmethode)", 3, 12,
              "Schreib den Satz in der Einrückmethode ab: Hauptsatz ganz links, jeden Nebensatz bzw. jede "
              "Partizipialgruppe eine Stufe eingerückt. Dann übersetze.")
    f.append(verse_block(verses(223, 225)))
    f.append(Lines(6, label="Einrückmethode:"))
    f.append(Lines(3, label="Übersetzung:"))
    solution("3.4", "Satzanalyse (v. 223–225)",
             "(Nebensatz, Fortsetzung von v. 220 ff.) <b>cum</b> puer audaci coepit gaudere volatu / "
             "&nbsp;&nbsp;&nbsp;deseruit<b>que</b> ducem / &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[caelique cupidine tractus] / "
             "&nbsp;&nbsp;&nbsp;altius egit iter.",
             "Drei Prädikate im cum-Satz: coepit – deseruit – egit; tractus ist ein PPP zu puer. "
             "Übersetzung: „... als der Junge begann, sich über den kühnen Flug zu freuen, den Führer verließ und, "
             "vom Verlangen nach dem Himmel gezogen, seinen Weg höher nahm.“")

    f += wordsearch_flows("3.5", "Wortgitter: Himmel, Meer & Natur", [
        ("CAELUM", "Himmel"), ("SOL", "Sonne"), ("UNDA", "Welle"), ("AURA", "Lufthauch"),
        ("PENNA", "Feder"), ("ALA", "Flügel"), ("CERA", "Wachs"), ("NIDUS", "Nest"), ("AVIS", "Vogel"),
        ("IGNIS", "Feuer"), ("TERRA", "Land, Erde"), ("AQUA", "Wasser"), ("PLUMA", "Flaumfeder"),
        ("LINUM", "Faden"),
    ], seed=5)
    f.append(sp(0.3))
    f.append(RatingRow("Wie sicher sitzen die Kasus?"))
    f.append(PageBreak())
    return f


# ============================================================
# KAPITEL 4: VOKABELN
# ============================================================

def vocab_table(items):
    data = [["", "Latein", "Formen", "Deutsch"]]
    for la, forms, de in items:
        data.append([CheckBox(11, "sitzt"), la, forms, de])
    return table(data, [0.8 * cm, 3.6 * cm, 6.3 * cm, 6.9 * cm], lat_cols=(1, 2), center_cols=(0,))


def kap4():
    f = chapter(4, "Vokabeln zum Ovid-Text", "Selektiv statt 300 Wörter: genau die, die im Text vorkommen")
    f += box("tipp", [
        "<b>So lernst du effektiv:</b> Rechte Spalte abdecken (Blatt oder Hand drüber), Latein > Deutsch aus dem "
        "Kopf sagen. Gewusst? Kästchen antippen. Nicht gewusst? Weiter – in Runde 2 nur noch die ohne Haken.",
        "Nicht nur anschauen! Erst das <b>aktive Abrufen</b> aus dem Gedächtnis verankert die Wörter.",
    ])
    for name, items in VOCAB_GROUPS:
        f += H1(name)
        f.append(vocab_table(items))
    f += H1("Kleinwörter, die Punkte kosten")
    f.append(P("Diese kurzen Wörter überliest man leicht – dabei steuern sie den ganzen Satz.", "body"))
    half = (len(SMALL_WORDS) + 1) // 2
    data = [["", "Latein", "Deutsch", "", "Latein", "Deutsch"]]
    for i in range(half):
        a = SMALL_WORDS[i]
        b = SMALL_WORDS[i + half] if i + half < len(SMALL_WORDS) else ("", "")
        data.append([CheckBox(11, "sitzt"), a[0], a[1], CheckBox(11, "sitzt") if b[0] else "", b[0], b[1]])
    f.append(table(data, [0.8 * cm, 3.3 * cm, 4.7 * cm, 0.8 * cm, 3.3 * cm, 4.7 * cm],
                   lat_cols=(1, 4), center_cols=(0, 3)))

    all_v = [v for _, items in VOCAB_GROUPS for v in items]
    rng = random.Random(42)
    test1 = rng.sample([v for v in all_v if v[0] not in ("inquit / ait",)], 24)
    f += task("4.1", "Vokabeltest Latein > Deutsch", 1, 10,
              "Ohne nachzuschauen! Danach mit der Liste vergleichen und Fehler im Kästchen markieren.")
    rows = []
    for i in range(12):
        a, b = test1[i], test1[i + 12]
        rows.append([a[0], "", b[0], ""])
    f.append(table([["Latein", "Deutsch", "Latein", "Deutsch"]] + rows,
                   [3.4 * cm, 5.4 * cm, 3.4 * cm, 5.4 * cm], lat_cols=(0, 2), row_h=0.95 * cm, zebra=False))
    solution("4.1", "Vokabeltest Latein > Deutsch", " · ".join(f"<i>{v[0]}</i> = {v[2]}" for v in test1))

    test2 = rng.sample([v for v in all_v if v not in test1 and v[0] != "inquit / ait"], 16)
    f += task("4.2", "Vokabeltest Deutsch > Latein (schwerer)", 2, 10,
              "Schreib das lateinische Wort mit Formen (z. B. Genitiv bzw. Stammformen).")
    rows = []
    for i in range(8):
        a, b = test2[i], test2[i + 8]
        rows.append([a[2], "", b[2], ""])
    f.append(table([["Deutsch", "Latein + Formen", "Deutsch", "Latein + Formen"]] + rows,
                   [3.6 * cm, 5.2 * cm, 3.6 * cm, 5.2 * cm], row_h=1.0 * cm, zebra=False))
    solution("4.2", "Vokabeltest Deutsch > Latein",
             " · ".join(f"{v[2]} = <i>{v[0]}, {v[1]}</i>" for v in test2))

    f += task("4.3", "Wortfamilien & Fremdwörter", 2, 8,
              "Welches lateinische Wort aus der Liste steckt in diesen deutschen/englischen Wörtern? "
              "Nutze das als Eselsbrücke!")
    fw = [("Aviation, Avionik", "avis – Vogel"), ("solar, Solarium", "sol – Sonne"),
          ("Aquarium", "aqua – Wasser"), ("Terrasse, Territorium", "terra – Land"),
          ("Ordnung, Order", "ordo – Reihe, Ordnung"), ("Nudist", "nudus – nackt"),
          ("Opus, Operation", "opus – Werk"), ("Imitation", "imitari – nachahmen"),
          ("Volatilität (= Flatterhaftigkeit)", "volare – fliegen"), ("Tremolo (Musik)", "tremere – zittern"),
          ("Nomen, Nominativ", "nomen – Name"), ("Sequenz, Konsequenz", "sequi – folgen")]
    f.append(fill_table(["Fremdwort", "lateinisches Wort + Bedeutung"], [[x[0]] for x in fw],
                        [6.6 * cm, 11.0 * cm], row_h=0.9 * cm, lat_cols=()))
    solution("4.3", "Wortfamilien & Fremdwörter", " · ".join(f"{a}: <i>{b}</i>" for a, b in fw))

    f += crossword_flows("4.4", "Kreuzworträtsel: Ovid-Wortschatz", [
        ("ALA", "Flügel"), ("PENNA", "Feder"), ("CERA", "Wachs"), ("CAELUM", "Himmel"), ("UNDA", "Welle"),
        ("PATER", "Vater"), ("NATUS", "Sohn"), ("VOLARE", "fliegen"), ("CADERE", "fallen"),
        ("TIMERE", "fürchten"), ("GAUDERE", "sich freuen"), ("SEPULCRUM", "Grab"), ("OSCULUM", "Kuss"),
        ("INFELIX", "unglücklich"), ("AUDAX", "kühn"), ("NOMEN", "Name"), ("ARTES", "Künste (Pl.)"),
        ("MONERE", "ermahnen"),
    ], seed=8, level=2)

    f += wordsearch_flows("4.5", "Wortgitter für Profis: Verben (alle Richtungen)", [
        ("VOLARE", "fliegen"), ("CADERE", "fallen"), ("TIMERE", "fürchten"), ("MONERE", "ermahnen"),
        ("SEQUI", "folgen"), ("TRAHERE", "ziehen"), ("CONDERE", "bestatten"), ("FLECTERE", "biegen"),
        ("TREMERE", "zittern"), ("GAUDERE", "sich freuen"), ("CAPTARE", "zu fangen suchen"),
        ("PONERE", "legen"),
    ], seed=17, hard=True, size=14)
    f.append(sp(0.3))
    f.append(RatingRow("Wie viele Vokabeln sitzen schon?"))
    f.append(PageBreak())
    return f


# ============================================================
# KAPITEL 5: ÜBERSETZUNGSTRAINING IN 3 STUFEN
# ============================================================

def help_table(pairs):
    half = (len(pairs) + 1) // 2
    rows = []
    for i in range(half):
        a = pairs[i]
        b = pairs[i + half] if i + half < len(pairs) else ("", "")
        rows.append([a[0], a[1], b[0], b[1]])
    t = table(rows, [3.3 * cm, 5.5 * cm, 3.3 * cm, 5.5 * cm], header=False, lat_cols=(0, 2))
    return t


def kap5():
    f = chapter(5, "Übersetzen in 3 Stufen", "Stufe 1 vereinfacht · Stufe 2 Original mit Hilfen · Stufe 3 Klausurmodus")
    f += box("ziel", [
        "Hier investierst du den größten Teil deiner Zeit. Jeder der 8 Abschnitte hat zwei Stufen:",
        "<b>Stufe 1 (Basis):</b> ein vereinfachter lateinischer Text mit demselben Inhalt – zum Warmwerden und "
        "um die Handlung zu kennen.<br/>"
        "<b>Stufe 2 (Aufbau):</b> der Originaltext mit Vokabelhilfen und Konstruktionshilfe.<br/>"
        "<b>Stufe 3 (Profi):</b> am Ende des Kapitels der ganze Text ohne Hilfen – wie in der Klausur.",
    ])
    f += box("trick", "Bei jedem Satz: <b>1.</b> alle Verben markieren <b>2.</b> zum Verb den Handelnden suchen "
                      "<b>3.</b> Akkusativ suchen <b>4.</b> erst dann ins Deutsche bringen. "
                      "In der Konstruktionshilfe sind Prädikate <b>fett</b>, Einschübe [<i>in Klammern</i>].")
    for s in SECTIONS:
        a, b = s["v"]
        f.append(PageBreak())
        f += H1(f'Abschnitt {s["nr"]} <font color="#7a6f63" size="11">· Verse {a}–{b}</font>')
        f.append(P(f'<b>{s["title"]}</b>', "h2"))
        # Stufe 1
        f += task(f'5.{s["nr"]}a', f'Stufe 1: {s["title"]} (vereinfacht)', 1, 8)
        f.append(Table([[P(s["easy"], "lat")]], colWidths=[CONTENT_W],
                       style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), PAPER),
                                         ("LEFTPADDING", (0, 0), (-1, -1), 10),
                                         ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                                         ("TOPPADDING", (0, 0), (-1, -1), 8),
                                         ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                                         ("LINEBEFORE", (0, 0), (0, -1), 3, GREEN)])))
        f.append(P(f'<font color="#7a6f63">Hilfen: {s["easy_voc"]}</font>', "small"))
        n_easy = max(4, len(s["easy"]) // 75)
        f.append(Lines(n_easy))
        solution(f'5.{s["nr"]}a', f'Stufe 1: {s["title"]}', s["easy_de"])
        # Stufe 2
        f += task(f'5.{s["nr"]}b', f'Stufe 2: {s["title"]} (Original)', 2, 15)
        f.append(verse_block(verses(a, b)))
        f.append(sp(0.15))
        f.append(P("<b>Wortangaben</b>", "small"))
        f.append(help_table(s["help"]))
        f += box("tipp", s["build"], "Konstruktionshilfe:")
        f.append(Lines(int((b - a + 1) * 1.5) + 2, label="Deine Übersetzung:"))
        f.append(CondPageBreak(5 * cm))
        f.append(P("<b>Grammatik-Check</b>", "h2"))
        for i, (q, _) in enumerate(s["check"], 1):
            f.append(P(f"{i}. {q}", "task"))
            f.append(Lines(1))
        solution(f'5.{s["nr"]}b', f'Stufe 2: {s["title"]} (v. {a}–{b})',
                 f'<b>Übersetzung:</b> {s["de"]}',
                 *[f"<b>{i}.</b> {q} – {ans}" for i, (q, ans) in enumerate(s["check"], 1)])

    # Stufe 3: alles ohne Hilfen
    f.append(PageBreak())
    f += task("5.9", "Stufe 3: Klausurmodus – der ganze Text ohne Hilfen", 3, 60,
              "Stell dir einen Timer. Übersetze so viel du schaffst – ohne Wortangaben. Unbekanntes markieren, "
              "Teilübersetzung schreiben, weitermachen. Danach mit den Lösungen 5.1b–5.8b vergleichen.")
    f.append(verse_block(verses(183, 209)))
    f.append(PageBreak())
    f.append(verse_block(verses(210, 235)))
    f.append(sp(0.3))
    f.append(Lines(60, label="Deine Übersetzung:"))
    solution("5.9", "Klausurmodus", "Vergleiche mit den Übersetzungen der Lösungen 5.1b bis 5.8b. "
             "Markiere jeden Fehler und trag ihn ins Fehlerprotokoll (Kapitel 7) ein.")
    f.append(sp(0.3))
    f.append(RatingRow("Wie sicher kannst du den Text übersetzen?"))
    f.append(PageBreak())
    return f


# ============================================================
# KAPITEL 6: STILMITTEL, INTERPRETATION, METRIK
# ============================================================

STILMITTEL = [
    ("Hyperbaton", "Zusammengehörige Wörter werden getrennt.", "longum ... / exilium (183 f.); ab alto ... nido (213 f.)",
     "hebt die getrennten Wörter hervor; kann den Inhalt abbilden (das Nest umschließt die Brut)"),
    ("Enjambement", "Der Satz läuft über das Versende hinaus.", "perosus / exilium (183 f.); mirabile patris / impediebat opus",
     "Spannung; das erste Wort im neuen Vers wird betont"),
    ("Chiasmus", "Überkreuzstellung (ABBA).", "omnia possideat, non possidet aera (187)",
     "stellt „alles“ und „Luft“ scharf gegenüber – Pointe des Plans"),
    ("Polyptoton", "Gleiches Wort in verschiedenen Formen.", "possideat – possidet (187)",
     "betont den Gegensatz: Macht des Minos vs. ihre Grenze"),
    ("Antithese", "Gegensatz.", "demissior – celsior; unda – ignis (204 f.)",
     "zeigt die zwei Gefahren; die Mitte ist das richtige Maß"),
    ("Vergleich", "Verbindung durch „wie“ (velut, sic).", "velut ales ... (213 f.); sic rustica ... fistula (191 f.)",
     "veranschaulicht: Dädalus als fürsorgliche Vogelmutter"),
    ("Parenthese", "Einschub in den Satz.", "(fuerant Delosque Parosque relictae) (221)",
     "Orientierung im Raum, Ruhe vor dem Sturz"),
    ("Polysyndeton", "Viele Bindewörter hintereinander.", "Delosque Parosque (221); -que ... -que",
     "Fülle, Aufzählung, ruhiger Fluss"),
    ("Anapher / Geminatio", "Wiederholung am Anfang bzw. desselben Worts.", "„Icare“ ... „Icare“ ... „Icare“ (231–233)",
     "verzweifeltes Rufen, Klage, Hilflosigkeit"),
    ("Paradoxon", "Scheinbarer Widerspruch.", "pater ... nec iam pater (231)",
     "ohne Sohn ist er kein Vater mehr – tiefster Verlust"),
    ("Metapher", "Bildlicher Ausdruck.", "remigium (228) für die Flügel; pennarum vincula (226)",
     "Flug wie eine Seefahrt; das Wachs als Fessel"),
    ("Alliteration", "Gleicher Anlaut.", "ponit ... pennas (189); pariter praecepta (208)",
     "Klang, Betonung"),
    ("Apostrophe", "Direkte Anrede.", "Icare (204, 231 ff.)", "Nähe, Dringlichkeit, Emotion"),
    ("Tempuswechsel", "Präsens mitten in der Vergangenheit.", "dimittit, novat, ponit, instruit ...",
     "Lebendigkeit, man ist „live“ dabei"),
]


def kap6():
    f = chapter(6, "Stilmittel, Interpretation & Metrik", "Erkennen > Belegen > Wirkung erklären")
    f += H1("1. Stilmittel mit Wirkung")
    f.append(table([["Stilmittel", "Definition", "Beispiel (Vers)", "Wirkung"]] + [list(x) for x in STILMITTEL],
                   [2.7 * cm, 4.2 * cm, 5.3 * cm, 5.4 * cm], bold_cols=(0,), lat_cols=(2,)))
    f += box("merke", "<b>Klausurformel:</b> Stilmittel <b>nennen</b> > Textstelle <b>zitieren</b> (mit Vers) > "
                      "<b>Wirkung</b> erklären > <b>Bezug zum Inhalt</b> herstellen. "
                      "Ein Stilmittel ohne Wirkung bringt fast keine Punkte!")
    f += H1("2. Interpretation: Worum geht es eigentlich?")
    f.append(table([
        ["Thema", "Kernaussage"],
        ["Dädalus", "Gefangener auf Kreta, sehnt sich nach der Heimat. Erkennt: Minos beherrscht Land und Meer, "
                    "aber nicht die Luft. Als genialer Erfinder „verändert er die Natur“ (naturam novat) – "
                    "Grenzüberschreitung durch Technik. Zugleich fürsorglicher, ängstlicher Vater."],
        ["Ikarus", "Kindlich, verspielt, ahnungslos (ignarus). Freut sich am kühnen Flug, verlässt den Führer, "
                   "fliegt aus Begierde nach dem Himmel zu hoch – missachtet die Warnung."],
        ["Hybris", "Überheblichkeit / Maßlosigkeit: Der Mensch überschreitet die ihm gesetzten Grenzen. "
                   "Dädalus (Technik gegen die Natur), Ikarus (Ungehorsam, zu hoher Flug). Der Absturz zeigt die Folge."],
        ["Das rechte Maß", "„Flieg in der Mitte!“ (medio limite) – der Mittelweg zwischen Wasser und Sonne; "
                           "vgl. die antike Idee der goldenen Mitte (aurea mediocritas)."],
        ["Schuldfrage", "Ikarus: missachtet die Warnung. Dädalus: seine Erfindung ermöglicht den Tod; er verflucht "
                        "am Ende selbst seine Künste (devovit suas artes)."],
        ["Aitiologie", "Ovid erklärt Namen: das Ikarische Meer (v. 230) und die Insel Ikaria (v. 235)."],
        ["Rezeption", "Bruegel, „Landschaft mit dem Sturz des Ikarus“: Pflüger, Hirte, Fischer (vgl. v. 217 f.) "
                      "arbeiten weiter – kaum jemand bemerkt den Sturz."],
    ], [3.0 * cm, 14.6 * cm], bold_cols=(0,)))
    f += box("tipp", "<b>Merksatz:</b> Dädalus = Erfinder + Flucht aus Not > Grenzüberschreitung. "
                     "Ikarus = Neugier + Ungehorsam > Grenzüberschreitung. Absturz = Konsequenz.")

    f.append(CondPageBreak(10 * cm))
    f += H1("3. Metrik: der Hexameter")
    f.append(table([
        ["Regel", "Erklärung"],
        ["Aufbau", "6 Versfüße. Fuß 1–4: Daktylus (– u u) oder Spondeus (– –). Fuß 5: fast immer Daktylus. "
                   "Fuß 6: – x (zweisilbig, letzte Silbe lang oder kurz)."],
        ["Naturlänge", "Langer Vokal oder Diphthong (ae, oe, au, ei, eu) ist lang: <i>Daedalus, caelum</i>."],
        ["Positionslänge", "Vokal vor zwei Konsonanten (auch über die Wortgrenze) oder vor x/z ist lang: "
                           "<i>interea</i> (in-), <i>exilium</i> (ex-)."],
        ["Achtung", "<i>qu</i> und <i>h</i> zählen nicht als Konsonant; Muta + Liquida (z. B. <i>pr, tr, cr</i>) kann kurz bleiben."],
        ["Elision", "Endvokal (oder Vokal + m) vor einem Vokal oder h fällt weg: <i>atque ita</i> > atqu(e) ita."],
    ], [3.0 * cm, 14.6 * cm], bold_cols=(0,)))
    f.append(P("Beispiel (v. 183):", "h2"))
    f.append(table([
        ["Fuß", "1", "2", "3", "4", "5", "6"],
        ["Silben", "Dae-da-lus", "in-te-re-", "a Cre-", "ten lon-", "gumque pe-", "rosus"],
        ["Maß", "– u u", "– u u", "– –", "– –", "– u u", "– x"],
    ], [2.2 * cm] + [2.56 * cm] * 6, bold_cols=(0,), lat_cols=(1, 2, 3, 4, 5, 6)))

    # ---------- Aufgaben ----------
    f += task("6.1", "Stilmittel erkennen und deuten", 2, 12,
              "Benenne das Stilmittel und erkläre in einem Satz seine Wirkung.")
    sm = [("omnia possideat, non possidet aera Minos (187)", "Chiasmus + Polyptoton",
           "Gegensatz: Minos besitzt alles – nur nicht die Luft; das ist Dädalus' Ausweg."),
          ("si demissior ibis ... si celsior (204 f.)", "Antithese",
           "zwei Extreme (Wasser/Feuer) – die Mitte ist der sichere Weg."),
          ("velut ales, ab alto / quae teneram prolem produxit in aera nido (213 f.)", "Vergleich (+ Hyperbaton)",
           "Dädalus als sorgende Vogelmutter: Liebe und Angst um das Kind."),
          ("pater infelix, nec iam pater (231)", "Paradoxon",
           "Mit dem Tod des Sohnes verliert er seine Rolle als Vater."),
          ("„Icare,“ dixit, / „Icare,“ dixit ... „Icare“ dicebat (231–233)", "Anapher / Geminatio",
           "verzweifelte, immer wiederholte Rufe – Hilflosigkeit."),
          ("remigioque carens (228)", "Metapher", "Die Flügel als Ruder – der Flug wie eine Seefahrt.")]
    for i, (st, _, _) in enumerate(sm, 1):
        f.append(P(f"<b>{i}.</b> <i>{st}</i>", "task"))
        f.append(Lines(2))
    solution("6.1", "Stilmittel erkennen", *[f"<b>{i}.</b> {a}: {b}" for i, (_, a, b) in enumerate(sm, 1)])

    f += task("6.2", "Gliederung: Finde Überschriften", 1, 6,
              "Gib jedem Abschnitt eine kurze, treffende Überschrift (ohne in Kapitel 5 nachzusehen!).")
    f.append(fill_table(["Verse", "Deine Überschrift"],
                        [[f'{s["v"][0]}–{s["v"][1]}'] for s in SECTIONS],
                        [3.0 * cm, 14.6 * cm], row_h=0.95 * cm, lat_cols=()))
    solution("6.2", "Gliederung", " · ".join(f'{s["v"][0]}–{s["v"][1]}: {s["title"]}' for s in SECTIONS))

    f += task("6.3", "Schuldfrage: Argumente sammeln", 2, 10,
              "Wer ist schuld am Tod des Ikarus? Sammle Argumente mit Textbeleg (Vers!).")
    t = Table([[P("<b>Dädalus ist (mit)schuldig, weil ...</b>", "cell"), P("<b>Ikarus ist schuldig, weil ...</b>", "cell")],
               [Lines(9), Lines(9)]], colWidths=[CONTENT_W / 2] * 2)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, LINE), ("BACKGROUND", (0, 0), (-1, 0), PAPER),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    f.append(t)
    solution("6.3", "Schuldfrage",
             "<b>Dädalus:</b> verändert die Natur (naturam novat, 189); seine Kunst ist „verderblich“ "
             "(damnosas artes, 215); bringt dem Kind das gefährliche Fliegen bei; ahnt die Gefahr (timet, 213; "
             "Tränen 210 f.) und lässt es trotzdem zu; verflucht am Ende selbst seine Künste (234).",
             "<b>Ikarus:</b> wird ausdrücklich gewarnt (203–208); freut sich am „kühnen“ Flug (audaci, 223); "
             "verlässt den Führer (deseruit ducem, 224); fliegt aus Begierde höher (cupidine tractus, 224 f.).",
             "<b>Fazit-Möglichkeit:</b> Beide überschreiten Grenzen (Hybris): Dädalus durch Technik gegen die Natur, "
             "Ikarus durch Ungehorsam und Maßlosigkeit. Ikarus zahlt den Preis, Dädalus trägt die Trauer.")

    f += task("6.4", "Interpretation schreiben: Opfer oder Täter?", 3, 20,
              "„Ikarus ist ein Opfer seines Vaters.“ – Nimm Stellung (ca. 10–12 Sätze). Nutze mindestens zwei "
              "Textbelege und ein Stilmittel.")
    f.append(Lines(14))
    solution("6.4", "Interpretation (Erwartungshorizont)",
             "Einleitung mit These. <b>Pro Opfer:</b> Ikarus ist ein Kind (puer), ahnungslos (ignarus, 196); der "
             "Vater bringt ihn in Gefahr und weiß das (Tränen, Angst: velut ales). <b>Contra:</b> klare Warnung "
             "mit Antithese demissior/celsior (204 f.); Ikarus verlässt aus eigener Begierde den Führer (224). "
             "<b>Stilmittel:</b> z. B. Paradoxon pater nec iam pater (231) zeigt, dass auch Dädalus ein Leidtragender "
             "ist. <b>Schluss:</b> abgewogenes Urteil, Bezug zum Hybris-Motiv.")

    f += task("6.5", "Skandieren: Längen und Kürzen", 3, 10,
              "Markiere über jeder Silbe lang (–) oder kurz (u), trenne die Versfüße mit einem Strich.")
    for nr in (184, 231):
        f.append(Scansion(OVID[nr].replace("„", "").replace("“", ""), nr))
        f.append(sp(0.2))
    solution("6.5", "Skandieren",
             "v. 184: ex-i-li | um tac- | tusque lo- | ci na- | talis a- | more = – u u | – – | – u u | – – | – u u | – x",
             "v. 231: at pater | infe- | lix nec | iam pater | Icare | dixit = – u u | – – | – – | – u u | – u u | – x")

    f += crossword_flows("6.6", "Kreuzworträtsel: Stilmittel", [
        ("CHIASMUS", "Überkreuzstellung ABBA"), ("HYPERBATON", "Trennung zusammengehöriger Wörter"),
        ("ENJAMBEMENT", "Satz läuft über das Versende"), ("ANAPHER", "Wiederholung am Anfang"),
        ("VERGLEICH", "velut ales"), ("PARENTHESE", "Einschub"), ("PARADOXON", "pater nec iam pater"),
        ("METAPHER", "remigium für Flügel"), ("ANTITHESE", "Gegensatz"), ("POLYPTOTON", "possideat – possidet"),
        ("HYBRIS", "Überheblichkeit, Maßlosigkeit"), ("ALLITERATION", "gleicher Anlaut"),
    ], seed=4, level=1, intro="Trage die Fachbegriffe (deutsch, ohne Umlaute/Leerzeichen) ein.")
    f.append(sp(0.3))
    f.append(RatingRow("Wie sicher bist du bei Stilmitteln & Interpretation?"))
    f.append(PageBreak())
    return f


# ============================================================
# KAPITEL 7: PROBEKLAUSUR & FEHLERPROTOKOLL
# ============================================================

def kap7():
    f = chapter(7, "Probeklausur", "90 Minuten · ohne Hilfsmittel · danach selbst korrigieren")
    f += box("info", [
        "<b>So geht's:</b> Timer auf 90 Minuten (60 min Übersetzung, 30 min Aufgaben). Handy weg. "
        "Danach mit den Lösungen korrigieren und die Punkte eintragen.",
        "<b>Übersetzung bewerten:</b> Start mit 40 Punkten; pro ganzem Fehler (Konstruktion, falscher Kasus/"
        "Tempus mit Sinnänderung) –2, pro halbem Fehler (Vokabel leicht daneben, Kleinigkeit) –1.",
    ])
    f += task("7.1", "Teil A: Übersetzung (v. 223–235)", 3, 60,
              "Übersetze den Text in angemessenes Deutsch. Der Satz beginnt mitten im Satzgefüge: "
              "„Und schon waren Samos, Delos ... erreicht, als ...“")
    f.append(verse_block(verses(223, 235)))
    f.append(P("<b>Angaben:</b> " + " · ".join([
        "<i>tabescere, tabui</i>: schmelzen", "<i>quatere</i>: schlagen", "<i>lacertus</i>: Arm",
        "<i>remigium</i>: Ruderwerk", "<i>caeruleus</i>: blau", "<i>devovere</i>: verfluchen",
        "<i>sepelire, sepultum</i>: begraben"]), "small"))
    f.append(Lines(22))
    solution("7.1", "Teil A: Übersetzung", SECTIONS[6]["de"], SECTIONS[7]["de"])

    f.append(PageBreak())
    f += task("7.2", "Teil B: Aufgaben (20 Punkte)", 3, 30)
    qs = [
        ("B1", 4, "Bestimme vollständig: <i>tabuerant</i> (227), <i>excipiuntur</i> (230), <i>requiram</i> (232), "
                  "<i>condidit</i> (235).", 4,
         "tabuerant: 3. Pl. Ind. Plqpf. Akt. (tabescere) · excipiuntur: 3. Pl. Ind. Präs. Pass. (excipere) · "
         "requiram: 1. Sg. Konj. Präs. Akt. (requirere), deliberativ · condidit: 3. Sg. Ind. Perf. Akt. (condere). "
         "Je 1 Punkt."),
        ("B2", 4, "Weise in v. 231–233 zwei Stilmittel nach und erläutere ihre Wirkung.", 4,
         "Paradoxon „pater ... nec iam pater“: Verlust der Vaterrolle. Anapher/Geminatio „Icare ... Icare ... "
         "Icare“: Verzweiflung, wiederholtes Rufen. (Auch möglich: Tempuswechsel dixit – dicebat.) "
         "Je 1 P. Nachweis + 1 P. Wirkung."),
        ("B3", 3, "Bestimme die Funktion der Ablative <i>remigio</i> (228), <i>caerulea aqua</i> (229 f.) und "
                  "<i>sepulcro</i> (234).", 3,
         "remigio: Abl. separativus (bei carere: ohne Ruderwerk) · caerulea aqua: Abl. beim Passiv/instrumenti "
         "(vom blauen Wasser aufgenommen) · sepulcro: Abl. loci (im Grab). Je 1 P."),
        ("B4", 6, "Inwiefern ist der Sturz des Ikarus eine Folge von Hybris? Beziehe auch Dädalus ein und "
                  "belege am Text.", 8,
         "Hybris = Grenzüberschreitung/Maßlosigkeit. Ikarus: audaci volatu, deseruit ducem, caeli cupidine "
         "tractus, altius egit iter (223–225). Dädalus: naturam novat (189), damnosas artes (215), devovit suas "
         "artes (234) als späte Einsicht. Strafe folgt unmittelbar (Wachs schmilzt). 2 P. Begriff, 2 P. Ikarus, "
         "2 P. Dädalus."),
        ("B5", 3, "Skandiere v. 231.", 2,
         "at pater | infe- | lix nec | iam pater | Icare | dixit: – u u | – – | – – | – u u | – u u | – x"),
    ]
    for code, pts, q, nlines, _ in qs:
        f.append(P(f'<b>{code}</b> <font color="#7a6f63">({pts} P.)</font>  {q}', "task"))
        if code == "B5":
            f.append(Scansion(OVID[231].replace("„", "").replace("“", ""), 231))
        else:
            f.append(Lines(nlines))
    solution("7.2", "Teil B", *[f"<b>{c}</b> ({p} P.): {a}" for c, p, _, _, a in qs])

    f.append(CondPageBreak(9 * cm))
    f += H1("Bewertung")
    f.append(table([["Teil", "max.", "erreicht"], ["A Übersetzung", "40", ""], ["B1 Formen", "4", ""],
                    ["B2 Stilmittel", "4", ""], ["B3 Ablative", "3", ""], ["B4 Interpretation", "6", ""],
                    ["B5 Metrik", "3", ""], ["Summe", "60", ""]],
                   [8 * cm, 3 * cm, 3 * cm], bold_cols=(0,), center_cols=(1, 2), row_h=0.8 * cm))
    f.append(sp(0.3))
    f.append(table([["Note", "1", "2", "3", "4", "5", "6"],
                    ["Punkte", "60–52", "51–44", "43–35", "34–27", "26–12", "11–0"]],
                   [2.6 * cm] + [2.5 * cm] * 6, bold_cols=(0,), center_cols=(1, 2, 3, 4, 5, 6)))

    f.append(PageBreak())
    f += task("7.3", "Fehlerprotokoll: aus Fehlern lernen", 1, 10,
              "Trag jeden Fehler aus Kapitel 5 und der Probeklausur ein. Die letzte Spalte (Regel) ist das, "
              "was du dir morgen früh noch einmal ansiehst.")
    f.append(fill_table(["Stelle", "Mein Fehler", "Richtig", "Regel / Merksatz"], [[""] for _ in range(16)],
                        [2.2 * cm, 4.6 * cm, 4.6 * cm, 6.2 * cm], row_h=1.0 * cm, lat_cols=()))
    solution("7.3", "Fehlerprotokoll", "Keine Musterlösung – das Protokoll ist dein persönlicher Spickzettel.")
    f.append(PageBreak())
    return f


# ============================================================
# SPICKZETTEL (1 Seite)
# ============================================================

def spickzettel():
    CTX.chapter = "Spickzettel"
    f = [Banner(None, "Spickzettel für morgen früh", "10 Minuten – nichts Neues mehr, nur wiederholen")]
    f.append(sp(0.25))
    small = lambda rows, w, **k: table(rows, w, font_st="cell", **k)
    left = [
        P("<b>Übersetzen</b>", "h2"),
        P("Verb > Wer? (Nom.) > Wen/was? (Akk.) > Wem? (Dat.) > Rest > Deutsch glätten. "
          "Adjektive per KNG zum Nomen. Unbekanntes: Teilübersetzung schreiben!", "cell"),
        P("<b>Endungen</b>", "h2"),
        small([["-o/-m", "ich"], ["-s", "du"], ["-t", "er/sie/es"], ["-mus", "wir"], ["-tis", "ihr"],
               ["-nt", "sie"], ["-erunt / -ere", "sie (Perf.)"], ["-tur / -ntur", "Passiv"]],
              [3.0 * cm, 5.2 * cm], header=False, lat_cols=(0,)),
        P("<b>Zeitzeichen</b>", "h2"),
        small([["-ba-", "Imperfekt: er rief"], ["-bi- / -e-", "Futur: er wird rufen"],
               ["Perfektstamm", "Perfekt: dixit, cepit, dedit"], ["-era-", "Plqpf.: er hatte ..."]],
              [3.0 * cm, 5.2 * cm], header=False, lat_cols=(0,)),
    ]
    right = [
        P("<b>Kasus-Fragen</b>", "h2"),
        small([["Nom.", "Wer?"], ["Gen.", "Wessen?"], ["Dat.", "Wem?"], ["Akk.", "Wen/was?"],
               ["Abl.", "womit, wodurch, woher, wo?"], ["Vok.", "Anrede: Icare!"]],
              [2.0 * cm, 6.2 * cm], header=False, bold_cols=(0,)),
        P("<b>Stilmittel</b>", "h2"),
        P("Hyperbaton = Trennung · Enjambement = Zeilensprung · Chiasmus = ABBA · Polyptoton = Wortstamm-"
          "Wiederholung · Antithese = Gegensatz · Vergleich = velut · Paradoxon = pater nec iam pater · "
          "Anapher = Icare, Icare. Immer: nennen > zitieren > Wirkung!", "cell"),
        P("<b>Interpretation</b>", "h2"),
        P("Dädalus = Erfinder, Flucht aus Not, verändert die Natur. Ikarus = Neugier, Ungehorsam, zu hoch. "
          "Hybris = Grenzüberschreitung. Mitte = richtiges Maß. Absturz = Konsequenz. "
          "Aitiologie: Ikarisches Meer.", "cell"),
    ]
    t = Table([[left, right]], colWidths=[CONTENT_W / 2, CONTENT_W / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 6)]))
    f.append(t)
    f.append(sp(0.2))
    f.append(P("<b>Checkliste vor der Arbeit</b>", "h2"))
    checks = ["Fehlerprotokoll (Spalte „Regel“) gelesen", "Vokabeln ohne Haken noch einmal abgefragt",
              "Abschnitt 4 und 7 (Warnung, Absturz) einmal laut übersetzt", "Stifte, Wasser, ausgeschlafen",
              "In der Arbeit: erst Verben markieren, dann übersetzen", "Am Ende: jede Lücke mit Teilübersetzung füllen"]
    rows = [[CheckBox(12, c), P(c, "cell")] for c in checks]
    ct = Table(rows, colWidths=[0.8 * cm, CONTENT_W - 0.8 * cm])
    ct.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    f.append(ct)
    return f


# ============================================================
# LÖSUNGEN & ANHANG
# ============================================================

def solutions_section(only_chapters=None):
    CTX.chapter = "Lösungen"
    f = [PageBreak(), Banner(None, "Lösungen", "Erst selbst probieren, dann vergleichen")]
    f.append(sp(0.3))
    last = None
    for chap, nr, title, flows in CTX.solutions:
        if only_chapters and chap not in only_chapters:
            continue
        if chap != last:
            f += H1(chap)
            last = chap
        f.append(KeepTogether([P(f'<font color="#7a1f2b"><b>{nr}</b></font>  <b>{title}</b>', "h2")] + flows[:1]))
        f += flows[1:]
        f.append(sp(0.15))
    return f


def appendix_grundwortschatz():
    """Liest die 500 Vokabeln aus vocab.js (Web-App), falls vorhanden."""
    src = script_folder / "vocab.js"
    if not src.exists():
        return []
    text = src.read_text(encoding="utf-8")
    titles = re.findall(r"^\s+'([^']+)',\s*$", text.split("const RAW")[0], re.M)
    m = re.search(r"const RAW = `(.*?)`;", text, re.S)
    if not m:
        return []
    words = [ln.strip().split("|") for ln in m.group(1).splitlines()
             if ln.strip() and not ln.strip().startswith("#")]
    words = [w for w in words if len(w) == 3]
    CTX.chapter = "Anhang"
    f = [PageBreak(), Banner(None, "Anhang: 500 Grundwörter", "Der Grundwortschatz aus der Lern-App – in 25er-Packs")]
    f.append(sp(0.2))
    f += box("tipp", "Diese Wörter kommen in fast jedem Lateintext vor. Für morgen nicht alle lernen – "
                     "aber nach der Arbeit: ein Pack pro Tag (auch in der Web-App mit smarter Wiederholung).")
    for p in range(0, len(words), 25):
        title = titles[p // 25] if p // 25 < len(titles) else ""
        data = [["", "Latein", "Formen", "Deutsch"]]
        for la, forms, de in words[p:p + 25]:
            data.append([CheckBox(10, "sitzt"), la, forms, de])
        f.append(CondPageBreak(6 * cm))
        f.append(P(f"Pack {p // 25 + 1}: {title}", "h2"))
        f.append(table(data, [0.7 * cm, 3.2 * cm, 6.2 * cm, 7.5 * cm], lat_cols=(1, 2), center_cols=(0,)))
    return f


# ============================================================
# SEITENGESTALTUNG & PDF ERZEUGEN
# ============================================================

def decorate(canv, doc):
    if getattr(canv, "_nohdr", None) == canv.getPageNumber():
        return
    canv.saveState()
    y = PAGE_H - 1.15 * cm
    canv.setFillColor(BORDEAUX)
    canv.setFont("Helvetica-Bold", 8)
    canv.drawString(MARGIN_X, y, "LATEIN · OVID: DAEDALUS & IKARUS")
    canv.setFillColor(MUTED)
    canv.setFont("Helvetica", 8)
    canv.drawRightString(PAGE_W - MARGIN_X, y, getattr(canv, "_chapter", ""))
    canv.setStrokeColor(GOLD)
    canv.setLineWidth(0.8)
    canv.line(MARGIN_X, y - 5, PAGE_W - MARGIN_X, y - 5)
    canv.setFillColor(MUTED)
    canv.setFont("Helvetica", 8.5)
    canv.drawCentredString(PAGE_W / 2, 0.9 * cm, f"– {canv.getPageNumber()} –")
    canv.restoreState()


def build(filename, parts, cover=False, with_tracker=False, with_solutions=True,
          solutions_only=False, appendix=False):
    global CTX
    CTX = Ctx()
    bodies = []
    for fn in parts:
        bodies += fn()
    story = []
    if cover:
        story += front_matter()
    if with_tracker:
        story += tracker()
    if not solutions_only:
        story += bodies
    if with_solutions and CTX.solutions:
        sol = solutions_section()
        story += sol[1:] if solutions_only else sol
    if appendix:
        story += appendix_grundwortschatz()
    path = OUT / filename
    doc = BaseDocTemplate(str(path), pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                          topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
                          title="Latein-Klausur-Turbo: Ovid, Daedalus & Ikarus",
                          author="Lernpaket", subject="Latein Klausurvorbereitung")
    frame = Frame(MARGIN_X, MARGIN_BOTTOM, CONTENT_W, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPageEnd=decorate)])
    doc.build(story)
    return path


CHAPTERS = [
    ("01_Methode.pdf", kap1),
    ("02_Verben_und_Zeitformen.pdf", kap2),
    ("03_Kasus_und_Satzbau.pdf", kap3),
    ("04_Vokabeln.pdf", kap4),
    ("05_Uebersetzung_3_Stufen.pdf", kap5),
    ("06_Stilmittel_Interpretation_Metrik.pdf", kap6),
    ("07_Probeklausur.pdf", kap7),
]


if __name__ == "__main__":
    made = []
    made.append(build("00_Komplettpaket.pdf", [fn for _, fn in CHAPTERS] + [spickzettel],
                      cover=True, with_tracker=True, appendix=True))
    for name, fn in CHAPTERS:
        made.append(build(name, [fn]))
    made.append(build("09_Loesungen.pdf", [fn for _, fn in CHAPTERS], solutions_only=True))
    made.append(build("10_Spickzettel.pdf", [spickzettel], with_solutions=False))

    print()
    print("=" * 60)
    print("✅ PDF-Sammlung erfolgreich erstellt!")
    print("=" * 60)
    print()
    for p in made:
        print(f"   {p.name}")
    print()
    print(f"Ordner: {OUT}")
    print()
    print("Tipp: Den Ordner aufs iPad schicken (AirDrop/iCloud) und die PDFs in")
    print("GoodNotes, Notability oder der Dateien-App öffnen – die Kästchen sind antippbar.")
    print()
