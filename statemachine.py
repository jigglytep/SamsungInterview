from sqliteProcess import executePendingTests, reTryDownload, wrtieDownloadCache, handle_change_request, handle_delete_request, handle_new_test_request
from testData import subject as sj
from testData import body as bd
from parseMail import subjectParse, bodyParse


class SchedulerState:
    def handle_emails(self, emails):
        pass

    def reTryDownload(self):
        pass

    def wrtieDownloadCache(self):
        pass

    def executePendingTests(self):
        pass


class IdleState(SchedulerState):
    def handle_emails(self, emails):
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
        return DownloadInProgressState()


class DownloadInProgressState(SchedulerState):
    def reTryDownload(self):
        reTryDownload()
        return self

    def wrtieDownloadCache(self):
        wrtieDownloadCache()
        return self

    def executePendingTests(self):
        executePendingTests()
        return IdleState()


class Scheduler:
    def __init__(self):
        self.state = IdleState()

    def process_emails(self, emails):
        self.state = self.state.handle_emails(emails)

    def retry_download(self):
        self.state = self.state.reTryDownload()

    def write_download_cache(self):
        self.state = self.state.wrtieDownloadCache()

    def execute_tests(self):
        self.state = self.state.executePendingTests()


def main():
    # create test emails

    emails = {i: {"subject": sj[i], "body": bd[i]} for i in range(len(sj))}
    scheduler = Scheduler()

    scheduler.process_emails(emails)
    scheduler.retry_download()
    scheduler.write_download_cache()
    scheduler.execute_tests()


if __name__ == '__main__':
    main()
