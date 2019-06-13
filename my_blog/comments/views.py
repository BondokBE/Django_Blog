from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Comment
from posts.models import Post
from .forms import CommentForm

def comment_thread(request, id):

    obj = get_object_or_404(Comment, id=id)

    content_object = obj.content_object  # the post that the comment is on
    content_id = obj.content_object.id

    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id,
    }
    
    form = CommentForm(request.POST or None, initial=initial_data)

    # print(form.errors)

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
        # the problem fixed by selecting [parent.get_absolute_url()]
        return redirect(new_comment.parent.get_absolute_url())

    context = {
        'comment_form': form,
        'comment': obj,
    }
    return render(request, 'comment_thread.html', context)

@login_required # (login_url='/login/')  # replaced with LOGIN_URL inside settings.py as default
def comment_delete(request, id=None):
    
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404

    # if comment.user != request.user:
    #     # raise Http404
    #     response = HttpResponse("You do not have permission to view this page!")
    #     response.status_code = 403
    #     return response

    if request.method == "POST":
        parent_url = comment.content_object.get_absolute_url()
        comment.delete()
        messages.success(request, "Comment Successfully Deleted!")
        return HttpResponseRedirect(parent_url)

    context = {
        'comment': comment,
    }
    return render(request, 'delete_comment.html', context)

