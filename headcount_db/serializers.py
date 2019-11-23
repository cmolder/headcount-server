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
    
    ''' Validates the attendance transaction as a whole '''
    def validate(self, data):
        # Check that the student is on the classroom's student roster.
        if data['student'] not in data['classroom'].students.all():
            raise serializers.ValidationError(f"{data['student']} is not on the roster for {data['classroom']}")
        return data
    
    class Meta:
        model = AttendanceTransaction
        fields = (
            'id',
            'student',
            'classroom',
            'time'
        )
