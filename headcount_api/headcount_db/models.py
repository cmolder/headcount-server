from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.
class Classroom(models.Model):
    department = models.CharField(max_length=4)
    number = models.CharField(max_length=5)
    name = models.CharField(max_length=200)
    professor = models.CharField(max_length=200)
    class_code = models.CharField(max_length=6, editable=False, unique=True)

    def __str__(self):
        """A string representation of the model"""
        return (self.department + " " + self.number + " " + self.name + " " + self.class_code)

    def save(self, *args, **kwargs):
        if not self.class_code:
            self.class_code = get_random_string(6).upper()
        return super(Classroom, self).save(*args, **kwargs)
