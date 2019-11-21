# headcount_db/serializers.py

from rest_framework import serializers
from .models import Classroom, Student, AttendanceTransaction

class ClassroomSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = (
            'id',
            'department',
            'number',
            'name',
            'professor',
            'class_code',
            'students',
            'active'
        )

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id',
            'student_id',
            'name',
            'year',
        )

class AttendanceTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceTransaction
        fields = (
            'id',
            'student',
            'classroom',
            'time'
        )
        
        


