import pickle
import os.path
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class InboxManager:
    """Manage Gmail inbox storage by removing messages by label."""

    def __init__(self):
        self.creds = authorize_service()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def remove(self, target_label='UNREAD'):
        """Public call to locate messages by label and send them to trash"""

        messages_to_move = self._list_by_label([target_label])
        # _list_by_label will return a string if no messages to locate
        if not isinstance(messages_to_move, list):
            exception = messages_to_move
            print(exception)
            return
        number_removed = self._move_to_trash(messages_to_move)
        print('%d messages were moved to trash.' % number_removed)

    def _list_by_label(self, target_label):
        """List all messages in mailbox with label_ids applied."""

        try:
            response = self.service.users().messages().list(
                userId='me',
                labelIds=target_label).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])
            # Handles pagination
            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId='me',
                    labelIds=target_label,
                    pageToken=page_token).execute()
                messages.extend(response['messages'])
            if messages: 
                return messages
            else: 
                return 'All messages with that label have been removed.'
        except HttpError as error:
            if parse_error(error) == 'invalidArgument':
                return 'No messages found with that label.'
            else:
                raise error

    def _move_to_trash(self, messages_to_move):
        """Move a list of messages to trash"""

        moved_messages = 0
        for msg in messages_to_move:
            response = self.service.users().messages().trash(
                userId='me',
                id=msg[u'id']).execute()
            print(response)
            moved_messages += 1
        return moved_messages


def authorize_service():
    """Verify account access privileges with OAuth

       The file token.pickle stores the user's access and refresh tokens, and is
       created automatically when the authorization flow completes for the
       first time.
    """

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
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def parse_error(error):
    """Access the reason behind a googleapiclient error

    Google does not provide a built-in method for parsing HttpError objects.
    Taking a look at the source code helps clear this up.
    github.com/googleapis/google-api-python-client/blob/master/googleapiclient/errors.py
    """

    error_response = json.loads(error.content)['error']['errors'][0]
    return error_response['reason']
