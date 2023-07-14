from datetime import datetime

class DownloadProgressStates:
    def handle_download(self, scheduler):
        # No action in DownloadProgressState
        pass
    
    def handle_change_request(self, scheduler):
        # No action in DownloadProgressState
        pass
    def handle_retry_request(self, scheduler):
        pass

    def handle_delete_request(self, scheduler):
        # No action in DownloadProgressState
        pass


# Abstract State class
class SchedulerState:
    def handle_parseing(self, email):
        pass

    def handle_download(self, scheduler):
        pass
    
    def handle_change_request(self, scheduler, due_date, source_sw, target_sw, binary_name, binary_size):
        pass
    
    def handle_delete_request(self, scheduler):
        pass
    
    def handle_due_date_reached(self, scheduler):
        pass
    
    def handle_download_success(self, scheduler):
        pass
    
    def handle_download_failed(self, scheduler):
        pass
from parseMail import bodyParse, subjectParse

# Concrete State classes
class IdleState(SchedulerState):
    def handle_download(self, scheduler):
        # Transition to DownloadProgressState
        scheduler.set_state(DownloadProgressState())
        scheduler.start_download()

    def handle_new_email(self, scheduler, newEmails):

        subject = subjectParse(newEmails["subject"])
        body = bodyParse(newEmails["body"])

        if subject["status"].upper() == "CHANGE":
            scheduler.set_state(SubmissionProgressState())
            self.handle_change_request(subject, body)
        if subject["status"].upper() == "NEW":
            pass
        
    def handle_change_request(self, subject, body):
        # No action in IdleState
        pass
    
    def handle_delete_request(self, scheduler):
        # No action in IdleState
        pass
    
    def handle_due_date_reached(self, scheduler):
        # No action in IdleState
        pass
    
    def handle_download_success(self, scheduler):
        # No action in IdleState
        pass
    
    def handle_download_failed(self, scheduler):
        # No action in IdleState
        pass

class DownloadProgressState(SchedulerState):
    def handle_download(self, scheduler):
        # No action in DownloadProgressState
        pass
    
    def handle_change_request(self, scheduler, due_date, source_sw, target_sw, binary_name, binary_size):
        # No action in DownloadProgressState
        pass
    
    def handle_delete_request(self, scheduler):
        # No action in DownloadProgressState
        pass
    
    def handle_due_date_reached(self, scheduler):
        # Transition to SubmissionProgressState
        scheduler.set_state(SubmissionProgressState())
        scheduler.startTest()
    
    def handle_download_success(self, scheduler):
        # No action in DownloadProgressState
        pass
    
    def handle_download_failed(self, scheduler):
        # Transition to IdleState
        scheduler.set_state(IdleState())

class SubmissionProgressState(SchedulerState):
    def handle_download(self, scheduler):
        # No action in SubmissionProgressState
        pass
    
    def handle_change_request(self, scheduler, due_date, source_sw, target_sw, binary_name, binary_size):
        # No action in SubmissionProgressState
        pass
    
    def handle_delete_request(self, scheduler):
        # No action in SubmissionProgressState
        pass
    
    def handle_due_date_reached(self, scheduler):
        # No action in SubmissionProgressState
        pass
    
    def handle_download_success(self, scheduler):
        # Transition to IdleState
        scheduler.set_state(IdleState())
    
    def handle_download_failed(self, scheduler):
        # Transition to IdleState
        scheduler.set_state(IdleState())

# Context class (Scheduler)
class Scheduler:
    def __init__(self):
        self.current_state = IdleState()
    
    def set_state(self, state):
        self.current_state = state
    
    def start_download(self):
        download_success = "Start API call"

        # Perform download operation
        if download_success:
            self.current_state.handle_download_success(self)
        else:
            self.current_state.handle_download_failed(self)
    
    def handle_change_request(self, due_date, source_sw, target_sw, binary_name, binary_size):
        self.current_state.handle_change_request(self, due_date, source_sw, target_sw, binary_name, binary_size)
    
    def handle_delete_request(self):
        self.current_state.handle_delete_request(self)
    
    def handle_due_date_reached(self):
        self.current_state.handle_due_date_reached(self)
    
    def startTest(self):
        # Perform submission operation
        submission_success = "Submit call to API"
        if submission_success:
            self.current_state.handle_download_success(self)
        else:
            self.current_state.handle_download_failed(self)


from emails import getEmails
from parseMail import bodyParse, subjectParse
def main():


    newEmails = getEmails()
    if 'error' in newEmails:
        return "error occured"
    if newEmails is None:
        return "no new emails"
    
    scheduler = Scheduler()
    
    for email in newEmails:
        subject = subjectParse(newEmails[email]["subject"])
        body = bodyParse(newEmails[email]["body"])
        if subject["status"].upper() == "NEW":




    # Handling requests
    scheduler.handle_change_request(due_date, source_sw, target_sw, binary_name, binary_size)
    scheduler.handle_delete_request()
    scheduler.handle_due_date_reached()
