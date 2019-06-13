from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash
)

from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
        UserLoginForm, 
        UserRegisterForm, 
        UpdateUser, 
        UpdateProfile,
)

from .models import Profile
from posts.models import Post


def user_login(request):
    print(request.user.is_authenticated)
    
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        
        messages.success(request, "Welcome back {}".format(username))
        return redirect("/")

    context = {
        "title": title,
        "login_form": form,
    }

    return render(request, 'login.html', context)


def user_register(request):
    # print(request.user.is_authenticated)
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        profile = Profile.objects.create(user=user)   
        messages.success(request, "Welcome {} {}! Your Account has been created.".format(user.first_name, user.last_name))
        return redirect('posts:base')
    
    context = {
        'title': title,
        'register_form': form
    }
    return render(request, 'register.html', context)

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out! hope to see you again")
    return redirect("/")

@login_required
def user_profile(request):
    post_list = Post.objects.filter(user=request.user)

    context = {
        'posts': post_list,
    }
    return render(request, 'profile.html', context)


def profile_edit(request):
    
    if request.method == "POST":
        u_form = UpdateUser(request.POST, instance=request.user)
        p_form = UpdateProfile(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('accounts:profile')

    else:
        u_form = UpdateUser(instance=request.user)
        p_form = UpdateProfile(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile_edit.html', context)


def password_change(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # makes user not login again
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'password_change.html', context)
