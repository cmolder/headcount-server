from django.shortcuts import render

from rest_framework import generics
from .models import *
from .serializers import *

''' Classroom API views'''
class ListClassroom(generics.ListCreateAPIView):
    serializer_class = ClassroomSeralizer

    def get_queryset(self):
        """
        Optionally restricts the returned classrooms to a given class code,
        by filtering against a 'class_code' query param in the URL.
        """
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
    queryset = AttendanceTransaction.objects.all()
    serializer_class = AttendanceTransactionSerializer

class DetailAttendanceTransaction(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceTransaction.objects.all()
    serializer_class = AttendanceTransactionSerializer