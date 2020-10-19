from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserProfileForm, UpdateProfileForm, PostForm, CommentForm
from django.contrib.auth import login, authenticate
from .models import Image, Comment, Profile, Follow
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import RedirectView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('qwerty')
            user = authenticate(username=username, user_password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='login')
def index(request):
    images = Image.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    params = {
        'images': images,
        'form': form,
        'users': users,

    }
    return render(request, 'gram_temp/index.html', params)


@login_required(login_url='login')
def profile(request, username):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        prof_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UserProfileForm(instance=request.user)
        up_prof_form = UpdateProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'up_prof_form': up_prof_form,
        'images': images,

    }
    return render(request, 'gram_temp/profile.html', params)


@login_required(login_url='login')
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_posts = user_prof.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_prof.profile)
    for follower in followers:
        params = {
            'user_prof': user_prof,
            'user_posts': user_posts,
            'followers': followers,
        }
    print(followers)
    return render(request, 'gram_temp/user_profile.html', params)


@login_required(login_url='login')
def post_comment(request, id):
    image = get_object_or_404(Image, pk=id)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = image
            savecomment.user = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    params = {
        'image': image,
        'form': form,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    return render(request, 'gram_temp/post.html', params)

def like_post(request):
    image = get_object_or_404(Image, id=request.POST.get('id'))
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        image.likes.remove(request.user)
        is_liked = False
    else:
        image.likes.add(request.user)
        is_liked = False

    params = {
        'image': image,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    if request.is_ajax():
        html = render_to_string('gram_temp/like.html', params, request=request)
        return JsonResponse({'form': html})


@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'gram_temp/search.html', params)
    else:
        message = "Invalid search! Please try again."
    return render(request, 'gram_temp/search.html', {'message': message})


def unfollow(request, to_unfollow):
    if request.method == 'GET':
        sec_user_profile = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=sec_user_profile)
        unfollow_d.delete()
        return redirect('user_profile', sec_user_profile.user.username)


def follow(request, to_follow_friend):
    if request.method == 'GET':
        new_user_profile = Profile.objects.get(pk=to_follow_friend)
        follow_s = Follow(follower=request.user.profile, followed=new_user_profile)
        follow_s.save()
        return redirect('user_profile', new_user_profile.user.username)