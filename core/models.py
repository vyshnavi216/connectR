

# class Note(models.Model):
#     SUBJECT_CHOICES = [
#         ('maths', 'Mathematics'),
#         ('physics', 'Physics'),
#         ('cs', 'Computer Science'),
#         ('other', 'Other'),
#     ]

#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
#     file = models.FileField(upload_to='notes/')
#     uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    SUBJECT_CHOICES = [
        ('maths', 'Mathematics'),
        ('physics', 'Physics'),
        ('cs', 'Computer Science'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
