from __future__ import print_function
from service import service

import base64
from googleapiclient.errors import HttpError


def getHistory():
    request = {
        'labelIds': ['INBOX', 'Label_2507546221306581876', 'UNREAD'], 
        'topicName': 'projects/gmail-test-363715/topics/SamsungPushTopic',
        'labelFilterBehavior': 'INCLUDE'
        }

    historyId = service.users().watch(userId='ltsenovoy@gmail.com', body=request).execute()
    return historyId['historyId']


def getEmails(historyId = 15586695 ):

    try:
        historyList = service.users().history().list(userId="ltsenovoy@gmail.com", startHistoryId=historyId).execute()
        emails = {}
        for history in historyList['history']:
            for message in history['messages']:
                msg = service.users().messages().get(userId="ltsenovoy@gmail.com", id=message['id']).execute()
                headers = msg["payload"]["headers"]

                subject = [i['value'] for i in headers if i["name"]=="Subject"]
                data = [base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8") for part in msg["payload"]["parts"] if part["mimeType"] in ["text/plain", "text/html"]]
                service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
                emails[message['id']] = {"subject": subject, "body":data}

        return emails

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    getEmails()