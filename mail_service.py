import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

def load_settings():
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    return settings


def send_email_notification(subject, message):
    settings = load_settings()
    # Email configuration
    sender_email = settings["mail"]["mail"]
    recipient_email = 'armando.de@larosapost.com'
    app_password = settings["mail"]["app_password"]
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create a message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message body
    body = MIMEText(message, 'plain')
    msg.attach(body)

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Close the SMTP connection
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def main():
    test_subject = "Test Email"
    test_message = "This is a test email message."

    result = send_email_notification(test_subject, test_message)

    if result:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")

if __name__ == "__main__":
    main()