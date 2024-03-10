import sys

sys.path.append("..")
import datetime
import unittest
from src.View import View
from src.Subtitle import Subtitle
from src.Movie import Movie


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.stoppedTime = datetime.datetime.now().timestamp()
        self.subtitle = Subtitle("English", "Subtitle content")
        self.movie = Movie("Movie Title", "Movie Description")
        self.view = View(self.stoppedTime, self.subtitle, self.movie)


    def test_getStoppedTime(self):
        self.assertEqual(self.view.getStoppedTime(), self.stoppedTime)


    def test_setStoppedTime(self):
        newStoppedTime = datetime.datetime.now().timestamp()
        self.view.setStoppedTime(newStoppedTime)
        self.assertEqual(self.view.getStoppedTime(), newStoppedTime)


    def test_getSubtitle(self):
        self.assertEqual(self.view.getSubtitle(), self.subtitle)


    def test_setSubtitle(self):
        newSubtitle = Subtitle("Spanish", "Subtitle content")
        self.view.setSubtitle(newSubtitle)
        self.assertEqual(self.view.getSubtitle(), newSubtitle)


    def test_getMovie(self):
        self.assertEqual(self.view.getMovie(), self.movie)


    def test_setMovie(self):
        newMovie = Movie("New Movie Title", "New Movie Description")
        self.view.setMovie(newMovie)
        self.assertEqual(self.view.getMovie(), newMovie)


    def test_setSubtitleOff(self):
        self.view.setSubtitleOff()
        self.assertIsNone(self.view.getSubtitle())


    def test_setSubtitleOn(self):
        newSubtitle = Subtitle("French", "Subtitle content")
        self.view.setSubtitleOn(newSubtitle)
        self.assertEqual(self.view.getSubtitle(), newSubtitle)


if __name__ == '__main__':
    unittest.main()
