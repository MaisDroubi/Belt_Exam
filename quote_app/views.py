from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from login_regist_app.models import *
from .models import *


def show_quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "this_user": User.objects.get(id=request.session['user_id']),
        "all_quotes": Quote.objects.all()
    }
    return render(request, "quotes.html",context)

def show_account(request,user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user': User.objects.get(id=user_id)
    }
    return render(request,'my_account.html', context)

def show_user_quotes(request,some_user_id):    
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'some_user': User.objects.get(id=some_user_id),
        'all_quotes': Quote.objects.all()
    }
    return render(request,'user_quotes.html', context)


def update_account(request,user_id):
    this_user = User.objects.get(id=user_id)
    errors = User.objects.edit_validator(request.POST, request.session)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/quotes/myaccount/{user_id}")
    else:    
        this_user.first_name = request.POST['first_name']
        this_user.last_name = request.POST['last_name']
        this_user.email = request.POST['email']
        this_user.save()
        return redirect('/quotes')

def add_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:    
        this_user = User.objects.get(id=request.session['user_id'])
        Quote.objects.create(quote=request.POST['quote'],author=request.POST['author'],user=this_user)
        return redirect('/quotes')

def delete_quote(request):
    this_quote = Quote.objects.get(id=request.POST['quote_id'])
    this_quote.delete()
    return redirect('/quotes')   

def like_quote(request):
    this_user = User.objects.get(id=request.session['user_id'])
    this_quote = Quote.objects.get(id=request.POST['quote_id'])
    users_likes = this_user.likes.all()
    count = 0
    for i in users_likes:
        if i.liked_quote == this_quote:
            count +=1
    if count < 1: 
        Like.objects.create(liked_quote=this_quote,liked_by=this_user)
        old_count = this_quote.like_count
        new_count = int(old_count) + 1
        this_quote.like_count = new_count
        this_quote.save()
    return redirect('/quotes')         