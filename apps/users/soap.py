from zeep import Client
from requests import Session
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
from zeep.wsse.username import UsernameToken


def send_sms(phone, text):
    session = Session()
    session.auth = HTTPBasicAuth('turan', 'turan2021')
    session.verify = False
    transport = Transport(session=session)
    client = Client(
        'http://turbosms.in.ua/api/wsdl.html',
        transport=transport,
        wsse=UsernameToken('turan', 'turan2021')
    )
    result = client.service.Auth(
        login="turan",
        password='turan2021',
    )
    print(f'{result} ->auth')
    phone = '+' + str(phone)
    result = client.service.SendSMS(
        sender="IT Alarm",
        destination=phone,
        text='Code ' + str(text),
    )
    print(f'{result} ->sendsms')
