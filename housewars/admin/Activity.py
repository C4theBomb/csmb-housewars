from django.http import HttpResponse
from django.contrib import admin, messages
from django.utils.translation import ngettext

from ..utils import get_random_string
from ..models import Activity, Award, Quota, UserEntry


class QuotaInline(admin.TabularInline):
    model = Quota
    extra = 0


class AwardsInline(admin.TabularInline):
    model = Award
    extra = 0


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'room_number']}),
        ('Activity Information', {
         'fields': ['default_quota', 'time', 'password']}),
    ]

    list_display = ['name', 'time', 'room_number', 'teacher', 'password',
                    'default_quota', 'hawk_signups', 'great_grey_signups', 'snowy_signups', 'eagle_signups']

    inlines = [QuotaInline, AwardsInline]

    actions = ['generate_passwords']

    @admin.display(description='Hawk')
    def hawk_signups(self, obj):
        if (obj.time == None):
            return "- | -"
        return str(UserEntry.objects.filter(house__name='Hawk', activity1=obj).count()) + ' | ' + str((UserEntry.objects.filter(house__name='Hawk', activity2=obj).count(), '-')[obj.time == 60])

    @admin.display(description='Great Grey')
    def great_grey_signups(self, obj):
        if (obj.time == None):
            return "- | -"
        return str(UserEntry.objects.filter(house__name='Great Grey', activity1=obj).count()) + ' | ' + str((UserEntry.objects.filter(house__name='Great Grey', activity2=obj).count(), '-')[obj.time == 60])

    @admin.display(description='Snowy')
    def snowy_signups(self, obj):
        if (obj.time == None):
            return "- | -"
        return str(UserEntry.objects.filter(house__name='Snowy', activity1=obj).count()) + ' | ' + str((UserEntry.objects.filter(house__name='Snowy', activity2=obj).count(), '-')[obj.time == 60])

    @admin.display(description='Eagle')
    def eagle_signups(self, obj):
        if (obj.time == None):
            return "- | -"
        return str(UserEntry.objects.filter(house__name='Eagle', activity1=obj).count()) + ' | ' + str((UserEntry.objects.filter(house__name='Eagle', activity2=obj).count(), '-')[obj.time == 60])

    @admin.action(description='Generate passwords for selected activities')
    def generate_passwords(self, request, queryset):
        for item in queryset:
            item.password = get_random_string(8)
            item.save()

        self.message_user(request, ngettext(
            'Generated password for %d activity.',
            'Generated passwords for %d activities.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)
