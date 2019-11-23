# headcount_db/serializers.py

from rest_framework import serializers
from rest_framework.validators import UniqueForDateValidator

from .models import Classroom, Student, AttendanceTransaction

class ClassroomSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'department', 'number', 'name', 'professor', 
                  'students', 'active', 'class_code']
        

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'name', 'year']

class AttendanceTransactionSerializer(serializers.ModelSerializer):
   
    def validate(self, data):

        # If the student is not on the class roster, then the
        # attendance transaction is not valid
        roster = Classroom.objects.get(id = data['classroom'])
        if data['student'] not in roster:
            raise serializers.ValidationError("student is not on the roster for classroom")

    class Meta:
        model = AttendanceTransaction
        fields = ['id', 'student','classroom','time']

        
        


