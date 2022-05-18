from django.contrib import admin
from django.db.models import Count
from .models import Activity, Entry


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Activity Information', {
         'fields': ['quota', 'time']}),
    ]

    list_display = ['name', 'time', 'quota', 'hawk_signups',
                    'great_grey_signups', 'snowy_signups', 'eagle_signups']

    @admin.display(description='Hawk Signups')
    def hawk_signups(self, obj):
        return str(Entry.hawk.filterActivity1(obj).count()) + " / " + str((Entry.hawk.filterActivity2(obj).count(), "N/A")[obj.time == 60])

    @admin.display(description='Great Grey Signups')
    def great_grey_signups(self, obj):
        return str(Entry.great_grey.filterActivity1(obj).count()) + " / " + str((Entry.great_grey.filterActivity2(obj).count(), "N/A")[obj.time == 60])

    @admin.display(description='Snowy Signups')
    def snowy_signups(self, obj):
        return str(Entry.snowy.filterActivity1(obj).count()) + " / " + str((Entry.snowy.filterActivity2(obj).count(), "N/A")[obj.time == 60])

    @admin.display(description='Eagle Signups')
    def eagle_signups(self, obj):
        return str(Entry.eagle.filterActivity1(obj).count()) + " / " + str((Entry.eagle.filterActivity2(obj).count(), "N/A")[obj.time == 60])


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {'fields': [
         'first_name', 'last_name', 'email', 'grade']}),
        ('House Wars Information', {
         'fields': ['house', 'activity1', 'activity2']}),
    ]

    list_display = ('first_name', 'last_name',
                    'house', 'activity1', 'activity2')

    list_filter = ['house', 'grade', 'activity1', 'activity2']
