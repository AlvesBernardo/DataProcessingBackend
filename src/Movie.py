from datetime import date
from Language import Language
from Genre import Genre
from Classification import Classification
class Movie() : 
    def __init__(self, title : str, year : date, amountOfEpisodes : int, amountOfSeasons : int, length : float, quality, classification : Classification,language : Language,subtitles : list,genre : Genre) : 
        self.__title = title
        self.__year = year
        self.__amountOfEpisodes = amountOfEpisodes
        self.__amountOfSeasons = amountOfSeasons
        self.__length = length
        self.__quality = quality
        self.__classification = classification
        self.__language = language
        self.__subtitles = subtitles
        self.__genre = genre
    def getTitle(self) :
        return self.__title
    def setTitle(self, title : str) :
        self.__title = title
    def getYear(self) :
        return self.__year
    def setYear(self, year : date) :
        self.__year = year
    def getAmountOfEpisodes(self) :
        self.__amountOfEpisodes
    def setAmountOfEpisodes(self, amountOfEpisodes : int) :
        self.__amountOfEpisodes = amountOfEpisodes
    def getAmountOfSeasons(self) :
        return self.__amountOfSeasons
    def setAmountOfSeasons(self, amountOfSeasons : int) :
        self.__amountOfSeasons = amountOfSeasons
    def getLength(self) :
        return self.__length
    def setLength(self, length : float) :
        self.__length = length
    def getQuality(self) :
        return self.__quality
    def setQuality(self, quality) :
        self.__quality = quality
    def getClassification(self) :
        return self.__classification
    def setClassification(self, classification : Classification) :
        self.__classification = classification
    def getLanguage(self) :
        return self.__language
    def setLanguage(self, language : Language) :
        self.__language = language
    def getSubtitles(self) :
        return self.__subtitles
    def setSubtitles(self, subtitles : list) :
        self.__subtitles = subtitles
    def getGenre(self) :
        return self.__genre
    def setGenre(self, genre : Genre) :
        self.__genre = genre

    

        