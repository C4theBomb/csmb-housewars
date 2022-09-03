from django.db import models


class Quota(models.Model):
    class Meta:
        unique_together = ('activity', 'house')

    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    house = models.ForeignKey('House', on_delete=models.CASCADE)
    quota = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.house}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
