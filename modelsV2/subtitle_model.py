from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subtitle(db.Model) : 
    idSubtitle = db.Column(db.Integer, primary_key=True)
    dtLanguage = db.Column(db.String)
    dtSubtitle = db.Column(db.String)
    fiMovie = db.Column(db.Integer, db.ForeignKey("movie.idMovie"))
    
    def __repr__(self):
        return '<Subtitle %r>' % self.idSubtitle