from django.contrib import admin

from .models import *


# Helps make the admin view much more clear
class ClassroomAdmin(admin.ModelAdmin):
    list_display = [
        'department', 
        'number', 
        'name', 
        'professor', 
        'active',
        'active_session',
    ]

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


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_id',
        'name',
        'year'
    ]

    ordering = ['student_id']

class AttendanceTransactionAdmin(admin.ModelAdmin):
    
    list_display = [
        'time',
        'student',
        'session'
    ]

    ordering = ['time']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['student', 'session', 'time']
        return ['time']

class ClassroomSessionAdmin(admin.ModelAdmin):
    list_display = [
        'class_code',
        'classroom',
        'start',
        'end',
    ]

    ordering = ['class_code', 'classroom']

    def get_readonly_fields(self, request, obj=None):
        return ['classroom', 'start', 'end', 'class_code']


# Register your models here.
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(AttendanceTransaction, AttendanceTransactionAdmin)
admin.site.register(ClassroomSession, ClassroomSessionAdmin)
    