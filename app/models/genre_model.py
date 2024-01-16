import sqlite3
import sqlalchemy
import sys
sys.path.append("..")
from ..config.connection_configuration import ConnectionConfiguration

db = SQLAlchamy()

class Gerne(object):
    idGerne = db.Column(db.Integer, primary_key=True)
    dtDescription = db.Column(db.String(50), nullable=False)
   