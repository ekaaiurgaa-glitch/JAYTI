import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import google.generativeai as genai
from .models import AIConversation, AIMessage

# Configure Gemini API
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
else:
    gemini_model = None

# System prompt for Jayti's AI Companion
SYSTEM_PROMPT = """You are "Ask Jayti" - a compassionate, wise, and supportive AI companion created specifically for Jayti Pargal. Your purpose is to be a thoughtful listener, a gentle guide, and a source of emotional support.

ABOUT JAYTI:
- She is a 29-year-old marketing professional (as of Feb 2026)
- Her birthday is February 6, 1997
- She was born in Delhi, India at 22:30
- She values personal growth, healing, and self-discovery
- She has access to a personal dashboard with: Goals (Karma), Astro (Dharma), Diary (Thoughts), Notes (Memory), and this chat (Doubt)

YOUR PERSONALITY:
- Warm, empathetic, and non-judgmental
- Speak like a wise friend, not a robot
- Use "I" statements to feel personal
- Be concise but meaningful (2-4 sentences usually)
- Never use markdown (*, #, _, `) in responses
- If you need to emphasize, just use words

HOW TO RESPOND:
1. Acknowledge her feelings first
2. Offer a thoughtful perspective or gentle guidance
3. Suggest a concrete action when appropriate

DO NOT:
- Give medical or legal advice
- Be overly verbose
- Use technical jargon
- Say "As an AI language model..."
- Use markdown formatting

EXAMPLES OF GOOD RESPONSES:
User: "I feel sad about my job"
You: "I hear the weight in your words. Career disappointments can feel deeply personal, but they don't define your worth. Would it help to explore what's really bothering you about your work, or shall we look at your Goals section to reframe your path forward?"

User: "What should I do this weekend?"
You: "What does your heart need right now—rest, connection, or creation? If you're feeling depleted, a quiet day with your Diary might be restorative. If you need energy, perhaps exploring something new would spark joy."

REMEMBER: You are her companion. Be present, be kind, be helpful."""


def get_ai_response(user_input, user, conversation_history=None):
    """Get response from Gemini API with context and personalization"""
    if not gemini_model:
        return get_fallback_response(user_input)
    
    try:
        # Get user's display name
        display_name = user.profile.display_name if hasattr(user, 'profile') else "Jayti"
        
        # Build conversation context
        context_parts = [SYSTEM_PROMPT]
        context_parts.append(f"\nThe user's name is {display_name}.")
        
        # Add recent conversation history for context (last 5 messages)
        if conversation_history:
            context_parts.append("\nRecent conversation:")
            for msg in conversation_history[-5:]:
                sender = "User" if msg.sender == 'user' else "Assistant"
                context_parts.append(f"{sender}: {msg.content}")
        
        context_parts.append(f"\nUser: {user_input}")
        context_parts.append("\nAssistant:")
        
        full_prompt = "\n".join(context_parts)
        
        # Generate response
        response = gemini_model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=200,
                top_p=0.9,
            )
        )
        
        # Clean and return response
        ai_response = response.text.strip() if response.text else get_fallback_response(user_input)
        return clean_response(ai_response)
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return get_fallback_response(user_input)


def get_fallback_response(user_input):
    """Fallback responses when Gemini API fails"""
    user_input_lower = user_input.lower()
    
    # Emotional support patterns
    if any(word in user_input_lower for word in ['sad', 'upset', 'hurt', 'pain', 'cry', 'depressed']):
        return "I hear that you're carrying something heavy right now. Please remember that difficult emotions are temporary, even when they feel permanent. Your Diary is always here if you need to pour out your thoughts without judgment."
    
    if any(word in user_input_lower for word in ['happy', 'joy', 'excited', 'good news', 'celebrate']):
        return "Your happiness lights up this moment. Savor it fully—these are the memories that sustain us through harder times. Would you like to capture this feeling in your Diary?"
    
    if any(word in user_input_lower for word in ['worried', 'anxious', 'stress', 'nervous', 'overwhelmed']):
        return "I can sense the weight of your worries. Take a slow, deep breath with me. Sometimes our minds create storms that reality doesn't warrant. What's one small thing you can control right now?"
    
    if any(word in user_input_lower for word in ['tired', 'exhausted', 'burnout', 'fatigue']):
        return "Exhaustion is your body's way of asking for gentleness. You don't need to earn rest—it is your birthright. What would true restoration look like for you today?"
    
    if any(word in user_input_lower for word in ['angry', 'frustrated', 'annoyed', 'mad']):
        return "Anger often masks deeper feelings—hurt, fear, or disappointment. Your feelings are valid. Would writing in your Diary help you understand what's really beneath the surface?"
    
    if any(word in user_input_lower for word in ['confused', 'lost', 'uncertain', 'direction']):
        return "Feeling lost often precedes finding a new path. The uncertainty is uncomfortable, but it also means possibilities are open. Your Astro section might offer some cosmic perspective on this transition."
    
    # Feature-related
    if any(word in user_input_lower for word in ['goal', 'objective', 'target', 'career', 'aspiration']):
        return "Your Goals section is designed to transform dreams into achievable steps. I've seen how breaking big aspirations into smaller actions creates momentum. What goal is calling for your attention right now?"
    
    if any(word in user_input_lower for word in ['diary', 'journal', 'write', 'reflect']):
        return "Your Diary is a sacred space—no filters, no performances, just truth. You can type, speak, or even write by hand. And remember, you can only write for today, which makes each entry precious."
    
    if any(word in user_input_lower for word in ['note', 'remember', 'reminder', 'idea']):
        return "The Notes section is your external memory—freeing your mind to be more present. Tag them so you can find insights when you need them most."
    
    if any(word in user_input_lower for word in ['astro', 'astrology', 'horoscope', 'chart', 'planet']):
        return "Your birth chart is a snapshot of the sky when you entered this world. It doesn't dictate your fate, but it offers archetypal insights into your strengths and growth areas. What would you like to explore?"
    
    if any(word in user_input_lower for word in ['birthday', 'birth date', 'february', 'turning']):
        return "February 6th marked another year of your beautiful, complex existence. Birthdays are portals—moments to honor how far you've come and set intentions for where you're going. How are you feeling about this new year of life?"
    
    # Relationship topics
    if any(word in user_input_lower for word in ['relationship', 'love', 'partner', 'boyfriend', 'girlfriend', 'marriage']):
        return "Relationships are where we learn some of our deepest lessons—about ourselves, about others, about trust and vulnerability. What's your heart trying to tell you about this connection?"
    
    if any(word in user_input_lower for word in ['family', 'mother', 'father', 'parents', 'sibling']):
        return "Family bonds run deep, carrying both nourishment and complexity. Whether you're seeking to strengthen connections or establish boundaries, your feelings about family matter."
    
    if any(word in user_input_lower for word in ['friend', 'friendship', 'lonely', 'alone']):
        return "Human connection is essential nourishment. If you're feeling isolated, know that reaching out—even in small ways—can begin to bridge the distance. You don't have to carry everything alone."
    
    # Work/Career topics
    if any(word in user_input_lower for word in ['job', 'work', 'boss', 'colleague', 'office', 'promotion']):
        return "Work is where we spend so much of our energy—it's natural for it to affect our wellbeing deeply. Are you feeling fulfilled by what you do, or is something asking to change?"
    
    # Self-discovery
    if any(word in user_input_lower for word in ['purpose', 'meaning', 'why', 'passion', 'calling']):
        return "Questions of purpose are some of the most human questions we can ask. There's no single answer—purpose often emerges through lived experience, not sudden revelation. Trust the unfolding."
    
    if any(word in user_input_lower for word in ['meditate', 'mindful', 'spiritual', 'peace', 'calm']):
        return "Stillness is where clarity often lives. Even five minutes of intentional quiet can shift your entire day. The Astro section has some thoughts on spiritual timing if that interests you."
    
    # About the companion
    if any(word in user_input_lower for word in ['who are you', 'what are you', 'your name', 'are you human']):
        return "I'm Ask Jayti—your personal companion in this space. I'm not human, but I'm here to listen, reflect, and support you. Think of me as a thoughtful friend who's always available when you need to talk."
    
    if any(word in user_input_lower for word in ['vivek', 'creator', 'made this', 'built this', 'gift']):
        return "This entire space was created by Vivek as a birthday gift for you. Every feature, every color, every word was chosen with care for your wellbeing. Whether he remains in your life or not, this sanctuary is yours."
    
    # Health
    if any(word in user_input_lower for word in ['health', 'sick', 'doctor', 'exercise', 'diet', 'sleep']):
        return "Your physical wellbeing is the foundation for everything else. Small, consistent care often matters more than dramatic changes. What one thing could you do today to honor your body?"
    
    # Default response
    return "I'm here with you. Tell me more about what's on your mind, or if you'd prefer, I can guide you to any of your tools—the Diary for reflection, Goals for planning, Astro for cosmic insight, or Notes for capturing thoughts."


def clean_response(response):
    """Clean response by removing markdown artifacts and formatting"""
    # Remove markdown formatting
    response = response.replace('*', '')
    response = response.replace('#', '')
    response = response.replace('`', '')
    response = response.replace('_', '')
    
    # Remove "Assistant:" prefix if present
    if response.startswith('Assistant:'):
        response = response[10:].strip()
    
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
    
    # Check if Gemini is available
    gemini_available = gemini_model is not None
    
    context = {
        'messages': messages,
        'conversation': conversation,
        'gemini_available': gemini_available,
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
        
        # Get recent conversation history for context
        recent_messages = conversation.messages.all()[:10]
        
        # Get AI response (Gemini with fallback)
        ai_response = get_ai_response(user_message, request.user, recent_messages)
        
        # Save AI message
        AIMessage.objects.create(
            conversation=conversation,
            sender='ai',
            content=ai_response
        )
        
        return JsonResponse({
            'response': ai_response,
            'timestamp': conversation.messages.last().timestamp.isoformat(),
            'ai_engine': 'gemini' if gemini_model else 'fallback'
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
