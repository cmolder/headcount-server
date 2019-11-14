# headcount_db/serializers.py

from rest_framework import serializers
from .models import Classroom

class ClassroomSeralizer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'department',
            'number',
            'name',
            'professor',
            'class_code',
        )

        model = Classroom