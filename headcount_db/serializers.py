# headcount_db/serializers.py

from rest_framework import serializers
from .models import *

class ClassroomSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = (
            'id',
            'department',
            'number',
            'name',
            'professor',
            'students',
            'active',
            'active_session'
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
