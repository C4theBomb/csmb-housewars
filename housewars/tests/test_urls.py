from django.test import TestCase
from django.urls import reverse, resolve

from housewars.views import EntryCreateView, PointsEntryCreateView


class TestUrls(TestCase):
    def test_entry_create_is_resolved(self):
        url = reverse('housewars:signup')
        self.assertEquals(resolve(url).func.view_class, EntryCreateView)

    def test_points_entry_create_is_resolved(self):
        url = reverse('housewars:add_points')
        self.assertEquals(resolve(url).func.view_class, PointsEntryCreateView)
