from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Note, Tag


@login_required
def note_list(request):
    """List all notes with search and filter"""
    notes = Note.objects.filter(user=request.user)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        notes = notes.filter(
            Q(title__icontains=query) | 
            Q(content_plain__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Tag filter
    tag_filter = request.GET.get('tag')
    if tag_filter:
        notes = notes.filter(tags__name=tag_filter)
    
    # Get all tags for this user
    user_tags = Tag.objects.filter(notes__user=request.user).distinct()
    
    context = {
        'notes': notes,
        'tags': user_tags,
        'query': query,
        'tag_filter': tag_filter,
    }
    return render(request, 'notes/note_list.html', context)


@login_required
def note_create(request):
    """Create a new note"""
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        tag_names = request.POST.get('tags', '').split(',')
        
        note = Note.objects.create(
            user=request.user,
            title=title,
            content=content,
        )
        
        # Process tags
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
                note.tags.add(tag)
        
        messages.success(request, 'Note created successfully.')
        return redirect('note_detail', pk=note.pk)
    
    return render(request, 'notes/note_form.html')


@login_required
def note_detail(request, pk):
    """View note details"""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_edit(request, pk):
    """Edit an existing note"""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    
    if request.method == 'POST':
        note.title = request.POST.get('title', '')
        note.content = request.POST.get('content', '')
        
        # Update tags
        note.tags.clear()
        tag_names = request.POST.get('tags', '').split(',')
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
                note.tags.add(tag)
        
        note.save()
        messages.success(request, 'Note updated successfully.')
        return redirect('note_detail', pk=note.pk)
    
    context = {
        'note': note,
        'tags': ', '.join([t.name for t in note.tags.all()]),
    }
    return render(request, 'notes/note_form.html', context)


@login_required
def note_delete(request, pk):
    """Delete a note"""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully.')
        return redirect('note_list')
    
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
