from app.extensions import db
from sqlalchemy.orm import relationship
from .account_model import Account
from .genre_model import Genre
class Profile(db.Model) : 
    __tablename__ = 'tblProfile'  # Specify the table name
    idProfile = db.Column(db.Integer, primary_key=True)
    dtName = db.Column(db.String(50))
    dtMinor = db.Column(db.Integer)
    dtProfileImage = db.Column(db.String(255))
    fiAccount = db.Column(db.Integer, db.ForeignKey("tblAccount.idAccount"))
    account = relationship("Account")
    fiGenre = db.Column(db.Integer, db.ForeignKey("tblGenre.idGenre"))
    genre = relationship("Genre")
    def __repr__(self):
        return '<View %r>' % self.idProfile