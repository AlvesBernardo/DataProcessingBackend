import unittest
import sys
from src.Quality import Quality

sys.path.append("..")


class TestQualityClass(unittest.TestCase):

    def test_initialization(self):
        quality = Quality("HD", 10.99)
        self.assertEqual(quality.get_description(), "HD")
        self.assertEqual(quality.get_price(), 10.99)

    def test_setters(self):
        quality = Quality("UHD", 13.99)
        quality.set_description("SD")
        quality.set_price(7.99)
        self.assertEqual(quality.get_description(), "SD")
        self.assertEqual(quality.get_price(), 7.99)


if __name__ == '__main__':
    unittest.main()
