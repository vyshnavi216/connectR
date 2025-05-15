from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'subject', 'file']
class NoteSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)