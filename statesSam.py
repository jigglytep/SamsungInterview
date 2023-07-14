from parseMail import subjectParse, bodyParse
from abc import ABC, abstractmethod

class SchedulerState(ABC):
    @abstractmethod
    def handle_email_request(self, context):
        pass

    @abstractmethod
    def handle_change_request(self, context):
        pass

    @abstractmethod
    def handle_delete_request(self, context):
        pass

    @abstractmethod
    def handle_due_date_reached(self, context):
        pass

    def transition_to(self, state):
        self.context.transition_to(state)


class NewRequestState(SchedulerState):
    def handle_email_request(self, context):
        context.start_download()
        context.transition_to(DownloadInProgressState())

    def handle_change_request(self, context):
        context.reschedule_job()
        context.transition_to(JobScheduledState())

    def handle_delete_request(self, context):
        context.mark_job_failed()
        context.delete_submission()

    def handle_due_date_reached(self, context):
        pass


class DownloadInProgressState(SchedulerState):
    def handle_email_request(self, context):
        pass

    def handle_change_request(self, context):
        context.stop_download()
        context.reinitiate_download()
        context.transition_to(DownloadInProgressState())

    def handle_delete_request(self, context):
        context.stop_download()
        context.mark_job_failed()
        context.delete_submission()

    def handle_due_date_reached(self, context):
        pass
    

class ProcessingState(SchedulerState):

    def handle_email_request(self, context, newEmails):
        subject = subjectParse(newEmails["subject"])
        body = bodyParse(newEmails["body"])

        if subject["status"].upper() == "DELETE":
            self.handle_delete_request(context, subject, body)
        if subject["status"].upper() == "CHANGE":
            self.handle_change_request(context, subject, body)
        if subject["status"].upper() == "NEW":
            self.handle_new_test_request(context, subject, body)
            

    def handle_change_request(self, context, subject, body):
        # get row from db
        # if new download state to downloading and call download function
        # update data
        # write data
        #transition to idles
        # context.transition_to(JobScheduledState())
        pass

    def handle_new_test_request(self, context, subject, body):
        # write data
        # download state to downloading and call download function
        pass

    def handle_delete_request(self, context):
        #get data from database
        #set current job to fial
        # call delete_submission()API
        pass


class SchedulerContext:
    # create database stuff here add static
    def __init__(self):
        self.state = ProcessingState()
    def transition_to(self, state):
        self.state = state

    def handle_email_request(self):
        self.state.handle_email_request(self)

    def handle_change_request(self):
        self.state.handle_change_request(self)

    def handle_delete_request(self):
        self.state.handle_delete_request(self)

    def handle_due_date_reached(self):
        self.state.handle_due_date_reached(self)

    def start_download(self):
        # Implement your logic here to start the download
        pass

    def stop_download(self):
        # Implement your logic here to stop the download
        pass

    def reinitiate_download(self):
        # Implement your logic here to reinitiate the download
        pass

    def delete_submission(self):
        # Implement your logic here to delete the submission
        pass

    def reschedule_job(self):
        # Implement your logic here to reschedule the job
        pass

    def mark_job_failed(self):
        # Implement your logic here to mark the job as failed
        pass

    def start_submission(self):
        # Implement your logic here to start the submission
        pass

