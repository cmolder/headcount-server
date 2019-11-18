from django.shortcuts import render

from rest_framework import generics
from .models import Classroom
from .models import Student
from .serializers import ClassroomSeralizer, StudentSerializer

# Create your views here.
class ListClassroom(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSeralizer

class DetailClassroom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSeralizer

class ListStudent(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer