from zeep import Client
from requests import Session
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
from zeep.wsse.username import UsernameToken
from core.settings import AUTH_TOKEN
import requests
import json

def send_sms(phone, text):
    url = 'https://im.smsclub.mobi/sms/send'
    data = json.dumps({
    'phone': [phone.replace('+', '')],
    'message' : str(text),
    'src_addr' : 'Shop Zakaz'
    })
    headers = {'Content-Type': 'application/json', 'Authorization':'Bearer ' + AUTH_TOKEN}
    result = requests.post(url,headers=headers, data=data)
    print(result)