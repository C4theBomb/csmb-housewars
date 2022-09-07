from django.db import models
from . import Activity


class Facilitator(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
