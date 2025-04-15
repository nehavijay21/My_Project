from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.timezone import now
from .models import Programme, Room, Course, Exam, Timetable, Teacher, DutyAllotment, DutyPreference
from .forms import ProgramForm, RoomForm, CourseForm, ExamForm, TimetableForm, TeacherForm, DutyAllotmentForm, DutyPreferenceForm
from datetime import datetime
from django.utils.dateparse import parse_date  # Import parse_date
from django.urls import reverse
import pandas as pd
from django.shortcuts import render, redirect
from .models import ExamAttendance, Student, StudentExam
from django.contrib import messages




@login_required()
def index(request):
    return render(request, 'index.html')

@login_required()
def manage_programs(request):
    return render(request, 'manage_programs.html')

@login_required()
def manage_rooms(request):
    return render(request, 'manage_rooms.html')

@login_required()
def manage_course(request):
    return render(request, 'manage_course.html')

@login_required()
def manage_exam(request):
    return render(request, 'manage_exam.html')

@login_required()
def manage_timetable(request):
    return render(request, 'manage_timetable.html')

@login_required()
def manage_teacher(request):
    return render(request, 'manage_teacher.html')

@login_required()
def manage_duty(request):
    duties = DutyAllotment.objects.all()  # Fetch duty allotments from database
    return render(request, 'duty_allotment.html', {'duties': duties})

@login_required()
def manage_preference(request):
    return render(request, 'manage_preference.html')

def chief_group_required(user):
    return user.groups.filter(name='Chief').exists()

def teacher_group_required(user):
    return user.groups.filter(name='Teacher').exists()

@login_required
def dashboard_view(request):
    user = request.user
    is_teacher = user.groups.filter(name='teacher').exists()
    is_chief = user.groups.filter(name='chief').exists()

    # Fetch ongoing exams based on Timetable dates
    ongoing_exams = Exam.objects.filter(timetable__date__gte=now().date()).distinct()

    # Fetch duty allotments and preferences for teachers
    if is_teacher:
        duty_allotments = DutyAllotment.objects.filter(teacher=user.teacher)
        duty_preferences = DutyPreference.objects.filter(teacher=user.teacher)
    else:  # Chief sees everything
        duty_allotments = DutyAllotment.objects.all()
        duty_preferences = DutyPreference.objects.all()

    context = {
        'is_teacher': is_teacher,
        'is_chief': is_chief,
        'ongoing_exams': ongoing_exams,
        'duty_allotments': duty_allotments,
        'duty_preferences': duty_preferences
    }
    return render(request, 'index.html', context)
    
@login_required()
@user_passes_test(chief_group_required)
def program_list(request):
    programs = Programme.objects.all()
    return render(request, 'program_list.html', {'programs': programs})

@login_required()
@user_passes_test(chief_group_required)
def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('program_list')
    else:
        form = ProgramForm()
    return render(request, 'add_program.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def edit_program(request, pk):
    program = get_object_or_404(Programme, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('program_list')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'add_program.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def delete_program(request, pk):
    program = get_object_or_404(Programme, pk=pk)
    if request.method == 'POST':
        program.delete()
        return redirect('program_list')
    return render(request, 'delete_program.html', {'program': program})

@login_required()
@user_passes_test(chief_group_required)
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

@login_required()
@user_passes_test(chief_group_required)
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'add_room.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'delete_room.html', {'room': room})

from django.db.models import IntegerField
from django.db.models.functions import Cast

import re
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course  # Ensure correct import

@login_required()
@user_passes_test(chief_group_required)
def course_list(request):
    order = request.GET.get('order', 'asc')  # Default to ascending

    # Extract numbers from course_code safely
    def extract_number(course):
        match = re.search(r'\d+', course.course_code)  # Extract first number
        return int(match.group()) if match else float('inf')  # Use high value if no number

    courses = list(Course.objects.all())  # Convert queryset to list for sorting

    # Sort using extracted numbers
    courses.sort(key=lambda c: extract_number(c), reverse=(order == 'desc'))

    return render(request, 'course_list.html', {'courses': courses, 'order': order})




@login_required()
@user_passes_test(chief_group_required)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})

@login_required()
@user_passes_test(chief_group_required)
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'delete_course.html', {'course': course})


from django.urls import reverse


@login_required()
@user_passes_test(chief_group_required)
def exam_list(request):
    exam = Exam.objects.all().order_by('-active', 'sem', 'year')
    return render(request, 'exam_list.html', {'exam': exam})


@login_required()
@user_passes_test(chief_group_required)
def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'add_exam.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def edit_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'add_exam.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def delete_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        return redirect('exam_list')
    return render(request, 'delete_exam.html', {'exam': exam})

@login_required()
@user_passes_test(chief_group_required)
def timetable_list(request):
    timetable= Timetable.objects.all()
    return render(request, 'timetable_list.html', {'timetable': timetable})

@login_required()
@user_passes_test(chief_group_required)
def add_timetable(request):
    ongoing_exams = Exam.objects.filter(active=True)  # Only active exams

    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable_list')
    else:
        form = TimetableForm()

    # Apply filtered exams to the form's exam field
    form.fields['exam'].queryset = ongoing_exams

    return render(request, 'add_timetable.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def edit_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    ongoing_exams = Exam.objects.filter(active=True)

    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('timetable_list')
    else:
        form = TimetableForm(instance=timetable)

    form.fields['exam'].queryset = ongoing_exams

    return render(request, 'add_timetable.html', {'form': form})


@login_required()
@user_passes_test(chief_group_required)
def delete_timetable(request, pk):
    timetable= get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        return redirect('timetable_list')
    return render(request, 'delete_timetable.html', {'timetable': timetable})


from django.http import JsonResponse
from .models import Course, Exam

def get_courses_by_exam(request):
    exam_id = request.GET.get('exam_id')
    if exam_id:
        try:
            exam = Exam.objects.get(pk=exam_id)
            courses = Course.objects.filter(sem=exam.sem)
            data = [{'id': c.pk, 'name': f'{c.course_code} - {c.course_title}'} for c in courses]
            return JsonResponse({'courses': data})
        except Exam.DoesNotExist:
            return JsonResponse({'error': 'Invalid exam ID'}, status=400)
    return JsonResponse({'error': 'No exam ID provided'}, status=400)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .models import Teacher
from .forms import TeacherForm, TeacherEditForm  # Add TeacherEditForm separately (without password)

@login_required()
@user_passes_test(chief_group_required)
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})

@login_required()
@user_passes_test(chief_group_required)
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Teacher added successfully!")
                return redirect('teacher_list')
            except Exception as e:
                messages.error(request, f"Error saving teacher: {e}")
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = TeacherForm()
    
    return render(request, 'add_teacher.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    user = teacher.user

    if request.method == "POST":
        form = TeacherEditForm(request.POST, instance=teacher)  # Only TeacherEditForm (no password)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated successfully!")
            return redirect('teacher_list')
    else:
        form = TeacherEditForm(instance=teacher)

    return render(request, 'add_teacher.html', {'form': form, 'edit_mode': True})

@login_required()
@user_passes_test(chief_group_required)
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.user.delete()
        return redirect('teacher_list')
    return render(request, 'delete_teacher.html', {'teacher': teacher})

@login_required()
@user_passes_test(chief_group_required)
def change_teacher_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect('teacher_list')
    else:
        form = PasswordChangeForm(user)

    full_name = f"{user.first_name} {user.last_name}"
    return render(request, 'change_password.html', {'form': form, 'full_name': full_name})


from django.contrib.auth.forms import SetPasswordForm

@login_required()
@user_passes_test(chief_group_required)
def reset_teacher_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Password reset successfully for {user.username}.')
            return redirect('teacher_list')
    else:
        form = SetPasswordForm(user)

    full_name = f"{user.first_name} {user.last_name}"
    return render(request, 'reset_password.html', {'form': form, 'full_name': full_name})


@login_required()
@user_passes_test(chief_group_required)
def duty_allotment(request):
    # Fetch all examination dates from the Timetable model
    exam_dates = Timetable.objects.all().order_by('date')

    # Count the number of duties assigned for each exam date
    duty_counts = {date.date: DutyAllotment.objects.filter(date=date.date).count() for date in exam_dates}

    return render(request, 'duty_allotment.html', {'exam_dates': exam_dates, 'duty_counts': duty_counts})

@login_required()
@user_passes_test(chief_group_required)
def manage_duty_allotments(request):
    selected_date = request.GET.get('date')  # Get date from the URL parameter
    if selected_date:
        duties = DutyAllotment.objects.filter(date=selected_date)  # Filter duties by selected date
    else:
        duties = DutyAllotment.objects.all()  # Show all duties if no date is selected

    return render(request, 'manage_duty_allotments.html', {'duties': duties, 'selected_date': selected_date})


@login_required()
@user_passes_test(chief_group_required)
def duty_list(request):
    date_str = request.GET.get('date')  # Get the date from URL parameters
    formatted_date = None  # Initialize formatted_date

    if date_str:
        # Try parsing the date in both possible formats
        formatted_date = parse_date(date_str)  # Handles 'YYYY-MM-DD' format
        if not formatted_date:
            try:
                formatted_date = datetime.strptime(date_str, "%b. %d, %Y").date()  # Handles 'Feb. 19, 2025' format
            except ValueError:
                formatted_date = None  # If conversion fails, return None

    # Query duties for the selected date, only show duties where a teacher is assigned
    duties = DutyAllotment.objects.filter(date=formatted_date, teacher__isnull=False) if formatted_date else []

    return render(request, 'duty_list.html', {'duties': duties, 'selected_date': formatted_date})


from django.utils.dateparse import parse_date
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Teacher, DutyAllotment
from .forms import DutyAllotmentForm

@login_required()
@user_passes_test(chief_group_required)
def add_duty(request):
    selected_date = request.GET.get('date', None)
    
    # Debugging: Print selected_date to check if it's coming in correct format
    print("Received date from URL:", selected_date)

    if not selected_date:
        messages.error(request, "No date provided. Please select a valid date.")
        return redirect('duty_allotment')

    # Try parsing YYYY-MM-DD format
    formatted_date = parse_date(selected_date)

    if not formatted_date:
        messages.error(request, f"Invalid date format received: {selected_date}")
        return redirect('duty_allotment')

    # Debugging: Print formatted date
    print("Parsed date:", formatted_date)

    # Fetch teachers who prefer this date
    preferred_teachers = Teacher.objects.filter(duty_preferences__pref_date=formatted_date).distinct()

    # Add duty count for each teacher
    for teacher in preferred_teachers:
        teacher.duty_counts = DutyAllotment.objects.filter(teacher=teacher, date=formatted_date).count()

    if request.method == 'POST':
        form = DutyAllotmentForm(request.POST)
        if form.is_valid():
            duty = form.save(commit=False)
            duty.date = formatted_date  # Ensure correct date is saved
            duty.save()
            messages.success(request, "Duty allotted successfully!")
            return redirect(reverse('duty_list') + f"?date={selected_date}")
        else:
            messages.error(request, "Form is invalid. Please check the entered data.")
    else:
        # Initialize form with correct date
        form = DutyAllotmentForm(initial={'date': formatted_date})

    return render(request, 'add_duty.html', {
        'form': form,
        'selected_date': formatted_date.strftime('%Y-%m-%d'),
        'preferred_teachers': preferred_teachers,
    })


    
@login_required()
@user_passes_test(chief_group_required)
def edit_duty(request, pk):
    duty = get_object_or_404(DutyAllotment, pk=pk)
    if request.method == 'POST':
        form = DutyAllotmentForm(request.POST, instance=duty)
        if form.is_valid():
            form.save()
            return redirect('duty_list')
    else:
        form = DutyAllotmentForm(instance=duty)
    return render(request, 'add_duty.html', {'form': form})

@login_required()
@user_passes_test(chief_group_required)
def delete_duty(request, pk):
    duty = get_object_or_404(DutyAllotment, pk=pk)  # Get the duty object or return 404
    selected_date = duty.date.strftime("%Y-%m-%d")  # Convert date to 'YYYY-MM-DD' format

    if request.method == 'POST':
        duty.delete()
        messages.success(request, "Duty deleted successfully!")

        # Redirect back to duty list with the selected date
        return redirect(f"{reverse('duty_list')}?date={selected_date}")

    return render(request, 'delete_duty.html', {'duty': duty})

@login_required()
def preference_list(request):
    teacher=Teacher.objects.get(user=request.user)
    preferences = DutyPreference.objects.filter(teacher=teacher)
    return render(request, 'preference_list.html', {'preferences': preferences})

@login_required()
@user_passes_test(teacher_group_required)
def add_preference(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = DutyPreferenceForm(request.POST, user=teacher)
        if form.is_valid():
            selected_dates = form.cleaned_data['pref_dates']
            for date in selected_dates:
                DutyPreference.objects.create(teacher=teacher, pref_date=date)
            messages.success(request, "Preferences saved successfully.")
            return redirect('preference_list')
    else:
        form = DutyPreferenceForm(user=teacher)

    return render(request, 'add_preference.html', {'form': form})

@login_required()
@user_passes_test(teacher_group_required)
def edit_preference(request, pk):
    preference = get_object_or_404(DutyPreference, pk=pk)
    if request.method == 'POST':
        form = DutyPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            return redirect('preference_list')
    else:
        form = DutyPreferenceForm(instance=preference)
    return render(request, 'add_preference.html', {'form': form})

@login_required()
@user_passes_test(teacher_group_required)
def delete_preference(request, pk):
    preference = get_object_or_404(DutyPreference, pk=pk)
    if request.method == 'POST':
        preference.delete()
        return redirect('preference_list')
    return render(request, 'delete_preference.html', {'preference': preference})

@login_required
@user_passes_test(teacher_group_required)
def duty_history(request):
    user = request.user

    # Ensure the user has a linked teacher profile
    if hasattr(user, 'teacher'):
        teacher = user.teacher
        duty_records = DutyAllotment.objects.filter(teacher=teacher)
    else:
        duty_records = []

    return render(request, 'duty_history.html', {'duty_records': duty_records})


@login_required()
@user_passes_test(chief_group_required)
def upload_nominal_roll(request):
    print("Upload view triggered")

    if request.method == 'POST':
        print("POST method confirmed")
        print("FILES content:", request.FILES)

        excel_file = request.FILES.get('file')
        if not excel_file:
            messages.error(request, "No file uploaded.")
            print("❌ No file found in request.FILES")
            return redirect('setup_nominal_roll')

        try:
            df = pd.read_excel(excel_file)
            print("✅ Excel file read successfully")
            print("🧾 Columns found in Excel:", df.columns.tolist())

            for _, row in df.iterrows():
                scribe_number = row.get('Scribe', '')
                scribe_number = scribe_number if pd.notna(scribe_number) and str(scribe_number).strip() else None

                exam_attendance, _ = ExamAttendance.objects.get_or_create(
                    date=row['Date'],
                    course_code=row['Course Code'],
                    course_title=row['Course Title']
                )

                student, _ = Student.objects.get_or_create(
                    register_number=row['Register Number'],
                    defaults={'scribe_number': scribe_number}
                )

                # Update scribe_number if different and not None
                if student.scribe_number != scribe_number and scribe_number:
                    student.scribe_number = scribe_number
                    student.save()

                StudentExam.objects.get_or_create(
                    exam_attendance=exam_attendance,
                    student=student
                )

            messages.success(request, 'Nominal Roll uploaded successfully!')

        except Exception as e:
            messages.error(request, f'Error uploading file: {str(e)}')
            print(f"❌ Error reading Excel: {e}")

        return redirect('setup_nominal_roll')

    # GET request → show summary
   # Show summary
    summary = {}
    for attendance in ExamAttendance.objects.all():
        student_exams = StudentExam.objects.filter(exam_attendance=attendance)

        total_students = student_exams.count()
        absent = student_exams.filter(is_absent=True).count()
        present = total_students - absent
        scribe_students = student_exams.filter(student__scribe_number__iexact='yes').count()

        summary[attendance.date] = {
            'total_students': total_students,
            'present': present,
            'absent': absent,
        }



    context = {
        'summary': summary,
    }
    return render(request, 'setup_nominal_roll.html', context)



@login_required()
@user_passes_test(chief_group_required)

def delete_nominal_roll(request):
    StudentExam.objects.all().delete()
    ExamAttendance.objects.all().delete()
    Student.objects.all().delete()

    messages.success(request, "All nominal roll entries deleted.")
    return redirect('setup_nominal_roll')

# views.py
@login_required
@user_passes_test(chief_group_required)
def mark_attendance(request, date):
    exam_attendance = get_object_or_404(ExamAttendance, date=date)
    student_exams = StudentExam.objects.filter(exam_attendance=exam_attendance)

    if request.method == 'POST':
        if 'clear' in request.POST:
            for se in student_exams:
                se.is_absent = False  # Mark all as present
                se.save()
            messages.success(request, "All attendance cleared. Everyone marked as present.")
        else:
            absent_ids = request.POST.getlist('absent')
            for se in student_exams:
                se.is_absent = str(se.student.register_number) in absent_ids
                se.save()
            messages.success(request, "Attendance successfully recorded.")
        return redirect('mark_attendance', date=date)

    total = student_exams.count()
    absent = student_exams.filter(is_absent=True).count()
    present = total - absent

    context = {
        'exam_attendance': exam_attendance,
        'student_exams': student_exams,
        'date': date,
        'total': total,
        'present': present,
        'absent': absent,
    }
    return render(request, 'mark_attendance.html', context)

