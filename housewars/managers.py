from django.db.models import Manager, F


class EntryManager(Manager):
    def filterActivity1(self, act):
        return self.filter(activity1=act)

    def filterActivity2(self, act):
        return self.filter(activity2=act)


class HawkEntryManager(EntryManager):
    def get_queryset(self):
        return super().get_queryset().filter(house='HAWK')


class EagleEntryManager(EntryManager):
    def get_queryset(self):
        return super().get_queryset().filter(house='EAGLE')


class GreatGreyEntryManager(EntryManager):
    def get_queryset(self):
        return super().get_queryset().filter(house='GREATGREY')


class SnowyEntryManager(EntryManager):
    def get_queryset(self):
        return super().get_queryset().filter(house='SNOWY')
