import random
import hashlib
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from .models import DailyThought, UserProfile


def get_daily_content():
    """Get daily thought and content based on date"""
    today = datetime.now()
    date_seed = today.strftime('%Y%m%d')
    
    # Get all active thoughts
    thoughts = list(DailyThought.objects.filter(is_active=True))
    
    if thoughts:
        # Use date-based hash for consistent daily selection
        hash_val = int(hashlib.md5(date_seed.encode()).hexdigest(), 16)
        thought = thoughts[hash_val % len(thoughts)]
    else:
        # Default thoughts if none in database
        default_thoughts = [
            {"content": "The lotus blooms most beautifully from the deepest and thickest mud.", "author": "Buddhist Proverb"},
            {"content": "Your strength is not measured by how much you can carry, but by how you rise after being broken.", "author": "Unknown"},
            {"content": "Every ending is a new beginning. Trust the journey.", "author": "Unknown"},
            {"content": "You are stronger than you know, more capable than you imagine, and loved more than you realize.", "author": "Unknown"},
            {"content": "The path to healing begins with a single breath of self-compassion.", "author": "Unknown"},
        ]
        thought_data = default_thoughts[hash_val % len(default_thoughts)]
        thought = type('obj', (object,), {
            'content': thought_data['content'],
            'author': thought_data['author'],
            'category': 'resilience'
        })
    
    return {
        'thought': thought,
        'date': today,
    }


def get_time_greeting():
    """Get time-appropriate greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return {
            'greeting': 'Good Morning',
            'theme': 'morning',
            'message': 'New beginnings await. Take a breath and begin.',
        }
    elif 11 <= hour < 17:
        return {
            'greeting': 'Good Afternoon',
            'theme': 'afternoon',
            'message': 'Persistence creates progress. You are doing well.',
        }
    elif 17 <= hour < 22:
        return {
            'greeting': 'Good Evening',
            'theme': 'evening',
            'message': 'Reflect on your day with kindness.',
        }
    else:
        return {
            'greeting': 'Good Night',
            'theme': 'night',
            'message': 'Rest is restoration. Tomorrow brings new light.',
        }


def login_view(request):
    """Custom login view with daily content and birthday recognition"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    error = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid credentials. Please try again."
    
    context = {
        'daily_content': get_daily_content(),
        'time_context': get_time_greeting(),
        'error': error,
        'is_birthday': datetime.now().day == 6 and datetime.now().month == 2,
    }
    
    return render(request, 'core/login.html', context)


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """Main dashboard with navigation to all modules"""
    # Get recent activity counts
    from notes.models import Note
    from diary.models import DiaryEntry
    from goals.models import Goal, Task
    
    recent_notes = Note.objects.filter(user=request.user).count()
    recent_diary = DiaryEntry.objects.filter(user=request.user).count()
    active_goals = Goal.objects.filter(user=request.user, status='active').count()
    pending_tasks = Task.objects.filter(goal__user=request.user, status='pending').count()
    
    context = {
        'recent_notes': recent_notes,
        'recent_diary': recent_diary,
        'active_goals': active_goals,
        'pending_tasks': pending_tasks,
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        profile = request.user.profile
        profile.display_name = request.POST.get('display_name', profile.display_name)
        profile.preferred_language = request.POST.get('preferred_language', profile.preferred_language)
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    return render(request, 'core/profile.html')


@login_required
def password_change_view(request):
    """Password change view"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'core/password_change.html', {'form': form})


@login_required
@require_POST
def birthday_seen(request):
    """Mark birthday message as seen"""
    try:
        profile = request.user.profile
        profile.birthday_message_seen_2026 = True
        profile.save()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False}, status=400)
