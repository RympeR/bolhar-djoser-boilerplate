from zeep import Client
from requests import Session
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
from zeep.wsse.username import UsernameToken
from apps.utils.func import client

def send_sms(phone, text):
    message = client.messages.create(
        body=f'Code ' + str(text),
        from_='+12053954148',
        to=phone
    )
