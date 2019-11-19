#  headcount_db/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('classrooms', views.ListClassroom.as_view()),            # Gets all classrooms in the database
    path('classrooms/<int:pk>', views.DetailClassroom.as_view()), # Gets classroom w/ provided Django ID
    
    path('students', views.ListStudent.as_view()),            # Gets all students in the database
    path('students/<int:pk>', views.DetailStudent.as_view()), # Gets student w/ provided Django ID
]