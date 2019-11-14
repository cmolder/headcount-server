#  headcount_db/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListClassroom.as_view()),
    path('<int:pk>/', views.DetailClassroom.as_view()),
]