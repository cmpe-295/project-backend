import requests
from django.conf import settings


def send_activation_email(to_email_id, link):
    return requests.post(
        settings.MAILGUN_API_DOMAIN,
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Spartan Safe Ride Help<nagkumar91@gmail.com>",
              "to": to_email_id,
              "subject": "Welcome To Spartan Safe Ride",
              "text": "Click on the link ("+link+") to activate your account",
              "html": "<html>Click on the <a href="+link+">LINK</a> to activate your account.</html>"})
