from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', views.password_change_view, name='password_change'),
    
    # Main pages
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Birthday API
    path('api/birthday-seen/', views.birthday_seen, name='birthday_seen'),
    
    # Health check for Railway deployment
    path('health/', views.health_check, name='health_check'),
]
