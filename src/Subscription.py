import datetime
from Quality import *


class Subscription:
    _payment = ""
    _dateOfSignUp = datetime
    _typeOfSubscription = Quality()
    _inviteDiscount = False
    _sevenDaysFreeTrail = False
    _price = float

    def __init__(
        self, payment, dateOfSignUp, Quality, inviteDiscount, sevenDaysFreeTrail, price
    ):
        self.payment = payment
        self.dateOfSignUp = dateOfSignUp
        self.type = Quality
        inviteDiscount = inviteDiscount
        self.sevenDaysFreeTrail = True
        self.price = price


# getters
def get_payment(self):
    return self.payment


def get_dateOfSignUp(self):
    return self.dateOfSignUp


def get_typeOfSubscription(self):
    return self.typeOfSubscription


def get_inviteDiscountStatus(self):
    return self.inviteDiscount


def get_secenDaysFreeTrailStatus(self):
    return self.sevenDaysFreeTrail


def get_price(self):
    return self.price


# setter method


def set_inviteDiscountStatus(self, inviteDiscount):
    self.inviteDiscount = inviteDiscount


def set_sevenDaysFreeTrailStatus(self, sevenDaysFreeTrail):
    self.sevenDaysFreeTrail = sevenDaysFreeTrail


def set_price(self, price):
    self.price = price


def set_dateOfSignUp(self, dateOfSignUp):
    self.dateOfSignUp = dateOfSignUp


def set_typeOfSubscription(self, typeOfSubscription):
    self.typeOfSubscription = typeOfSubscription


def set_payment(self, payment):
    self.payment = payment


def set_price(self, price):
    self.price = price


def is_within_seven_days(self):
    time_difference = datetime.datetime.now() - self.dateOfSignUp

    return 0 <= time_difference.days < 7


def freeTrail(self):
    self.sevenDaysFreeTrail = self.is_within_seven_days()


def calculate_price(self):
        if isinstance(self.typeOfSubscription, ShQuality):
            self.price = 7.99
        elif isinstance(self.typeOfSubscription, HDQuality):
            self.price = 10.99
        elif isinstance(self.typeOfSubscription, UHDQuality):
            self.price = 13.99