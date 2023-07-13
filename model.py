from sqlalchemy import MetaData, Column, Table, Integer, String, DateTime
meta = MetaData()


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class tests(db.Model):
    __tablename__ = "tests"
    id = Column("id", Integer, primary_key=True)
    EVT_TYPE = Column("EVT_TYPE", String)
    MODEL_LIST = Column("MODEL_LIST", String)
    SU_NO = Column("SU_NO", String)
    SUType = Column("SUType", String)
    dueDate = Column("dueDate", DateTime)
    SourceSoftware = Column("SourceSoftware", String)
    TargetSoftware = Column("TargetSoftware", String)
    BinaryName = Column("BinaryName", String)
    BinarySize = Column("BinarySize", String)

# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///db_file.db', echo = True)


# insert_statement = insert(tests).values(
#         EVT_TYPE="NEW",
#         MODEL_LIST="SM-G731U",
#         SU_NO="21",
#         SUType="Regular",
#         dueDate="2023-7-15 12:00:00",
#         SourceSoftware="abc",
#         TargetSoftware="GHI",
#         BinaryName="ABC_GHI",
#         BinarySize="567"
# #     )

# EVT_TYPE =
# MODEL_LIST =
# SU_NO =
# SUType =
# # dueDate =
# # SourceSoftware =
# # TargetSoftware =
# # BinaryName =
# # BinarySize =

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# # create the extension
# db = SQLAlchemy()
# # create the app
# app = Flask(__name__)
# # configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# # initialize the app with the extension
# db.init_app(app)
# import datetime

# x = tests(id = 124,         
#     EVT_TYPE="NEW",
#     MODEL_LIST="SM-G731U",
#     SU_NO="21",
#     SUType="Regular",
#     dueDate=datetime.datetime(2020, 5, 17),
#     SourceSoftware="abc",
#     TargetSoftware="GHI",
#     BinaryName="ABC_GHI",
#     BinarySize="567")