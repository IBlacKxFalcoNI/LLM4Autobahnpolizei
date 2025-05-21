import os
import yaml
#from ..autobahn_api.autobahn_api_client import AutobahnApiClient
import autobahn_api.autobahn_api_client
from autobahn_api.autobahn_api_client import AutobahnApiClient


def autobahn_selection():
    """
    Basic function using simple methods.
    The terminal asks the user which highway they would like to select from a list.
    The user should enter the name of the highway (e.g., A980).
    """

    config_path = os.path.join(os.getcwd(), "config", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    base_url = config.get("autobahn_api_url")

    client = AutobahnApiClient(base_url)
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

    config_path = os.path.join(os.getcwd(), "config", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    base_url = config.get("autobahn_api_url")

    client = AutobahnApiClient(base_url)
    
    # TODO: increase the performance. get_all_data is timeconsuming and inefficient. Idea: Collect/Update the data per highway wenn needed. 
    autobahn_data = client.get_all_data()

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


if __name__ == "__main__":
    advanced_autobahn_selection()