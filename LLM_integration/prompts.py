import json

def _format_data_for_llm(data, title):
    """
    Format a list of dictionaries into a readable string for the LLM.
    Ensures that the input is a list and not empty.
    """
    if not data or not isinstance(data, list):
        return f"Keine {title} Daten verfügbar."

    formatted_items = []
    for i, item in enumerate(data):
        item_details = [f"{key}: {value}" for key, value in item.items() if value is not None]
        formatted_items.append(f"--- {title} #{i+1} ---\n" + "\n".join(item_details))
    return "\n\n".join(formatted_items)


def generate_einsatz_email_prompt(road_id, roadworks_data, warnings_data, closures_data):
    """
    Generates a prompt for the LLM to create an email to the highway patrol regarding potential incidents.

    Args:
        road_id (str): ID of the highway (eg. "A8").
        roadworks_data (list): List of dictionaries with roadwork informations.
        warnings_data (list): List of dictionaries with warning informations.
        closures_data (list): List of dictionaries with closure informations.

    Returns:
        str: Full prompt for the LLM.
    """
    roadworks_str = _format_data_for_llm(roadworks_data, "Baustelle")
    warnings_str = _format_data_for_llm(warnings_data, "Verkehrsmeldung")
    closures_str = _format_data_for_llm(closures_data, "Sperrung")

    prompt = f"""
Du bist ein KI-Assistent für die Autobahnpolizei. Deine Aufgabe ist es, die aktuelle Verkehrslage auf der Autobahn {road_id} zu analysieren und eine prägnante, handlungsorientierte E-Mail für die Bereitschaft zu formulieren.

**Ziel der E-Mail:**
Informiere die Autobahnpolizei-Bereitschaft über relevante Vorkommnisse (Baustellen, Verkehrsmeldungen, Sperrungen) auf der Autobahn {road_id}, die möglicherweise einen sofortigen Einsatz erfordern oder eine besondere Aufmerksamkeit verdienen.
Schlage zudem vor, wohin die Bereitschaft aktuell fahren könnte und was dort zu tun wäre.

**Priorisiere folgende Informationen in deiner Analyse und E-Mail:**
1.  **Sperrungen:** Sind Vollsperrungen oder größere Teilsperrungen vorhanden? Wo genau und wie lange? Was ist die empfohlene Umleitung?
2.  **Verkehrsmeldungen:** Gibt es Unfälle, gefährliche Objekte auf der Fahrbahn, Falschfahrer, Staus mit hohem Rückstaupotenzial oder andere akute Gefahren? Wo genau ist der Vorfall und welche Maßnahmen sind denkbar (z.B. Absicherung, Bergung, Verkehrsleitung)?
3.  **Baustellen:** Gibt es größere Baustellen, die zu erheblichen Verkehrsbehinderungen führen oder eine besondere Überwachung erfordern (z.B. an Unfallschwerpunkten)?

**Instruktionen für die E-Mail:**
* **Betreffzeile:** Beginne mit "Einsatzhinweis {road_id}:" gefolgt von einer kurzen, prägnanten Zusammenfassung der wichtigsten Punkte (z.B. "Einsatzhinweis A8: Unfall und Baustelle bei Stuttgart").
* **Anrede:** "Sehr geehrte Kolleginnen und Kollegen der Autobahnpolizei-Bereitschaft,"
* **Einleitung:** Kurze Zusammenfassung der aktuellen Lage.
* **Details:** Liste die relevantesten Vorkommnisse in Stichpunkten auf, jeweils mit:
    * Art des Vorkommnisses (z.B. "Sperrung", "Verkehrsmeldung", "Baustelle")
    * Genauer Ort/Abschnitt (Kilometerangaben oder nahegelegene Städte/Anschlussstellen)
    * Kurze Beschreibung der Lage und ihrer Auswirkungen.
    * **Konkrete Empfehlung für den Einsatzort und die Aufgabe der Bereitschaft.**
* **Abschluss:** "Mit freundlichen Grüßen,"
* **Signatur:** "Ihr KI-Verkehrsassistent"

**Rohdaten für die Analyse der Autobahn {road_id}:**

<Baustellen>
{roadworks_str}
</Baustellen>

<Verkehrsmeldungen>
{warnings_str}
</Verkehrsmeldungen>

<Sperrungen>
{closures_str}
</Sperrungen>

Bitte generiere jetzt die komplette E-Mail im angegebenen Format. Wenn keine relevanten Vorkommnisse vorliegen, formuliere eine entsprechende kurze E-Mail.
"""
    return prompt


def generate_summary_prompt(text_to_summarize):
    """
    Generates a prompt for the LLM to summarize a given text.
    """
    return f"""
Fasse den folgenden Text prägnant zusammen und extrahiere die wichtigsten Informationen. Konzentriere dich auf Orte, Ereignisse und potenzielle Auswirkungen:

Text:
{text_to_summarize}
"""


if __name__ == "__main__":
    # Example data
    example_roadworks = [
        {"id": "rw1", "title": "Fahrbahnerneuerung", "coordLat": 48.7758, "coordLong": 9.1829, "roadId": "A8", "km": "170.5", "extent": "von Ausfahrt Stuttgart-Vaihingen bis Dreieck Leonberg", "description": "Fahrbahnerneuerung auf dem rechten Fahrstreifen, Verkehrsbehinderungen möglich."},
        {"id": "rw2", "title": "Brückenprüfung", "coordLat": 48.65, "coordLong": 9.30, "roadId": "A8", "km": "185.0", "extent": "bei Kirchheim unter Teck", "description": "Kurzzeitige Einengung, geringe Auswirkung."}
    ]

    example_warnings = [
        {"id": "warn1", "title": "Unfall mit Stau", "coordLat": 48.75, "coordLong": 9.20, "roadId": "A8", "km": "175.2", "extent": "zwischen Stuttgart-Möhringen und Degerloch", "description": "PKW-Unfall auf dem linken Fahrstreifen, 5 km Stau. Rettungskräfte sind unterwegs."},
        {"id": "warn2", "title": "Gegenstand auf Fahrbahn", "coordLat": 48.70, "coordLong": 9.25, "roadId": "A8", "km": "180.0", "extent": "Höhe Flughafen Stuttgart", "description": "Großer Gegenstand auf dem mittleren Fahrstreifen."}
    ]

    example_closures = [
        {"id": "clos1", "title": "Vollsperrung", "coordLat": 48.78, "coordLong": 9.18, "roadId": "A8", "km": "169.0", "extent": "Ausfahrt Stuttgart-Vaihingen", "description": "Vollsperrung der Ausfahrt wegen dringender Reparaturen bis 18:00 Uhr."},
        {"id": "clos2", "title": "Teilsperrung", "coordLat": 48.80, "coordLong": 9.15, "roadId": "A8", "km": "165.0", "extent": "Zufahrt Autobahnkreuz Stuttgart", "description": "Rechter Fahrstreifen gesperrt aufgrund von Fahrbahnschäden."}
    ]

    # Test with all data
    full_prompt = generate_einsatz_email_prompt("A8", example_roadworks, example_warnings, example_closures)
    print("\n--- Vollständiger Prompt mit allen Daten ---")
    print(full_prompt)

    # Test with partial data
    empty_warnings_prompt = generate_einsatz_email_prompt("A8", example_roadworks, [], example_closures)
    print("\n--- Prompt mit fehlenden Verkehrsmeldungen ---")
    print(empty_warnings_prompt)

    # Test with empty data
    no_data_prompt = generate_einsatz_email_prompt("A8", [], [], [])
    print("\n--- Prompt ohne Daten ---")
    print(no_data_prompt)