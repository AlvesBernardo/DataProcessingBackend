from ..extensions import db

class View(db.Model) : 
    __tablename__ = 'tblView'  # Specify the table name
    idView = db.Column(db.Integer, primary_key=True)
    dtMovieTime = db.Column(db.DateTime, nullable=False )
    fiSubtitle = db.Column(db.Integer, db.ForeignKey("[dbo].tblSubtitle.idSubtitle"))
    fiMovie = db.Column(db.Integer, db.ForeignKey("[dbo].tblMovie.idMovie"))
    fiProfile = db.Column(db.Integer, db.ForeignKey("[dbo].tblProfile.idProfile"))

    def __repr__(self):
        return '<View %r>' % self.idView