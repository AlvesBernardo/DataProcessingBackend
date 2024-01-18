from app.extensions import db
from sqlalchemy.orm import relationship
from .quality_model import Quality
from .genre_model import Genre
from .language_model import Language
from .classification_model import Classification
class Movie(db.Model) :
    __tablename__ = 'tblMovie'  # Specify the table name
    idMovie = db.Column(db.Integer, primary_key=True)
    dtTitle = db.Column(db.String(255))
    dtYear = db.Column(db.Date)
    dtAmountOfEp = db.Column(db.Integer)
    dtAmountOfSeasons = db.Column(db.Integer)
    dtLength = db.Column(db.Time)
    dtMinAge = db.Column(db.Integer)
    fiType = db.Column(db.Integer, db.ForeignKey("tblQuality.idType"))
    quality = relationship("Quality")
    fiLanguage = db.Column(db.Integer, db.ForeignKey("tblLanguage.idLanguage"))
    language = relationship("Language")
    fiClassification = db.Column(db.Integer,db.ForeignKey("tblClassification.idClassification"))
    classification = relationship("Classification")
    fiGenre = db.Column(db.Integer, db.ForeignKey("tblGenre.idGenre"))
    genre = relationship("Genre")
    def __repr__(self):
        return '<View %r>' % self.idMovie