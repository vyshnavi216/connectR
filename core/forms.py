from django import forms
from .models import Note
from .models import Comment

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'subject', 'file']

class NoteSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Replace 'text' with the actual field(s) in your Comment model