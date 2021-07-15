import random
from twilio.rest import Client
import os
import environ
env = environ.Env()
env_file = '.env'
# if env_file.exists():
env.read_env(str(env_file))
acount_sid = 'AC387b7c232d6acb1a2834a84ad56d703d'
auth_token =  env.str('TWILIO_KEY')
print(auth_token)
# client = Client(acount_sid,auth_token)
# code = random.randint(1,19999)
# phone = "+380953091094"
# message =client.messages.create(
#     body=str(code),
#     from_='+18337740633',
#     to=phone
# )
