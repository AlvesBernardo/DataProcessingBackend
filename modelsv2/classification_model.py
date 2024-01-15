import sqlite3
import sqlalchemy
import sys
sys.path.append("..")
from sqlalchemy import Table, Column, Integer, String, MetaData
from config.connection_configuration import engine


db = sqlalchemy()
meta = MetaData()
meta.bind = engine
db.init_app(meta)
class Classification(db.Model):
    idClassification = db.Column(db.Integer, primary_key=True)
    dtDescription = db.Column(db.String(50), nullable=False)
    