import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append("..")
from config.connection_configuration import engine

db = SQLAlchemy()

class language(object):
    __tablename__ = 'dbo.tblLanguage'
    idLanguage = db.Column(db.Integer, primary_key=True)
    dtLanguage = db.Column(db.String(50), nullable=False)
   
    def __repr__(self):
        return f'<Language {self.idLanguage}>'