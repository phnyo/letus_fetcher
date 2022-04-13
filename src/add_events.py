import datetime
import os.path
import json
import hashlib
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def cred_and_post():
    print('[FUNCTION] start cred_and_post')
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        print('[MIS] trying with credential')
        service = build('calendar', 'v3', credentials=creds)
        
        # Read the json file
        with open('./calendar.json', 'r') as fi:
            print('[MIS] read calendar.json')
            calendar_data_dict = json.load(fi)
            
            hashval_match_flg = False
            print('[MIS] calculate hashval for summary in calendar.json')
            cat_summary = ""
            for num in calendar_data_dict:
                cat_summary.join(calendar_data_dict[num]['SUMMARY'])
            cat_summary_hashval = hashlib.md5(cat_summary.encode()).hexdigest()
            
            print('[MIS] compare hashval')
            if os.path.exists('./dict_hashval'):
                with open('./dict_hashval', 'r') as fi:
                    prev_hashval = fi.read()
                    if cat_summary_hashval == prev_hashval:
                        hashval_match_flg = True

                if hashval_match_flg == True:
                    print('[FUNCTION] hashval matched. end cred_and_post')
                    return
                
                else 
                    with open('./dict_hashval', 'w') as fo:
                        fo.write(cat_summary_hashval)

        # else fetch the title list
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        monthLater = datetime.datetime.utcnow() + datetime.timedelta(days=31)
        monthLater = monthLater.isoformat() + 'Z'
        events_list = service.events().list(calendarId='primary', timeMin=now, timeMax=monthLater).execute()
        
        # if an event is not included, then post
        events_set = set()
        for event in events_list['items']:
            events_set.add(event['summary'])

        for num in calendar_data_dict:
            if not calendar_data_dict[num]['SUMMARY'] in events_set:
                end_date_str = re.sub('T', ' ', calendar_data_dict[num]['DTEND'][:-9])
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
                start_date = end_date + datetime.timedelta(hours=-3)
                
                print(start_date, end_date)
                
                insert_result = service.events().insert(calendarId='primary',
                        body= {
                            "summary": calendar_data_dict[num]['SUMMARY'],
                            "start": {
                                "dateTime": datetime.datetime.strftime(start_date, "%Y-%m-%dT%H:%M:00+09:00")
                            },
                            "end": {
                                "dateTime": datetime.datetime.strftime(end_date, "%Y-%m-%dT%H:%M:00+09:00")
                            },
                            
                        }
                    ).execute()
                print(insert_result)

    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == "__main__":
    cred_and_post()
