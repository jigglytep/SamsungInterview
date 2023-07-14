import sqlite3
from datetime import datetime, timedelta
from communications import notify, startDownload
import api
from handlers import handle_delete_request

# DB Connection and Cursor to communicate with the database
con = sqlite3.connect('instance/project.db', check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

con.create_function("notify", 7, notify)
con.create_function("startDownload", 5, startDownload)

# TRIGGER Definitions for the database to communicate with the Communicatoin Functions

# cur.execute("DROP TRIGGER downloader")
# cur.execute("DROP TRIGGER notifier")
# cur.execute("""CREATE TRIGGER downloader AFTER INSERT ON tests BEGIN SELECT startDownload(NEW.id,
#             NEW.MODEL_LIST, NEW.SU_NO, NEW.SUType, NEW.SourceSoftware); END;""")
# cur.execute("""CREATE TRIGGER notifier AFTER UPDATE ON tests BEGIN SELECT notify(
#     NEW.id, NEW.MODEL_LIST, NEW.SU_NO, NEW.SUType, NEW.SourceSoftware, OLD.SourceSoftware, NEW.EVT_TYPE); END;""")


# Simple Caching Storage
downloadStatus = {}


def wrtieDownloadCache(data=downloadStatus):
    for i in data:
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
        datetime.strptime(data["dueDate"], '%m/%d/%Y'),
        data["SourceSoftware"],
        data["TargetSoftware"],
        data["BinaryName"],
        data["BinarySize"],
        data["EVT_TYPE"],
        data["downloadState"]
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


# def get(id):
#     sql = f"SELECT * FROM TESTS WHERE id = {id};"
#     cur.execute(sql)
#     return dict(cur.fetchone())


# def getBySubject(data):
#     sql = f"""SELECT * FROM TESTS WHERE MODEL_LIST = {data["MODEL_LIST"]} and SU_NO = {data["SU_NO"]} and SUType = {data["SUType"]};"""
#     cur.execute(sql)
#     return dict(cur.fetchone())
