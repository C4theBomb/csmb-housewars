from django.contrib import admin
from django.http import HttpResponse
from django.db.models import F

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
