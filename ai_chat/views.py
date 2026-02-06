import aiml
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AIConversation, AIMessage

# Initialize AIML kernel
kernel = aiml.Kernel()

# Check if brain file exists, if not, learn from aiml files
BRAIN_FILE = "jaytipargal_brain.brn"

if os.path.isfile(BRAIN_FILE):
    kernel.bootstrap(brainFile=BRAIN_FILE)
else:
    # Set predicates for initial configuration
    kernel.setPredicate("name", "Jayti")
    kernel.setPredicate("current_goal", "personal growth")
    
    # The AIML files will be loaded from the aiml directory
    # For now, we'll use built-in patterns and responses
    kernel.bootstrap(learnFiles="aiml/startup.xml", commands="load aiml b")
    kernel.saveBrain(BRAIN_FILE)


def get_ai_response(user_input, user):
    """Get response from AIML kernel with personalization"""
    # Set user-specific predicates
    kernel.setPredicate("name", user.profile.display_name if hasattr(user, 'profile') else "Jayti")
    
    # Get response
    response = kernel.respond(user_input.upper())
    
    # If no AIML match, provide fallback responses
    if not response or response == "":
        response = get_fallback_response(user_input)
    
    # Clean up the response (remove markdown artifacts)
    response = clean_response(response)
    
    return response


def get_fallback_response(user_input):
    """Fallback responses when AIML doesn't match"""
    user_input_lower = user_input.lower()
    
    # Emotional support patterns
    if any(word in user_input_lower for word in ['sad', 'upset', 'hurt', 'pain', 'cry']):
        return "I hear that you're going through a difficult time. Your feelings are valid. Would writing in your Diary help you process these emotions?"
    
    if any(word in user_input_lower for word in ['happy', 'joy', 'excited', 'good news']):
        return "I'm glad to hear you're feeling positive. These moments are worth savoring. Consider noting this in your Diary to remember this feeling."
    
    if any(word in user_input_lower for word in ['worried', 'anxious', 'stress', 'nervous']):
        return "It sounds like you're carrying some worry. Take a deep breath. Would it help to break down what's concerning you into smaller parts in your Goals section?"
    
    if any(word in user_input_lower for word in ['tired', 'exhausted', 'burnout', 'overwhelmed']):
        return "You sound like you need rest. Remember that taking care of yourself is not a luxury—it's essential. What would help you recharge right now?"
    
    # Feature-related
    if any(word in user_input_lower for word in ['goal', 'objective', 'target']):
        return "The Goals section can help you break down your aspirations into actionable steps. You can set marketing career goals and track your progress. Would you like to explore that?"
    
    if any(word in user_input_lower for word in ['diary', 'journal', 'write']):
        return "Your Diary is a private space for daily reflection. You can write by typing, speaking, or even using a stylus. Only today's entry can be written, but you can always read past entries."
    
    if any(word in user_input_lower for word in ['note', 'remember', 'reminder']):
        return "The Notes section is perfect for capturing thoughts, ideas, and information you want to keep. You can organize them with tags and search them anytime."
    
    if any(word in user_input_lower for word in ['astro', 'astrology', 'horoscope', 'chart']):
        return "Your Astro section displays your Vedic birth chart based on your birth details. It offers guidance on favorable periods and insights into your planetary positions."
    
    if any(word in user_input_lower for word in ['birthday', 'birth date', 'february']):
        return "Your birthday on February 6th marks not just another year, but an opportunity for renewal. How are you feeling about the year ahead?"
    
    # About the companion
    if any(word in user_input_lower for word in ['who are you', 'what are you', 'your name']):
        return "I'm here as a companion on your journey—someone to talk to when you need to think out loud, seek clarity, or simply share a moment. I'm not human, but I'm here for you."
    
    if any(word in user_input_lower for word in ['vivek', 'creator', 'made this', 'built this']):
        return "This space was created with care and thought for your wellbeing. The intention behind it is to provide you with tools for self-reflection, growth, and organization."
    
    # Default response
    return "I'm here to listen and support you. Would you like to talk about what's on your mind, or would you prefer guidance on using any of the features in your personal space?"


def clean_response(response):
    """Clean response by removing markdown artifacts"""
    # Remove markdown formatting
    response = response.replace('*', '')
    response = response.replace('#', '')
    response = response.replace('`', '')
    response = response.replace('_', '')
    
    # Ensure proper HTML formatting
    response = response.replace('\n', '<br>')
    
    return response


@login_required
def chat_interface(request):
    """Main chat interface"""
    # Get or create conversation
    conversation, created = AIConversation.objects.get_or_create(
        user=request.user,
    )
    
    messages = conversation.messages.all()[:50]  # Last 50 messages
    
    context = {
        'messages': messages,
        'conversation': conversation,
    }
    return render(request, 'ai_chat/chat_interface.html', context)


@csrf_exempt
@require_POST
def send_message(request):
    """Handle AJAX message sending"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Get or create conversation
        conversation, _ = AIConversation.objects.get_or_create(user=request.user)
        
        # Save user message
        AIMessage.objects.create(
            conversation=conversation,
            sender='user',
            content=user_message
        )
        
        # Get AI response
        ai_response = get_ai_response(user_message, request.user)
        
        # Save AI message
        AIMessage.objects.create(
            conversation=conversation,
            sender='ai',
            content=ai_response
        )
        
        return JsonResponse({
            'response': ai_response,
            'timestamp': conversation.messages.last().timestamp.isoformat()
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def chat_history(request):
    """View chat history"""
    conversation = AIConversation.objects.filter(user=request.user).first()
    messages = conversation.messages.all() if conversation else []
    
    context = {
        'messages': messages,
    }
    return render(request, 'ai_chat/chat_history.html', context)


@login_required
def clear_conversation(request):
    """Clear conversation history"""
    if request.method == 'POST':
        AIConversation.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
