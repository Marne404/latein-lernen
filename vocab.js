/* 500 wichtige Lateinvokabeln, 20 Packs à 25 Wörter.
   Format je Zeile:  Lemma|Formen / Hinweise|Deutsche Bedeutung(en)
   Zeilen mit # beginnen einen neuen Pack (nur Kommentar, die Packs werden automatisch alle 25 Wörter getrennt). */

const PACK_SIZE = 25;

const PACK_TITLES = [
  'Grundwörter',
  'Wichtige Verben I',
  'Menschen & Familie',
  'Sachen & Begriffe',
  'Adjektive & Zahlen',
  'Adjektive der 3. Deklination',
  'Pronomen & Adverbien',
  'Präpositionen & Konjunktionen',
  'Subjunktionen & Zeitadverbien',
  'Verben der a-Konjugation',
  'Verben der e-Konjugation & Co.',
  'Verben der konsonantischen Konj. I',
  'Verben der konsonantischen & i-Konj. II',
  'Deponentien & Unregelmäßiges',
  'Krieg, Bewegung & Komposita',
  'Substantive a- & o-Deklination',
  'Substantive: Neutra & mehr',
  'Substantive der 3. Deklination',
  'Abstrakta, u- & e-Deklination',
  'Zahlen, Steigerung & Rest',
];

const RAW = `
# Pack 1
et|et|und, auch
non|non|nicht
est|esse, sum, fui|sein
in|in + Abl. / + Akk.|in, an, auf (wo?); in ... hinein, gegen (wohin?)
sed|sed|aber, sondern
cum|cum + Abl. / cum + Konj.|mit; als, weil, obwohl
ad|ad + Akk.|zu, an, bei, nach
ut|ut|wie; damit, dass; sodass
qui|qui, quae, quod|der, die, das (Relativpronomen); welcher
ab|ab, a + Abl.|von, von ... her, durch
ex|ex, e + Abl.|aus, von ... her
ne|ne|dass nicht, damit nicht; nicht
si|si|wenn, falls
neque|neque, nec|und nicht, auch nicht, weder
atque|atque, ac|und, und auch
quod|quod|weil; dass
is|is, ea, id|er, sie, es; dieser, jener
hic|hic, haec, hoc|dieser, diese, dieses
ille|ille, illa, illud|jener; er, sie, es
ipse|ipse, ipsa, ipsum|selbst, eigentlich
omnis|omnis, omne|jeder, ganz; (Pl.) alle
magnus|magnus, -a, -um|groß, bedeutend
bonus|bonus, -a, -um|gut
malus|malus, -a, -um|schlecht, schlimm
multus|multus, -a, -um|viel (Pl. viele)
# Pack 2
habere|habeo, habui, habitum|haben, halten für
facere|facio, feci, factum|machen, tun, handeln
dicere|dico, dixi, dictum|sagen, sprechen, nennen
videre|video, vidi, visum|sehen
videri|videor, visus sum|scheinen, gelten als
venire|venio, veni, ventum|kommen
dare|do, dedi, datum|geben
ponere|pono, posui, positum|setzen, stellen, legen
ire|eo, ii (ivi), itum|gehen
vocare|voco, vocavi, vocatum|rufen, nennen, einladen
amare|amo, amavi, amatum|lieben, gern haben
laudare|laudo, laudavi, laudatum|loben
portare|porto, portavi, portatum|tragen, bringen
stare|sto, steti, statum|stehen
vincere|vinco, vici, victum|siegen, besiegen
mittere|mitto, misi, missum|schicken, werfen, loslassen
petere|peto, petivi, petitum|erstreben, bitten, angreifen
scribere|scribo, scripsi, scriptum|schreiben
legere|lego, legi, lectum|lesen, auswählen
ducere|duco, duxi, ductum|führen, ziehen; meinen
audire|audio, audivi, auditum|hören
capere|capio, cepi, captum|nehmen, fangen, erobern
tenere|teneo, tenui, tentum|halten, festhalten, besitzen
manere|maneo, mansi, mansum|bleiben, warten
currere|curro, cucurri, cursum|laufen, eilen
# Pack 3
homo|homo, hominis m.|Mensch
vir|vir, viri m.|Mann
femina|femina, -ae f.|Frau
puer|puer, pueri m.|Junge, Kind
puella|puella, -ae f.|Mädchen
pater|pater, patris m.|Vater
mater|mater, matris f.|Mutter
filius|filius, -i m.|Sohn
filia|filia, -ae f.|Tochter
frater|frater, fratris m.|Bruder
soror|soror, sororis f.|Schwester
amicus|amicus, -i m.|Freund
dominus|dominus, -i m.|Herr
servus|servus, -i m.|Sklave, Diener
rex|rex, regis m.|König
deus|deus, -i m.|Gott
dea|dea, -ae f.|Göttin
miles|miles, militis m.|Soldat
populus|populus, -i m.|Volk
civis|civis, civis m./f.|Bürger(in)
urbs|urbs, urbis f.|Stadt (bes. Rom)
terra|terra, -ae f.|Land, Erde
aqua|aqua, -ae f.|Wasser
vita|vita, -ae f.|Leben
mors|mors, mortis f.|Tod
# Pack 4
res|res, rei f.|Sache, Ding, Angelegenheit
tempus|tempus, temporis n.|Zeit, Zeitpunkt
locus|locus, -i m.|Ort, Stelle
bellum|bellum, -i n.|Krieg
pax|pax, pacis f.|Frieden
dies|dies, diei m./f.|Tag
nox|nox, noctis f.|Nacht
manus|manus, -us f.|Hand; Schar
oculus|oculus, -i m.|Auge
caput|caput, capitis n.|Kopf; Hauptstadt
corpus|corpus, corporis n.|Körper
animus|animus, -i m.|Geist, Mut, Sinn
verbum|verbum, -i n.|Wort
nomen|nomen, nominis n.|Name
lex|lex, legis f.|Gesetz
ius|ius, iuris n.|Recht
virtus|virtus, virtutis f.|Tapferkeit, Tüchtigkeit, Tugend
gloria|gloria, -ae f.|Ruhm
copia|copia, -ae f.|Menge, Vorrat; (Pl.) Truppen
pecunia|pecunia, -ae f.|Geld
res publica|res publica, rei publicae f.|Staat, Gemeinwesen
templum|templum, -i n.|Tempel
domus|domus, -us f.|Haus
via|via, -ae f.|Weg, Straße
navis|navis, navis f.|Schiff
# Pack 5
novus|novus, -a, -um|neu
antiquus|antiquus, -a, -um|alt, altehrwürdig
parvus|parvus, -a, -um|klein, gering
longus|longus, -a, -um|lang, weit
altus|altus, -a, -um|hoch, tief
pulcher|pulcher, pulchra, pulchrum|schön
miser|miser, misera, miserum|arm, unglücklich
liber|liber, libera, liberum|frei
primus|primus, -a, -um|der erste
secundus|secundus, -a, -um|der zweite; günstig
tertius|tertius, -a, -um|der dritte
meus|meus, -a, -um|mein
tuus|tuus, -a, -um|dein
suus|suus, -a, -um|sein, ihr (reflexiv)
noster|noster, nostra, nostrum|unser
vester|vester, vestra, vestrum|euer
alius|alius, alia, aliud|ein anderer
alter|alter, altera, alterum|der eine/andere (von zweien)
solus|solus, -a, -um|allein, einzig
totus|totus, -a, -um|ganz
nullus|nullus, -a, -um|kein
unus|unus, una, unum|ein, einer
duo|duo, duae, duo|zwei
tres|tres, tria|drei
paucus|paucus, -a, -um|wenig (Pl. wenige)
# Pack 6
fortis|fortis, forte|tapfer, stark
gravis|gravis, grave|schwer, ernst, schlimm
levis|levis, leve|leicht
brevis|brevis, breve|kurz
facilis|facilis, facile|leicht
difficilis|difficilis, difficile|schwierig
felix|felix, felicis|glücklich, erfolgreich
ingens|ingens, ingentis|ungeheuer groß
audax|audax, audacis|kühn, verwegen
sapiens|sapiens, sapientis|weise, klug
potens|potens, potentis|mächtig
similis|similis, simile|ähnlich
dissimilis|dissimilis, dissimile|unähnlich
talis|talis, tale|so beschaffen, ein solcher
qualis|qualis, quale|wie beschaffen
tantus|tantus, -a, -um|so groß
quantus|quantus, -a, -um|wie groß
communis|communis, commune|gemeinsam, allgemein
nobilis|nobilis, nobile|adlig, berühmt
turpis|turpis, turpe|hässlich, schändlich
utilis|utilis, utile|nützlich
crudelis|crudelis, crudele|grausam
dulcis|dulcis, dulce|süß, angenehm
celer|celer, celeris, celere|schnell
acer|acer, acris, acre|scharf, heftig, eifrig
# Pack 7
ego|ego, mei|ich
tu|tu, tui|du
nos|nos, nostri/nostrum|wir
vos|vos, vestri/vestrum|ihr
se|sui, sibi, se|sich (reflexiv)
quis|quis, quid|wer? was?
quisque|quisque, quaeque, quodque|jeder (einzelne)
quidam|quidam, quaedam, quoddam|ein gewisser, ein
aliquis|aliquis, aliquid|irgendjemand, etwas
nemo|nemo, neminis|niemand
nihil|nihil|nichts
idem|idem, eadem, idem|derselbe
iste|iste, ista, istud|dieser (da), jener
nunc|nunc|jetzt
tum|tum, tunc|dann, damals
iam|iam|schon, bald
semper|semper|immer
saepe|saepe|oft
numquam|numquam|niemals
ibi|ibi|dort
ubi|ubi|wo; sobald
unde|unde|woher
quo|quo|wohin
nam|nam|denn, nämlich
ita|ita|so, auf diese Weise
# Pack 8
per|per + Akk.|durch, hindurch
pro|pro + Abl.|vor, für, anstelle von
de|de + Abl.|von, von ... herab, über
ob|ob + Akk.|wegen
propter|propter + Akk.|wegen
inter|inter + Akk.|zwischen, unter
contra|contra + Akk.|gegen
apud|apud + Akk.|bei
ante|ante + Akk.|vor
post|post + Akk.|nach, hinter
sub|sub + Akk. / Abl.|unter
super|super + Akk.|über, oberhalb
sine|sine + Abl.|ohne
trans|trans + Akk.|über ... hinüber, jenseits
circum|circum + Akk.|um ... herum
extra|extra + Akk.|außerhalb
intra|intra + Akk.|innerhalb
aut|aut|oder; aut ... aut: entweder ... oder
vel|vel|oder, sogar
-que|-que (angehängt)|und
enim|enim|denn, nämlich
igitur|igitur|also, daher
itaque|itaque|deshalb, daher
autem|autem|aber, andererseits
tamen|tamen|dennoch, trotzdem
# Pack 9
quia|quia|weil
quamquam|quamquam|obwohl
dum|dum|während, solange; bis
postquam|postquam|nachdem
priusquam|priusquam|bevor, ehe
nisi|nisi|wenn nicht, außer
quam|quam|wie; als (nach Komp.); möglichst (+ Superl.)
etiam|etiam|auch, sogar, noch
quoque|quoque|auch
tamquam|tamquam|wie, gleichsam
modo|modo|nur, eben erst
tandem|tandem|endlich, schließlich
denique|denique|schließlich, überhaupt
primum|primum|zuerst, zum ersten Mal
deinde|deinde|dann, darauf
postea|postea|später, danach
interim|interim|inzwischen
statim|statim|sofort
mox|mox|bald
olim|olim|einst, einmal
hodie|hodie|heute
heri|heri|gestern
cras|cras|morgen
ergo|ergo|also, folglich
vero|vero|aber, in der Tat
# Pack 10
clamare|clamo, clamavi, clamatum|schreien, rufen
rogare|rogo, rogavi, rogatum|fragen, bitten
orare|oro, oravi, oratum|bitten, beten, reden
laborare|laboro, laboravi, laboratum|arbeiten, sich anstrengen
parare|paro, paravi, paratum|vorbereiten, beschaffen
pugnare|pugno, pugnavi, pugnatum|kämpfen
superare|supero, superavi, superatum|besiegen, übertreffen
liberare|libero, liberavi, liberatum|befreien
servare|servo, servavi, servatum|retten, bewahren
vitare|vito, vitavi, vitatum|meiden
spectare|specto, spectavi, spectatum|betrachten, anschauen
cogitare|cogito, cogitavi, cogitatum|denken, überlegen
narrare|narro, narravi, narratum|erzählen
monstrare|monstro, monstravi, monstratum|zeigen
necare|neco, necavi, necatum|töten
iuvare|iuvo, iuvi, iutum|unterstützen, helfen
temptare|tempto, temptavi, temptatum|versuchen, angreifen
iudicare|iudico, iudicavi, iudicatum|urteilen, beurteilen
appellare|appello, appellavi, appellatum|nennen, ansprechen
occupare|occupo, occupavi, occupatum|besetzen, ergreifen
putare|puto, putavi, putatum|glauben, meinen
nuntiare|nuntio, nuntiavi, nuntiatum|melden, berichten
exspectare|exspecto, exspectavi, exspectatum|erwarten, warten
donare|dono, donavi, donatum|schenken
dubitare|dubito, dubitavi, dubitatum|zweifeln, zögern
# Pack 11
monere|moneo, monui, monitum|mahnen, warnen
movere|moveo, movi, motum|bewegen, beeindrucken
timere|timeo, timui|fürchten
debere|debeo, debui, debitum|müssen, schulden
docere|doceo, docui, doctum|lehren
respondere|respondeo, respondi, responsum|antworten
sedere|sedeo, sedi, sessum|sitzen
valere|valeo, valui|stark sein, gesund sein, gelten
iubere|iubeo, iussi, iussum|befehlen
placere|placeo, placui, placitum|gefallen
persuadere|persuadeo, persuasi, persuasum + Dat.|überreden, überzeugen
terrere|terreo, terrui, territum|erschrecken
tacere|taceo, tacui, tacitum|schweigen
ridere|rideo, risi, risum|lachen
oportet|oportet, oportuit|es ist nötig, man muss
licet|licet, licuit|es ist erlaubt
studere|studeo, studui + Dat.|sich bemühen, streben nach
favere|faveo, favi, fautum + Dat.|begünstigen, gewogen sein
nocere|noceo, nocui, nocitum + Dat.|schaden
cavere|caveo, cavi, cautum|sich hüten, sich vorsehen
prohibere|prohibeo, prohibui, prohibitum|hindern, abhalten
praebere|praebeo, praebui, praebitum|gewähren, darbieten
sentire|sentio, sensi, sensum|fühlen, meinen, merken
complere|compleo, complevi, completum|füllen, erfüllen
augere|augeo, auxi, auctum|vermehren, vergrößern
# Pack 12
agere|ago, egi, actum|handeln, treiben, verhandeln
vivere|vivo, vixi, victum|leben
vertere|verto, verti, versum|wenden, drehen
trahere|traho, traxi, tractum|ziehen, schleppen
regere|rego, rexi, rectum|lenken, leiten, beherrschen
pellere|pello, pepuli, pulsum|stoßen, schlagen, vertreiben
cedere|cedo, cessi, cessum|gehen, weichen, nachgeben
claudere|claudo, clausi, clausum|schließen, einschließen
cognoscere|cognosco, cognovi, cognitum|erkennen, kennenlernen; (Perf.) wissen
colere|colo, colui, cultum|bebauen, pflegen, verehren
credere|credo, credidi, creditum + Dat.|glauben, vertrauen
discere|disco, didici|lernen, erfahren
dividere|divido, divisi, divisum|teilen, trennen
gerere|gero, gessi, gestum|tragen, ausführen, führen
metuere|metuo, metui|fürchten
occidere|occido, occidi, occisum|töten
perdere|perdo, perdidi, perditum|verlieren, vernichten
quaerere|quaero, quaesivi, quaesitum|suchen, fragen
relinquere|relinquo, reliqui, relictum|zurücklassen, verlassen
solvere|solvo, solvi, solutum|lösen, bezahlen
surgere|surgo, surrexi, surrectum|aufstehen, sich erheben
ludere|ludo, lusi, lusum|spielen
dimittere|dimitto, dimisi, dimissum|entlassen, wegschicken
defendere|defendo, defendi, defensum|verteidigen, abwehren
ostendere|ostendo, ostendi, ostentum|zeigen
# Pack 13
accipere|accipio, accepi, acceptum|annehmen, erhalten, empfangen
incipere|incipio, coepi, inceptum|anfangen
conficere|conficio, confeci, confectum|vollenden, erschöpfen
efficere|efficio, effeci, effectum|bewirken, schaffen
interficere|interficio, interfeci, interfectum|töten
cogere|cogo, coegi, coactum|zwingen, versammeln
iacere|iacio, ieci, iactum|werfen
fugere|fugio, fugi|fliehen, meiden
rapere|rapio, rapui, raptum|rauben, raffen
cupere|cupio, cupivi, cupitum|wünschen, wollen
aspicere|aspicio, aspexi, aspectum|erblicken, ansehen
respicere|respicio, respexi, respectum|zurückblicken, berücksichtigen
recipere|recipio, recepi, receptum|zurücknehmen, aufnehmen
scire|scio, scivi, scitum|wissen
munire|munio, munivi, munitum|befestigen, schützen
custodire|custodio, custodivi, custoditum|bewachen
dormire|dormio, dormivi, dormitum|schlafen
invenire|invenio, inveni, inventum|finden, erfinden
convenire|convenio, conveni, conventum|zusammenkommen
pervenire|pervenio, perveni, perventum|gelangen
reperire|reperio, repperi, repertum|finden, erfahren
punire|punio, punivi, punitum|bestrafen
aperire|aperio, aperui, apertum|öffnen
vincire|vincio, vinxi, vinctum|fesseln
impedire|impedio, impedivi, impeditum|hindern
# Pack 14
sequi|sequor, secutus sum|folgen
loqui|loquor, locutus sum|sprechen
progredi|progredior, progressus sum|vorrücken
pati|patior, passus sum|leiden, zulassen
mori|morior, mortuus sum|sterben
nasci|nascor, natus sum|geboren werden, entstehen
uti|utor, usus sum + Abl.|benutzen, gebrauchen
vereri|vereor, veritus sum|fürchten, scheuen
hortari|hortor, hortatus sum|ermahnen, auffordern
conari|conor, conatus sum|versuchen
mirari|miror, miratus sum|sich wundern, bewundern
arbitrari|arbitror, arbitratus sum|glauben, meinen
sperare|spero, speravi, speratum|hoffen
oriri|orior, ortus sum|entstehen, sich erheben
ingredi|ingredior, ingressus sum|betreten, hineingehen
egredi|egredior, egressus sum|hinausgehen
fieri|fio, factus sum|werden, geschehen
posse|possum, potui|können
velle|volo, volui|wollen
nolle|nolo, nolui|nicht wollen
malle|malo, malui|lieber wollen
ferre|fero, tuli, latum|tragen, bringen, ertragen
abire|abeo, abii, abitum|weggehen
redire|redeo, redii, reditum|zurückgehen, zurückkehren
exire|exeo, exii, exitum|hinausgehen
# Pack 15
adesse|adsum, adfui|da sein, anwesend sein, helfen
abesse|absum, afui|fehlen, abwesend sein, entfernt sein
prodesse|prosum, profui + Dat.|nützen
deesse|desum, defui|fehlen
transire|transeo, transii, transitum|hinübergehen, überschreiten
intrare|intro, intravi, intratum|eintreten
appropinquare|appropinquo, appropinquavi, appropinquatum|sich nähern
oppugnare|oppugno, oppugnavi, oppugnatum|angreifen, bestürmen
expugnare|expugno, expugnavi, expugnatum|erobern
vastare|vasto, vastavi, vastatum|verwüsten
delere|deleo, delevi, deletum|zerstören
vulnerare|vulnero, vulneravi, vulneratum|verwunden
fugare|fugo, fugavi, fugatum|in die Flucht schlagen
cadere|cado, cecidi, casum|fallen
tangere|tango, tetigi, tactum|berühren
premere|premo, pressi, pressum|drücken, bedrängen
resistere|resisto, restiti + Dat.|Widerstand leisten
constituere|constituo, constitui, constitutum|aufstellen, beschließen
instituere|instituo, institui, institutum|einrichten, beginnen, unterrichten
statuere|statuo, statui, statutum|festsetzen, beschließen
contendere|contendo, contendi, contentum|eilen, kämpfen, behaupten
tendere|tendo, tetendi, tentum|spannen, streben
praeesse|praesum, praefui + Dat.|an der Spitze stehen, leiten
interesse|intersum, interfui|dabei sein, teilnehmen; interest: es ist wichtig
praeferre|praefero, praetuli, praelatum|vorziehen
# Pack 16
patria|patria, -ae f.|Vaterland, Heimat
insula|insula, -ae f.|Insel
silva|silva, -ae f.|Wald
porta|porta, -ae f.|Tor, Tür
causa|causa, -ae f.|Grund, Ursache, Sache; (+ Gen.) wegen
fama|fama, -ae f.|Gerücht, Ruf
fortuna|fortuna, -ae f.|Schicksal, Glück
victoria|victoria, -ae f.|Sieg
provincia|provincia, -ae f.|Provinz
epistula|epistula, -ae f.|Brief
villa|villa, -ae f.|Landhaus
hora|hora, -ae f.|Stunde
agricola|agricola, -ae m.|Bauer
poeta|poeta, -ae m.|Dichter
nauta|nauta, -ae m.|Seemann
ager|ager, agri m.|Acker, Feld
liber (Buch)|liber, libri m.|Buch
magister|magister, magistri m.|Lehrer
equus|equus, -i m.|Pferd
annus|annus, -i m.|Jahr
ventus|ventus, -i m.|Wind
numerus|numerus, -i m.|Zahl, Menge
campus|campus, -i m.|Feld, Ebene
murus|murus, -i m.|Mauer
gladius|gladius, -i m.|Schwert
# Pack 17
auxilium|auxilium, -i n.|Hilfe
consilium|consilium, -i n.|Plan, Rat, Beschluss
imperium|imperium, -i n.|Befehl, Herrschaft, Reich
periculum|periculum, -i n.|Gefahr
proelium|proelium, -i n.|Schlacht
oppidum|oppidum, -i n.|Stadt (kleinere)
regnum|regnum, -i n.|Königsherrschaft, Reich
signum|signum, -i n.|Zeichen, Feldzeichen, Statue
studium|studium, -i n.|Eifer, Streben, Studium
otium|otium, -i n.|Muße, Freizeit
negotium|negotium, -i n.|Geschäft, Aufgabe, Mühe
officium|officium, -i n.|Pflicht, Dienst
exemplum|exemplum, -i n.|Beispiel, Vorbild
beneficium|beneficium, -i n.|Wohltat
initium|initium, -i n.|Anfang
saxum|saxum, -i n.|Fels, Stein
ferrum|ferrum, -i n.|Eisen, Schwert
aurum|aurum, -i n.|Gold
castra|castra, -orum n. Pl.|Lager
arma|arma, -orum n. Pl.|Waffen
socius|socius, -i m.|Gefährte, Bundesgenosse
inimicus|inimicus, -i m.|(persönlicher) Feind
cibus|cibus, -i m.|Speise, Nahrung
vinum|vinum, -i n.|Wein
tectum|tectum, -i n.|Dach, Haus
# Pack 18
hostis|hostis, hostis m.|Feind (des Staates)
pars|pars, partis f.|Teil, Richtung, Seite
mons|mons, montis m.|Berg
mare|mare, maris n.|Meer
flumen|flumen, fluminis n.|Fluss
ignis|ignis, ignis m.|Feuer
lux|lux, lucis f.|Licht
vox|vox, vocis f.|Stimme, Wort
pes|pes, pedis m.|Fuß
iter|iter, itineris n.|Weg, Marsch, Reise
genus|genus, generis n.|Art, Geschlecht, Gattung
opus|opus, operis n.|Werk, Arbeit; opus est: es ist nötig
scelus|scelus, sceleris n.|Verbrechen
vulnus|vulnus, vulneris n.|Wunde
pectus|pectus, pectoris n.|Brust, Herz
imperator|imperator, imperatoris m.|Feldherr, Kaiser
orator|orator, oratoris m.|Redner
consul|consul, consulis m.|Konsul
senator|senator, senatoris m.|Senator
senatus|senatus, -us m.|Senat
princeps|princeps, principis m.|erster Mann, Fürst, Kaiser
dux|dux, ducis m.|Führer, Feldherr
libertas|libertas, libertatis f.|Freiheit
civitas|civitas, civitatis f.|Bürgerschaft, Staat
voluntas|voluntas, voluntatis f.|Wille, Wunsch
# Pack 19
amor|amor, amoris m.|Liebe
dolor|dolor, doloris m.|Schmerz, Kummer
timor|timor, timoris m.|Furcht
honor|honor, honoris m.|Ehre, Amt
labor|labor, laboris m.|Arbeit, Mühe
mos|mos, moris m.|Sitte, Brauch; (Pl.) Charakter
ratio|ratio, rationis f.|Vernunft, Berechnung, Art und Weise
oratio|oratio, orationis f.|Rede
natura|natura, -ae f.|Natur, Wesen
cura|cura, -ae f.|Sorge, Pflege
spes|spes, spei f.|Hoffnung
fides|fides, fidei f.|Treue, Glaube, Vertrauen
facies|facies, faciei f.|Gesicht, Aussehen
acies|acies, aciei f.|Schlachtreihe, Schärfe
exercitus|exercitus, -us m.|Heer
metus|metus, -us m.|Furcht
adventus|adventus, -us m.|Ankunft
impetus|impetus, -us m.|Angriff, Ansturm
usus|usus, -us m.|Gebrauch, Nutzen, Erfahrung
cursus|cursus, -us m.|Lauf, Fahrt
fructus|fructus, -us m.|Frucht, Ertrag
magistratus|magistratus, -us m.|Beamter, Amt
motus|motus, -us m.|Bewegung, Aufruhr
casus|casus, -us m.|Fall, Zufall
vis|vis, vim, vi f. (Pl. vires)|Gewalt, Kraft
# Pack 20
quattuor|quattuor|vier
quinque|quinque|fünf
decem|decem|zehn
centum|centum|hundert
mille|mille|tausend
ceterus|ceterus, -a, -um|übrig, der Übrige (Pl. die anderen)
reliquus|reliquus, -a, -um|übrig, restlich
proximus|proximus, -a, -um|der nächste
summus|summus, -a, -um|der höchste, oberste
maximus|maximus, -a, -um|der größte
melior|melior, melius|besser
peior|peior, peius|schlechter
maior|maior, maius|größer
minor|minor, minus|kleiner
plus|plus, pluris|mehr
optimus|optimus, -a, -um|der beste
verus|verus, -a, -um|wahr, richtig
falsus|falsus, -a, -um|falsch
iustus|iustus, -a, -um|gerecht
certus|certus, -a, -um|sicher, bestimmt
carus|carus, -a, -um|lieb, teuer
satis|satis|genug
valde|valde|sehr
bene|bene|gut
male|male|schlecht
`;

/** Parst RAW in eine Liste von Wortobjekten. */
const WORDS = RAW.split('\n')
  .map(l => l.trim())
  .filter(l => l && !l.startsWith('#'))
  .map((line, id) => {
    const [la, forms, de] = line.split('|');
    return { id, la, forms, de, pack: Math.floor(id / PACK_SIZE), cls: wordClass(la, forms) };
  });

/** Grobe Wortart für sinnvolle Antwortalternativen im Multiple-Choice. */
function wordClass(la, forms) {
  if (/ sum\b/.test(forms) || /re$/.test(la) || /^(posse|velle|nolle|malle|ferre|fieri|esse|ire|oportet|licet)$/.test(la)) return 'v';
  if (/ (m|f|n)\.( |$)|m\.\/f\.| Pl\.$/.test(forms)) return 'n';
  if (/-a, -um|, -a$|, -is|, e$|, [a-z]+e$|, [a-z]+us$|, [a-z]+ius$/.test(forms) && !/ \+ /.test(forms)) return 'a';
  if (/ \+ (Akk|Abl|Gen|Dat)/.test(forms) && !/(eo|o|or)\b.*,/.test(forms)) return 'p';
  return 'x';
}
