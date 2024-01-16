from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.app import db
class Account(db.Model):
    __tablename__ = 'dbo.tblAccount'
    idAccount = db.Column(db.Integer, primary_key=True)
    dtEmail = db.Column(db.String(255), nullable=False)
    dtPassword = db.Column(db.String(255), nullable=False)
    isAccountBlocked = db.Column(db.Boolean, nullable=False, default=False)
    dtIsAdmin = db.Column(db.Boolean, nullable=False, default=False)
    #fiSubscription = db.relationship("Subscription", backref="Account")  # Adjust relationship names
    fiLanguage_id = db.Column(db.Integer, db.ForeignKey('dbo.tblLanguage.idLanguage'))
    fiLanguage = relationship("Language", back_populates="accounts")
    def save(self):
        db.session.add(self)
        db.session.commit()        
class Language(db.Model):
    __tablename__ = 'dbo.tblLanguage'
    idLanguage = db.Column(db.Integer, primary_key=True)
    dtLanguage = db.Column(db.String(50), nullable=False)
    accounts = relationship("Account", back_populates="fiLanguage")
