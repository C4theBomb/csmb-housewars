from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class House(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)

    @property
    def current_points(self):
        return self.pointsentry_set.aggregate(sum=Coalesce(Sum('award__points'), 0)).get('sum')

    @property
    def total_points(self):
        return self.current_points + self.points

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
