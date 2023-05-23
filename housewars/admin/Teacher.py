from django.contrib import admin, messages
from django.http import HttpResponse
from django.db.models import F
from django.utils.translation import ngettext

import io
import zipfile

from housewars.utils import load_pdf
from housewars.models import Teacher, UserEntry


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {'fields': [
            'first_name', 'last_name']}),
        ('House Wars Information', {
            'fields': ['grade', 'house', 'activity']}),
    ]

    list_display = ('first_name', 'last_name', 'house', 'grade', 'activity')

    actions = ['export_mentor_to_pdf']

    @admin.action(description='Remove activity from selected teachers')
    def remove_activity(self, request, queryset):
        queryset.update(activity=None)

        self.message_user(request, ngettext(
            'Removed activity for %d teacher.',
            'Removed activities for %d teachers.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Remove house from selected teachers')
    def remove_activity(self, request, queryset):
        queryset.update(house=None)

        self.message_user(request, ngettext(
            'Removed house for %d teacher.',
            'Removed houses for %d teachers.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Remove grade from selected teachers')
    def remove_activity(self, request, queryset):
        queryset.update(grade=None)

        self.message_user(request, ngettext(
            'Removed grade for %d teacher.',
            'Removed grades for %d teachers.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Export mentor to pdf')
    def export_mentor_to_pdf(self, request, queryset):
        file_list = {}

        for teacher in queryset:
            user_entries = UserEntry.objects.filter(
                grade=teacher.grade, house=teacher.house)

            # Augment the queryset with extra data
            user_entries = user_entries.annotate(
                a1_room=F('activity1__room_number')).annotate(a2_room=F('activity2__room_number'))

            # Select headers that are to be unpacked
            headers = ['first_name', 'last_name', 'grade', 'house',
                       'activity1', 'a1_room', 'activity2', 'a2_room']

            file = load_pdf(user_entries, headers)

            file_list[f"{teacher.last_name}, {teacher.first_name}"] = file

        outfile = io.BytesIO()
        with zipfile.ZipFile(outfile, 'w') as zf:
            for name, file in file_list.items():
                zf.writestr(f"{name}.pdf", file.getvalue())
        outfile = outfile.getvalue()

        response = HttpResponse(
            outfile, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=mentor.zip'

        return response
