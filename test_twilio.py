import random
from twilio.rest import Client


acount_sid = 'AC3bce9d49f6e044010b3d392f4b9e5921'
auth_token = '79a1ee2b55bd3b360d2f9260c4cab91f'
client = Client(acount_sid,auth_token)
code = random.randint(1,19999)
phone = "+380953091094"
message =client.messages.create(
    body=str(code),
    from_='+12053954148',
    to=phone
)
