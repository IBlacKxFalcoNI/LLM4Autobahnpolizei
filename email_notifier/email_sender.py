import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import yaml
from dotenv import load_dotenv

class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password, sender_email, receiver_email):
        """
        Initializes the email sender.

        Args:
            smtp_server (str): Address of the SMTP server (eg. "smtp.gmail.com").
            smtp_port (int): Port of the SMTP server (often 587).
            smtp_username (str): Username for SMTP authentication.
            smtp_password (str): App-Password for SMTP authentication. (App-password recommended!).
            sender_email (str): The sender email address.
            receiver_email (str): The recipient email address (highway police).
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        # self.smtp_password = smtp_password # use .env
        self.sender_email = sender_email
        self.receiver_email = receiver_email

        load_dotenv()
        self.smtp_password = os.environ.get("SMTP_PASSWORD")
        if not self.smtp_password:
            raise ValueError("The environment variable SMTP_PASSWORD is not set.")
        

    def send_email(self, subject, body):
        """
        Sends an email with the specified subject and content.

        Args:
            subject (str): Subject of the email.
            body (str): Content of the email.

        Returns:
            bool: True, if the email was sent successfully, otherwise False.
        """
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = Header(subject, 'utf-8')

        try:
            # Establish connection to the SMTP server
            # For TLS (port 587) use start_tls()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            print(f"E-Mail '{subject}' erfolgreich an {self.receiver_email} gesendet.")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"Fehler bei der SMTP-Authentifizierung: Überprüfen Sie Benutzername und Passwort. Details: {e}")
            return False
        except smtplib.SMTPConnectError as e:
            print(f"Fehler beim Verbinden mit dem SMTP-Server: Überprüfen Sie Serveradresse und Port. Details: {e}")
            return False
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist beim E-Mail-Versand aufgetreten: {e}")
            return False

if __name__ == "__main__":
    # To test email functionality
    # Make sure your config.yaml is filled out correctly and the email account details are valid.

    config_path = os.path.join(os.getcwd(), "config", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Read email config from YAML
    smtp_server = config.get("smtp_server")
    smtp_port = config.get("smtp_port")
    smtp_username = config.get("smtp_username")
    smtp_password = config.get("smtp_password")
    sender_email = config.get("sender_email")
    receiver_email = config.get("test_receiver_email")

    if not all([smtp_server, smtp_port, smtp_username, smtp_password, sender_email, receiver_email]):
        print("Bitte füllen Sie alle E-Mail-Konfigurationsfelder in config.yaml aus.")
    else:
        email_sender = EmailSender(smtp_server, smtp_port, smtp_username, smtp_password, sender_email, receiver_email)

        test_subject = "Test-Einsatzhinweis von Ihrem KI-Assistenten"
        test_body = """ Sehr geehrte Kolleginnen und Kollegen der Autobahnpolizei-Bereitschaft,
        dies ist eine Test-E-Mail von Ihrem KI-Verkehrsassistenten.
        Aktuell liegen keine kritischen Vorkommnisse vor.

        Mit freundlichen Grüßen,
        Ihr KI-Verkehrsassistent
        """

        print(f"Versuche, eine Test-E-Mail an {receiver_email} zu senden...")
        if email_sender.send_email(test_subject, test_body):
            print("Test-E-Mail-Versand erfolgreich abgeschlossen.")
        else:
            print("Test-E-Mail-Versand fehlgeschlagen. Fehlermeldungen überprüfen.")