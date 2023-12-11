import datetime
from .Quality import Quality



class Subscription:
    _payment = ""
    _dateOfSignUp = None
    _typeOfSubscription = ""
    _inviteDiscount = False
    _sevenDaysFreeTrail = False
    _price = float

    def __init__(
        self, payment, dateOfSignUp, typeOfSubscription, inviteDiscount, sevenDaysFreeTrail, price
        ):
         if not isinstance(typeOfSubscription, Quality):
            raise ValueError("typeOfSubscription must be an instance of Quality or its subclass.")
         self._payment = payment
         self.set_dateOfSignUp(dateOfSignUp)          
         self.type = typeOfSubscription
         self.inviteDiscount = inviteDiscount
         self.sevenDaysFreeTrail = True
         self.price = price


    # getters
    def get_payment(self):
        return self._payment


    def get_dateOfSignUp(self):
        return self._dateOfSignUp


    def get_typeOfSubscription(self):
        return self._typeOfSubscription


    def get_inviteDiscountStatus(self):
        return self._inviteDiscount


    def get_secenDaysFreeTrailStatus(self):
        return self._sevenDaysFreeTrail


    def get_price(self):
        return self._price


    # setter method


    def set_inviteDiscountStatus(self, inviteDiscount):
        self._inviteDiscount = inviteDiscount


    def set_sevenDaysFreeTrailStatus(self, sevenDaysFreeTrail):
        self._sevenDaysFreeTrail = sevenDaysFreeTrail


    def set_price(self, price):
        self._price = price


    def set_dateOfSignUp(self, dateOfSignUp):
        if isinstance(dateOfSignUp, datetime.date):
            self._dateOfSignUp = dateOfSignUp
        else:
            raise ValueError("dateOfSignUp must be an instance of datetime.date.")

    def set_typeOfSubscription(self, typeOfSubscription):
        self._typeOfSubscription = typeOfSubscription


    def set_payment(self, payment):
        self._payment = payment


    def set_price(self, price):
        self._price = price


    def is_within_seven_days(self):
        time_difference = datetime.datetime.now() - self.dateOfSignUp

        return 0 <= time_difference.days < 7


    def freeTrail(self):
        self.sevenDaysFreeTrail = self.is_within_seven_days()


    def calculate_price(self):
            if isinstance(self.typeOfSubscription, ShQuality):
                self._price = 7.99
            elif isinstance(self.typeOfSubscription, HDQuality):
                self._price = 10.99
            elif isinstance(self.typeOfSubscription, UHDQuality):
                self._price = 13.99