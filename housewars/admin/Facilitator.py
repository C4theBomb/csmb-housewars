from django.contrib import admin

from housewars.models import Facilitator


@admin.register(Facilitator)
class FacilitatorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'activity')

    fieldsets = [
        ('Personal Information', {'fields': [
            'first_name', 'last_name']}),
        ('House Wars Information', {
            'fields': ['activity']}),
    ]
