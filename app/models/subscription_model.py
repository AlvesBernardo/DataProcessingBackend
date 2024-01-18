from app.extensions import db
from sqlalchemy.orm import relationship
from .quality_model import Quality
class Subcription(db.Model) :
    __tablename__ = 'tblSubscription'
    idSubscription = db.Column(db.Integer, primary_key=True)
    dtPayment = db.Column(db.String)
    dtDateOfSigUp = db.Column(db.Date)
    dt7DaysFree = db.Column(db.Integer)
    dtInviteDiscount = db.Column(db.Boolean)
    dtSubscriptionPrice = db.Column(db.Float)
    fiType = db.Column(db.Integer, db.ForeignKey("tblQuality.idType"))
    quality = relationship("Quality")
    def __repr__(self):
        return '<Subcription %r>' % self.idSubscription