from flask import Flask
from config.connection_configuration import engine
from flask_sqlalchemy import SQLAlchemy



# Creating the SQLAlchemy instance
db = SQLAlchemy()

class Account(db.Model):
    idAccount = db.Column(db.Integer, primary_key=True)
    dtEmail = db.Column(db.String(50), nullable=False)
    dtPassword = db.Column(db.String(50), nullable=False)
    dtIsAccountBlocked = db.Column(db.Boolean(True), nullable=False, default=False)
    dtIsAdmin = db.Column(db.Boolean(True), nullable=False, default=False)
    fiSubscription = db.relationship("dbo.tbl0Subscription", backref="dbo.tblAccount")