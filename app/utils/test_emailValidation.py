import unittest
from utils.emailValidation import check

class EmailValidationTests(unittest.TestCase):
    def test_valid_email(self):
        email = "test@example.com"
        self.assertTrue(check(email))


    def test_invalid_email(self):
        email = "invalid_email"
        self.assertFalse(check(email))


    def test_invalid_email_format(self):
        email = "test@example"
        self.assertFalse(check(email))


    def test_invalid_email_domain(self):
        email = "test@example.123"
        self.assertFalse(check(email))


    def test_invalid_email_length(self):
        email = "a" * 256 + "@example.com"
        self.assertFalse(check(email))

if __name__ == '__main__':
    unittest.main()