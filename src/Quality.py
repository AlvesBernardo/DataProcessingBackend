#from flask import Flask

class Quality:
    description = ""
    price = float

    def __init__(self, description, price):
        self.description = description
        self.price = price
        
    #getters
    def get_description(self): 
        return self.description

    def get_price(self):
        return self.price

    #setters

    def set_description(self, description):
        self.description = description

    def set_price(self, price):
        self.price = price