from django.db import models
from django.forms import ValidationError
from django.db.models import F

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
    session1_signups = models.IntegerField(default=0)
    session2_signups = models.IntegerField(default=0)
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
        if self.activity2:
            if self.activity1.time + self.activity2.time != 60:
                raise ValidationError(
                    "Please pick activities adding up to one hour.")
            else:
                super().clean()
        else:
            if self.activity1.time != 60:
                raise ValidationError(
                    "Please pick activities adding up to one hour.")
            else:
                super().clean()

    def save(self, *args, **kwargs):
        print(self.activity1)
        if (self.activity1):
            self.activity1.session1_signups += 1
            self.activity1.save()
        if (self.activity2):
            self.activity2.session2_signups += 1
            self.activity2.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
