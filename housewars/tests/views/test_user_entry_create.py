import enum
from django.test import TestCase, Client
from django.urls import reverse

from housewars.models import Activity, House


class UserEntryCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('housewars:signup')
        self.house = House.objects.create(name='Hawk')
        self.activity = Activity.objects.create(
            name='Dodgeball', time=30, default_quota=5)
        self.full_activity = Activity.objects.create(
            name='Dodgeball', time=30)

    def test_POST(self):
        user_info_form = {
            'user-first_name': 'Test',
            'user-last_name': 'User',
            'user-email': 'asdfasdf@slps.org',
            'user-grade': 9,
            'user-house': self.house.id,
            'entry_create_view-current_step': 'user'
        }

        activity_form = {
            'activity-activity1': self.activity.id,
            'activity-activity2': self.activity.id,
            'entry_create_view-current_step': 'activity'
        }

        steps_data = [user_info_form, activity_form]

        for data in steps_data:
            self.client.post(self.url, data)

        self.assertEquals(self.house.userentry_set.count(), 1)

    def test_full_activity_POST(self):
        user_info_form = {
            'user-first_name': 'Test',
            'user-last_name': 'User',
            'user-email': 'asdfasdf@slps.org',
            'user-grade': 9,
            'user-house': self.house.id,
            'entry_create_view-current_step': 'user'
        }

        activity_form = {
            'activity-activity1': self.full_activity.id,
            'activity-activity2': self.full_activity.id,
            'entry_create_view-current_step': 'activity'
        }

        steps_data = [user_info_form, activity_form]

        for data in steps_data:
            self.client.post(self.url, data)

        self.assertEquals(self.house.userentry_set.count(), 0)
