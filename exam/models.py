from django.db import models
from django.contrib.auth.models import User
def ordinal(n):
    try:
        n = int(n)
    except:
        return n
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


# Create your models here.
class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name

class Programme(models.Model):
    LEVEL_CHOICES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('FYUG','Four year UG'),
        ('IPG','Integrated PG'),
    ]
    programme_name = models.CharField(max_length=255)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.IntegerField()

    def __str__(self):
        return self.programme_name

# Course Model
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=50)
    course_title = models.CharField(max_length=150)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    exam_duration = models.IntegerField()
    sem = models.IntegerField()
    syllabus_year = models.IntegerField()

    def __str__(self):
        return self.course_title
    
    def get_dept_name(self):  
        return self.dept_id.dept_name

# Exam Model
class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    sem = models.IntegerField()
    year = models.IntegerField()
    level = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    month = models.CharField(max_length=50)

    def __str__(self):
        return f"{ordinal(self.sem)} Semester {self.level} Examination {self.month} {self.year}"


# Timetable Model
class Timetable(models.Model):
    SESSION_CHOICES = [
        ('Forenoon', 'Forenoon'),
        ('Afternoon', 'Afternoon'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    session = models.CharField(max_length=50, choices=SESSION_CHOICES)  # ✅ Add choices

    def __str__(self):
        return f"{self.course.course_code} - {self.course.course_title} on {self.date}"


# Room Model
class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_no = models.CharField(max_length=50)
    no_of_rows = models.IntegerField()
    no_of_columns = models.IntegerField()
    block_no = models.CharField(max_length=50)

    def __str__(self):
        return self.room_no

# Teacher Model


class Teacher(models.Model):
    DESIGNATION_CHOICES = [
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Guest Lecturer','Guest Lecturer'),
        ('Junior Lecturer','Junior Lecturer'),
        ('Professor','Professor')
    ]
    GENDER_CHOICES=[
        ('Female','Female'),
        ('Male','Male')
    ]
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True )
    phone_num=models.CharField(max_length=10,blank=True, null=True)
    designation=models.CharField(max_length=50, choices=DESIGNATION_CHOICES,default="Assistant Professor")
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default="Female")
    role=models.CharField(max_length=100,default="Teacher")

    def __str__(self):
        return self.user.username


# Duty Preference Model
class DutyPreference(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="duty_preferences")
    pref_date = models.DateField()

    def __str__(self):
        return f"Preference of {self.teacher.user.username} on {self.pref_date}"

    
class DutyAllotment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="duties")
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="duties")
    hours = models.PositiveIntegerField()

    def __str__(self):
        return f"Duty of {self.teacher.user.username} in Room {self.room.room_no} on {self.date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'date'], name='unique_teacher_duty_per_day')
        ]





class Examination(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)  # Links to Exam
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Links to Course
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')])

    def __str__(self):
        return f"{self.course.course_title} on {self.date}"

# models.py

from django.db import models
class ExamAttendance(models.Model):
    date = models.DateField()
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=255)

    class Meta:
        unique_together = ('date', 'course_code')

    def __str__(self):
        return f"{self.date} - {self.course_code} - {self.course_title}"


class Student(models.Model):
    register_number = models.CharField(max_length=20)
    scribe_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.register_number


class StudentExam(models.Model):
    exam_attendance = models.ForeignKey(ExamAttendance, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_absent= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.register_number} - {self.exam_attendance.course_code}"
