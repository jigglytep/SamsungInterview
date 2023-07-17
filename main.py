from sqliteProcess import executePendingTests, reTryDownload, wrtieDownloadCache, handle_change_request, handle_delete_request, handle_new_test_request
from testData import subject as sj
from testData import body as bd
from parseMail import subjectParse, bodyParse


def main():
    # create test emails
    emails = {i: {"subject": sj[i], "body": bd[i]} for i in range(len(sj))}

    for email in emails:
        subject = subjectParse(emails[email]["subject"])
        body = bodyParse(emails[email]["body"])
        if subject and body:
            if subject["EVT_TYPE"].upper() == "DELETE":
                handle_delete_request(subject, body)
                continue
            if subject["EVT_TYPE"].upper() == "CHANGE":
                handle_change_request(subject, body)
                continue
            if subject["EVT_TYPE"].upper() == "NEW":
                handle_new_test_request(email, subject, body)
                continue
    reTryDownload()
    wrtieDownloadCache()
    executePendingTests()


if __name__ == '__main__':
    main()
