Python Projekt zur Interaktion mit der Autobahn App API (https://autobahn.api.bund.dev/).

Generierung von Einsatzvorschlägen für die Autobahnpolizei-Bereitschaft.


Python project for interacting with the Autobahn App API (https://autobahn.api.bund.dev/). 

Generating deployment suggestions for the Autobahn Police on-call team.

---

# Installation

In the top level directory, run:

``` 
pip install -e .
```

**For LLM:**
- Set your Gemini API key in environment variable `GEMINI_API_KEY`.
- The `llm_model` can be set in the `config.yaml` file.

**For email notifications / SMTP:**
- Set your SMTP password in environment variable `SMTP_PASSWORD`.
- Set your SMTP server, port and username in the `config.yaml` file.
- Set the sender and receiver email address in the `config.yaml` file.

---

# Usage

```
python core/interactive_suggestions.py
```
Running the code allows you to select a highway and a type of hazard for which a deployment suggestion will be generated. No email will be sent.

```
python core/main.py
```
Work in progress. Aim is an fully automated generation of deployment suggestions which will be sent via email.

---

# Structure

*autobahn_api/:* Interaction with the Autobahn API

*config/:* General config, privacy related things in .env

*core/:* Files for actual use

*email_notifier/:* Sending the emails

*LLM_integration/:* Interaction with the LLM API (Gemini)
