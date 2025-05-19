import os
import yaml
from dotenv import load_dotenv
import google.generativeai as genai

class LLMApiHandler:
    def __init__(self, model_name):
        """
        Initializes the LLM API handler for Google Gemini.

        Args:
            model_name (str): The name of the Gemini model to be used (eg "gemini-pro").
        """
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("The environment variable GEMINI_API_KEY is not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_response(self, prompt):
        """
        Sends a prompt to the Google Gemini API and returns the response.
        Args:
            prompt (str): The prompt to be sent to Gemini.
        Returns:
            str: The generated response of the LLM or None in case of error.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error interacting with the Google Gemini API: {e}")
            return None

if __name__ == "__main__":
    # For Testin (OpenAI API-Key und model name required in config.yaml)
    config_path = os.path.join(os.getcwd(), "config", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    gemini_model = config.get("llm_model")

    warning_details = {
    "extent": "8.61785,52.97344,8.69904,53.00507",
    "identifier": "V0FSTklOR19fbWRtLnZpel9fTE1TLU5JL3JfTE1TLU5JLzIxMjI2MF9EICBOSSBMTVMtTkkgIC4w",
    "routeRecommendation": [],
    "coordinate": {
        "lat": "53.005070",
        "long": "8.699040"
    },
    "footer": [],
    "icon": "101",
    "isBlocked": "false",
    "description": [
        "Beginn: 25.05.2021 00:00",
        "Ende: 30.11.2021 23:59",
        "",
        "A1 Bremen Richtung Osnabrück",
        "zwischen Dreieck Stuhr und Groß Ippener",
        "Fahrbahnverengung, geänderte Verkehrsführung, Staugefahr, bis voraussichtlich 30.11.2021",
        "Erweiterung PWC Kiekut."
    ],
    "title": "A1 | AS Delmenhorst-Ost (58b) - AS Groß Ippener (59)",
    "point": "8.699040,53.005070",
    "display_type": "WARNING",
    "lorryParkingFeatureIcons": [],
    "future": "false",
    "subtitle": "Bremen Richtung Osnabrück",
    "startTimestamp": "2021-05-25T00:00:00.000+0200"
    }

    if gemini_model:
        llm_handler = LLMApiHandler(gemini_model)
        test_prompt = "Fasse die folgenden Verkehrsmeldungen kurz zusammen: "
        response = llm_handler.generate_response(test_prompt + str(warning_details))
        if response:
            print(f"Answer from Gemini: {response}")
        else:
            print("Couldn't get a response from Gemini.")
    else:
        print("Please configure the Gemini model name in config.yaml.")