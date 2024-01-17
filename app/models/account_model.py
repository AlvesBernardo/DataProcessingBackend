

from app.extensions import db
class Account(db.Model):
    __tablename__ = 'tblAccount'  # Specify the table name
    idAccount = db.Column(db.Integer, primary_key=True)
    dtEmail = db.Column(db.String(255), nullable=False)
    dtPassword = db.Column(db.String(255), nullable=False)
    isAccountBlocked = db.Column(db.Boolean, nullable=False, default=False)  # Use 'isAccountBlocked' instead of 'dtIsAccountBlocked'
    dtIsAdmin = db.Column(db.Boolean, nullable=False, default=False)
    fiSubscription = db.Column(db.Integer, db.ForeignKey("[dbo].tblSubscription.idSubscription")) # Adjust relationship names
    fiLanguage = db.Column(db.Integer, db.ForeignKey("[dbo].tblLanguage.idLanguage"))

    def __repr__(self):
        return '<Quality %r>' % self.idAccount