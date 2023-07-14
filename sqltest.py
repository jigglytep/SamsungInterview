import sqlite3
import asyncio

con = sqlite3.connect('instance/project.db', check_same_thread = False)
con.row_factory = sqlite3.Row   #   add this row
cur = con.cursor()

downloadStatus = {}


def startDownload(id, model_names_list, SU_NO, SUType, SourceSoftware):
    # String []model_names_list, int SU_NO, String SUType, String [] binary_list_to_download
    print(f"Data base is calling start_download(['{model_names_list}'], {SU_NO}, '{SUType}', ['{SourceSoftware}'],)")
    print("id", id)
    print("SourceSoftwar", SourceSoftware)
    downloadStatus[id] = "Downloaded"

def notify(id, model_names_list, SU_NO, SUType, NEWSourceSoftware, OLDSofware):
    if NEWSourceSoftware != OLDSofware:
        print("Download Statu updated")
        startDownload(id, model_names_list, SU_NO, SUType, NEWSourceSoftware)



con.create_function("notify", 6, notify)
con.create_function("startDownload", 5, startDownload)
cur.execute("DROP TRIGGER downloader")
cur.execute("""CREATE TRIGGER downloader AFTER INSERT ON tests BEGIN SELECT startDownload(NEW.id, 
            NEW.MODEL_LIST, NEW.SU_NO, NEW.SUType, NEW.SourceSoftware); END;""")

cur.execute("DROP TRIGGER notifier")
cur.execute("""CREATE TRIGGER notifier AFTER UPDATE ON tests BEGIN SELECT notify(
    NEW.id, NEW.MODEL_LIST, NEW.SU_NO, NEW.SUType, NEW.SourceSoftware, OLD.SourceSoftware); END;""")

def insertNew(data):
    sql = f"""
    INSERT INTO "tests" (
    "id",
    "EVT_TYPE", "MODEL_LIST", 
    "SU_NO", "SUType", "dueDate", 
    "SourceSoftware", "TargetSoftware", "BinaryName", 
    "BinarySize", "email", "jobState", "downloadState", "EVT_TYPE") VALUES 
        ({data["id"]}, "{data["EVT_TYPE"]}", "{data["MODEL_LIST"]}",
        {data["SU_NO"]}, "{data["SUType"]}", datetime('{data["dueDate"]}'),
        "{data["SourceSoftware"]}","{data["TargetSoftware"]}","{data["BinaryName"]}",
        "{data["BinarySize"]}", "email", "{data["jobState"]}","{data["downloadState"]}", "{data["EVT_TYPE"]}"
        );"""
    cur.execute(sql)
    con.commit()

def updateDownLoadState(data):
    sql = f"""UPDATE tests SET "downloadState" = "{data["downloadState"]}" WHERE id =  "{data["id"]}" """
    cur.execute(sql)
    con.commit()

def update(data):
    sql = f"""UPDATE "tests" SET
    "dueDate" = datetime('{data["dueDate"]}'),
    "SourceSoftware" = "{data["SourceSoftware"]}",
    "TargetSoftware" = "{data["TargetSoftware"]}",
    "BinaryName" = "{data["BinaryName"]}",
    "BinarySize" = "{data["BinarySize"]}"
    WHERE MODEL_LIST = "{data["MODEL_LIST"]}" and SU_NO = {data["SU_NO"]} and SUType = "{data["SUType"]}";"""

    cur.execute(sql)
    con.commit()


def get(id):
    sql = f"SELECT * FROM TESTS WHERE id = {id};"
    cur.execute(sql)
    return dict(cur.fetchone())

def getBySubject(data):
    sql = f"""SELECT * FROM TESTS WHERE MODEL_LIST = {data["MODEL_LIST"]} and SU_NO = {data["SU_NO"]} and SUType = {data["SUType"]};"""
    cur.execute(sql)
    return dict(cur.fetchone())






























# cur.execute("""CREATE TRIGGER notifier AFTER INSERT ON tests BEGIN SELECT startDownload(NEW.id); END;""")

# cur.execute("DROP TRIGGER notifier")
# cur.execute("""CREATE TRIGGER notifier AFTER UPDATE ON tests BEGIN SELECT notify(
#             OLD.model_list
#             OLD.id,
#             OLD.EVT_TYPE,
#             OLD.MODEL_LIST,
#             OLD.SU_NO,
#             OLD.SUType,
#             OLD.dueDate,
#             OLD.SourceSoftware,
#             OLD.TargetSoftware,
#             OLD.BinaryName,
#             OLD.BinarySize,
#             OLD.jobState,
#             OLD.downloadState,
#             OLD.EVT_TYPE
# ); END;""")



# cur.execute(sql)
# con.commit()



# import sqlite3

# def notify(*x):
#     print ("Hello",*x)

# def startDownload(id):
#     row = get(id)



# print(sqlite3.version)

# con.create_function("notify", 1, notify)
# con.create_function("startDownload", 1, startDownload)