from django.contrib import admin
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, FileResponse

import csv

from housewars.models import UserEntry
from housewars.utils import unpack_values, load_pdf


class MentorListFilter(admin.SimpleListFilter):
    title = 'mentor teacher'

    parameter_name = 'mentor'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request).annotate(full_name=Concat(F(
            'house__teacher__first_name'), Value(' '), F('house__teacher__last_name'))).values_list('house__teacher', 'full_name').distinct()

        return qs

    def queryset(self, request, queryset):
        if (self.value() == None):
            return queryset

        return queryset.filter(house__teacher=self.value(), grade=F('house__teacher__grade'))


@admin.register(UserEntry)
class UserEntryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {'fields': [
         'first_name', 'last_name', 'email', 'grade']}),
        ('House Wars Information', {
         'fields': ['house', 'activity1', 'activity2']}),
    ]

    list_display = ('first_name', 'last_name',
                    'house', 'mentor_teacher', 'activity1', 'activity1_teacher', 'activity2', 'activity2_teacher')

    list_filter = ['house', 'grade', MentorListFilter, 'activity1',
                   'activity1__teacher', 'activity2', 'activity2__teacher']

    search_fields = ['first_name', 'last_name']

    actions = ['export_to_csv', 'export_to_pdf']

    @admin.display(description='Activity 1 Teacher')
    def activity1_teacher(self, obj):
        if (obj.activity1 == None):
            return None

        return obj.activity1.teacher

    @admin.display(description='Mentor Teacher')
    def mentor_teacher(self, obj):
        return obj.mentor

    @admin.display(description='Activity 2 Teacher')
    def activity2_teacher(self, obj):
        if (obj.activity2 == None):
            return None

        return obj.activity2.teacher

    @admin.action(description='Export selected to csv')
    def export_to_csv(self, request, queryset):
        # Augment the querset with extra data
        queryset = queryset.annotate(
            a1_room=F('activity1__room_number')).annotate(a2_room=F('activity1__room_number'))

        # Initialize csv object writers
        response = HttpResponse(content_type='text/csv', headers={
                                'Content-Disposition': 'attachment; filename="export.csv"'},)
        writer = csv.writer(response, delimiter=";")

        # Select headers that are to be unpacked
        headers = ['first_name', 'last_name', 'grade', 'house',
                   'activity1', 'a1_room', 'activity2', 'a2_room']

        # Unpack queryset data
        data = unpack_values(queryset, headers)

        # Write data into tables
        writer.writerows(data)

        return response

    @admin.action(description='Export selected to pdf')
    def export_to_pdf(self, request, queryset):
        # Augment the querset with extra data
        queryset = queryset.annotate(
            a1_room=F('activity1__room_number')).annotate(a2_room=F('activity2__room_number'))

        # Select headers that are to be unpacked
        headers = ['first_name', 'last_name', 'grade', 'house',
                   'activity1', 'a1_room', 'activity2', 'a2_room']

        # Unpack queryset data
        file = load_pdf(queryset, headers)

        return FileResponse(file, as_attachment=True, filename='export.pdf')
