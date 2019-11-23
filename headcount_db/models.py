from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

''' 
Classroom model 
'''
class Classroom(models.Model):

    ''' Classroom fields '''
    department = models.CharField(max_length=4)   # i.e. CSCE, HIST
    number     = models.CharField(max_length=5)   # i.e. 3193, 2074H
    name       = models.CharField(max_length=200) # i.e. "Programming Paradigms"
    professor  = models.CharField(max_length=200) # i.e. "Dr. John Doe", "Dr. Garret Gardenhire, Ph.D."
    class_code = models.CharField(max_length=6, editable=False, unique=True, null=True, default=None) # i.e. "A9BDX3" (randomly generated)
    students   = models.ManyToManyField('Student', blank=True)
    active     = models.BooleanField(default=False) # Class code is generated when class is active


    ''' Updates the class code upon being activated '''
    def update_class_code(self):
        if(self.active == False):
            self.class_code = None

        elif(self.active == True and self.class_code == None):
            self.class_code = get_random_string(6).upper()


    ''' Saves the Classroom '''
    def save(self, *args, **kwargs):
        self.update_class_code()
        return super(Classroom, self).save(*args, **kwargs)

    
    ''' String representation '''
    def __str__(self):
        if self.class_code is not None:
            return (str(self.id) + " " + self.department + " " + self.number + " " + self.name + " " + self.class_code)
        return (str(self.id) + " " + self.department + " " + self.number + " " + self.name + " (inactive)")



'''
Student model
'''
class Student(models.Model): 
    YEAR_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'), 
        ('SR', 'Senior'),
        ('GR', 'Graduate')
    ]

    numeric = RegexValidator(r'^[0-9]*$', 'Only numeric student IDs (consisting of 0-9) are allowed.')


    ''' Student fields '''
    student_id = models.CharField(max_length=9, validators=[numeric]) # Student ID
    name       = models.CharField(max_length=200)                     # First and last name
    year       = models.CharField(max_length=2, choices=YEAR_CHOICES, default='FR')


    ''' String representation '''
    def __str__(self):
        return (str(self.id) + " " + self.name + " " + self.student_id + " " + self.year)



'''
Attendance transaction model
- Stores records of students marking themselves present in classes
'''
class AttendanceTransaction(models.Model):

    
    ''' Validates the Classroom '''
    def validate_classroom(classroom):
        # Django Admin interface sends an integer representing a Classroom's
        # Django ID, so we need to obtain the associated Classroom first
        # ------
        # Django REST API sends the actual Classroom object, so we can
        # directly parse the field
        if type(classroom) is int:
            classroom = Classroom.objects.get(id = classroom)

        if type(classroom) is Classroom:
            if classroom.active is not True:
                raise ValidationError((f"{classroom} is not active"), params={'classroom': classroom})
        else:
            raise ValidationError(f"{classroom} is not of type Classroom or valid Django ID", params={'classroom': classroom})


    ''' Attendance transaction fields '''
    classroom = models.ForeignKey('Classroom', validators=[validate_classroom], on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    time = models.DateTimeField(editable=False)
        

    ''' Validates the attendance transaction as a whole '''
    def clean(self):
        # Check that the student is on the classroom's student roster.
        if self.student not in self.classroom.students.all():
            raise ValidationError((f"{self.student} is not on the roster for {self.classroom}"), 
                                  params={'student': self.student, 'classroom': self.classroom})



    ''' Saves the AttendanceTransaction '''
    def save(self, *args, **kwargs):
        # On creation, set the time field to current time
        if not self.id:
            self.time = timezone.now()
        return super(AttendanceTransaction, self).save(*args, **kwargs)


    ''' String representation '''
    def __str__(self):
        return (str(self.id) + " " + str(self.student.name) + " at " + str(self.classroom.name) + " on " + self.time.strftime("%m/%d/%y"))
