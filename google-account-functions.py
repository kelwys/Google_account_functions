import os
import json
import hashlib
from apiclient import discovery
from google.oauth2 import service_account


#Google Variables
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user',
          'https://www.googleapis.com/auth/admin.directory.group',
          'https://www.googleapis.com/auth/admin.directory.group.member'
          ]

CLIENT_SECRET_FILE = os.path.join(local_da_sua_base_dir.BASE_DIR, "your_app", "your_dir", "your_api.json")
APPLICATION_NAME = 'app'


#Google Functions
def get_credentials_google():
    credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)
    return credentials

def list_user_google(email):
    credentials = get_credentials_google()
    delegated_credentials = credentials.with_subject('your_mail_admin')

    service = discovery.build('admin', 'directory_v1', credentials=delegated_credentials)

    query = 'email:{}'.format(email)
    results = service.users().list(customer='my_customer', query=query, maxResults=1, orderBy='email').execute()
    users = results.get('users', [])

    if not users:
        return False
    else:
        return True

def changepassword_user_google(primaryEmail, password):
    credentials = get_credentials_google()
    delegated_credentials = credentials.with_subject('your_mail_admin')
    service = discovery.build('admin', 'directory_v1', credentials=delegated_credentials)
    data = {}
    data['password'] = password
    results = service.users().update(userKey=primaryEmail, body=data).execute()
    return results

def create_user_google(fullName, givenName, familyName, primaryEmail, gender, emails, password, list_groupKey):
    data = json.load(open(os.path.join(settings.BASE_DIR, "your_app", "your_dir", "new_user_google.json")))
    data['name']['fullName'] = fullName
    data['name']['givenName'] = givenName
    data['name']['familyName'] = familyName
    data['primaryEmail'] = primaryEmail
    data['gender'] = gender
    data['emails'] = emails
    data['password'] = hashlib.md5(password.encode('utf8')).hexdigest()

    credentials = get_credentials_google()
    delegated_credentials = credentials.with_subject('your_mail_admin')
    service = discovery.build('admin', 'directory_v1', credentials=delegated_credentials)
    results = service.users().insert(body=data).execute()
    for groupKey in list_groupKey:
        body = {"email": primaryEmail, "role": "MEMBER", "memberKey": primaryEmail}
        results1 = service.members().insert(groupKey=groupKey, body=body).execute()

    return results