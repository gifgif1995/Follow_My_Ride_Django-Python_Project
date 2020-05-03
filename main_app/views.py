from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.utils import timezone


def home(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['id']),
    }
    return render(request, 'home.html', context)

def add_rides(request, id):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['id']),
        'ride': Ride.objects.get
    }
    return render(request, 'add_rides.html', context)

def follow_rides(request, id):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['id']),
    }
    return render(request, 'follow_rides.html', context)

def ride_blog(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
        'comments': Comment.objects.all(),
        'show_all_messages': Message.objects.all()
    }
    return render(request, 'ride_blog.html', context)

def message(request):
    Message.objects.create(message=request.POST['message'], 
    user=User.objects.get(id=request.session['id'])) 
    return redirect('/main_app/ride_blog')

def comment(request):
    Comment.objects.create(comment=request.POST['comment'], 
    user=User.objects.get(id=request.session['id']), 
    message= Message.objects.get(id=request.POST["message_id"]))
    return redirect('/main_app/ride_blog')

def home_message(request):
    Message.objects.create(message=request.POST['message'], 
    user=User.objects.get(id=request.session['id'])) 
    return redirect('/main_app/home')

def delete_message(request, message_id):
    this_message = Message.objects.get(id=int(message_id))
    this_message.delete()
    return redirect('/main_app/ride_blog')

def my_account(request, user_id):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user_info': User.objects.get(id=int(user_id)),
    }
    return render(request, 'my_account.html', context)

def update_account(request):
    errors = User.objects.validate_update(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main_app/my_account/'+str(request.session['id']))
    else:
        this_user= User.objects.get(id=request.session['id'])
        this_user.first_name= request.POST['first_name']
        this_user.last_name= request.POST['last_name']
        this_user.email= request.POST['email']
        this_user.save()
        messages.success(request, 'User Info Updated Successfully!')
    return redirect('/main_app/my_account/'+str(request.session['id']))

def logout(request):
    request.session.clear()
    return redirect('/')
