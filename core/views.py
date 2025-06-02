from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Note
from .forms import NoteSearchForm
from .forms import NoteSearchForm
from .models import Notification
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse
from .forms import CommentForm

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': notifications})
def home(request):
    notes = Note.objects.all().order_by('-uploaded_at')
    return render(request, 'core/home.html', {'notes': notes})

def explore_notes(request):
    notes = Note.objects.all().order_by('-uploaded_at')
    comment_forms = {note.id: CommentForm() for note in notes}
    return render(request, 'core/explore_notes.html', {'notes': notes, 'comment_forms': comment_forms})


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
            form.save_m2m()
            messages.success(request, 'Note uploaded successfully!')

            # Remove or comment out this block:
            # followers = User.objects.filter(followed_subjects=note.subject)
            # for follower in followers.exclude(id=request.user.id):
            #     Notification.objects.create(
            #         user=follower,
            #         message=f"New note uploaded in {note.subject}!"
            #     )

            return redirect('upload')
    else:
        form = NoteForm()
    notes = Note.objects.all()
    return render(request, 'core/upload.html', {'form': form, 'notes': notes})

@login_required
def add_comment_to_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.user = request.user
            comment.save()
            # Notify note owner
            if note.uploaded_by != request.user:
                Notification.objects.create(
                    user=note.uploaded_by,
                    message=f"{request.user.username} commented on your note '{note.title}'."
                )
    return redirect('explore_notes')



@user_passes_test(lambda u: u.is_superuser)
def send_announcement(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        for user in User.objects.all():
            Notification.objects.create(
                user=user,
                message=f"Announcement: {message}"
            )
        messages.success(request, "Announcement sent!")
        return redirect('home')
    return render(request, 'core/send_announcement.html')



@login_required
def download_file(request, file_id):
    note = get_object_or_404(Note, id=file_id)
    # Your file sending logic here, for example:
    response = FileResponse(note.file_field.open(), as_attachment=True)

    # Add this notification code:
    if note.uploaded_by != request.user:
        Notification.objects.create(
            user=note.uploaded_by,
            message=f"{request.user.username} downloaded your note '{note.title}'."
        )

    return response

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.user = request.user
            comment.save()
            # Notify note owner
            if note.uploaded_by != request.user:
                Notification.objects.create(
                    user=note.uploaded_by,
                    message=f"{request.user.username} commented on your note '{note.title}'."
                )
            return redirect('note_detail', note_id=note.id)
    else:
        form = CommentForm()
    return render(request, 'core/note_detail.html', {'note': note, 'form': form})




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
