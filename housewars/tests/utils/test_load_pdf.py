from django.test import TestCase

import io

from housewars.utils import load_pdf
from housewars.models import House


class UnpackValuesTest(TestCase):
    def setUp(self):
        House.objects.create(name="Hawk")
        House.objects.create(name="Snowy")

        self.test_queryset = House.objects.all()

    def test_matching_object_instance(self):
        headers = [field.name for field in House._meta.fields]

        self.assertIsInstance(
            load_pdf(self.test_queryset, headers), io.BytesIO)
