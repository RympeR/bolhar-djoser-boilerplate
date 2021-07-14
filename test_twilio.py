import random
from twilio.rest import Client


acount_sid = 'AC387b7c232d6acb1a2834a84ad56d703d'
auth_token = '1017eb4ca8bbe6b16801aab751dd79b7'
client = Client(acount_sid,auth_token)
code = random.randint(1,19999)
phone = "+380953091094"
message =client.messages.create(
    body=str(code),
    from_='+18337740633',
    to=phone
)
