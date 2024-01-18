from app.extensions import db
from sqlalchemy.orm import relationship
from .subtitle_model import Subtitle
from .movie_model import Movie
from .profile_model import Profile
class View(db.Model) : 
    __tablename__ = 'tblView'  # Specify the table name
    idView = db.Column(db.Integer, primary_key=True)
    dtMovieTime = db.Column(db.DateTime, nullable=False )
    fiSubtitle = db.Column(db.Integer, db.ForeignKey("tblSubtitle.idSubtitle"))
    subtitle = relationship("Subtitle")
    fiMovie = db.Column(db.Integer, db.ForeignKey("tblMovie.idMovie"))
    movie = relationship("Movie")
    fiProfile = db.Column(db.Integer, db.ForeignKey("tblProfile.idProfile"))
    profile = relationship("Profile")
    def __repr__(self):
        return '<View %r>' % self.idView