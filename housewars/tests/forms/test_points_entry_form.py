from django.test import TestCase

from housewars.forms import PointsEntryForm
from housewars.models import Activity, House, Award


class PointsEntryFormTest(TestCase):
    def setUp(self):
        self.house = House.objects.create(name='Hawk')
        self.activity = Activity.objects.create(name='Dodgeball', time=30)
        self.activity2 = Activity.objects.create(name='Dodgeball', time=30)
        self.award = Award.objects.create(name='1st', activity=self.activity)

    def test_valid_time(self):
        form = PointsEntryForm(data={
            'house': self.house.id,
            'activity': self.activity.id,
            'award': self.award.id
        })

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = PointsEntryForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
