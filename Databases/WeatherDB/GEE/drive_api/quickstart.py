from __future__ import print_function

import io

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    # file_id = '1a3USa3wfeyaiiaG_m3WYMp6WtHyXcRZN'
    file_id = '1D_Kb7USNoH1GkFIMtrkQWUjpk5s6gIC-'
    results = service.files().list(q=f"'{file_id}' in parents",
                                   spaces='drive',
                                   fields="nextPageToken, files(id, name, modifiedTime, md5Checksum)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)

    # file_id = 'MM5ARAIQ7ODBXLLG3WYNCNKP'
    #
    # request = service.files().get_media(fileId=file_id)
    # with open('test.tif', 'wb') as fh:
    #     downloader = MediaIoBaseDownload(fh, request)
    #     done = False
    #     while done is False:
    #         status, done = downloader.next_chunk()
    #         print("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':
    main()
