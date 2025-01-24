from django.contrib import admin
from .models import Department, Programme, Course, Exam, Timetable, Room, Teacher, DutyPreference, DutyAllotment

admin.site.register(Department)
admin.site.register(Programme)
admin.site.register(Course)
admin.site.register(Exam)
admin.site.register(Timetable)
admin.site.register(Room)
admin.site.register(Teacher)
admin.site.register(DutyPreference)
admin.site.register(DutyAllotment)