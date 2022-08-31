from django.db import models
from . import House, Activity


class PointsEntry(models.Model):
    class Meta:
        verbose_name_plural = "Point Entries"

    name = models.CharField(max_length=100)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    password = models.CharField(
        max_length=15, default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
