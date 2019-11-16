# headcount_db/serializers.py

from rest_framework import serializers
from .models import Classroom, Student

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
        
        


