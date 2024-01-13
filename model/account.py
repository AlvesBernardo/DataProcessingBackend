from . import db
from enum import Enum

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    isAccountBlocked = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(50), nullable=False)
    subscription = db.Column(db.String(50))
    isAccountActivated = db.Column(db.Boolean, default=False)
    profiles = db.relationship('Profile', backref='account', lazy=True)

    def User(self, email, password, language, subscription=None):
        self.email = email
        self.password = password
        self.language = language
        self.subscription = subscription 
        
    def getId(self):
        return self.id
        
    def setId(self, id):
        self.id = id
        
    def getEmail(self):
        return self.email
        
    def setEmail(self, email):
        self.email = email
        
    def getPassword(self):
        return self.password
        
    def resetPassword(self, password):
        self.password = password
        
    def isAccountBlocked(self):
        return self.isAccountBlocked

    def setAccountBlocked(self, isAccountBlocked):
        self.isAccountBlocked = isAccountBlocked
        
    def isAdmin(self):
        return self.isAdmin
    
    def setAdmin(self, isAdmin):
        self.isAdmin = isAdmin
    
    def getLanguage(self):
        return self.language
    
    def setLanguage(self, language):
        self.language = language
    
    def getSubscription(self):
        return self.subscription
    
    def setSubscription(self, subscription):
        self.subscription = subscription
    
    def getIsAccountActivated(self):
        return self.isAccountActivated    
    
    def setIsAccountActivated(self, isAccountActivated):
        self.isAccountActivated = isAccountActivated
        
    def getProfiles(self):
        return self.profiles
    
    def setProfiles(self, profiles):
        self.profiles = profiles
        
    # def getInviteCode(self):
    
    