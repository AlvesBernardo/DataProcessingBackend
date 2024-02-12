from app.extensions import db
from sqlalchemy.orm import relationship
class TimesPlayed(db.Model) :
    __tablename__ = 'tblTimesPlayed'  # Specify the table name
    idTimesPlayed = db.Column (db.Integer,primary_key = True)
    dtPlayCount = db.Column(db.Integer)
    fiMovie = db.Column(db.Integer, db.ForeignKey("tblMovie.idMovie"))
    movie = relationship("Movie")