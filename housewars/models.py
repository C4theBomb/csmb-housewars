from django.db import models
from django.forms import ValidationError

from .managers import Session1Activities, Session2Activities


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

    session1 = Session1Activities()
    session2 = Session2Activities()

    @property
    def session1_signups(self):
        return Entry.objects.filter(activity1=self).count()

    @property
    def session2_signups(self):
        return Entry.objects.filter(activity2=self).count()

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

    HouseChoices = (
        ('HAWK', 'Hawk'),
        ('GREATGREY', 'Great Grey'),
        ('EAGLE', 'Eagle'),
        ('SNOWY', 'Snowy')
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    grade = models.IntegerField(choices=GradeChoices)
    house = models.CharField(choices=HouseChoices, max_length=15)
    activity1 = models.ForeignKey(
        Activity, related_name='activity1', on_delete=models.CASCADE)
    activity2 = models.ForeignKey(
        Activity, related_name='activity2', on_delete=models.CASCADE, blank=True, null=True)

    def clean(self):
        if self.activity2 and self.activity1.time + self.activity2.time != 60:
            raise ValidationError(
                "Please pick activities adding up to one hour.")
        elif not self.activity2 and self.activity1.time != 60:
            raise ValidationError(
                "Please pick activities adding up to one hour.")
        else:
            super().clean()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
