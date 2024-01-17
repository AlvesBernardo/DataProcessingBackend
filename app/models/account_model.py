from sqlalchemy.orm import relationship
from app.extensions import db
from .subscription_model import  Subcription
from .language_model import Language
class Account(db.Model):
    __tablename__ = 'tblAccount'  # Use double underscores for special SQLAlchemy attributes
    idAccount = db.Column(db.Integer, primary_key=True)
    dtEmail = db.Column(db.String(255), nullable=False)
    dtPassword = db.Column(db.String(255), nullable=False)
    isAccountBlocked = db.Column(db.Boolean, nullable=False, default=False)
    dtIsAdmin = db.Column(db.Boolean, nullable=False, default=False)
    fiSubscription = db.Column(db.Integer, db.ForeignKey("tblSubscription.idSubscription"))  # Adjust the ForeignKey
    subscription = relationship("Subcription")  # This should match the class name of the related model
    fiLanguage = db.Column(db.Integer, db.ForeignKey("tblLanguage.idLanguage"))

    language = relationship("Language")
    def repr(self):  # Use double underscores for special method
        return '<Account %r>' % self.idAccount