import datetime
import pytz
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .config import GOOGLE_CALENDAR_ID, GOOGLE_SERVICE_ACCOUNT_JSON_PATH

def _service():
    scopes = ['https://www.googleapis.com/auth/calendar']
    creds = Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_JSON_PATH, scopes=scopes)
    return build('calendar', 'v3', credentials=creds)

def create_event(title, description, start_dt, end_dt=None):
    service = _service()
    if end_dt is None:
        end_dt = start_dt + datetime.timedelta(hours=1)
    event = {
        'summary': title,
        'description': description or "",
        'start': {'dateTime': start_dt.isoformat()},
        'end': {'dateTime': end_dt.isoformat()},
    }
    created = service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event).execute()
    return created.get('id')

def delete_event(event_id):
    service = _service()
    service.events().delete(calendarId=GOOGLE_CALENDAR_ID, eventId=event_id).execute()
