from django.test import TestCase, Client
from django.urls import reverse

from housewars.models import Activity, House, Teacher, UserEntry


class UserEntryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.house = House.objects.create(name='Hawk', points=30)
        self.activity = Activity.objects.create(name='Dodgeball', time=30)
        self.entry = UserEntry.objects.create(
            first_name='Test', last_name='User', email='test.user@slps.org', grade=9, house=self.house, activity1=self.activity, activity2=self.activity)
        self.teacher = Teacher.objects.create(
            first_name='Test', last_name='Teacher', grade=9, house=self.house)

    def test_mentor(self):
        self.assertEquals(self.entry.mentor, self.teacher)
