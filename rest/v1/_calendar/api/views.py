from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse

import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import AccessTokenCredentials

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

credentials_json = {"installed":{"client_id":"330448514266-ulng9ntqk7i9st7lsln8usp3c46f9q0v.apps.googleusercontent.com","project_id":"text-detect-294806","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}

# Create your views here.
class GoogleCalendarInitView(View):
    def post(self, request, *args, **kwargs):
        creds = None
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    credentials_json, SCOPES)
                creds = flow.run_local_server(port=0)

        # redirect to a new URL:
        request.session['creds'] = creds
        return HttpResponseRedirect('/api/GoogleCalendarRedirectView/')

    def get(self, request, *args, **kwargs):
        return render(request, 'creds.html')

class GoogleCalendarRedirectView(View):
    def get(self, request, *args, **kwargs):
        creds = request.session['creds']
        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=365, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return HttpResponse('No Records in your Calendar.')

            # Prints the start and name of the next 10 events
            events_print = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
                events_print.append({
                    "start": start,
                    "summary": event['summary']
                })

            return render(request, 'events.html', {'events': events_print})

        except HttpError as error:
            print('An error occurred: %s' % error)
            return HttpResponse('Hello, World! Error')

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')