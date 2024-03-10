from app.extensions import db
from sqlalchemy.orm import relationship


class Code(db.Model):
    __tablename__ = 'tblCode'
    idCode = db.Column(db.Integer, primary_key=True)
    dtCode = db.Column(db.Integer)
    fiEmail = db.Column(db.Integer, db.ForeignKey("tblAccount.dtEmail"))
    account = relationship("Account")

    def __repr__(self):
        return '<Code %r>' % self.idCode