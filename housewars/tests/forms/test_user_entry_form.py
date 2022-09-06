from django.test import TestCase

from housewars.forms import UserEntryForm
from housewars.models import House


class UserEntryFormTest(TestCase):
    def setUp(self):
        self.house = House.objects.create(name='Hawk', points=30)

    def test_valid(self):
        form = UserEntryForm(data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@slps.org',
            'grade': 9,
            'house': self.house.id
        })

        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = UserEntryForm(data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@gmail.com',
            'grade': 9,
            'house': self.house.id
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_no_data(self):
        form = UserEntryForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)
