from app.extensions import db
from sqlalchemy.orm import relationship


class WatchList(db.Model):
    __tablename__ = 'tblWatchList'
    idWatchList = db.Column(db.Integer, primary_key=True)
    fiMovie = db.Column(db.Integer, db.ForeignKey("tblMovie.idMovie"))
    movie = relationship("Movie")
    fiProfile = db.Column(db.Integer, db.ForeignKey("tblProfile.idProfile"))
    profile = relationship("Profile")
