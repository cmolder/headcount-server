from django.shortcuts import render

from rest_framework import generics
from .models import *
from .serializers import *

''' Classroom API views'''
class ListClassroom(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSeralizer

class DetailClassroom(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassroomSeralizer
    queryset = Classroom.objects.all()


''' Student API views '''
class ListStudent(generics.ListCreateAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        '''
        student_id - (optional) restricts the returned Students to the one
        with the given nine-digit student ID
        '''
        queryset = Student.objects.all()
        student_id = self.request.query_params.get('student_id', None)

        if student_id is not None:
            queryset = queryset.filter(student_id = student_id)

        return queryset

class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


''' Instructor API views '''
class ListInstructor(generics.ListCreateAPIView):
    serializer_class = InstructorSerializer

    def get_queryset(self):
        queryset = Instructor.objects.all()

        return queryset

class DetailInstructor(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()


''' Attendance transaction API views '''
class ListAttendanceTransaction(generics.ListCreateAPIView):
    serializer_class = AttendanceTransactionSerializer

    def get_queryset(self):
        '''
        classroom - (optional) restricts the returned
        attendance transactions to those associated with sessions 
        of Classroom with the given Django ID. [ NOT classroom's class_code!! ]

        student - (optional) restricts the returned
        attendance transactions to those associated with the Student
        with the given Django ID. [ NOT student's student_id!! ]

        student_id - (optional) restricts the returned
        attendance transactions to those associated with the Student
        with the given nine-digit student id.

        date - (optional) in form YYYY-MM-DD restricts the returned
        attendance transactions to those that happened on said date.
        '''
        queryset   = AttendanceTransaction.objects.all()

        classroom  = self.request.query_params.get('classroom', None)
        student_id = self.request.query_params.get('student_id', None)

        date       = self.request.query_params.get('date', None)

        if classroom is not None:
            queryset = queryset.filter(session__classroom__id = classroom)

        if student is not None:
            queryset = queryset.filter(student__id = student)

        if student_id is not None:
            queryset = queryset.filter(student__student_id = student_id)

        if date is not None:
            queryset = queryset.filter(time__date = date)

        return queryset

class DetailAttendanceTransaction(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceTransactionSerializer
    queryset = AttendanceTransaction.objects.all()


''' Classroom session API views '''
class ListClassroomSession(generics.ListAPIView):
    serializer_class = ClassroomSessionSerializer

    def get_queryset(self):
        '''
        classroom - (optional) restricts the returned classroom sessions
        to those associtaed with the Classrooms with the given Django ID.

        class_code - (optional) restricts the returned classroom sessions
        to those with the given class code.
        '''
        
        queryset = ClassroomSession.objects.all()

        classroom = self.request.query_params.get('classroom', None)
        class_code = self.request.query_params.get('class_code', None)

        if classroom is not None:
            queryset = queryset.filter(classroom__id = classroom)

        if class_code is not None:
            queryset = queryset.filter(class_code = class_code)

        return queryset

class DetailClassroomSession(generics.ListCreateAPIView):
    serializer_class = ClassroomSessionSerializer
    queryset = ClassroomSession.objects.all()