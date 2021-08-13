import random
import requests
import json
import environ
env = environ.Env()
env_file = '.env'
env.read_env(str(env_file))
auth_token =  env.str('SMSCLUB_KEY')
code = random.randint(1,19999)
url = 'https://im.smsclub.mobi/sms/send';
url_codes = 'https://im.smsclub.mobi/sms/status';
data = json.dumps({
    'phone': ['+380953091094'],
    'message' : str(code),
    'src_addr' : 'Shop Zakaz'
})
data_info = json.dumps({
    'id_sms': ['878953762'],
})
headers = {'Content-Type': 'application/json', 'Authorization':'Bearer ' + auth_token}
result = requests.post(url,headers=headers, data=data)
print(result.json())
result = requests.post(url_codes,headers=headers, data=data_info)
print(result.json())