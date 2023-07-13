
from model import db, app, tests
import datetime


def writeNew(data):
    
    row = tests(
    id = data["id"],
    EVT_TYPE= data["EVT_TYPE"],
    MODEL_LIST= data["MODEL_LIST"],
    SU_NO= data["SU_NO"],
    SUType= data["SUType"],
    dueDate= data["dueDate"],
    SourceSoftware= data["SourceSoftware"],
    TargetSoftware= data["TargetSoftware"],
    BinaryName= data["BinaryName"],
    BinarySize= data["BinarySize"]
    )

    with app.app_context():
        db.session.add(row)
        db.session.commit()

def updateRow(data):
    row = tests.query