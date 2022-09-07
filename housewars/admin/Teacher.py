from django.contrib import admin

from housewars.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {'fields': [
            'first_name', 'last_name']}),
        ('House Wars Information', {
            'fields': ['grade', 'house', 'activity']}),
    ]

    list_display = ('first_name', 'last_name', 'house', 'grade', 'activity')
