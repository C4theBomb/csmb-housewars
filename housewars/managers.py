from django.db.models import Manager


class EntryManager(Manager):
    def filterActivity1(self, act):
        return self.filter(activity1=act)

    def filterActivity2(self, act):
        return self.filter(activity2=act)


class HawkEntryManager(EntryManager):
    def get_queryset(self):
        return super().get_queryset().filter(house__name='Hawk')


class EagleEntryManager(EntryManager):
    def get_queryset(self):
        return super().get_queryset().filter(house__name='Eagle')


class GreatGreyEntryManager(EntryManager):
    def get_queryset(self):
        return super().get_queryset().filter(house__name='Great Grey')


class SnowyEntryManager(EntryManager):
    def get_queryset(self):
        return super().get_queryset().filter(house__name='Snowy')
