from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.db.models import Sum, F
from django.db.models.functions import Coalesce

from ..models import House, PointsEntry


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'current_points', 'total_points')
    actions = ['finalize_points']

    @admin.display(description='Current Housewars Points')
    def current_points(self, obj):
        return obj.current_points

    @admin.display(description='Total Points')
    def total_points(self, obj):
        return obj.total_points

    @admin.action(description='Finalize selected house points')
    def finalize_points(self, request, queryset):
        updated = queryset.update(
            points=queryset.aggregate(points__sum=Coalesce(Sum('pointsentry__points'), 0)).get('points__sum') + F('points'))
        PointsEntry.objects.filter(pk__in=queryset).delete()
        self.message_user(request, ngettext(
            'Finalized house points for %d house.',
            'Finalized house points for %d houses.',
            updated,
        ) % updated, messages.SUCCESS)
