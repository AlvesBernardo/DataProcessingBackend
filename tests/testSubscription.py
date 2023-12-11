import sys 
import unittest
sys.path.append("..")
import datetime
from src.Subscription import Subscription
from src.Quality import Quality

class TestSubscriptionClass(unittest.TestCase):
    hd_quality = Quality("HD", 10.99)
    def test_initialization(self):
        
        subscription = Subscription(
            "Paypal",
            datetime.date(2022, 12, 25), # Corrected initialization
            hd_quality,
            False,
            False,
            10.99,
        )
        self.assertEqual(subscription.get_payment(), "Paypal")
        actual_date_of_signup = subscription.get_dateOfSignUp()
        expected_date_of_signup = datetime.date(2022, 12, 25)  # Corrected date
        self.assertEqual(actual_date_of_signup, expected_date_of_signup, f"Actual: {actual_date_of_signup}")
        self.assertEqual(subscription.get_typeOfSubscription(), HDQuality)
        self.assertEqual(subscription.get_inviteDiscountStatus(), False)
        self.assertEqual(subscription.get_sevenDaysFreeTrailStatus(), False)
        self.assertEqual(subscription.get_price(), 10.99)

if __name__ == '__main__':  ##this will check if the script is being ran as teh main program
    unittest.main()
