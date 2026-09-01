import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
p=r'C:/Users/arija/ziyancorp/credentials/sa_key.json'
cred=service_account.Credentials.from_service_account_file(p, scopes=['https://www.googleapis.com/auth/drive'])
d=build('drive','v3',credentials=cred)
try:
    a=d.about().get(fields='storageQuota,user').execute()
    print('STORAGE:', json.dumps(a.get('storageQuota',{}), indent=2))
    print('USER:', a.get('user',{}))
except Exception as e:
    print('ERR', e)
