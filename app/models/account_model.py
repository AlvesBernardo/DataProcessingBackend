from sqlalchemy.orm import relationship
from app.extensions import db

class Account(db.Model):
    __tablename__ = 'tblAccount'
    idAccount = db.Column(db.Integer, primary_key=True)
    dtEmail = db.Column(db.String(255), nullable=False)
    dtPassword = db.Column(db.String(255), nullable=False)
    isAccountBlocked = db.Column(db.Boolean, nullable=False, default=False)
    dtFailedLoginAttemps = db.Column(db.Integer, nullable=False, default=0)
    dtAccountBlockedTill = db.Column(db.DateTime, nullable=True)
    dtIsAdmin = db.Column(db.Boolean, nullable=False, default=False)
    fiSubscription = db.Column(db.Integer, db.ForeignKey("tblSubscription.idSubscription"))
    subscription = relationship("Subcription")
    fiLanguage = db.Column(db.Integer, db.ForeignKey("tblLanguage.idLanguage"))
    language = relationship("Language")
    def repr(self):
        return '<Account %r>' % self.idAccount