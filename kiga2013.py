# -*- coding: utf8 -*-
# 
# Umfrage Kiga 2013
#

JA = [
    u"ja"
]
JA_NEIN = [
    u"ja",
    u"eher ja",
    u"teilweise",
    u"eher nein",
    u"nein",
    u"weiß nicht",
]
GUT_SCHLECHT = [
    u"gut",
    u"eher gut",
    u"teilweise",
    u"eher schlecht",
    u"schlecht",
    u"weiß nicht",
]

def survey_factory():
    survey = {}
    survey["title"] = u"Elternbefragung 2013"
    survey["questions"] = []
    survey["questions"].append({
        "type": "free-comment",
        "title": u"Elternbefragung 2013",
        "toc": u"Zur Umfrage",
        "question": u"""
<p>
Liebe Eltern! </p>
<p>
Hier findet Ihr die diesjährige schriftliche Elternbefragung,
die der Elternbeirat zusammen mit dem Erzieherinnenteam erarbeitet hat. </p>
<p>
Ziel des Fragebogens ist es, Eure Zufriedenheit mit unserem Kindergarten
abzufragen und wichtige Impulse zu geben, ihn weiterzuentwickeln. Dafür 
ist es wichtig, Eure Meinung zu verschiedenen Bereichen des 
Kindergartenlebens wie Räumlichkeiten, Informationsfluss, Wohlbefinden 
der Eltern und der Kinder zu erfahren. Diese Fragen bilden den ersten 
Teil des Fragebogens. Im zweiten Teil gehen wir kurz auf aktuelle Themen
ein. Das sind diesmal Fragen rund um das Thema Umbau/Renovierung.</p>
<p>
Die Ergebnisse können die Zustände im Kindergarten positiv bestätigen oder 
aber auch dazu führen, Veränderungen zu erarbeiten und umzusetzen. Indem 
Ihr also die vorliegenden Fragen beantwortet, tragt Ihr dazu bei, dass wir 
die Rahmenbedingungen im Kindergarten zu unser aller Zufriedenheit 
gestalten können. Das kommt den Eltern, den Erzieherinnen und natürlich 
ganz besonders unseren Kindern zugute. </p>
<p>
Wir bitten jeden Elternteil bzw. alle Erziehungsberechtigten, einen 
eigenen Fragebogen vollständig auszufüllen. Bei Unklarheiten sprecht
uns gerne an.
</p>
<p>
Selbstverständlich werdet Ihr über die Ergebnisse informiert. </p>
<p>
Die Teilnahme an der Befragung ist freiwillig. Die Auswertung erfolgt 
anonym. </p>
<p>
Bitte füllt Eure Fragebogen bis spätestens Sonntag, den 03. März 
aus. </p>
<p>
Ein großes Dankeschön schon mal für Eure Unterstützung </p>
<p>
vom Elternbeirat: Patrick Schemitz </p>
<p>
und vom Team: Petra Welte </p>
            """,
        "subquestions": [],
        "comment": None,
        "answer": None,
    })
    survey["questions"].append({
        "type": "free-comment",
        "title": u"Anleitung und Hilfe",
        "toc": u"Anleitung",
        "question": u"""
<h2> Fragen </h2>
<p>
  Die Fragen - die komplette Frageliste einer Umfrage findet sich in der
  rechten Spalte - sind natürlich der Schwerpunkt der Umfrage. Es gibt
  verschiedene Fragetypen: bei manchen ist eine Mehrfachauswahl erlaubt,
  bei anderen nicht; meist ist ein Feld für Kommentare, Anregungen etc.
  vorgesehen.
</p>
<p>
  Unter jeder Frage gibt es zwei Knöpfe, "Weiter" und "Zwischenspeichern".
  Normalerweise, wenn man die Umfrage in einem Rutsch ausfüllt, ist
  Zwischenspeichern nicht notwendig, und erst ganz am Schluß, bei der
  Abgabe, wird man auf "Abschicken" clicken. Wenn man aber den Fragebogen
  nicht "am Stück" ausfüllen möchte, kann man jederzeit zwischenspeichern
  und morgen weitermachen.
</p>
<p>
  Der "Weiter"-Button führt zur nächsten Frage. Um zu früheren Fragen
  zurückzukehren, könnt Ihr die Fragen im Inhaltsverzeichnis in der
  rechten Spalte anclicken. Dabei geht nichts verloren, Ihr braucht nicht
  zwischenspeichern.
</p>
<h2> Stimmabgabe </h2>
<p>
  Sind alle Fragen beantwortet, werdet Ihr im letzten Punkt nach
  Eurem <b>Vote-Code</b> gefragt. Das ist die lange Zahl auf dem
  Umfrage-Zettel. Die sorgt dafür, daß jeder nur eine Stimme abgibt,
  und daß die Stimmabgabe trotzdem anonym ist - nämlich durch eine
  anonyme Vote-Code-Ausgabe.
</p>
<p>
  Wenn Ihr nach Eingabe und Abschicken des Vote-Codes <b>keine</b>
  "Vielen Dank für Deine Teilnahme"-Seite seht, war der Vote-Code
  falsch. Vermutlich vertippt, oder Ihr versucht grade, den Vote-Code
  Eures Partners nochmal zu verwenden. Probiert es nochmal, <i>Eure
  Eingaben wurden behalten</i>, Ihr müßt nicht nochmal alles eintippen,
  nur den Vote-Code auf der "Fertig"-Seite; Ihr könnt direkt wieder
  dortin springen.
</p>
<h2> Mehr Hilfe </h2>
<p>
  Falls es noch Fragen gibt, bitte per Mail an patrick.schemitz@web.de
</p>
            """,
        "subquestions": [
        ],
        "comment": None,
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Meine Kinder",
        "toc": u"Meine Kinder",
        "question": u"Ich habe ein Kind in der ...",
        "answer_type": "checkbox",
        "choices": JA,
        "subquestions": [
            u"Blumengruppe",
            u"Wiesengruppe",
            u"Baumgruppe"
        ],
        "comment": None,
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Die Gebäude des Kindergartens",
        "toc": u"Die Gebäude",
        "question": u"Wie beurteilst Du im Kindergarten St. Michael...",
        "answer_type": "radio",
        "choices": GUT_SCHLECHT,
        "subquestions": [
            u"... den Garderobenbereich",
            u"... die sonstigen räumlichen Angebote",
            u"... die Sauberkeit",
            u"... das sonstige Erscheinungsbild",
            u"... die Sicherheit",
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Das Erzieherinnen-Team",
        "toc": u"Das Team",
        "question": u"Welchen Eindruck hast Du vom Erzieherinnen-Team?",
        "answer_type": "radio",
        "choices": GUT_SCHLECHT,
        "subquestions": [
            u"Welchen Eindruck hast Du vom Erzieherinnen-Team?",
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Der Elternbeirat",
        "toc": u"Der EB",
        "question": u"Wie beurteilst Du die Arbeit des aktuellen Elternbeirates?",
        "answer_type": "radio",
        "choices": GUT_SCHLECHT,
        "subquestions": [
            u"Arbeit des aktuellen Elternbeirates",
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Umgang mit Rückmeldungen",
        "toc": u"Rückmeldungen",
        "question": u"Wie ist der Umgang mit Rückmeldungen (d.h. Nachfragen, Lob, Kritik oder Beschwerden)?",
        "answer_type": "radio",
        "choices": GUT_SCHLECHT,
        "subquestions": [
            u"Erzieherinnen-Team",
            u"Elternbeirat",
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Persönliches Engagement",
        "toc": u"Engagement",
        "question": u"Möchtest Du mit persönlichem Engagement Aktivitäten im Kindergarten unterstützen?",
        "answer_type": "checkbox",
        "choices": JA,
        "subquestions": [
            u"Hauswirtschaftlicher Bereich",
            u"Baulicher Bereich",
            u"Pädagogischer Bereich",
            u"Begleitung auf Exkursionen",
            u"Sonstiges (bitte unten angeben)",
        ],
        "comment": u"Sonstiges persönliches Engagement",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Der Informationsfluß",
        "toc": u"Informationsfluß",
        "question": u"Bist Du mit dem Informationsfluß zufrieden bezüglich...",
        "answer_type": "radio",
        "choices": JA_NEIN,
        "subquestions": [
            u"... alltäglicher organisatorischer Belange?",
            u"... der allgemeinen pädagogischen Arbeit?",
            u"... Euer Kind betreffend?",
            u"... getroffener oder anstehender <b>Entscheidungen des Trägers</b> (z.B. den Umbau betreffend)?",
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Welche Information auf welchem Weg?",
        "toc": u"Informationswege",
        "question": u"Auf welchem Wege möchtest Du informiert werden über...",
        "answer_type": "checkbox",
        "choices": [
            u"Einzelgespräche",
            u"Tür + Angel Gespräche",
            u"Infowand",
            u"Email",
        ],
        "subquestions": [
            u"Termine (Waldtage, Sport, Veranstaltungen etc)",
            u"Allgemeine Terminänderungen",
            u"Aktionen für eine Teilgruppe (Exkursionen, Kochtage, Projekte)",
            u"Einladungen vom Team (Elternabend, Elterntreff etc)",
            u"Einladungen von Eltern oder Elternbeirat (Ausflüge, Papa-Kind-Zelten, Stammtisch)",
            u"Infos aus der Kirchengemeinde (Gottesdienste, Feste etc)",
            u"Planung und Organisation von Veranstaltungen mit Listen (Helfer, Teilnehmer)",
            u"Adressen der Eltern",
            u"Externe Informationen (Schulamt, Gesundheitsamt etc)",
            u"Reflexion nach Aktionen (Dank an Eltern etc)",
            u"Information über den Entwicklungsstand des Kindes",
            u"Kurzinfos über das Kind (Unwohlsein, Geschehnisse)",
            u"Persönliche Terminabsprachen (Geburtstagsfeier, Schulranzen mitbringen etc)",
        ],
        "comment": None,
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Regeln und Rituale",
        "toc": u"Regeln und Rituale",
        "question": u"Bist Du mit den Regeln und Ritualen des Kindergartens vertraut (z. B. Essen, Geburtstage, Abholzeiten, Hofregeln)?",
        "answer_type": "radio",
        "choices": JA_NEIN,
        "subquestions": [
            u"Bist Du mit den Regeln und Ritualen des Kindergartens vertraut?"
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Gemeinsame Unternehmungen",
        "toc": u"Unternehmungen",
        "question": u"Bist Du zufrieden mit den Festen und Ausflügen, die Kinder, Team und Eltern gemeinsam unternehmen?",
        "answer_type": "radio",
        "choices": JA_NEIN,
        "subquestions": [
            u"Häufigkeit von Festen",
            u"Art der Feste",
            u"Häufigkeit von Ausflügen",
            u"Art der Ausflüge",
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Wohlfühlen und Zufriedenheit",
        "toc": u"Wohlfühlen",
        "question": u"",
        "answer_type": "radio",
        "choices": JA_NEIN,
        "subquestions": [
            u"Fühlt sich Dein Kind im Kindergarten wohl?",
            u"Fühlst Du Dich im Kindergarten wohl?",
            u"Konntest Du Kontakte zu anderen Eltern knüpfen?",
            u"Würdest Du den Kindergarten Freunden und Bekannten empfehlen?",
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Gestaltung und Gewichtung der Angebote",
        "toc": u"Angebote",
        "question": u"Wie wünschest Du Dir die Gestaltung der verschiedenen Angebote im Kindergarten?",
        "answer_type": "radio",
        "choices": [
            u"mehr",
            u"gut so",
            u"weniger",
            u"egal",
            u"weiß nicht",
        ],
        "subquestions": [
            u"Basteln, Malen",
            u"Erzählen, Vorlesen",
            u"Experimentieren",
            u"Backen, Kochen",
            u"Religiöse Erziehung",
            u"Ruhe, Entspannung",
            u"Singen, Musizieren",
            u"Tanzen, Turnen",
            u"Spielen drinnen",
            u"Spielen draußen",
            u"Werken",
            u"Erkundungen im Ort",
            u"Exkursionen, Ausflüge",
            u"Spazieren gehen",
            u"Spielplatz besuchen",
            u"Wald entdecken",
            u"Werteerziehung",
        ],
        "comment": u"Anmerkungen",
        "answer": None,
    })
    survey["questions"].append({
        "type": "yes-no",
        "title": u"Aktuelles: Umbau",
        "toc": u"Umbau",
        "question": u"An Pfingsten beginnen die Umbau- und Renovierungsarbeiten in unserem Kindergaren. Für den  21., 22., und 23. Mai haben wir uns ein Waldprogramm für unsere Kinder ausgedacht. Am Freitag, den 24. Mai ist der Kindergartern geschlossen. Danach beginnen die Pfingstferien. Am Montag, den 3. Juni sehen wir uns alle wieder im Übergangskindergarten Pfarrsaal.",
        "answer_type": "checkbox",
        "choices": JA,
        "subquestions": [
            u"Ich bin bereit, bei den Vorbereitungen zur Abriss-Disco am 17.05. zu helfen",
            u"Ich bin bereit, die Kindergruppe und die Erzieherinnen am 21., 22. oder 23. Mai in den Wald zu begleiten",
            u"Ich bin bereit, den Erzieherinnen am 21., 22. oder 23. Mai beim Umzug vom Kindergarten ins Pfarrzentrum zu helfen",
            u"Ich bin bereit, dem Erzieherinnenteam am 24. Mai dabei zu helfen, den Übergangskindergarten komplett einzurichten",
        ],
        "comment": u"Allgemeine Kommentare zum Umbau:",
        "answer": None,
    })
    survey["questions"].append({
        "type": "free-comment",
        "title": u"Anmerkungen (positiv)",
        "toc": u"Positive Anmerkungen",
        "question": u"Was Du schon immer einmal <b>an Positivem</b> zum Thema Kindergarten St. Michael loswerden wolltest (z.B. zur Eingewöhnungsphase, Vorbereitung auf die Schule, Tagesablauf, Konzept, Erzieherinnen)",
        "comment": "",
        "answer": None,
    })
    survey["questions"].append({
        "type": "free-comment",
        "title": u"Anmerkungen (negativ)",
        "toc": u"Negative Anmerkungen",
        "question": u"Was Du schon immer einmal <b>an Negativem</b> zum Thema Kindergarten St. Michael loswerden wolltest (z.B. zur Eingewöhnungsphase, Vorbereitung auf die Schule, Tagesablauf, Konzept, Erzieherinnen)",
        "comment": "",
        "answer": None,
    })
    survey["questions"].append({
        "type": "free-comment",
        "title": u"Anmerkungen zum Fragebogen",
        "toc": u"Fragebogen",
        "question": u"Hast Du Anmerkungen zum Fragebogen selbst (fehlt z.B. etwas)?",
        "comment": "",
        "answer": None,
    })
    survey["questions"].append({
        "type": "votecode",
        "title": u"Fragebogen abgeben",
        "toc": u"Fertig",
        "question": u"Um den Umfragebogen abzugeben, bitte gib hier den <b>Vote-Code</b> ein. Der Vote-Code steht auf dem Stück Papier, daß Du zur Umfrage erhalten hast (das mit den Gummibärchen). Achtung: jeder Vote-Code kann genau einmal benutzt werden!",
        "comment": "",
        "answer": None,
    })
    return survey

