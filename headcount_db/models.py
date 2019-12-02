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
    instructor = models.ForeignKey('Instructor', related_name='+', blank=True,
                 null=True, default=None, on_delete = models.SET_DEFAULT)
    students   = models.ManyToManyField('Student', blank=True)
    active     = models.BooleanField(default=False) # When set to true, creates a new ClassroomSession
                                                    # When set to false, ends the Session and clears it from
                                                    # this object
    active_session = models.ForeignKey('ClassroomSession', related_name='+', 
                     editable=False, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT)


    ''' Saves the Classroom '''
    def save(self, *args, **kwargs):

        # If the Classroom was just activated,
        # create a new ClassroomSession (which provides the class code
        # and start time)
        if self.active and self.active_session is None:
            self.active_session = ClassroomSession.objects.create(classroom=self)

        # If the classroom was just deactivated,
        # log the end time and remove the active session
        # from this classroom
        elif self.active is False and self.active_session is not None:
            self.active_session.end = timezone.now()
            self.active_session.save()
            self.active_session = None

        return super(Classroom, self).save(*args, **kwargs)


    ''' String representation '''
    def __str__(self):
        if self.active_session is not None:
            return f'{self.department} {self.number} {self.name} ({self.active_session.class_code})'
        return f'{self.department} {self.number} {self.name} (inactive)'



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
        return f'{self.id} {self.name} {self.student_id} {self.year}'


'''
Instructor model
'''
class Instructor(models.Model):
    TITLE_CHOICES = [
        ('MR', 'Mr.'),
        ('MS', 'Ms.'),
        ('MRS', 'Mrs.'),
        ('DR', 'Dr.'),
        ('PF', 'Professor'),
        ('NONE', '')
    ]

    title = models.CharField(max_length=4, choices=TITLE_CHOICES, default='NONE')
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title} {self.name}'



'''
Attendance transaction model
- Stores records of students marking themselves present in classes
'''
class AttendanceTransaction(models.Model):

    
    ''' Validates the Session '''
    def validate_session(session):
        # Django Admin interface sends an integer representing a ClassroomSession's
        # Django ID, so we need to obtain the associated ClassroomSession first
        # ------
        # Django REST API sends the actual ClassroomSession object, so we can
        # directly parse the field
        if type(session) is int:
            session = ClassroomSession.objects.get(id = session)

        if type(session) is ClassroomSession:
            if session.class_code is None:
                raise ValidationError((f'{session} is no longer active'), 
                                    params={'session': session, 'classroom': session.classroom})
            elif session.classroom is None:
                raise ValidationError((f'{session} is not associated with a classroom'),
                                    params={'session': session, 'classroom': session.classroom})
        else:
            raise ValidationError(f'{session} is not of type ClassroomSession or valid Django ID', 
                                  params={'session': session})


    ''' Attendance transaction fields '''
    session = models.ForeignKey('ClassroomSession', validators=[validate_session], on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    time = models.DateTimeField(editable=False)
        

    ''' Validates the attendance transaction as a whole '''
    def clean(self):
        # Check that the student is on the session classroom's roster.
        if self.student not in self.session.classroom.students.all():
            raise ValidationError((f'{self.student} is not on the roster for {self.session.classroom}'), 
                                  params={'student': self.student, 'classroom': self.session.classroom})


    ''' Saves the AttendanceTransaction '''
    def save(self, *args, **kwargs):
        # On creation, set the time field to current time
        if not self.id:
            self.time = timezone.now()
        return super(AttendanceTransaction, self).save(*args, **kwargs)


    ''' String representation '''
    def __str__(self):
        time_str = self.time.strftime('%m/%d/%Y %I:%M %p').lstrip('0').replace(' 0', ' ')
        return f'{self.id} {self.student.name} at {self.session.classroom.name} on {time_str}'


'''
Classrooom session model
- Stores records of periods where classes were active
'''
class ClassroomSession(models.Model):

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


    ''' Classroom session fields '''
    classroom  = models.ForeignKey('Classroom', validators=[validate_classroom], on_delete=models.CASCADE)
    class_code = models.CharField(default=None, null=True, unique=True, editable=False, max_length=6) # Class code associated with this session
    start = models.DateTimeField(editable=False)
    end   = models.DateTimeField(default=None, blank=True, null=True)


    ''' Saves the classroom session '''
    def save(self, *args, **kwargs):

        # On creation, set start time field to current time
        if not self.id:
            self.start = timezone.now()
            self.class_code = get_random_string(6).upper()

        # If the end time has been indicated (i.e. the session is over),
        # remove the class code
        if self.end is not None:
            self.class_code = None

        return super(ClassroomSession, self).save(*args, **kwargs)



    ''' String representation '''
    def __str__(self):
        start_date = self.start.strftime('%m/%d/%Y')
        start_str = self.start.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')

        if self.end is None:
            return f'({self.class_code}) {self.classroom.department} {self.classroom.number} on {start_date}, {start_str}'
        else:
            end_str = self.end.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            return f'(inactive) {self.classroom.department} {self.classroom.number} on {start_date}, {start_str} to {end_str}'
    