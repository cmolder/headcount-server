from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *

# Helps make the admin view much more clear

''' Classroom admin '''
class ClassroomAdmin(admin.ModelAdmin):
    list_display = [
        'department', 
        'number', 
        'name', 
        'instructor', 
        'active',
        'active_session',
    ]

    list_filter = ['active', 'department']
    search_fields = ['department', 'number', 'name', 'instructor']

    ordering = ['department', 'number']
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(active=True)
        for item in queryset:
            item.save()

    make_active.short_description = "Activate selected classrooms"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        for item in queryset:
            item.save()

    make_inactive.short_description = "Deactivate selected classrooms"


''' Student admin '''
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_id',
        'name',
        'year',
        #'user'
    ]

    list_filter   = ['year']
    ordering      = ['student_id']
    search_fields = ['name', 'student_id']


''' Instructor admin '''
class InstructorAdmin(admin.ModelAdmin):

    list_display = [
        'title',
        'name',
        #'user'
    ]

    ordering      = ['name']
    search_fields = ['name']


''' Attendance transaction admin '''
class AttendanceTransactionAdmin(admin.ModelAdmin):
    
    list_display = [
        'session',
        'student',
        'time'
    ]

    list_filter   = ['time']
    ordering      = ['session', 'time']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['student', 'session', 'time']
        return ['time']


''' Classroom session admin '''
class ActiveSessionFilter(admin.SimpleListFilter):
    title = _('active session')   # Title displayed in the sidebar
    parameter_name = 'class_code' # Parameter that will be filtered against in the query

    def lookups(self, request, model_admin):
        # First element of each tuple is coded value that is used in queryset,
        # Second element of each tuple is the name displayed for that option in the sidebar
        return (
            ('active', _('Active sessions')),
            ('inactive', _('Inactive sessions'))
        )

    # Filters the list of objects
    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.exclude(class_code = None)
        if self.value() == 'inactive':
            return queryset.filter(class_code = None)

class ClassroomSessionAdmin(admin.ModelAdmin):
    list_display = [
        'classroom',
        'class_code',
        'start',
        'end',
    ]

    list_filter = [ActiveSessionFilter, 'start']

    ordering = ['classroom', 'class_code']

    def get_readonly_fields(self, request, obj=None):
        return ['classroom', 'start', 'end', 'class_code']


# Register your models here.
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(AttendanceTransaction, AttendanceTransactionAdmin)
admin.site.register(ClassroomSession, ClassroomSessionAdmin)
    