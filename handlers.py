
from sqliteProcess import update, insertNew, downloadStatus, wrtieDownloadCache
from api import delete_submission


def handle_delete_request(subject, body):
    data = subject | body
    data["jobState"] = "IDLE"
    data["downloadState"] = "CANCELED"
    data["EVT_TYPE"] = "Failed"
    update(data)
    api.delete_submission(
        data["MODEL_LIST"], data["SU_NO"], data["SUType"])


def handle_change_request(subject, body):
    data = subject | body
    update(data)
    wrtieDownloadCache()


def handle_new_test_request(id, subject, body):
    data = subject | body
    data["id"] = id
    data["jobState"] = "IDLE"
    data["downloadState"] = "DOWNLOADING"
    data["EVT_TYPE"] = "TEST"
    insertNew(data)
    print(downloadStatus)
    data["downloadState"] = downloadStatus[id]
    wrtieDownloadCache()
