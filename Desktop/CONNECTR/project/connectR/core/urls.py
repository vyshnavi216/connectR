from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.user_login, name='login'),  # Login page
    path('logout/', views.user_logout, name='logout'),  # Logout
    path('upload/', views.upload_note, name='upload'),  # Upload notes
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),  # Delete file
    path('explore-notes/', views.explore_notes, name='explore_notes'),  # Explore notes
   
]

from django.contrib.auth import views as auth_views

urlpatterns += [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('download/<int:note_id>/', views.download_note, name='download_note'),
     path('note/<int:note_id>/', views.note_detail, name='note_detail'),
     path('report-note/<int:note_id>/', views.report_note, name='report_note'),
     path('rate/<int:note_id>/', views.rate_note, name='rate_note'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)