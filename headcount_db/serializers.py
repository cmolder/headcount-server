# headcount_db/serializers.py

from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id',
            'student_id',
            'name',
            'year',
        )

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = (
            'user',
            'name',
            'title'
        )

class AttendanceTransactionSerializer(serializers.ModelSerializer):
    
    ''' Validates the attendance transaction as a whole '''
    def validate(self, data):
        # Check that the student is on the session classroom's roster.
        student = data['student']
        session = data['session']

        if student not in session.classroom.students.all():
            raise serializers.ValidationError(f'{student} is not on the roster for {session.classroom}')
        return data
    
    class Meta:
        model = AttendanceTransaction
        fields = (
            'id',
            'session',
            'student',
            'time'
        )

class ClassroomSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomSession
        fields = (
            'id',
            'classroom',
            'class_code',
            'start',
            'end'
        )

class ClassroomSerializer(serializers.ModelSerializer):
    
    active_session = ClassroomSessionSerializer(read_only = True)

    class Meta:
        model = Classroom
        fields = (
            'id',
            'department',
            'number',
            'name',
            'instructor',
            'students',
            'active',
            'active_session',
        )
