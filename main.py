from emails import getEmails
from sqltest import getBySubject, update, insertNew, downloadStatus, updateDownLoadState
from testEmail import subject as sj
from testEmail import body as bd
from parseMail import subjectParse, bodyParse

def new_email_request(newEmails):
    subject = subjectParse(newEmails["subject"])
    body = bodyParse(newEmails["body"])

    if subject["EVT_TYPE"].upper() == "DELETE":
        handle_delete_request(subject, body)
    if subject["EVT_TYPE"].upper() == "CHANGE":
        handle_change_request(subject, body)
    if subject["EVT_TYPE"].upper() == "NEW":
        handle_new_test_request(subject, body)






def handle_change_request( subject, body):
    data = subject|body
    update(data)

def handle_new_test_request(id, subject, body):
    data = subject|body
    data["id"] = id
    data["jobState"] = "IDLE"
    data["downloadState"] = "DOWNLOADING"
    data["EVT_TYPE"] = "TEST"
    insertNew(data)
    print(downloadStatus)
    data["downloadState"] = downloadStatus[id]
    updateDownLoadState(data)

def handle_delete_request(subject, body):
    data = subject|body
    data["jobState"] = "IDLE"
    data["downloadState"] = ""
    data["EVT_TYPE"] = "Failed"
    update(data)

def main():
    emails = {'12345678901' :{"subject": sj, "body":bd}}

    for email in emails:
        subject = subjectParse(emails[email]["subject"])
        body = bodyParse(emails[email]["body"])
        if subject["EVT_TYPE"].upper() == "DELETE":
            handle_delete_request(subject, body)
            #TODO: implement THIS!
        if subject["EVT_TYPE"].upper() == "CHANGE":
            handle_change_request(subject, body)
        if subject["EVT_TYPE"].upper() == "NEW":
            handle_new_test_request(email, subject, body)
    
    #TODO:
    # FIX: date not showingup in database
        # run the test functionality

        # run the downloader for failed jobs
if __name__ == '__main__':
    main()