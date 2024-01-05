from datetime import datetime
from Subtitle import Subtitle
from Movie import Movie
class View() :
    def __init__(self,stoppedTime : datetime.timestamp , subtitle : Subtitle , movie : Movie ) :
        self.__stoppedTime = stoppedTime
        self.__subtitle = subtitle
        self.__movie = movie
    def getStoppedTime(self) :
        return self.__stoppedTime
    def setStoppedTime(self, stoppedTime : datetime.timestamp) :
        self.__stoppedTime = stoppedTime
    def getSubtitle(self) : 
        return self.__subtitle
    def setSubtitle(self, subtitle : Subtitle) :
        self.__subtitle = subtitle
    def getMovie(self) :
        return self.__movie
    def setMovie(self, movie : Movie) :
        self.__movie = movie
    def setSubtitleOff() : 
        pass
    def setSubtitleOn() :
        pass