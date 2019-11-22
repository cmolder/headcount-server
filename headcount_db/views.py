from django.shortcuts import render

from rest_framework import generics
from .models import *
from .serializers import *

''' Classroom API views'''
class ListClassroom(generics.ListCreateAPIView):
    serializer_class = ClassroomSeralizer

    def get_queryset(self):
        '''
        Optional field (class_code) restricts the returned Classrooms to the one
        with a the given six-digit class code
        '''
        queryset = Classroom.objects.all()
        code = self.request.query_params.get('class_code', None)

        if code is not None:
            queryset = queryset.filter(class_code = code)

        return queryset

class DetailClassroom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSeralizer



''' Student API views '''
class ListStudent(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



''' Attendance transcation API views '''
class ListAttendanceTransaction(generics.ListCreateAPIView):
    serializer_class = AttendanceTransactionSerializer

    def get_queryset(self):
        '''
        Optional field (classroom) restricts the returned
        attendance transactions to those associated with the Classroom
        with the given Django ID.

        Optional field (student) restricts the returned
        attendance transactions to those associated with the Student
        with the given Django ID. [ NOT student's student_id!! ]


        Optional field (date) in form YEAR-MM-DD restricts the returned
        attendance transactions to those that happened on said date.
        '''
        queryset  = AttendanceTransaction.objects.all()
        student   = self.request.query_params.get('student', None)
        classroom = self.request.query_params.get('classroom', None)
        date      = self.request.query_params.get('date', None)

        if classroom_id is not None:
            queryset = queryset.filter(classroom__id = classroom)

        if student_id is not None:
            queryset = queryset.filter(student__id = student)

        if date is not None:
            queryset = queryset.filter(time__date = date)

        return queryset


class DetailAttendanceTransaction(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceTransaction.objects.all()
    serializer_class = AttendanceTransactionSerializer
