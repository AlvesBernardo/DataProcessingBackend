from app.extensions import db
class Movie(db.Model) :
    __tablename__ = 'tblMovie'  # Specify the table name
    idMovie = db.Column(db.Integer, primary_key=True)
    dtTitle = db.Column(db.String(255))
    dtYear = db.Column(db.Date)
    dtAmountOfEp = db.Column(db.Integer)
    dtAmountOfSeasons = db.Column(db.Integer)
    dtLength = db.Column(db.Time)
    dtMinAge = db.Column(db.Integer)
    fiType = db.Column(db.Integer, db.ForeignKey("[dbo].tblType.idType"))
    fiGenre = db.Column(db.Integer, db.ForeignKey("[dbo].tlbGenre.idGenre"))
    fiLanguage = db.Column(db.Integer, db.ForeignKey("[dbo].tblLanguage.idLanguage"))
    
    def __repr__(self):
        return '<View %r>' % self.idMovie