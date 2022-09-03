from django.db import models


class Award(models.Model):
    activity = models.ForeignKey(
        'Activity', on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.activity})"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
