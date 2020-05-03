from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'login.html')

def index_register(request):
    return render(request, 'registration.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/index_register')
    else:
        pwhash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwhash.decode(), username=request.POST['username'])
        request.session['id'] = user.id
    return redirect('/main_app/home/')


def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
    return redirect('/main_app/home/')

def logout(request):
    request.session.clear()
    return redirect('/')
