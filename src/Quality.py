from QualityTypeEnum import QualityType
class Quality:
    _instances = []
    _max_instances = 3

    def __init__(self, description : QualityType, price : float):
        if len(Quality._instances) >= Quality._max_instances:
            raise ValueError("Only three instances of Quality are allowed.")
        self.__description = description
        self.__price = price
        Quality._instances.append(self)

    # getters
    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    # setters
    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = price

    @classmethod
    def get_instances(cls):
        return cls._instances
