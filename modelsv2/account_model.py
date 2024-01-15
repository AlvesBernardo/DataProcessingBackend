from flask import Flask
from config.connection_configuration import engine
from flask_sqlalchemy import SQLAlchemy
# Creating the SQLAlchemy instance
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'dbo.tblAccount'  # Specify the table name

    idAccount = db.Column(db.Integer, primary_key=True)
    dtEmail = db.Column(db.String(255), nullable=False)
    dtPassword = db.Column(db.String(255), nullable=False)
    isAccountBlocked = db.Column(db.Boolean, nullable=False, default=False)  # Use 'isAccountBlocked' instead of 'dtIsAccountBlocked'
    dtIsAdmin = db.Column(db.Boolean, nullable=False, default=False)
    fiSubscription = db.relationship("Subscription", backref="dbo.tblSubcription")  # Adjust relationship names
    fiLanguage = db.relationship("Language", backref="dbo.tblLanguage")  # Adjust relationship names
def some_function():
    from modelsv2.subscription_model import Subcription
    from modelsv2.language_model import language