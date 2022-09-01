from django.contrib import admin

from ..models import Activity, UserEntry


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Activity Information', {
         'fields': ['quota', 'time']}),
    ]

    list_display = ['name', 'time', 'quota', 'teacher', 'password', 'hawk_signups',
                    'great_grey_signups', 'snowy_signups', 'eagle_signups']

    @admin.display(description='Hawk Signups')
    def hawk_signups(self, obj):
        if (obj.time == None):
            return "- | -"
        return str(UserEntry.hawk.filterActivity1(obj).count()) + " | " + str((UserEntry.hawk.filterActivity2(obj).count(), "-")[obj.time == 60])

    @admin.display(description='Great Grey Signups')
    def great_grey_signups(self, obj):
        if (obj.time == None):
            return "- | -"
        return str(UserEntry.great_grey.filterActivity1(obj).count()) + " | " + str((UserEntry.great_grey.filterActivity2(obj).count(), "-")[obj.time == 60])

    @admin.display(description='Snowy Signups')
    def snowy_signups(self, obj):
        if (obj.time == None):
            return "- | -"
        return str(UserEntry.snowy.filterActivity1(obj).count()) + " | " + str((UserEntry.snowy.filterActivity2(obj).count(), "-")[obj.time == 60])

    @admin.display(description='Eagle Signups')
    def eagle_signups(self, obj):
        if (obj.time == None):
            return "- | -"
        return str(UserEntry.eagle.filterActivity1(obj).count()) + " | " + str((UserEntry.eagle.filterActivity2(obj).count(), "-")[obj.time == 60])
