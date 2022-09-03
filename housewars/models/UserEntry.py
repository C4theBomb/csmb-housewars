from django.db import models
from django.core.exceptions import ValidationError

from . import House, Activity


class UserEntry(models.Model):
    class Meta:
        verbose_name_plural = "User Entries"

    GradeChoices = (
        (9, '9th/Freshman'),
        (10, '10th/Sophomore'),
        (11, '11th/Junior'),
        (12, '12th/Senior'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    grade = models.IntegerField(choices=GradeChoices)
    house = models.ForeignKey(
        House, on_delete=models.CASCADE)
    activity1 = models.ForeignKey(
        Activity, related_name='activity1', on_delete=models.CASCADE)
    activity2 = models.ForeignKey(
        Activity, related_name='activity2', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def mentor(self):
        return self.house.teacher.get(grade=self.grade)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        # Check to verify that there are 60 minutes of activities
        if self.activity2 and self.activity1.time + self.activity2.time != 60:
            raise ValidationError(
                "Please pick activities adding up to one hour.")
        elif not self.activity2 and self.activity1.time != 60:
            raise ValidationError(
                "Please pick activities adding up to one hour.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
