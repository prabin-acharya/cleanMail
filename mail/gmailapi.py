from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import time

from email.mime.text import MIMEText
#from email import errors

from .models import Email

import base64
import email
import json
from datetime import datetime


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


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

service = build('gmail', 'v1', credentials=creds)


def data_encoder(text):
    if len(text)>0:
        message = base64.urlsafe_b64decode(text)
        message = str(message, 'utf-8')
        message = email.message_from_string(message)
    return message

def readMessage(content)->str:
    message = None
    if "data" in content['payload']['body']:
        message = content['payload']['body']['data']
        message = data_encoder(message)
    elif "data" in content['payload']['parts'][0]['body']:
        message = content['payload']['parts'][0]['body']['data']
        message = data_encoder(message)
    else:
        print("body has no data.")
    return message

def get_inbox_gmails():
    # Call the Gmail API
    results = service.users().messages().list(userId='me',labelIds=["INBOX"],q="is:unread category:primary").execute()
    messages = results.get('messages', [])

    for message in messages:#[:message_count]
        save_mail(message)

def send_gmail(recipient, subject, body):
    mail_from = service.users().getProfile(userId='me').execute()['emailAddress']
    mail_to = recipient
    mail_subject = subject
    mail_body = body

    mail = MIMEText(mail_body)
    mail['to'] = mail_to
    mail['from'] = mail_from
    mail['subject'] = mail_subject
    raw = base64.urlsafe_b64encode(mail.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    try:
        mail = (service.users().messages().send(userId='me', body=body).execute())
        print("Your mail has been sent")
    except errors.MessageError as error:
        print("An error occured.Mail not sent.")


def get_sent_gmails():
    results = service.users().messages().list(userId='me',labelIds=["SENT"]).execute()
    messages = results.get('messages', [])

    for message in messages[:5]:
        save_mail(message)

def save_mail(message):
    mail = service.users().messages().get(userId='me', id=message['id'], format="full").execute()
    headers=mail["payload"]["headers"]

    user = service.users().getProfile(userId='me').execute()['emailAddress']

    gmail_id = message['id']

    for i in headers:
        if i["name"] == "From" or i["name"] == "from":
            sender = i["value"]
            #sender = json.dumps(sender[0])
            #sender = sender.strip('\"')

        elif i["name"] == "To" or i["name"] == "to":
            recipients = i["value"]
            #recipients = json.dumps(recipients[0])
            #recipients = recipients.strip('\"')

        elif i["name"] == "Subject" or i["name"] == "subject":
            subject = i["value"]
            #subject = json.dumps(subject[0])

        elif i["name"] == "Date" or i["name"] == "date":
            date = i["value"]
            #Wed, 23 Jun 2021 20:18:44 +0000'  '%a, %d %b %Y %X %Z'
            '''try:
                date = datetime.strptime(date, '%a, %d %b %Y %X %z')
            except ValueError:
                try:
                    date = datetime.strptime(date, '%a, %d %b %Y %X %Z')
                except:
                    date = date[:-5]
                    date = datetime.strptime(date, '%a, %d %b %Y %X %z')
            print(date)
            #date = json.dumps(date[0])'''

    body = readMessage(mail)

    mail2 = Email(
        user = user,
        gmail_id = gmail_id,
        sender = sender,
        recipients = recipients,
        subject = subject,
        body = body,
        timestamp = date
        )
    mail2.save()
