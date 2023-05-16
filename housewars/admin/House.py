from django.contrib import admin

from housewars.models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'current_points', 'total_points')

    @admin.display(description='Current Housewars Points')
    def current_points(self, obj):
        return obj.current_points

    @admin.display(description='Total Points')
    def total_points(self, obj):
        return obj.total_points
