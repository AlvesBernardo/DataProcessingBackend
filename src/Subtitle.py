from Movie import Movie
from Language import Language

class Subtitle() :
    def __init__(self , movie : Movie , language : Language , filePath : str) :
        self.__language = language
        self.__movie = movie
    def getLanguage(self) :
        return self.__language
    def setLanguage(self, language) :
        self.__language = language
    def getMovie(self) :
        return self.__movie
    def setMovie(self, movie : Movie) :
        self.__movie = movie
    def getFilePath(self) :
        return self.__filePath
    def setFilePath(self, filePath : str) :
        self.__filePath = filePath