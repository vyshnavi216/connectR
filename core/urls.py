from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_note, name='upload'),
    path('note/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('explore-notes/', views.explore_notes, name='explore_notes'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'), 
    path('note/<int:note_id>/add_comment/', views.add_comment_to_note, name='add_comment_to_note'),
    path('notifications/', views.notifications, name='notifications'),

]

