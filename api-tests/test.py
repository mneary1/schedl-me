import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Developers Console
FLOW = OAuth2WebServerFlow(
    client_id='475773583117-esfd3rimutvvfshr8smq6072seon9puo.apps.googleusercontent.com',
    client_secret='vtQ9XhiBwQ_Go9zfTYbHHEb8',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='schedl-me/0.1')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google Developers Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='AIzaSyAv6-nkNFoTIysN0lpdsmCoryjGEup0NKo')

page_token = None
while True:
  calendar_list = service.calendarList().list(pageToken=page_token).execute()
  for calendar_list_entry in calendar_list['items']:
		if calendar_list_entry['accessRole'] == 'owner':
			calender_id = calendar_list_entry['id']
			events = service.events().list(calendarId=calender_id, pageToken=page_token).execute()
			print calendar_list_entry['summary'] + ":"
		for event in events['items']:
			print "\t"+event['summary']

  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    break
'''
events = service.events().list(calendarId='primary',pageToken=None).execute()
for event in events['items']:
	print event['summary']
'''
