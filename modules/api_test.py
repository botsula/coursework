

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/tasks', 'https://www.googleapis.com/auth/tasks.readonly']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              CREDENTIALS_JSON, SCOPES)
          creds = flow.run_local_server()
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)
  service = build('tasks', 'v1', credentials=creds)
  # Call the Tasks API
  results = service.tasks().list(tasklist='@default').execute()
  items = results.get('items', [])
  if not items:
      print('No task lists found.')
  else:
       print('Tasks:')
       for item in items:
           try:
               print(u'{0} ({1})'.format(item['title'], item['notes']))
           except KeyError:
               print(u'{0}'.format(item['title']))
               
