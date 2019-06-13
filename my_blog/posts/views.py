from urllib.parse import quote_plus

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .utils import get_read_time
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment


def post_create(request):
    
    if not request.user.is_authenticated: # or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)  # request.POST => for form validation 

    if form.is_valid() and request.method == "POST":
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'Post Created Successfully')  
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {'form': form}
    return render(request, 'post_create.html', context)

def post_edit(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)  # request.POST => for form validation 
    
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise Http404
    
    if form.is_valid() and request.method == "POST":
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Updates saved!')
        return HttpResponseRedirect(instance.get_absolute_url()) 
    else:
        messages.error(request, 'Not saved')
    
    context = {
        'title': post.title,
        'post': post,
        'form': form,
    }
    return render(request, 'post_create.html', context=context)

@login_required
def post_delete(request, slug=None):
    
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise Http404
        
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Post Successfully deleted')

    return redirect('posts:base')


def post_list(request):
    post_list = Post.objects.active()  # .filter(draft=False).filter(publish__lte=timezone.now())  # .order_by("-time_stamp")
    if request.user.is_superuser or request.user.is_staff:
        post_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        post_list = Post.objects.all()
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
            # Q(user__first_name__icontains=query) |
            # Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(post_list, 5)  # Show 25 posts per page
    # page_request_var = 'page'  # to make it mor dynamic for pagination
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    create_url = reverse('posts:post_create')
    
    context = {
        'post_list': post_list,
        'posts': posts,
        # 'page_request_var': page_request_var,
        'create': create_url,
    }

    return render(request, 'base.html', context)


def post_details(request, slug=None):
    post_list = Post.objects.active()
    post = get_object_or_404(Post, slug=slug)
    # if post.publish > timezone.now().date() or post.draft:
    #     if not request.user.is_authenticated or not request.user.is_superuser:
    #         raise Http404
    
    share_string = quote_plus(post.content)
    
    initial_data = {
        "content_type": post.get_content_type,
        "object_id": post.id,
    }
    
    # post read time 
    read_time = get_read_time(post.content)
    # print(type(read_time))
    
    form = CommentForm(request.POST or None, initial=initial_data)
    
    if form.is_valid() and request.user.is_authenticated:
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
            
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        
        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = post.comments # Comment.objects.filter_by_instance(post)  # without @property

    context = {
        'post': post,
        'share_string': share_string,
        'comments': comments,
        'comment_form': form,
        'read_time': read_time,
    }
    return render(request, 'post.html', context=context)

# About, Contact sections

def about(request):
    context = {}
    return render(request, 'about.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)



''' 
# this for checking if the user is authenticated or not
if request.user.is_authenticated:
        context = {'title': 'this text for authenticated user'}
        return render(request, 'index.html', context=context)
    else:
        context = {'title': 'this text for non authenticated users'}
        return render(request, 'index.html', context=context)
    
'''
