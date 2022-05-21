from django.db import models
from .managers import HawkEntryManager, GreatGreyEntryManager, SnowyEntryManager, EagleEntryManager, EntryManager


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


class House(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class UserEntry(models.Model):
    class Meta:
        verbose_name_plural = "User Entries"

    objects = EntryManager()
    hawk = HawkEntryManager()
    great_grey = GreatGreyEntryManager()
    snowy = SnowyEntryManager()
    eagle = EagleEntryManager()

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
    house = models.ForeignKey(
        House, on_delete=models.CASCADE)
    activity1 = models.ForeignKey(
        Activity, related_name='activity1', on_delete=models.CASCADE)
    activity2 = models.ForeignKey(
        Activity, related_name='activity2', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PointsEntry(models.Model):
    class Meta:
        verbose_name_plural = "Point Entries"

    name = models.CharField(max_length=100)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    points = models.IntegerField()
    reason = models.TextField(blank=False)
