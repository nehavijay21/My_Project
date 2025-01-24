from django.shortcuts import render, get_object_or_404, redirect
from .models import Programme
from .forms import ProgramForm

def index(request):
    return render(request, 'index.html')

def manage_programs(request):
    return render(request, 'manage_programs.html')

def manage_rooms(request):
    return render(request, 'manage_rooms.html')

# Add more views as needed


def program_list(request):
    programs = Programme.objects.all()
    return render(request, 'program_list.html', {'programs': programs})

def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_programs')
    else:
        form = ProgramForm()
    return render(request, 'add_program.html', {'form': form})

def edit_program(request, pk):
    program = get_object_or_404(Programme, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('manage_programs')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'add_program.html', {'form': form})

def delete_program(request, pk):
    program = get_object_or_404(Programme, pk=pk)
    if request.method == 'POST':
        program.delete()
        return redirect('manage_programs')
    return render(request, 'delete_program.html', {'program': program})
