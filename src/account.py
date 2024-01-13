from .Subscription import Subscription
from typing import List, Type
from .profile import Profile

class Account:
    _email = ""
    _password = ""
    _profileList = List[Type[Profile]]
    _max_profiles = 4  
    _typeOfSubscription = Subscription
    _isAccountBlocked = False
    _isAdmin = False
    _language = ""



    def __init__(self, email="", password="", profile_list=None, subscription=None,
                 is_account_blocked=False, is_admin=False, language=""):
        self._email = email
        self._password = password
        self._profile_list = []
        self._type_of_subscription = subscription or Subscription()
        self._is_account_blocked = is_account_blocked
        self._is_admin = is_admin
        self._language = language

    # Getters
    def get_email(self):
        return self._email

    def get_password(self):
        return self._password

    def get_profile_list(self):
        return self._profile_list

    def get_max_profiles(self):
        return self._max_profiles

    def get_type_of_subscription(self):
        return self._type_of_subscription

    def is_account_blocked(self):
        return self._is_account_blocked

    def is_admin(self):
        return self._is_admin

    def get_language(self):
        return self._language

    # Setters
    def set_email(self, email):
        self._email = email

    def set_password(self, password):
        self._password = password

    def set_profile_list(self, profile_list):
        self._profile_list = profile_list

    def set_max_profiles(self, max_profiles):
        self._max_profiles = max_profiles

    def set_type_of_subscription(self, subscription):
        self._type_of_subscription = subscription

    def set_account_blocked(self, is_account_blocked):
        self._is_account_blocked = is_account_blocked

    def set_admin(self, is_admin):
        self._is_admin = is_admin

    def set_language(self, language):
        self._language = language

    @classmethod
    def get_instances(cls):
        return cls._instances
