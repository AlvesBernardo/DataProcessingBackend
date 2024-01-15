from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subcription(db.Model) : 
    idSubscription = db.Column(db.Integer, primary_key=True)
    dtPayment = db.Column(db.String)
    dtDateOfSignUp = db.Column(db.Date)
    dt7DaysFree = db.Column(db.Integer)
    dtInviteDiscountStatus = db.Column(db.Boolean)
    dtSubscriptionPrice = db.Column(db.Float)
    fiType = db.Column(db.Integer, db.ForeignKey("quality.idType"))
    
    def __repr__(self):
        return '<Subcription %r>' % self.idSubscription