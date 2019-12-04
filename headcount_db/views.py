from django.shortcuts import render

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

''' Classroom API views'''
class ListClassroom(generics.ListCreateAPIView):

    # TO WORK WITHOUT LOGIN, SIMPLY REMOVE THIS LINE :)
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomSerializer

    # Get all classrooms where the user is an Instructor
    def get_queryset(self):
        '''
        is_instructor - filters the returned Classrooms to the ones
        where the user is the Instructor

        is_student - filters the returned Classrooms to the ones
        where the user is a Student on the roster

        One of the two filters is required, otherwise the
        query returns an empty array
        '''

        queryset = Classroom.objects.all()
        user     = self.request.user

        is_instructor = self.request.query_params.get('is_instructor', 'False')
        is_student    = self.request.query_params.get('is_student', 'False')

        if is_instructor == 'True':
            queryset = queryset.filter(instructor__user = user)

        if is_student == 'True':
            studentset = Student.objects.filter(user = user)
            queryset = queryset.filter(students__in = studentset)

        if is_student != 'True' and is_instructor != 'True':
            queryset = Classroom.objects.none()

        return queryset


    


class DetailClassroom(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()


''' Student API views '''
class ListStudent(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


''' Instructor API views '''
class ListInstructor(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstructorSerializer

    def get_queryset(self):
        '''
        is_user - (optional) restricts the returned Instructors to the
        one associated with the currently signed-in user
        '''
        queryset = Instructor.objects.all()
        is_user  = self.request.query_params.get('is_user', 'False')

        if is_user == 'True':
            user = self.request.user
            queryset = queryset.filter(user = user)

        return queryset

class DetailInstructor(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()


''' Attendance transaction API views '''
class ListAttendanceTransaction(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceTransactionSerializer

    def get_queryset(self):
        '''
        classroom - (optional) restricts the returned
        attendance transactions to those associated with sessions 
        of Classroom with the given Django ID. [ NOT classroom's class_code!! ]

        X student - (optional) restricts the returned
        X attendance transactions to those associated with the Student
        X with the given Django ID. [ NOT student's student_id!! ]

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

        if student_id is not None:
            queryset = queryset.filter(student__student_id = student_id)

        if date is not None:
            queryset = queryset.filter(time__date = date)

        return queryset

class DetailAttendanceTransaction(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceTransactionSerializer
    queryset = AttendanceTransaction.objects.all()


''' Classroom session API views '''
class ListClassroomSession(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomSessionSerializer
    queryset = ClassroomSession.objects.all()