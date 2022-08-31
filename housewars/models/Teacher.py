from django.db import models
from . import House, Activity


class Teacher(models.Model):
    GradeChoices = (
        (9, '9th/Freshman'),
        (10, '10th/Sophomore'),
        (11, '11th/Junior'),
        (12, '12th/Senior'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    house = models.ForeignKey(
        House, related_name='teacher', default=None, blank=True, null=True, on_delete=models.SET_NULL)
    grade = models.IntegerField(choices=GradeChoices)
    activity = models.OneToOneField(
        Activity, related_name='teacher', default=None, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
