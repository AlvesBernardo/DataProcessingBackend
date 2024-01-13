from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profile(db.Model) : 
    idUser = db.Column(db.Integer, primary_key=True)
    dtName = db.Column(db.String)
    dtPicture = db.Column(db.String)
    dtIsMinor = db.Column(db.Boolean)
    dtLanguage = db.Column(db.String)
    fiAccount = db.Column(db.Integer, db.ForeignKey("account.idAccount"))
    fiGenre = db.Column(db.Integer, db.ForeignKey("genre.idGenre"))
    