from app.extensions import db
from sqlalchemy.orm import relationship
from .subtitle_model import Subtitle
from .movie_model import Movie
from .profile_model import Profile
class Code(db.Model) :
    __tablename__ = 'tblCode'  # Specify the table name
    idCode = db.Column (db.Integer,primary_key = True)
    dtCode = db.Column(db.Integer)
    fiAccount = db.Column(db.Integer, db.ForeignKey("tblAccount.idAccount"))
    account = relationship("Account")