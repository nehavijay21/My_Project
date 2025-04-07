from django import forms
from .models import Programme, Department
from .models import Room,Course,Exam
from .models import Timetable
from .models import Teacher
from .models import DutyAllotment
from .models import DutyPreference

class ProgramForm(forms.ModelForm):
    # Choices for level field
    LEVEL_CHOICES =[
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('FYUG','Four year UG'),
        ('IPG','Integrated PG'),
    ]
    
    # Dropdown for level field
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Dropdown for department field, linked to the Department table
    dept = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Department"
    )

    class Meta:
        model = Programme
        fields = ['programme_name', 'dept', 'level', 'duration']
        widgets = {
            'programme_name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_no', 'no_of_rows', 'no_of_columns', 'block_no']
        widgets = {
            'room_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Room Number'}),
            'no_of_rows': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Number of Rows'}),
            'no_of_columns': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Number of Columns'}),
            'block_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Block Number'}),
        }
        labels = {
            'room_no': 'Room Number',
            'no_of_rows': 'Number of Rows',
            'no_of_columns': 'Number of Columns',
            'block_no': 'Block Number',
        }


class CourseForm(forms.ModelForm):
    dept_name = forms.CharField(
        label="Department Name",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Course
        fields = [
            'course_code', 
            'course_title', 
            'dept_id',  
            'exam_duration', 
            'sem', 
            'syllabus_year'
        ]
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Code'}),
            'course_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Title'}),
            'dept_id': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for Department
            'exam_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Exam Duration'}),
            'sem': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Semester'}),
            'syllabus_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Syllabus Year'}),
        }
        labels = {
            'course_code': 'Course Code',
            'course_title': 'Course Title',
            'dept_id': 'Department',
            'exam_duration': 'Exam Duration',
            'sem': 'Semester',
            'syllabus_year': 'Syllabus Year',
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['dept_name'].initial = self.instance.dept_id.dept_name  # Set read-only department name


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['sem', 'year', 'level', 'active', 'month']
        widgets = {
            'sem': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Semester'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year'}),
            'level': forms.Select(choices=[
            ('UG', 'Undergraduate'),
            ('PG', 'Postgraduate'),
            ('FYUG','Four year UG'),
            ('IPG','Integrated PG')
            ], attrs={'class': 'form-control'}),
            'active': forms.Select(choices=[
                (True, 'Yes'),
                (False, 'No')
            ], attrs={'class': 'form-control'}),
            'month': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Month'}),
        }
        labels = {
            'sem': 'Semester',
            'year': 'Year',
            'level': 'Level',
            'active': 'Active',
            'month': 'Month',
        }

from django import forms
from django.utils import timezone
from .models import Timetable, Course

class TimetableForm(forms.ModelForm):
    SESSION_CHOICES = [
        ('Forenoon', 'Forenoon'),
        ('Afternoon', 'Afternoon'),
    ]

    session = forms.ChoiceField(
        choices=SESSION_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Timetable
        fields = ['exam', 'course', 'date', 'session']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(TimetableForm, self).__init__(*args, **kwargs)
        
        # Modify the display format of the course field
        self.fields['course'].queryset = Course.objects.all()
        self.fields['course'].label_from_instance = lambda obj: f"{obj.course_code} - {obj.course_title}"

        self.fields['course'].empty_label = '--------'

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("Error:Timetable cannot be scheduled for a past date. Please select a valid date.")
        return date




from django import forms
from django.contrib.auth.models import User, Group
from .models import Teacher, Department
import re


# Validator for phone numbers
def validate_phone(value):
    if not re.match(r'^\d{10}$', value):
        raise forms.ValidationError('Invalid phone number. Please enter a 10-digit number.')


class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )
    phone_num = forms.CharField(
        max_length=10,
        required=True,
        validators=[validate_phone],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit Phone Number'})
    )
    designation = forms.ChoiceField(
        choices=Teacher.DESIGNATION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=Teacher.GENDER_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dept = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=[('Teacher', 'Teacher'), ('Examination Chief', 'Examination Chief')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="Password",
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'dept', 'designation', 'role', 'phone_num', 'gender']

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.instance.pk:  # If updating an existing user
            user = User.objects.get(pk=self.instance.pk)

        user.set_password(self.cleaned_data['password'])  # Hash the password
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()

            # Get or create Teacher instance
            teacher, created = Teacher.objects.get_or_create(
            user=user,
            defaults={
                'phone_num': self.cleaned_data['phone_num'],
                'designation': self.cleaned_data['designation'],
                'gender': self.cleaned_data['gender'],
                'dept': self.cleaned_data['dept'],
                'role': self.cleaned_data['role'],
            }
            )

            if not created:
                teacher.phone_num = self.cleaned_data['phone_num']
                teacher.designation = self.cleaned_data['designation']
                teacher.gender = self.cleaned_data['gender']
                teacher.dept = self.cleaned_data['dept']
                teacher.role = self.cleaned_data['role']
                teacher.save()

            # Update Group
            role = self.cleaned_data['role']
            if role == 'Examination Chief':
                group = Group.objects.get(name='Examination Chief')
                user.is_staff = True
            else:
                group = Group.objects.get(name='Teacher')

            user.groups.clear()  # Remove previous group
            user.groups.add(group)
            user.save()

        return user  # ✅ Correctly placed inside the method



class DutyAllotmentForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),  # Show all teachers
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a Teacher"
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = DutyAllotment
        fields = ['teacher', 'date', 'room', 'hours']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }



from django import forms
from .models import DutyPreference, Timetable

class DutyPreferenceForm(forms.ModelForm):
    pref_date = forms.ChoiceField(choices=[], label="Preferred Date", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DutyPreference
        fields = ['teacher', 'pref_date']
        widgets = {
            'teacher': forms.HiddenInput(),  # Hide the teacher field
        }
        labels = {
            'pref_date': 'Preferred Date',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        exam_dates = Timetable.objects.values_list('date', flat=True).distinct()
        self.fields['pref_date'].choices = [(date, date) for date in exam_dates]

        if user:
            self.fields['teacher'].initial = user  # Set the logged-in teacher
