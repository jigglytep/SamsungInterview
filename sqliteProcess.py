import sqlite3
from datetime import datetime, timedelta
from communications import notify, startDownload
import api


# DB Connection and Cursor to communicate with the database
con = sqlite3.connect('instance/project.db', check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute("""DELETE FROM tests;""")
con.commit()

con.create_function("notify", 8, notify)
con.create_function("startDownload", 5, startDownload)

# TRIGGER Definitions for the database to communicate with the Communicatoin Functions
try:
    cur.execute("DROP TRIGGER downloader")
    cur.execute("DROP TRIGGER notifier")
except sqlite3.OperationalError as e:
    print("Did not need to delete triggers.")

try:
    cur.execute("""CREATE TRIGGER downloader AFTER INSERT ON tests BEGIN SELECT startDownload(NEW.id,
                NEW.MODEL_LIST, NEW.SU_NO, NEW.SUType, NEW.SourceSoftware); END;""")
    cur.execute("""CREATE TRIGGER notifier AFTER UPDATE ON tests BEGIN SELECT notify(
    NEW.id, NEW.MODEL_LIST, NEW.SU_NO, NEW.SUType, NEW.SourceSoftware, OLD.SourceSoftware, NEW.EVT_TYPE, NEW.downloadState); END;""")
except sqlite3.OperationalError as e:
    print("Did not need to create triggers.")


# Simple Caching Storage
downloadStatus = {}


def wrtieDownloadCache(data=downloadStatus):
    for i in list(data):
        sql = f"""UPDATE tests SET "downloadState" = "{data[i]}" WHERE id =  "{i}" ;"""
        cur.execute(sql)
        con.commit()
        del data[i]


def updateDownLoadState(data):
    sql = f"""UPDATE tests SET "downloadState" = "{data["downloadState"]}" WHERE id =  "{data["id"]}" """
    cur.execute(sql)
    con.commit()


def insertNew(data):
    sql = f"""
        INSERT INTO "tests" (
        "id",
        "EVT_TYPE",
        "MODEL_LIST",
        "SU_NO",
        "SUType",
        "dueDate",
        "SourceSoftware",
        "TargetSoftware",
        "BinaryName",
        "BinarySize",
        "email",
        "jobState",
        "downloadState") 
    VALUES 
        (?,?,?,?,?,?,?,?,?,?,?,?,?);"""

    data_tuple = (
        data["id"],
        data["EVT_TYPE"],
        data["MODEL_LIST"],
        data["SU_NO"],
        data["SUType"],
        datetime.strptime(data["dueDate"], '%m/%d/%Y'),
        data["SourceSoftware"],
        data["TargetSoftware"],
        data["BinaryName"],
        data["BinarySize"],
        "email",
        data["jobState"],
        data["downloadState"])

    cur.execute(sql, data_tuple)
    con.commit()


def update(data):
    oldData = getBySubject(data)

    sql = f"""UPDATE "tests" SET
    "dueDate" = ?,
    "SourceSoftware" = ?,
    "TargetSoftware" = ?,
    "BinaryName" = ?,
    "BinarySize" = ?,
    "EVT_TYPE" = ?,
    "downloadState" = ?
    WHERE MODEL_LIST = "{data["MODEL_LIST"]}" and SU_NO = {data["SU_NO"]} and SUType = "{data["SUType"]}";"""

    data_tuple = (
        datetime.strptime(data.get("dueDate", oldData["dueDate"]), '%m/%d/%Y'),
        data.get("SourceSoftware", oldData["SourceSoftware"]),
        data.get("TargetSoftware", oldData["TargetSoftware"]),
        data.get("BinaryName", oldData["BinaryName"]),
        data.get("BinarySize", oldData["BinarySize"]),
        data.get("EVT_TYPE", oldData["EVT_TYPE"]),
        data.get("downloadState", oldData["downloadState"])
    )

    cur.execute(sql, data_tuple)
    con.commit()


def reTryDownload():
    tomorrow = datetime.today() + timedelta(days=1)

    sql = """SELECT * FROM TESTS
    WHERE dueDate > ? AND downloadState is not "INTERUPTED" or "CANCELED";"""
    data_tuple = (tomorrow, )

    cur.execute(sql, data_tuple)
    result = cur.fetchall()
    rows = [dict(i) for i in result]
    for row in rows:
        row["downloadState"] = startDownload(
            row["id"],
            row["MODEL_LIST"],
            row["SU_NO"],
            row["SUType"],
            row["SourceSoftware"])
        if row["dueDate"] == tomorrow:
            handle_delete_request(row, {})


def executePendingTests():
    sql = """SELECT * FROM TESTS
    WHERE dueDate = ? AND downloadState = "Downloaded";"""
    data_tuple = (datetime.today(), )
    cur.execute(sql, data_tuple)
    result = cur.fetchall()
    rows = [dict(i) for i in result]
    for row in rows:
        startDownload(
            row["id"],
            row["MODEL_LIST"],
            row["SU_NO"],
            row["SUType"],
            row["SourceSoftware"])

        row["EVT_TYPE"] = api.start_submission(
            [row["MODEL_LIST"]], row["SU_NO"], row["SUType"], row["SourceSoftware"], row["BinaryName"], row["BinarySize"])
        row["status"] = "Finished"
        update(row)


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
    data["downloadState"] = "NEW"
    data["EVT_TYPE"] = "TEST"
    insertNew(data)
    # print(downloadStatus)
    downloadStatus[id] = data["downloadState"]
    wrtieDownloadCache()


def getByPK(id):
    sql = f"SELECT * FROM TESTS WHERE id = {id};"
    cur.execute(sql)
    return dict(cur.fetchone())


def getBySubject(data):
    sql = f"""SELECT * FROM TESTS WHERE MODEL_LIST = "{data["MODEL_LIST"]}" and SU_NO = {data["SU_NO"]} and SUType = "{data["SUType"]}";"""
    cur.execute(sql)
    return dict(cur.fetchone())
