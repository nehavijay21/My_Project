from django.urls import path
from . import views
from .views import duty_allotment 
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),


    path('manage_programs/', views.manage_programs, name='manage_programs'),
    path('manage_rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage_course/', views.manage_course, name='manage_course'),
    path('manage_exam/', views.manage_exam, name='manage_exam'),
    path('manage_timetable/', views.manage_timetable, name='manage_timetable'),
    path('manage_teacher/', views.manage_teacher, name='manage_teacher'),
    path('manage_duty/', views.manage_duty, name='manage_duty'),
    # Add more paths as needed

    path('program_list/', views.program_list, name='program_list'),
    path('add-program/', views.add_program, name='add_program'),
    path('edit-program/<int:pk>/', views.edit_program, name='edit_program'),
    path('delete-program/<int:pk>/', views.delete_program, name='delete_program'),

    path('room_list/', views.room_list, name='room_list'),
    path('add-room/', views.add_room, name='add_room'),
    path('edit-room/<int:pk>/', views.edit_room, name='edit_room'),
    path('delete-room/<int:pk>/', views.delete_room, name='delete_room'),

    path('course_list/', views.course_list, name='course_list'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:pk>/', views.delete_course, name='delete_course'),

    path('exam_list/', views.exam_list, name='exam_list'),
    path('add-exam/', views.add_exam, name='add_exam'),
    path('edit-exam/<int:pk>/', views.edit_exam, name='edit_exam'),
    path('delete-exam/<int:pk>/', views.delete_exam, name='delete_exam'),
    

    path('timetable_list/', views.timetable_list, name='timetable_list'),
    path('add-timetable/', views.add_timetable, name='add_timetable'),
    path('edit-timetable/<int:pk>/', views.edit_timetable, name='edit_timetable'),
    path('delete-timetable/<int:pk>/', views.delete_timetable, name='delete_timetable'),
    path('ajax/get-courses/', views.get_courses_by_exam, name='get_courses_by_exam'),

    path('teacher_list/', views.teacher_list, name='teacher_list'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('edit-teacher/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('delete-teacher/<int:pk>/', views.delete_teacher, name='delete_teacher'),
    path('teacher/<int:user_id>/change-password/', views.change_teacher_password, name='change_teacher_password'),
    path('teacher/<int:user_id>/reset-password/', views.reset_teacher_password, name='reset_teacher_password'),

    path('duty-allotment/', duty_allotment, name='duty_allotment'),
    path('duty_list/', views.duty_list, name='duty_list'),
    path('add-duty/', views.add_duty, name='add_duty'),
    path('edit-duty/<int:pk>/', views.edit_duty, name='edit_duty'),
    path('delete-duty/<int:pk>/', views.delete_duty, name='delete_duty'),

    path('preferences/', views.preference_list, name='preference_list'),
    path('preferences/add/', views.add_preference, name='add_preference'),
    path('preferences/edit/<int:pk>/', views.edit_preference, name='edit_preference'),
    path('preferences/delete/<int:pk>/', views.delete_preference, name='delete_preference'),

    path('duty-history/', views.duty_history, name='duty_history'),
    path('exam-attendance/', views.upload_nominal_roll, name='setup_nominal_roll'),
    path('exam-attendance/delete/', views.delete_nominal_roll, name='delete_nominal_roll'),
    path('exam-attendance/<str:date>/<str:course_code>/', views.mark_attendance, name='mark_attendance'),

    path('generate-excel/', views.generate_excel, name='generate_excel'),
    path('get-exam-dates/', views.get_exam_dates, name='get_exam_dates'),

     path('chief-duties/', views.chief_duty_history, name='chief_duty_history'),

]
