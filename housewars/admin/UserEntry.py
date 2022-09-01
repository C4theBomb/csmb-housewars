from django.contrib import admin
from django.db.models import F, Value
from django.db.models.functions import Concat

from ..models import UserEntry


class MentorListFilter(admin.SimpleListFilter):
    title = 'mentor teacher'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'mentor'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        qs = model_admin.get_queryset(request).annotate(full_name=Concat(F(
            'house__teacher__first_name'), Value(' '), F('house__teacher__last_name'))).values_list('house__teacher', 'full_name').distinct()

        return qs

    def queryset(self, request, queryset):
        if (self.value() == None):
            return queryset

        return queryset.filter(house__teacher=self.value(), grade=F('house__teacher__grade'))


@ admin.register(UserEntry)
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

    @ admin.display(description='Activity 1 Teacher')
    def activity1_teacher(self, obj):
        if (obj.activity1 == None):
            return None

        return obj.activity1.teacher

    @ admin.display(description='Mentor Teacher')
    def mentor_teacher(self, obj):
        return obj.mentor

    @ admin.display(description='Activity 2 Teacher')
    def activity2_teacher(self, obj):
        if (obj.activity2 == None):
            return None

        return obj.activity2.teacher
