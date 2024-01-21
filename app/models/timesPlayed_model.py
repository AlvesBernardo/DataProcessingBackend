from app.extensions import db
from sqlalchemy.orm import relationship
from .subtitle_model import Subtitle
from .movie_model import Movie
from .profile_model import Profile
class Code(db.Model) :
    __tablename__ = 'tblTimesPlayed'  # Specify the table name
    idTimesPlayed = db.Column (db.Integer,primary_key = True)
    dtPlayCount = db.Column(db.Integer)
    fiMovie = db.Column(db.Integer, db.ForeignKey("tblMovie.idMovie"))
    movie = relationship("Movie")