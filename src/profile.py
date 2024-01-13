from account import Account
from Genre import Genre
from View import View
from typing import List, Type
from Classification import Classification
from imageType_enum import ImageType

class Profile:
    _user = Account
    _name = ""
    _picture = []
    _max_pictures = 4  
    _Language = ""
    _toWatchList = []
    _selectedGenre = List[Type[Genre]]
    _viewList = List[Type[View]]
    _language = ""
    _classification = List[Type[Classification]]

    def __init__(self, user: Account, name: str = "", picture: List[str] = None,
                 max_pictures: int = 4, language: str = "", to_watch_list: List[str] = None,
                 selected_genre: List[Genre] = None, view_list: List[View] = None,
                 classification: List[Classification] = None):

        self._user = user
        self._name = name
        self._picture = picture or []
        self._max_pictures = max_pictures
        self._language = language
        self._to_watch_list = to_watch_list or []
        self._selected_genre = selected_genre or []
        self._view_list = view_list or []
        self._classification = classification or []

    # Getters
    def get_user(self):
        return self._user

    def get_name(self):
        return self._name

    def get_picture(self):
        return self._picture

    def get_max_pictures(self):
        return self._max_pictures

    def get_language(self):
        return self._language

    def get_to_watch_list(self):
        return self._to_watch_list

    def get_selected_genre(self):
        return self._selected_genre

    def get_view_list(self):
        return self._view_list

    def get_classification(self):
        return self._classification

    # Setters
    def set_user(self, user: Type[Account]):
        self._user = user

    def set_name(self, name: str):
        self._name = name

    def set_picture(self, picture: List[str]):
        if picture is not None:
            for img in picture:
                if not isinstance(img, ImageType):
                    raise ValueError(f"Invalid image type: {img}")
            if len(picture) > self._max_pictures:
                raise ValueError(f"Number of images exceeds the maximum allowed ({self._max_pictures})")
        self._picture = picture or []


    def set_max_pictures(self, max_pictures: int):
        self._max_pictures = max_pictures

    def set_language(self, language: str):
        self._language = language

    def set_to_watch_list(self, to_watch_list: List[str]):
        self._to_watch_list = to_watch_list or []

    def set_selected_genre(self, selected_genre: List[Type[Genre]]):
        self._selected_genre = selected_genre or []

    def set_view_list(self, view_list: List[Type[View]]):
        self._view_list = view_list or []

    def set_classification(self, classification: List[Type[Classification]]):
        self._classification = classification or []
    @classmethod
    def get_instances(cls):
        return cls._instances
