from django.test import TestCase, Client
from django.urls import reverse

from housewars.models import Activity


class FacilitatorCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('housewars:facilitator')
        self.activity = Activity.objects.create(name='Dodgeball', time=30)

    def test_GET(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'housewars/general_form.html')

    def test_POST(self):
        response = self.client.post(self.url, {
            'first_name': 'Test',
            'last_name': 'User',
            'activity': self.activity.id
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.activity.facilitator_set.count(), 1)

    def test_failed_POST(self):
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.activity.facilitator_set.count(), 0)
