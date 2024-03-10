import sys
import unittest
import datetime
from src.Subscription import Subscription
from src.Quality import Quality

sys.path.append("..")


class TestSubscriptionClass(unittest.TestCase):
    hd_quality = Quality("HD", 10.99)

    def test_initialization(self):
        subscription = Subscription(
            "Paypal",
            datetime.date(2022, 12, 25),
            self.hd_quality,
            False,
            False,
            10.99,
        )
        self.assertEqual(subscription.get_payment(), "Paypal")
        actual_date_of_signup = subscription.get_dateOfSignUp()
        expected_date_of_signup = datetime.date(2022, 12, 25)
        self.assertEqual(actual_date_of_signup, expected_date_of_signup, f"Actual: {actual_date_of_signup}")
        self.assertEqual(subscription.get_typeOfSubscription(), self.hd_quality)
        self.assertEqual(subscription.get_inviteDiscountStatus(), False)
        self.assertEqual(subscription.get_sevenDaysFreeTrailStatus(), False)
        self.assertEqual(subscription.get_price(), 10.99)


if __name__ == '__main__':
    unittest.main()
