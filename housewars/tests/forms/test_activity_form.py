from django.test import TestCase

from housewars.forms import ActivityForm
from housewars.models import Activity, House


class ActivityFormTest(TestCase):
    def setUp(self):
        self.activity30 = Activity.objects.create(name='Dodgeball', time=30)
        self.activity60 = Activity.objects.create(name='Dodgeball', time=60)

    def test_valid_time(self):
        form = ActivityForm(data={
            'activity1': self.activity30.id,
            'activity2': self.activity30.id,
        })

        self.assertTrue(form.is_valid())

    def test_invalid_time(self):
        form = ActivityForm(data={
            'activity1': self.activity60.id,
            'activity2': self.activity30.id,
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_no_data(self):
        form = ActivityForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
