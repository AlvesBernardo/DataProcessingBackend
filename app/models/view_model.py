from app.extensions import db
class View(db.Model) : 
    idView = db.Column(db.Integer, primary_key=True)
    dtMovieTime = db.Column(db.Interval, nullable=False )
    fiSubtitle = db.Column(db.Integer, db.ForeignKey("subtitle.idSubtitle"))
    fiMovie = db.Column(db.Integer, db.ForeignKey("movie.idMovie"))
    
    def __repr__(self):
        return '<View %r>' % self.idView