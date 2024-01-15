import sqlite3
import sqlalchemy
import sys
sys.path.append("..")
from config.connection_configuration import ConnectionConfiguration

db = SQLAlchamy()

class language(object):
    idLanguage = db.Column(db.Integer, primary_key=True)
    dtLanguage = db.Column(db.String(50), nullable=False)
   