
from model import db, app, tests
import sqlalchemy as sa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

@sa.event.listens_for(db.engine, 'connect')
def on_connect(dbapi_connection, connection_record):
    dbapi_connection.create_function('doubleit', 1, doubleit)


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

