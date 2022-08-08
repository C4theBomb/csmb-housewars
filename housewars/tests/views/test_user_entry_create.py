from django.test import TestCase
from django.urls import reverse

from ..models import Activity, House


class UserEntryCreateViewTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('housewars:signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('housewars:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'housewars/entry_form.html')
