from . import db
from .enums import ImageType

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.Enum(ImageType), nullable=False)
    is_minor = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(50), nullable=False)
    to_watch_list = db.relationship('Movie', secondary='profile_movie', backref='profiles', lazy='dynamic')
    selected_genres = db.relationship('SelectedGenre', backref='profile', lazy=True)
    view_list = db.relationship('View', backref='profile', lazy=True)
    classification_preferences = db.relationship('Classification', backref='profile', lazy=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def Profile(self, user, name, picture, age, language):
        self.user = user
        self.name = name
        self.picture = picture
        self.is_minor = age < 18
        self.language = language
        
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
    def getPicture(self):
        return self.picture
    
    def setPicture(self, picture):
        self.picture = picture
        
    def getIs_minor(self):
        return self.is_minor
    
    def setIs_minor(self, is_minor):
        self.is_minor = is_minor
        
    def getLanguage(self):
        return self.language
    
    def setLanguage(self, language):
        self.language = language
        
    def get_to_watch_list(self):
        return self.to_watch_list
    
    def set_to_watch_list(self, to_watch_list):
        self.to_watch_list = to_watch_list
        
    def get_selected_genres(self):
        return self.selected_genres
    
    def set_selected_genres(self, selected_genres):
        self.selected_genres = selected_genres
        
    def get_view_list(self):
        return self.view_list
    
    def set_view_list(self, view_list):
        self.view_list = view_list
        
    def get_classification_preferences(self):
        return self.classification_preferences
    
    def set_classification_preferences(self, classification_preferences):
        self.classification_preferences = classification_preferences
        
    def get_account_id(self):
        return self.account_id
    
    def set_account_id(self, account_id):
        self.account_id = account_id
    