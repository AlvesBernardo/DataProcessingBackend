from extensions import db
class Subtitle(db.Model) : 
    __tablename__ = 'tblSubtitle'  # Specify the table name
    idSubtitle = db.Column(db.Integer, primary_key=True)
    fiMovie = db.Column(db.Integer, db.ForeignKey("[dbo].tblMovie.idMovie"))
    fiLanguage = db.Column(db.Integer, db.ForeignKey("[dbo].tblLanguage.idLanguage"))

    def __repr__(self):
        return '<Subtitle %r>' % self.idSubtitle