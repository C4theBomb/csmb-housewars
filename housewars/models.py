from django.db import models
from django.forms import ValidationError

# Create your models here.


class Activity(models.Model):
    class Meta:
        verbose_name_plural = "Activities"

    TimeslotChoices = [
        (30, '30'),
        (60, '60')
    ]

    name = models.CharField(max_length=100)
    quota = models.IntegerField()
    time = models.IntegerField(choices=TimeslotChoices)

    def __str__(self):
        return f"{self.name} ({self.time})"


class Entry(models.Model):
    class Meta:
        verbose_name_plural = "Entries"

    GradeChoices = (
        (9, '9th/Freshman'),
        (10, '10th/Sophomore'),
        (11, '11th/Junior'),
        (12, '12th/Senior'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    grade = models.IntegerField(choices=GradeChoices)
    activity1 = models.ForeignKey(
        Activity, related_name='activity1', on_delete=models.CASCADE)
    activity2 = models.ForeignKey(
        Activity, related_name='activity2', on_delete=models.CASCADE)

    def clean(self):
        if self.activity1.time + self.activity2.time > 60:
            raise ValidationError(
                "Please only pick activities adding up to one hour.")
        else:
            super().clean()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
