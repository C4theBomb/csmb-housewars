from django.contrib import admin

from ..models import PointsEntry


@admin.register(PointsEntry)
class PointsEntryAdmin(admin.ModelAdmin):
    list_display = ('activity', 'name', 'house', 'points')
