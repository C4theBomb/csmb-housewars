from django.test import TestCase

from housewars.utils import get_random_string


class GetRandomStringTest(TestCase):
    def test_string_of_length_8(self):
        string = get_random_string(8)
        self.assertEqual(len(string), 8)

    def test_string_of_length_6(self):
        string = get_random_string(6)
        self.assertEqual(len(string), 6)
