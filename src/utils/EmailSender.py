import smtplib
from email.mime.text import MIMEText

from src.utils.LogManager import Logs


class EmailSender:
    @staticmethod
    def send_email(recipient, subject, body, smtp_server, smtp_port, username, password):
        # Message configuration
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = username
        message["To"] = recipient

        # Connect to the SMTP server using a 'with' statement
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS (Transport Layer Security) for security

            try:
                # Authenticate with the server
                server.login(username, password)

                # Send the email
                server.sendmail(username, recipient, message.as_string())

            except Exception as e:
                print(f"Error sending email: {e}")
                Logs.error_log_manager_custom(f"Error sending email: {e}")
