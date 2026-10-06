# ============================================================
# OVID – DAEDALUS & IKARUS
# Lernpaket als PDF
#
# Funktioniert in praktisch jeder normalen Python-Umgebung:
# VS Code, PyCharm, IDLE, Thonny, Jupyter, Google Colab usw.
#
# Voraussetzung:
#     pip install reportlab
# ============================================================

from pathlib import Path

# ------------------------------------------------------------
# ReportLab importieren
# ------------------------------------------------------------

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Table,
        TableStyle,
        PageBreak,
    )
    from reportlab.lib import colors
    from reportlab.lib.styles import (
        getSampleStyleSheet,
        ParagraphStyle,
    )
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.units import cm

except ImportError:
    print("\n❌ Das Modul 'reportlab' ist nicht installiert.")
    print("\nInstalliere es mit:")
    print("    pip install reportlab")
    print("\nDanach dieses Programm erneut starten.")
    raise SystemExit


# ------------------------------------------------------------
# PDF-Datei
# ------------------------------------------------------------

# Die PDF wird im gleichen Ordner wie dieses Python-Skript
# gespeichert.
#
# Falls die Umgebung keinen __file__-Pfad besitzt
# (z. B. manche Jupyter-Umgebungen), wird der aktuelle
# Arbeitsordner verwendet.

try:
    script_folder = Path(__file__).resolve().parent
except NameError:
    script_folder = Path.cwd()

pdf_path = script_folder / "Ovid_Daedalus_Ikarus_Klausur_Lernpaket.pdf"


# ------------------------------------------------------------
# PDF-Dokument einrichten
# ------------------------------------------------------------

doc = SimpleDocTemplate(
    str(pdf_path),
    pagesize=A4,
    leftMargin=1.5 * cm,
    rightMargin=1.5 * cm,
    topMargin=1.4 * cm,
    bottomMargin=1.4 * cm,
)


# ------------------------------------------------------------
# Textstile
# ------------------------------------------------------------

styles = getSampleStyleSheet()

styles.add(
    ParagraphStyle(
        name="T",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=10,
    )
)

styles.add(
    ParagraphStyle(
        name="H",
        parent=styles["Heading1"],
        fontSize=15,
        leading=18,
        spaceBefore=7,
        spaceAfter=6,
    )
)

styles.add(
    ParagraphStyle(
        name="B",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        spaceAfter=5,
    )
)

styles.add(
    ParagraphStyle(
        name="Box",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        borderWidth=0.6,
        borderPadding=7,
        spaceBefore=4,
        spaceAfter=7,
    )
)


story = []


# ============================================================
# 1. ÜBERSETZUNG
# ============================================================

story += [
    Paragraph("Ovid – Daedalus & Ikarus", styles["T"]),

    Paragraph(
        "Gezieltes Lernpaket für deine Lateinarbeit – "
        "Schwerpunkt Übersetzung + Stilmittel + Interpretation",
        styles["B"],
    ),

    Paragraph(
        "<b>Priorität:</b> Du musst heute nicht ganz Latein neu lernen. "
        "Trainiere vor allem: Satzbau erkennen, zentrale Vokabeln "
        "beherrschen, Stilmittel mit Wirkung erklären und die "
        "Hybris-Deutung sicher formulieren.",
        styles["Box"],
    ),

    Paragraph(
        "1. Übersetzung: deine 7-Schritte-Routine",
        styles["H"],
    ),
]


rows = [
    ["1", "Prädikat", "Verb markieren; Person und Zeit bestimmen."],
    ["2", "Subjekt", "Wer handelt? Nominativ suchen."],
    ["3", "Objekte", "Akkusativ = wen/was? Dativ = wem?"],
    [
        "4",
        "Kasus",
        "Genitiv = wessen? Ablativ = wodurch/womit/woher?",
    ],
    [
        "5",
        "Zusammenbauen",
        "Zusammengehörige Wörter trotz freier Wortstellung verbinden.",
    ],
    [
        "6",
        "Sichern",
        "Erst wörtlich/grammatisch korrekt übersetzen.",
    ],
    [
        "7",
        "Glätten",
        "Dann natürliches, sinnvolles Deutsch schreiben.",
    ],
]

table = Table(
    rows,
    colWidths=[
        0.7 * cm,
        4 * cm,
        12.1 * cm,
    ],
)

table.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)

story.append(table)

story.append(
    Paragraph(
        "<b>Notfall:</b> Wenn ein Wort fehlt, nicht hängen bleiben. "
        "Satzkern übersetzen, Stelle markieren, weitergehen und später "
        "zurückkommen.",
        styles["Box"],
    )
)

story.append(PageBreak())


# ============================================================
# 2. ZENTRALE TEXTSTELLEN
# ============================================================

story += [
    Paragraph("2. Zentrale Textstellen", styles["T"]),

    Paragraph(
        "Diese Formulierungen aus deinen Unterrichtsnotizen solltest "
        "du inhaltlich und grammatisch erkennen.",
        styles["B"],
    ),
]

key = [
    [
        "Daedalus pelago clausus erat",
        "Daedalus war vom Meer eingeschlossen.",
    ],
    [
        "perosus Cretam et longum exilium",
        "Kreta und das lange Exil hassend.",
    ],
    [
        "tactus amore natalis loci",
        "von der Liebe zum Geburtsort berührt.",
    ],
    [
        "Terras licet",
        "Der Landweg ist zwar möglich/offen.",
    ],
    [
        "Undas obstruat",
        "Er mag den Wasserweg versperren.",
    ],
    [
        "Caelo patet",
        "Der Himmel steht offen.",
    ],
    [
        "Ergo ibimus",
        "Also werden wir gehen.",
    ],
    [
        "Omnia possidet Minos, non possidet aëra",
        "Minos besitzt alles, aber nicht die Lüfte/den Himmel.",
    ],
    [
        "Pennas in ordine ponit",
        "Er legt die Federn in einer Reihe an.",
    ],
    [
        "A minima coeptas",
        "Beginnend mit den kleinsten.",
    ],
    [
        "longam breviore sequenti",
        "eine längere folgt der kürzeren; Ablativus absolutus.",
    ],
]

table = Table(
    [["Latein", "Sinn"]] + key,
    colWidths=[7.2 * cm, 9.6 * cm],
    repeatRows=1,
)

table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
)

story.append(table)

story += [
    Paragraph(
        "<b>Grammatik-Merker:</b> "
        "<i>erat</i> = Imperfekt von esse. "
        "<i>clausus</i> = PPP → zusammen „war eingeschlossen“. "
        "<i>tactus</i> = PPP von tangere. "
        "<i>amore</i> = Ablativ. "
        "<i>ibimus</i> = Futur „wir werden gehen“. "
        "<i>possidet</i> = „besitzt“.",
        styles["Box"],
    ),

    PageBreak(),

    Paragraph(
        "3. Stilmittel – Definition + Wirkung",
        styles["T"],
    ),
]


# ============================================================
# 3. STILMITTEL
# ============================================================

dev = [
    [
        "Hyperbaton",
        "Zusammengehörige Wörter werden getrennt.",
        "<i>longum ... exilium</i>",
        "Kann die Bedeutung des getrennten Begriffs hervorheben; "
        "hier die Länge des Exils.",
    ],
    [
        "Enjambement",
        "Satz läuft über das Versende hinaus.",
        "Satzende ≠ Versende",
        "Kann Spannung erzeugen oder eine Stelle hervorheben.",
    ],
    [
        "Polyptoton",
        "Gleicher Wortstamm in verschiedenen grammatischen Formen.",
        "Wiederholung von <i>possid-</i>",
        "Betont die Verbindung bzw. den Gegensatz.",
    ],
    [
        "Chiasmus",
        "Überkreuzstellung: ABBA.",
        "<i>Omnia possidet // non possidet aëra</i>",
        "Verstärkt die symmetrische Gegenüberstellung: "
        "Besitz vs. Nicht-Besitz.",
    ],
]

table = Table(
    [["Stilmittel", "Definition", "Beispiel", "Wirkung"]] + dev,
    colWidths=[
        2.5 * cm,
        5 * cm,
        4 * cm,
        5.3 * cm,
    ],
    repeatRows=1,
)

table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.7),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
)

story.append(table)

story.append(
    Paragraph(
        "<b>Klausurformel:</b> Stilmittel nennen → Textstelle zeigen "
        "→ Wirkung erklären → Bezug zum Inhalt herstellen.",
        styles["Box"],
    )
)

story.append(PageBreak())


# ============================================================
# 4. INTERPRETATION
# ============================================================

story += [
    Paragraph(
        "4. Interpretation: Daedalus, Ikarus, Hybris",
        styles["T"],
    ),

    Paragraph(
        "<b>Daedalus:</b> Gefangener auf Kreta, vom Meer eingeschlossen, "
        "hasst Exil und sehnt sich nach der Heimat. Er erkennt: Minos "
        "kontrolliert Land und Meer, aber nicht den Himmel. Deshalb "
        "baut er Flügel.",
        styles["B"],
    ),

    Paragraph(
        "<b>Ikarus:</b> Folgt zunächst dem Vater. Dann erfreut er sich "
        "am Flug, fliegt höher und wird von der Neugier auf den Himmel "
        "angezogen. Er missachtet die Warnung und gerät in Gefahr.",
        styles["B"],
    ),

    Paragraph(
        "<b>Hybris:</b> Überheblichkeit bzw. Grenzüberschreitung. "
        "Daedalus überwindet mit seiner Erfindung die natürlichen "
        "Grenzen des Menschen; Ikarus überschreitet durch seinen zu "
        "hohen Flug die gesetzte Grenze. Der Absturz zeigt die Folgen "
        "der Maßlosigkeit.",
        styles["Box"],
    ),

    Paragraph(
        "<b>Schuldfrage:</b> Ikarus trägt Verantwortung, weil er die "
        "Warnung missachtet. Daedalus kann aber ebenfalls kritisch "
        "gesehen werden, weil seine Erfindung die Grenzüberschreitung "
        "ermöglicht und er die Gefahr möglicherweise unterschätzt. "
        "Dadurch wird Ikarus' Tod auch als hoher Preis der Flucht und "
        "als Folge von Hybris deutbar.",
        styles["Box"],
    ),

    Paragraph(
        "Merksatz: "
        "<b>Daedalus = Erfinder + Flucht aus Not → Grenzüberschreitung.</b> "
        "<b>Ikarus = Neugier + Ungehorsam → Grenzüberschreitung.</b> "
        "<b>Absturz = Konsequenz.</b>",
        styles["Box"],
    ),

    PageBreak(),

    Paragraph(
        "5. Vokabeln für genau diesen Themenbereich",
        styles["T"],
    ),
]


# ============================================================
# 5. VOKABELN
# ============================================================

vocab = [
    ("pelagus", "Meer / offene See"),
    ("claudere", "schließen / einschließen"),
    ("perosus", "hassend / verabscheuend"),
    ("exilium", "Exil / Verbannung"),
    ("tangere", "berühren"),
    ("amor", "Liebe"),
    ("natalis", "zum Geburtsort gehörig"),
    ("locus", "Ort"),
    ("terra", "Land / Erde"),
    ("unda", "Welle / Wasser"),
    ("obstruere", "versperren"),
    ("caelum", "Himmel"),
    ("patere", "offenstehen"),
    ("possidere", "besitzen"),
    ("aer / aëra", "Luft / Lüfte"),
    ("hortari", "ermahnen"),
    ("sequi", "folgen"),
    ("ala", "Flügel"),
    ("animus", "Geist / Sinn"),
    ("demittere", "hinablenken / hinabsenken"),
    ("novare", "erneuern / verändern"),
    ("natura", "Natur"),
    ("penna", "Feder"),
    ("ordo", "Reihe / Ordnung"),
    ("ponere", "setzen / legen"),
    ("minimus", "kleinst-"),
    ("brevis", "kurz"),
    ("gaudere", "sich freuen"),
    ("relinquere", "verlassen / zurücklassen"),
    ("altus", "hoch / tief"),
    ("cupido", "Verlangen / Begierde"),
    ("iter", "Weg / Reise"),
    ("sol", "Sonne"),
    ("cera", "Wachs"),
    ("cadere", "fallen"),
    ("pater", "Vater"),
    ("filius", "Sohn"),
    ("infelix", "unglücklich"),
    ("dicere", "sagen"),
    ("monere", "warnen"),
    ("videre", "sehen"),
]


# Vokabeln auf zwei Spalten verteilen
vr = [["Latein", "Deutsch", "Latein", "Deutsch"]]

half = (len(vocab) + 1) // 2

for i in range(half):

    a = vocab[i]

    if i + half < len(vocab):
        b = vocab[i + half]
    else:
        b = ("", "")

    vr.append([
        a[0],
        a[1],
        b[0],
        b[1],
    ])


table = Table(
    vr,
    colWidths=[
        3.2 * cm,
        5.1 * cm,
        3.2 * cm,
        5.1 * cm,
    ],
    repeatRows=1,
)

table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.2),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]
    )
)

story.append(table)

story.append(PageBreak())


# ============================================================
# 6. SELBSTTEST
# ============================================================

story += [
    Paragraph(
        "6. Selbsttest für heute Abend",
        styles["T"],
    ),

    Paragraph(
        "Beantworte die Fragen ohne nachzusehen. Danach kontrollierst "
        "du mit deinen Notizen.",
        styles["B"],
    ),

    Paragraph(
        "1. Warum ist der Luftweg für Daedalus die einzige echte "
        "Fluchtmöglichkeit?",
        styles["H"],
    ),

    Paragraph(
        "Antwort: _________________________________________________________________",
        styles["B"],
    ),

    Paragraph(
        "2. Was ist ein Hyperbaton und welche Wirkung hat es bei "
        "<i>longum ... exilium</i>?",
        styles["H"],
    ),

    Paragraph(
        "Antwort: _________________________________________________________________",
        styles["B"],
    ),

    Paragraph(
        "3. Erkläre den Chiasmus bei "
        "<i>Omnia possidet Minos, non possidet aëra</i>.",
        styles["H"],
    ),

    Paragraph(
        "Antwort: _________________________________________________________________",
        styles["B"],
    ),

    Paragraph(
        "4. Was bedeutet Hybris und wie zeigt sie sich bei "
        "Daedalus/Ikarus?",
        styles["H"],
    ),

    Paragraph(
        "Antwort: _________________________________________________________________",
        styles["B"],
    ),

    Paragraph(
        "5. Wer trägt die Schuld am Unglück? Nenne Argumente "
        "für beide Seiten.",
        styles["H"],
    ),

    Paragraph(
        "Antwort: _________________________________________________________________"
        "<br/>"
        "__________________________________________________________________________",
        styles["B"],
    ),

    Paragraph(
        "7. Morgen: 5-Minuten-Spickzettel im Kopf",
        styles["T"],
    ),

    Paragraph(
        "<b>Übersetzung:</b> Verb → Wer? → Wen/was? → Wem? "
        "→ Rest → sinnvolles Deutsch.",
        styles["Box"],
    ),

    Paragraph(
        "<b>Stilmittel:</b> Hyperbaton = Trennung; "
        "Enjambement = Zeilensprung; "
        "Polyptoton = Wortstamm-Wiederholung; "
        "Chiasmus = ABBA.",
        styles["Box"],
    ),

    Paragraph(
        "<b>Interpretation:</b> Daedalus = Flucht/Erfindung; "
        "Ikarus = Neugier/Ungehorsam; "
        "Hybris = Grenzüberschreitung; "
        "Absturz = Konsequenz.",
        styles["Box"],
    ),

    Paragraph(
        "<b>Heute Abend:</b> 20 min Vokabeln → 45–60 min Übersetzung "
        "→ 15 min Stilmittel → 15 min Interpretation → schlafen.",
        styles["Box"],
    ),
]


# ============================================================
# PDF ERZEUGEN
# ============================================================

doc.build(story)


# ============================================================
# ERFOLGSMELDUNG
# ============================================================

print()
print("=" * 60)
print("✅ PDF erfolgreich erstellt!")
print("=" * 60)
print()
print(f"Datei: {pdf_path}")
print()
print("Die PDF befindet sich im gleichen Ordner wie dieses Python-Programm.")
print()
