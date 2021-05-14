import random
from twilio.rest import Client


acount_sid = 'AC7e26aa22e1d6d1f9439687e1959c6a67'
acount_token = 'f79382fab3faabc4a162a6d08153637e'
client = Client(acount_sid,acount_token)
code = random.randint(1,19999)
phone = "+380953091094"
message =client.messages.create(
    body=str(code),
    from_='+13615416379',
    to=phone
)
