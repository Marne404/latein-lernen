# Latein lernen

Mobile-first Vokabeltrainer für die **500 wichtigsten Lateinvokabeln** in 20 Packs à 25 Wörter.
Reines HTML/CSS/JS, kein Build, keine Abhängigkeiten – Fortschritt wird lokal im Browser gespeichert,
die Seite funktioniert offline (PWA, „Zum Startbildschirm hinzufügen“).

## Starten
    npx http-server .      # oder: python3 -m http.server
und `http://localhost:8080` öffnen. Auch als statische Seite hostbar (GitHub Pages o. ä.).

## So funktioniert das Lernen
- **Neue Wörter** (Runden à 5–25): Vorstellen → Multiple-Choice (Latein→Deutsch) → Selbstabfrage. Jedes neue Wort muss
  2× in Folge richtig sein; Fehler kommen schon nach 2–3 Karten wieder.
- **Smarte Wiederholung** (Leitner-System, 6 Boxen): 10 Min → 1 Tag → 3 → 7 → 16 → 35 Tage.
  Fehlerfrei = eine Box höher, Fehler = zwei Boxen zurück. „Sicher“ = ab Box 4.
- **Wiederholen** auf der Startseite mischt alle fälligen Wörter packübergreifend, älteste zuerst.
- **Fortschritt**: Gesamtring, Fortschrittsbalken je Pack (sicher / in Arbeit / neu), Tagesziel, Streak.
- Modi: Smart, Karten (Wischen), Auswahl, Tippen (mit Toleranz für Tippfehler) – unter ⚙️.
- Fortschritt lässt sich als Text sichern / auf anderem Gerät wiederherstellen.

Die Vokabeln stehen in `vocab.js` (`Lemma|Formen|Bedeutung`, je 25 Zeilen = ein Pack) und lassen sich leicht anpassen.
