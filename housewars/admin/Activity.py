from django.http import HttpResponse
from django.contrib import admin, messages
from django.db.models import F
from django.utils.translation import ngettext

import io
import zipfile

from housewars.utils import get_random_string, load_pdf
from housewars.models import Activity, Award, Quota, UserEntry
from housewars.utils import load_pdf


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

    actions = ['generate_passwords', 'export_a1_to_pdf', 'export_a2_to_pdf']

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
        for activity in queryset:
            activity.password = get_random_string(8)
            activity.save()

        self.message_user(request, ngettext(
            'Generated password for %d activity.',
            'Generated passwords for %d activities.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Export activity 1 attendance to pdf')
    def export_a1_to_pdf(self, request, queryset):
        file_list = {}

        for activity in queryset:
            user_entries = activity.activity1

            # Augment the queryset with extra data
            user_entries = user_entries.annotate(
                a1_room=F('activity1__room_number')).annotate(a2_room=F('activity2__room_number'))

            # Select headers that are to be unpacked
            headers = ['first_name', 'last_name', 'grade', 'house',
                       'activity1', 'a1_room', 'activity2', 'a2_room']

            file = load_pdf(user_entries, headers)

            file_list[f"{activity.name} - 1"] = file

        outfile = io.BytesIO()
        with zipfile.ZipFile(outfile, 'w') as zf:
            for name, file in file_list.items():
                zf.writestr(f"{name}.pdf", file.getvalue())
        outfile = outfile.getvalue()

        response = HttpResponse(
            outfile, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=activity1_attendance.zip'

        return response

    @admin.action(description='Export activity 2 attendance to pdf')
    def export_a2_to_pdf(self, request, queryset):
        file_list = {}

        for activity in queryset:
            user_entries = activity.activity2

            # Augment the queryset with extra data
            user_entries = user_entries.annotate(
                a1_room=F('activity1__room_number')).annotate(a2_room=F('activity2__room_number'))

            # Select headers that are to be unpacked
            headers = ['first_name', 'last_name', 'grade', 'house',
                       'activity1', 'a1_room', 'activity2', 'a2_room']

            file = load_pdf(user_entries, headers)

            file_list[f"{activity.name} - 2"] = file

        outfile = io.BytesIO()
        with zipfile.ZipFile(outfile, 'w') as zf:
            for name, file in file_list.items():
                zf.writestr(f"{name}.pdf", file.getvalue())
        outfile = outfile.getvalue()

        response = HttpResponse(
            outfile, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=activity2_attendance.zip'

        return response
