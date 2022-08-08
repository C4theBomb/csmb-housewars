from django.test import TestCase


class TrueIsTrue(TestCase):
    def test_true_is_true(self):
        self.assertTrue(True)

    def test_true_is_false(self):
        self.assertFalse(False)
