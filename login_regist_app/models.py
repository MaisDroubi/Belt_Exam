from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name'])<2:
            errors["last_name"] = "Last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):              
            errors['email'] = "Invalid email address!"
        emails = User.objects.filter(email=postData["email"])
        if len(emails) > 0:
            errors['email_duplicate'] = "That email already exists"
        if len(postData['password'])<8:
            errors["password"] = "Password should be at least 8 characters"
        if len(postData['password'])>45:
            errors["password"] = "Password should be less than 45 charcters"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords do not match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData['email'])
            if user.password != postData['password']:
                errors["incorrect_pw"] = "Incorrect password"
        except:
            errors["email_login"] = "Email not found"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):               
            errors['email_login'] = "Please enter a valid email address"
        return errors
    
    def edit_validator(self, postData, sessionData):
        errors = {}
        if postData['first_name'] == "" or postData['last_name'] == "" or postData['email'] == "":
            errors["all_fields"] = "All fields must be filled."
        else:    
            if len(postData['first_name'])<2:
                errors["first_name"] = "First name should be at least 2 characters"
            if len(postData['first_name'])>100:
                errors["first_name"] = "First name should be less than 100 charcters"
            if len(postData['last_name'])<2:
                errors["last_name"] = "Last name should be at least 2 characters"
            if len(postData['last_name'])>100:
                errors["last_name"] = "Last name should be less than 100 charcters"
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email']):                
                errors['email'] = "Invalid email address!"
            emails = User.objects.filter(email=postData["email"])
            other_emails = User.objects.exclude(id=sessionData['user_id'])
            if emails[0] in other_emails:
                errors['email_duplicate'] = "That email already exists"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)
    objects = UserManager()


