from src.Subscription import Subscription
import unittest

class TestSubscriptionClass(unittest.TestCase):
    def test_initialization(self):
        subscription = Subscription(
            "Paypal",
            datetime.datetime(2021, 1, 1),
            HDQuality,
            False,
            False,
            10.99,
        )
        self.assertEqual(subscription.get_payment(), "Paypal")
        self.assertEqual(subscription.get_dateOfSignUp(), datetime.datetime(2021, 1, 1))
        self.assertEqual(subscription.get_typeOfSubscription(), HDQuality)
        self.assertEqual(subscription.get_inviteDiscountStatus(), False)
        self.assertEqual(subscription.get_sevenDaysFreeTrailStatus(), False)
        self.assertEqual(subscription.get_price(), 10.99)