from django.urls import path
from . import views

urlpatterns = [
    # Classroom API endpoints
    path('classroom', views.ListClassroom.as_view()),            # Gets all Classroom objects (with optional filters)
    path('classroom/<int:pk>', views.DetailClassroom.as_view()), # Gets Classroom with provided Django ID
    
    # Student API endpoints
    path('student', views.ListStudent.as_view()),            # Gets all Student objects (with optional filters)
    path('student/<int:pk>', views.DetailStudent.as_view()), # Gets Student with provided Django ID

    # Attendance transaction API endpoints
    path('attendance', views.ListAttendanceTransaction.as_view()),            # Gets all AttendanceTransaction objects (with optional filters)
    path('attendance/<int:pk>', views.DetailAttendanceTransaction.as_view()), # Gets AttendanceTransaction with provided Django ID

    path('session', views.ListClassroomSession.as_view()),           # Gets all ClassroomSession objects (with optional filters)
    path('session/<int:pk>', views.DetailClassroomSession.as_view()) # Gets ClassroomSession with provided Django ID


]