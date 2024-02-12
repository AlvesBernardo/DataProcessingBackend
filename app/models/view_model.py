from app.extensions import db
from sqlalchemy.orm import relationship
class View(db.Model) : 
    __tablename__ = 'tblView'  # Specify the table name
    idView = db.Column(db.Integer, primary_key=True)
    fiSubtitle = db.Column(db.Integer, db.ForeignKey("tblSubtitle.idSubtitle"))
    subtitle = relationship("Subtitle")
    fiMovie = db.Column(db.Integer, db.ForeignKey("tblMovie.idMovie"))
    movie = relationship("Movie")
    fiProfile = db.Column(db.Integer, db.ForeignKey("tblProfile.idProfile"))
    profile = relationship("Profile")
    dtMovieTime = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return '<View %r>' % self.idView