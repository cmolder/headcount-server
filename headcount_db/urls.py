#  headcount_db/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('classroom', views.ListClassroom.as_view()),            # Gets all classrooms in the database
    path('classroom/<int:pk>', views.DetailClassroom.as_view()), # Gets classroom w/ provided Django ID
    
    path('student', views.ListStudent.as_view()),            # Gets all students in the database
    path('student/<int:pk>', views.DetailStudent.as_view()), # Gets student w/ provided Django ID

    path('attendance', views.ListAttendanceTransaction.as_view()),            # Gets all attendance transactions in the database
    path('attendance/<int:pk>', views.DetailAttendanceTransaction.as_view()), # Gets attendance transaction w/ provided Django ID
]