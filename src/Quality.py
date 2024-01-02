#from flask import Flask

class Quality:
    _instances = []
    _max_instances = 3
    _description = ""
    _price = float

    def __init__(self, description, price):
        if len(Quality._instances) >= Quality._max_instances:
            raise ValueError("Only three instances of Quality are allowed.")
        self._description = description
        self._price = price
        
    #getters
    def get_description(self): 
        return self._description

    def get_price(self):
        return self._price

    #setters

    def set_description(self, description):
        self._description = description

    def set_price(self, price):
        self._price = price
    
    @classmethod
    def get_instances(cls):
        return cls._instances