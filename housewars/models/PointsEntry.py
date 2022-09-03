from django.db.models import Model, ForeignKey, CharField, CASCADE, Q, F
from smart_selects.db_fields import ChainedForeignKey
from . import Award


class PointsEntry(Model):
    class Meta:
        verbose_name_plural = "Point Entries"

    activity = ForeignKey(
        'Activity', related_name='Activity', on_delete=CASCADE)
    house = ForeignKey('House', on_delete=CASCADE)
    award = ChainedForeignKey(Award, chained_field="activity",
                              chained_model_field="activity", on_delete=CASCADE)
    password = CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.activity}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
