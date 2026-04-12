# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Category, Thread, Reply
from .forms import ThreadForm, ReplyForm

def thread_list(request):
    """Public view to browse all threads."""
    category_slug = request.GET.get('category')
    symbol_query = request.GET.get('symbol')
    
    # Order by pinned first, then most recently updated (bumps active threads)
    threads = Thread.objects.all().order_by('-is_pinned', '-updated_at')
    
    if category_slug:
        threads = threads.filter(category__slug=category_slug)
    if symbol_query:
        threads = threads.filter(symbol__icontains=symbol_query)

    categories = Category.objects.all()

    return render(request, 'forum/thread_list.html', {
        'threads': threads,
        'categories': categories,
        'current_category': category_slug,
        'current_symbol': symbol_query
    })

def thread_detail(request, pk):
    """Public view for a single thread, handles reply form submissions."""
    thread = get_object_or_404(Thread, pk=pk)
    replies = thread.replies.all().order_by('created_at')
    form = ReplyForm()

    # Handle reply submission directly on the detail page
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('core:login') # Ensure login
        
        if not thread.is_locked:
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.thread = thread
                reply.author = request.user
                reply.save()
                
                # "Bump" the thread's updated_at timestamp
                thread.save() 
                return redirect('forum:thread_detail', pk=thread.pk)

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'replies': replies,
        'form': form,
    })

@login_required
def create_thread(request):
    """Protected view to create a new thread."""
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('forum:thread_detail', pk=thread.pk)
    else:
        # Pre-fill symbol if passed via URL parameter (e.g., from the Chart page)
        initial_symbol = request.GET.get('symbol', '')
        form = ThreadForm(initial={'symbol': initial_symbol})

    return render(request, 'forum/thread_create.html', {'form': form})

@login_required
def edit_thread(request, pk):
    """Allows the thread author to edit their thread."""
    thread = get_object_or_404(Thread, pk=pk)
    
    if request.user != thread.author:
        raise PermissionDenied("You do not have permission to edit this thread.")
        
    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('forum:thread_detail', pk=thread.pk)
    else:
        form = ThreadForm(instance=thread)

    return render(request, 'forum/thread_edit.html', {'form': form, 'thread': thread})

@login_required
def edit_reply(request, pk):
    """Allows the reply author to edit their reply."""
    reply = get_object_or_404(Reply, pk=pk)
    
    if request.user != reply.author:
        raise PermissionDenied("You do not have permission to edit this reply.")
        
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            return redirect('forum:thread_detail', pk=reply.thread.pk)
    else:
        form = ReplyForm(instance=reply)

    return render(request, 'forum/reply_edit.html', {'form': form, 'reply': reply})

@login_required
def delete_reply(request, pk):
    """Allows the reply author to delete their reply."""
    reply = get_object_or_404(Reply, pk=pk)
    
    if request.user != reply.author:
        raise PermissionDenied("You do not have permission to delete this reply.")
        
    thread_pk = reply.thread.pk
    
    if request.method == 'POST':
        reply.delete()
        return redirect('forum:thread_detail', pk=thread_pk)

    return render(request, 'forum/reply_confirm_delete.html', {'reply': reply})