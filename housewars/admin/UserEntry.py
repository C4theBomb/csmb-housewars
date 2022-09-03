from django.contrib import admin
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, FileResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib.colors import black
import csv
import io

from ..models import UserEntry


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
        field_names = [field.name for field in queryset.model._meta.fields]

        response = HttpResponse(content_type='text/csv', headers={
                                'Content-Disposition': 'attachment; filename="export.csv"'},)

        writer = csv.writer(response, delimiter=";")
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for row in queryset:
            values = []
            for field in field_names:
                value = getattr(row, field)
                if value is None:
                    value = ''
                values.append(value)
            writer.writerow(values)

        return response

    @admin.action(description='Export selected to pdf')
    def export_to_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        elements = []

        field_names = [field.name for field in queryset.model._meta.fields]
        data = []
        data.append(field_names)
        for row in queryset:
            values = []
            for field in field_names:
                value = getattr(row, field)
                if value is None:
                    value = ''
                values.append(value)
            data.append(values)

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, black), ('BOX', (0, 0), (-1, -1), 0.25, black)]))
        elements.append(table)

        doc.build(elements)

        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename='download.pdf')
