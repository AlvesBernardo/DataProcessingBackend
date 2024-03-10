from app.extensions import db
from sqlalchemy.orm import relationship


class Profile(db.Model):
    __tablename__ = 'tblProfile'
    idProfile = db.Column(db.Integer, primary_key=True)
    dtName = db.Column(db.String(50))
    dtMinor = db.Column(db.Integer)
    dtProfileImage = db.Column(db.String(255))
    fiAccount = db.Column(db.Integer, db.ForeignKey("tblAccount.idAccount"))
    account = relationship("Account")
    fiGenre = db.Column(db.Integer, db.ForeignKey("tblGenre.idGenre"))
    genre = relationship("Genre")

    def __repr__(self):
        return '<Profile %r>' % self.idProfile
