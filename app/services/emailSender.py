from mailjet_rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY_EMAIL_SENDER")
api_secret = os.getenv("API_SECRET_KEY_EMAIL_SENDER")
sender_email = os.getenv("SENDER_EMAIL_ADDRESS")


def send_email(receiver_email, subject, body):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Me"
                },
                "To": [
                    {
                        "Email": receiver_email,
                        "Name": "Netflix project"
                    }
                ],
                "Subject": subject,
                "TextPart": "Greetings from Netflix!",
                "HTMLPart": body
            }
        ]
    }

    mailjet.send.create(data=data)

# Use the function
# send_email("receiver_email@example.com")
