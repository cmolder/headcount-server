from django.contrib import admin

from .models import Classroom, Student, AttendanceTransaction


# Helps make the admin view much more clear
class ClassroomAdmin(admin.ModelAdmin):
    list_display = [
        'department', 
        'number', 
        'name', 
        'professor', 
        'class_code', 
        'active'
    ]

    ordering = ['department', 'number']
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(active=True)
        for item in queryset:
            item.save()

    make_active.short_description = "Activate selected classes"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        for item in queryset:
            item.save()

    make_inactive.short_description = "Deactivate selected classes"


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
        'classroom'
    ]

    ordering = ['time']


# Register your models here.
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(AttendanceTransaction, AttendanceTransactionAdmin)
    