from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")    
    else:    
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        newUser = User.objects.create(first_name=request.POST["first_name"],last_name=request.POST["last_name"],email=request.POST["email"],password=pw_hash)
        request.session['user_id'] = newUser.id
        return redirect("/quotes")

def login(request):
    user = User.objects.filter(email=request.POST["email"])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST["password"].encode(),logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect("/quotes")
    login_errors = User.objects.login_validator(request.POST)     
    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value, extra_tags=key)
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def success(request):
    context = {
        "this_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'success.html', context)