from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage_programs/', views.manage_programs, name='manage_programs'),
    path('manage_rooms/', views.manage_rooms, name='manage_rooms'),
    # Add more paths as needed

    path('program_list/', views.program_list, name='program_list'),
    path('add-program/', views.add_program, name='add_program'),
    path('edit-program/<int:pk>/', views.edit_program, name='edit_program'),
    path('delete-program/<int:pk>/', views.delete_program, name='delete_program'),
]
