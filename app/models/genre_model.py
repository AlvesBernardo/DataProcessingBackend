import sqlite3
import sqlalchemy
from app.extensions import db

class Gerne(object):
    idGerne = db.Column(db.Integer, primary_key=True)
    dtDescription = db.Column(db.String(50), nullable=False)
   