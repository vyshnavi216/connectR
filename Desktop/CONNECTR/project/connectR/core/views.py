from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Note
from .forms import CustomRegistrationForm
from django.http import FileResponse, Http404
import os
from .models import Profile

def home(request):
    notes = Note.objects.all().order_by('-uploaded_at')
    return render(request, 'core/home.html', {'notes': notes})




from .forms import CustomRegistrationForm

def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Automatically validates and saves the user
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
        else:
            # If the form is invalid, display the errors
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


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
    # notes = Note.objects.all()
    notes = Note.objects.filter(uploaded_by=request.user)
    return render(request, 'core/upload.html', {'form': form, 'notes': notes})


from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Note  # Use the correct model name

def delete_file(request, file_id):
    note = get_object_or_404(Note, id=file_id)  # Use the Note model
    note.delete()
    return redirect(reverse('home'))  # Redirect to the home page or another page


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # This hashes the password
        if commit:
            user.save()
            print("User is_active:", user.is_active)
        return user


from django.shortcuts import render
from django.db.models import Q

# Define semester-to-subject mapping
SEMESTER_SUBJECTS = {
    "1": ["maths", "C programming", "Physics", "introduction to cyber security", "introduction to design thinking", "electronics and communication"],
    "2": ["maths", "C++", "Chemistry", "CAED", "Engineering Exploration", "Electrical Engineering"],
    "3": ["maths", "DSA", "Operating System", "DDCO", "EDC", "Python", "Java", "SCR"],
    "4": ["maths", "DBMS", "Unix", "IIOT", "DAA", "FSD"],
   
    # Add more semesters and their corresponding subjects here
}

def explore_notes(request):
    notes = Note.objects.all()

    # Get filter values from the request
    semester = request.GET.get('semester')
    subject = request.GET.get('subject')
    file_type = request.GET.get('file_type')
    uploaded_by = request.GET.get('uploaded_by')
    query = request.GET.get('q')

    # Filter notes based on the selected semester
    if semester:
        notes = notes.filter(semester=semester)

    # Filter subjects dynamically based on the selected semester
    if semester and semester in SEMESTER_SUBJECTS:
        subjects = SEMESTER_SUBJECTS[semester]
    else:
        # Default to all subjects if no semester is selected
        subjects = Note.objects.values_list('subject', flat=True).distinct()

    # Apply additional filters
    if subject:
        notes = notes.filter(subject=subject)
    if file_type:
        notes = notes.filter(file__iendswith=file_type)
    if uploaded_by:
        notes = notes.filter(uploaded_by__username=uploaded_by)
    if query:
        notes = notes.filter(
            Q(subject__icontains=query) |
            Q(description__icontains=query) |
            Q(title__icontains=query)
        )

    # Define all semesters explicitly
    semesters = ["1", "2", "3", "4", "5", "6", "7", "8"]

    # Get unique users for filters
    users = Note.objects.values_list('uploaded_by__username', flat=True).distinct()

    return render(request, 'core/explore_notes.html', {
        'notes': notes,
        'subjects': subjects,
        'semesters': semesters,
        'users': users,
    })

def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.views += 1
    note.save()
    return render(request, 'core/view_note.html', {'note': note})

def download_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.downloads += 1
    note.save()
    file_path = note.file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("File not found")
    # Then serve the file for download

from django.contrib.auth.decorators import login_required
from .models import Note, Feedback

@login_required
def user_dashboard(request):
    user = request.user
    notes = Note.objects.filter(uploaded_by=user)
    
    total_uploads = notes.count()
    total_downloads = sum(note.downloads for note in notes)
    total_views = sum(note.views for note in notes)
    
    top_notes = notes.order_by('-views')[:5]
    
    # Streak (example: uploads in the last 7 days)
    from datetime import timedelta
    from django.utils import timezone
    last_week = timezone.now() - timedelta(days=7)
    weekly_uploads = notes.filter(upload_date__gte=last_week).count()
    
    context = {
        'total_uploads': total_uploads,
        'total_downloads': total_downloads,
        'total_views': total_views,
        'top_notes': top_notes,
        'weekly_uploads': weekly_uploads,
    }
    return render(request, 'core/user_dashboard.html', context)

from django.http import HttpResponse

def report_note(request, note_id):
    return HttpResponse("Report feature coming soon!")

from .models import Note, Rating

def rate_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        stars = int(request.POST.get('rating'))
        existing_rating = Rating.objects.filter(note=note, user=request.user).first()
        if existing_rating:
            existing_rating.stars = stars
            existing_rating.save()
        else:
            Rating.objects.create(note=note, user=request.user, stars=stars)
    return redirect('view_note', note_id=note_id)

def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    ratings = Rating.objects.filter(note=note)
    average_rating = round(sum(r.stars for r in ratings) / ratings.count(), 1) if ratings.exists() else None
    related_notes = Note.objects.filter(author=note.author).exclude(id=note.id)[:4]
    return render(request, 'view_note.html', {
        'note': note,
        'related_notes': related_notes,
        'average_rating': average_rating
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})

