Python Projekt zur Interaktion mit der Autobahn App API (https://autobahn.api.bund.dev/).
Generierung von Einsatzvorschlägen für die Autobahnpolizei-Bereitschaft.


autobahn_api/: Interaktion mit der Autobahn-API

email_notifier/: Versenden der E-Mails

LLM_integration/: Interaktion der LLM-API 

# Installation

In the top level directory, run:

``` 
pip install -e .
```

Set your Gemini API key in environment variable `GEMINI_API_KEY`.

# Usage

```
python core/interactive_suggestions.py
```
Running the code allows you to select a highway and a type of hazard for which an operation suggestion will be generated.