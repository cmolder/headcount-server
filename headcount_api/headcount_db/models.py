# headcount_db/modelspy

from django.db import models
from django.utils.crypto import get_random_string

class Classroom(models.Model):
    department = models.CharField(max_length=4, default='') # ex CSCE
    number = models.CharField(max_length=5, default='')     # ex 3193H / 3513
    title = models.CharField(max_length=200, default='')
    professor = models.CharField(max_length=200)
    class_code = models.CharField(max_length=6, primary_key=True, 
                    editable=False, unique=True, default='000000') # 6-char long alphanumeric class code (0..9, A..Z)

    def save(self, *args, **kwargs):
        if not self.class_code:
            self.class_code = get_random_string(6).upper()
        return super(Classroom, self).save(*args, **kwargs)

    def __str__(self):
        """A string representation of the model."""
        return self.department + " " + self.number + " " + self.title + " " + self.class_code

