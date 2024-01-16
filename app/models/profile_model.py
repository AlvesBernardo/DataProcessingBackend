from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profile(db.Model) : 
    __tablename__ = 'tblProfile'  # Specify the table name
    idProfile = db.Column(db.Integer, primary_key=True)
    dtName = db.Column(db.String(50))
    dtMinor = db.Column(db.Integer)
    dtProfileImage = db.Column(db.String(255))
    fiAccount = db.Column(db.Integer, db.ForeignKey("[dbo].tblAccount.idAccount"))
    fiGenre = db.Column(db.Integer, db.ForeignKey("[dbo].tblGenre.idGenre"))

    def __repr__(self):
        return '<View %r>' % self.idProfile