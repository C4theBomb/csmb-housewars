from django.test import TestCase

from housewars.forms import FacilitatorForm
from housewars.models import Activity


class FacilitatorFormTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(name='Dodgeball', time=30)

    def test_valid_input(self):
        form = FacilitatorForm(data={
            'first_name': 'Test',
            'last_name': 'User',
            'activity': self.activity.id
        })

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = FacilitatorForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
