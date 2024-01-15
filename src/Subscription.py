import datetime
from Quality import Quality
import QualityTypeEnum


class Subscription:
    _payment = ""
    _dateOfSignUp = None
    _typeOfSubscription = ""
    _inviteDiscount = False
    _sevenDaysFreeTrail = False
    _price = float

    def __init__(
        self, payment : str, dateOfSignUp : datetime.date, typeOfSubscription : QualityTypeEnum.QualityType,
            inviteDiscount : bool, sevenDaysFreeTrail : bool, price : float
        ):

         self._payment = payment
         self.set_dateOfSignUp(dateOfSignUp)          
         self._typeOfSubscription = typeOfSubscription
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


    def get_sevenDaysFreeTrailStatus(self):
        return self._sevenDaysFreeTrail

    def get_price(self):
        return self._price  # Update this line



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
            self._price += self._typeOfSubscription["price"]