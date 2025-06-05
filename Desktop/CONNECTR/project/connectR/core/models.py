

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


# from django.db import models
# from django.contrib.auth.models import User

# class Note(models.Model):
#     SUBJECT_CHOICES = [
#         ('maths', 'Mathematics'),
#         ('physics', 'Physics'),
#         ('cs', 'Computer Science'),
#         ('other', 'Other'),
#     ]
#     from django.db import models
# from django.contrib.auth.models import User

# class Note(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     subject = models.CharField(max_length=100)  # Allow users to type the subject
#     semester = models.CharField(max_length=50)  # Add semester field
#     file = models.FileField(upload_to='notes/')
#     uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    SUBJECT_CHOICES = [
        ('maths', 'Mathematics'),
        ('physics', 'Physics'),
        ('cs', 'Computer Science'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=100)  # Or use choices=SUBJECT_CHOICES
    semester = models.CharField(max_length=50)
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class Feedback(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default-profile.png')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


from PIL import Image

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)


    

