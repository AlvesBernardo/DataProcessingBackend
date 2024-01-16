import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append("..")
from ..config.connection_configuration import engine
import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Language(db.Model):
    __tablename__ = 'dbo.tblLanguage'
    idLanguage = db.Column(db.Integer, primary_key=True)
    dtLanguage = db.Column(db.String(50), nullable=False)
    accounts = relationship("modelsv2.account_model.Account", back_populates="fiLanguage")
