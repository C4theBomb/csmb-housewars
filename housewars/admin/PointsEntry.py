from django.contrib import admin
from django.db.models import F

from ..models import PointsEntry


class ValidatedPasswordFilter(admin.SimpleListFilter):
    title = 'valid password'

    parameter_name = 'valid'

    def lookups(self, request, model_admin):
        return (('True', True), ('False', False))

    def queryset(self, request, queryset):
        if (self.value() == 'True'):
            return queryset.filter(password=F('activity__password'))
        elif (self.value() == 'False'):
            return queryset.exclude(password=F('activity__password'))
        else:
            return queryset


@admin.register(PointsEntry)
class PointsEntryAdmin(admin.ModelAdmin):
    list_display = ('activity', 'award', 'house', 'validated')

    list_filter = ('activity', ValidatedPasswordFilter)

    @admin.display(description='Validated', boolean=True)
    def validated(self, obj):
        return obj.password == obj.activity.password
