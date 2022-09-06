from django.test import TestCase

from housewars.models import Activity, House, Award, PointsEntry


class HouseModelTest(TestCase):
    def setUp(self):
        self.house = House.objects.create(name='Hawk', points=30)
        self.activity = Activity.objects.create(name='Dodgeball', time=30)
        self.award = Award.objects.create(
            activity=self.activity, name='1st', points=30)

    def test_current_points(self):
        PointsEntry.objects.create(
            activity=self.activity, house=self.house, award=self.award)

        self.assertEquals(self.house.current_points, 30)

    def test_total_points(self):
        PointsEntry.objects.create(
            activity=self.activity, house=self.house, award=self.award)

        self.assertEquals(self.house.total_points, 60)
