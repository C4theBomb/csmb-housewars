from django.contrib import admin
from .models import Activity, Entry


@admin.action(description='Reset signup counter')
def resetSignupCounters(modeladmin, request, queryset):
    queryset.update(session1_signups=0, session2_signups=0)


class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Activity Information', {
         'fields': ['quota', 'time', 'session1_signups', 'session2_signups']}),
    ]

    list_display = ('name', 'time', 'quota',
                    'session1_signups', 'session2_signups')

    actions = [resetSignupCounters]


class EntryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {'fields': [
         'first_name', 'last_name', 'email', 'grade']}),
        ('House Wars Information', {
         'fields': ['house', 'activity1', 'activity2']}),
    ]

    list_display = ('first_name', 'last_name',
                    'house', 'activity1', 'activity2')

    list_filter = ['house', 'grade']


# Register your models here.
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Entry, EntryAdmin)
