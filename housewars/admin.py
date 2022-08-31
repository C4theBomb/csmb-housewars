from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce

from .models import Activity, House, Teacher, PointsEntry, UserEntry


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Activity Information', {
         'fields': ['quota', 'time']}),
    ]

    list_display = ['name', 'time', 'quota', 'teacher', 'hawk_signups',
                    'great_grey_signups', 'snowy_signups', 'eagle_signups']

    @admin.display(description='Hawk Signups')
    def hawk_signups(self, obj):
        return str(UserEntry.hawk.filterActivity1(obj).count()) + " | " + str((UserEntry.hawk.filterActivity2(obj).count(), "-")[obj.time == 60])

    @admin.display(description='Great Grey Signups')
    def great_grey_signups(self, obj):
        return str(UserEntry.great_grey.filterActivity1(obj).count()) + " | " + str((UserEntry.great_grey.filterActivity2(obj).count(), "-")[obj.time == 60])

    @admin.display(description='Snowy Signups')
    def snowy_signups(self, obj):
        return str(UserEntry.snowy.filterActivity1(obj).count()) + " | " + str((UserEntry.snowy.filterActivity2(obj).count(), "-")[obj.time == 60])

    @admin.display(description='Eagle Signups')
    def eagle_signups(self, obj):
        return str(UserEntry.eagle.filterActivity1(obj).count()) + " | " + str((UserEntry.eagle.filterActivity2(obj).count(), "-")[obj.time == 60])


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'current_points', 'total_points')

    @admin.display(description='Current Housewars Points')
    def current_points(self, obj):
        return PointsEntry.objects.filter(house__name=obj.name).aggregate(points__sum=Coalesce(Sum('points'), 0)).get('points__sum')

    @admin.display(description='Total Points')
    def total_points(self, obj):
        return self.current_points(obj) + obj.points


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {'fields': [
            'first_name', 'last_name']}),
        ('House Wars Information', {
            'fields': ['grade', 'house', 'activity']}),
    ]

    list_display = ('first_name', 'last_name', 'grade', 'activity')


@admin.register(UserEntry)
class EntryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {'fields': [
         'first_name', 'last_name', 'email', 'grade']}),
        ('House Wars Information', {
         'fields': ['house', 'activity1', 'activity2']}),
    ]

    list_display = ('first_name', 'last_name',
                    'house', 'activity1', 'activity1_teacher', 'activity2', 'activity2_teacher')

    list_filter = ['house', 'grade', 'activity1',
                   'activity1__teacher', 'activity2', 'activity2__teacher']

    @admin.display(description='Activity 1 Teacher')
    def activity1_teacher(self, obj):
        if (obj.activity1 == None):
            return None

        return obj.activity1.teacher

    @admin.display(description='Activity 2 Teacher')
    def activity2_teacher(self, obj):
        if (obj.activity2 == None):
            return None

        return obj.activity2.teacher


@admin.register(PointsEntry)
class PointsEntryAdmin(admin.ModelAdmin):
    list_display = ('activity', 'name', 'house', 'points')
