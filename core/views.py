from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Note

def home(request):
    notes = Note.objects.all().order_by('-uploaded_at')
    return render(request, 'core/home.html', {'notes': notes})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'core/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'core/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

from .forms import NoteForm
from .models import Note
from django.contrib.auth.decorators import login_required

# @login_required
# def upload_note(request):
#     if request.method == 'POST':
#         form = NoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.uploaded_by = request.user
#             note.save()
#             messages.success(request, 'Note uploaded successfully!')
#             return redirect('home')
#     else:
#         form = NoteForm()
#     return render(request, 'core/upload.html', {'form': form})

@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully!')
            return redirect('upload')  # Redirect to the upload page
    else:
        form = NoteForm()

    # Fetch all notes to display
    notes = Note.objects.all()
    return render(request, 'core/upload.html', {'form': form, 'notes': notes})


from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Note  # Use the correct model name
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
def delete_file(request, file_id):
    # Fetch the Note instance by its ID
    note = get_object_or_404(Note, id=file_id)

    # Check if the logged-in user is the one who uploaded the file
    if note.uploaded_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete this file.")

    # If the user is authorized, delete the note
    note.delete()
    return redirect('home')  # Replace 'home' with the name of your desired redirect view
from django.shortcuts import render

def explore_notes(request):
    # Fetch the latest notes from the database
    notes = Note.objects.all().order_by('-uploaded_at')  # Adjust query as needed
    return render(request, 'core/explore_notes.html', {'notes': notes})