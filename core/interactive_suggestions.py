import os
import yaml
from autobahn_api.autobahn_api_client import AutobahnApiClient
from LLM_integration.llm_api_handler import LLMApiHandler
from LLM_integration.prompts import generate_einsatz_email_prompt

def autobahn_selection():
    """
    Basic function using simple methods.
    The terminal asks the user which highway they would like to select from a list.
    The user should enter the name of the highway (e.g., A980).
    """

    config_path = os.path.join(os.getcwd(), "config", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    autobahn_base_url = config.get("autobahn_api_url")

    client = AutobahnApiClient(autobahn_base_url)
    # autobahn_ids = {
    #     "roads": ["A1", "A2", "A8", "A9", "A10", "A11", "A12", "A71", "A96", "A98", "A100", "A103", "A111", "A980", "A995"]
    # }
    autobahn_ids = client.get_available_roads()

    autobahn_list = autobahn_ids["roads"]

    print("Bitte geben Sie die Bezeichnung der gewünschten Autobahn ein (z.B. A980):")
    print(", ".join(autobahn_list)+".")

    while True:
        #auswahl = input("Ihre Auswahl: ").strip().upper()  # Clean input and convert to uppercase
        autobahn_input = filter(str.isdigit, input("Ihre Auswahl: ")) # only consider digit inputs
        autobahn_string = "A"+"".join(autobahn_input)
        if autobahn_string in autobahn_list:
            print(f"Sie haben die Autobahn {autobahn_string} ausgewählt.")
            break
        else:
            print(f"Ungültige Eingabe {autobahn_string} . Bitte geben Sie eine Autobahn aus der Liste ein.")

    autobahn_id = autobahn_string

    roadworks = client.get_roadworks(autobahn_id)
    warnings = client.get_warnings(autobahn_id)
    closures = client.get_closures(autobahn_id)

    autobahn_id_dict = {**roadworks, **warnings, **closures}

    print(f'Auf der Autobahn {autobahn_id} liegen {len(autobahn_id_dict["roadworks"])} Baustelle(n), {len(warnings["warning"])} Verkehrsmeldung(en) und {len(closures["closure"])} Sperrung(en) vor.')


def advanced_autobahn_selection():
    """
    Interactive function which allows the user to chose a specific highway and aquire information. 
    """

    #1. Load config
    config_path = os.path.join(os.getcwd(), "config", "config.yaml")
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)    
        print("Konfiguration erfolgreich geladen.")

    except FileNotFoundError:
        print(f"Fehler: Konfigurationsdatei '{config_path}' nicht gefunden.")
        return
    except yaml.YAMLError as e:
        print(f"Fehler beim Laden der Konfigurationsdatei: {e}")
        return
    
    #2. Initialise clients
    try:
        # Autobahn API
        autobahn_base_url = config.get("autobahn_api_url")
        if not autobahn_base_url:
            raise ValueError("autobahn_api_url nicht in config.yaml gefunden.")
        autobahn_client = AutobahnApiClient(autobahn_base_url)
        print("Autobahn API Client initialisiert.")

        # LLM Handler (Gemini)
        gemini_model = config.get("llm_model")
        if not gemini_model:
            raise ValueError("llm_model (Gemini) nicht in config.yaml gefunden.")
        llm_handler = LLMApiHandler(gemini_model)
        print("Gemini LLM Handler initialisiert.")

    except ValueError as e:
        print(f"Fehler bei der Initialisierung: {e}")
        return
    except Exception as e:
        print(f"Unerwarteter Fehler bei der Initialisierung: {e}")
        return
    
    #3. Collect highway data
    # TODO: increase the performance. get_all_data is timeconsuming and inefficient. Idea: Collect/Update the data per highway when needed. 
    autobahn_data = autobahn_client.get_all_data()

    #4. Select highway
    print("Bitte geben Sie die Bezeichnung der gewünschten Autobahn ein (z.B. A980):")
    print(", ".join(str(key) for key in autobahn_data) +".")

    while True:
        autobahn_input = filter(str.isdigit, input("Ihre Auswahl: ")) # only consider digit inputs
        autobahn_string = "A"+"".join(autobahn_input)
        if autobahn_string in autobahn_data:
            print(f"Sie haben die Autobahn {autobahn_string} ausgewählt.")
            break
        else:
            print(f"Ungültige Eingabe {autobahn_string} . Bitte geben Sie eine Autobahn aus der Liste ein.")

    autobahn_id = autobahn_string
    print(f'Auf der Autobahn {autobahn_id} liegen {len(autobahn_data[autobahn_id]["roadworks"])} Baustelle(n), {len(autobahn_data[autobahn_id]["warning"])} Verkehrsmeldung(en) und {len(autobahn_data[autobahn_id]["closure"])} Sperrung(en) vor.')

    #5. Select hazard type
    print("Bitte geben Sie die Art der Meldungen ein zu der eine Einsatzempfehlung gewünscht ist:")
    print("[0] Alle,  [1] Baustellen,  [2] Verkehrsmeldungen,  [3] Sperrungen.")
    while True:
        type_input = filter(str.isdigit, input("Ihre Auswahl: ")) # only consider digit inputs
        type_string = "".join(type_input)
        if type_string:
            type_int = int(type_string)
            break
        else:
            print(f"Ungültige Eingabe {autobahn_string} . Bitte geben Sie eine Autobahn aus der Liste ein.")
        
    if type_int == 1:
        print(f"Sie haben sich für Einsatzempfehlungen zu Baustellen entschieden.")
        roadwork_data = autobahn_data[autobahn_id]["roadworks"]
        warnings_data = []
        closures_data = []
        
    elif type_int == 2:
        print(f"Sie haben sich für Einsatzempfehlungen zu Verkehrsmeldungen entschieden.")
        roadwork_data = []
        warnings_data = autobahn_data[autobahn_id]["warning"]
        closures_data = []
        
    elif type_int == 3:
        print(f"Sie haben sich für Einsatzempfehlungen zu Sperrungen entschieden.")
        roadwork_data = []
        warnings_data = []
        closures_data = autobahn_data[autobahn_id]["closure"]
    
    else:   # default for all int inputs
        print(f"Sie haben sich für Einsatzempfehlungen zu allen Meldungen entschieden.")
        roadwork_data = autobahn_data[autobahn_id]["roadworks"]
        warnings_data = autobahn_data[autobahn_id]["warning"]
        closures_data = autobahn_data[autobahn_id]["closure"]

    #6. Generate LLM prompt
    email_prompt = generate_einsatz_email_prompt(autobahn_id, roadwork_data, warnings_data, closures_data)

    #7. Call LLM
    print(f"Generiere E-Mail-Inhalt für {autobahn_id} mit Gemini...")
    generated_email_content = llm_handler.generate_response(email_prompt)
    if generated_email_content:
        print(f"E-Mail-Inhalt für {autobahn_id} generiert. Inhalt wird nicht versendet. Hier der Inhalt: \n")
        print(generated_email_content)
    else:
        print(f"Konnte keinen E-Mail-Inhalt für Autobahn {autobahn_id} generieren.")

    
    print("\nAutobahn-KI-Assistent beendet.")


if __name__ == "__main__":
    advanced_autobahn_selection()