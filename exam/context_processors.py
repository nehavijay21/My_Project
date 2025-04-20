from django.contrib.auth.models import Group
from .models import Exam, DutyAllotment, DutyPreference

def is_chief(request):
    return {'is_chief': request.user.groups.filter(name='Chief').exists()}

def is_teacher(request):
    context = {'is_teacher': request.user.groups.filter(name='Teacher').exists()}
    
    if request.user.is_authenticated and context['is_teacher']:
        teacher = request.user.teacher  # Assuming a OneToOne relationship exists

        # Fetch ongoing exams
        ongoing_exams = Exam.objects.filter(active=True)  


        # Fetch duty allotments for this teacher
        duty_allotted_dates = DutyAllotment.objects.filter(teacher=teacher)

        # Fetch preferred duty dates for this teacher
        preferred_dates = DutyPreference.objects.filter(teacher=teacher)

        context.update({
            'ongoing_exams': ongoing_exams,
            'duty_allotted_dates': duty_allotted_dates,
            'preferred_dates': preferred_dates,
        })

    return context
