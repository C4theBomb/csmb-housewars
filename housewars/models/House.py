from django.db import models


class House(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
