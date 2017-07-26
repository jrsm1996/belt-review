from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.contrib import messages
from .models import User, Secret

def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

def index(request):
    if 'user_id' in request.session:
        return redirect('/secrets')
    return render(request, 'login_app/index.html')

def login(request):
    if request.method == 'POST':
        errors = User.objects.validateLogin(request.POST)
        if errors:
            flashErrors(request, errors)
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['user_id'] = user.id
            return redirect('/secrets')
    return redirect('/')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validateRegistration(request.POST)
        if errors:
            flashErrors(request, errors)
        else:
            user = User.objects.createUser(request.POST)
            request.session['user_id'] = user.id
            return redirect('/secrets')
    return redirect('/')

def secrets(request):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.currentUser(request)
    secrets = Secret.objects.all().order_by('-created_at')
    friends = current_user.friends.all()
    strangers = User.objects.exclude(id__in = friends).exclude(id=current_user.id)
    context = {
        'current_user': current_user,
        'secrets': secrets,
        'friends': friends,
        'strangers': strangers
    }
    return render(request, 'login_app/secrets.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def post(request):
    if request.method == 'POST':
        user = User.objects.currentUser(request)
        Secret.objects.create(content = request.POST['content'], user = user)
    return redirect('/secrets')

def delete(request, id):
    secret = Secret.objects.get(id = id)
    secret.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def like(request, id):
    user = User.objects.currentUser(request)
    secret = Secret.objects.get(id = id)
    secret.liked_by.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unlike(request, id):
    user = User.objects.currentUser(request)
    secret = Secret.objects.get(id = id)
    secret.liked_by.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def popular(request):
    current_user = User.objects.currentUser(request)
    secrets = Secret.objects.annotate(liked_count = Count('liked_by')).order_by('-liked_count')
    friends = current_user.friends.all()
    strangers = User.objects.exclude(friends__in = friends).exclude(id = current_user.id)
    context = {
        'current_user': current_user,
        'secrets': secrets,
        'friends': friends,
        'strangers': strangers
    }
    return render(request, 'login_app/popular.html', context)

def addfriend(request, id):
    user = User.objects.currentUser(request)
    friend = User.objects.get(id = id)
    user.friends.add(friend)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delfriend(request, id):
    user = User.objects.currentUser(request)
    friend = User.objects.get(id = id)
    user.friends.remove(friend)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
