from django.test import TestCase

from housewars.utils import unpack_values
from housewars.models import House


class UnpackValuesTest(TestCase):
    def setUp(self):
        House.objects.create(name="Hawk")
        House.objects.create(name="Snowy")

        self.test_queryset = House.objects.all()

    def test_valid_row_headers(self):
        """Correctly unpacks the headers into the first index"""
        values = unpack_values(self.test_queryset)
        self.assertEqual(
            values[0], [field.name for field in House._meta.fields])

    def test_complete_values(self):
        """Maintains the complete queryset and returns it"""
        values = unpack_values(self.test_queryset)
        queryset = list(self.test_queryset.values_list())
        for row in queryset:
            self.assertIn(list(row), values)
