from django.test import TestCase, Client
from django.urls import reverse

from housewars.models import Activity, House, Award


class PointsEntryCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('housewars:add_points')
        self.house = House.objects.create(name='Hawk')
        self.activity = Activity.objects.create(name='Dodgeball', time=30)
        self.award = Award.objects.create(activity=self.activity, name='1st')

    def test_GET(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'housewars/pointsentry_form.html')

    def test_POST(self):
        response = self.client.post(self.url, {
            'house': self.house.id,
            'activity': self.activity.id,
            'award': self.award.id
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.house.pointsentry_set.count(), 1)

    def test_failed_POST(self):
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.house.pointsentry_set.count(), 0)
