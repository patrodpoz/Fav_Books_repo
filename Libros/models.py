from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta

import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z -]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z -]+$')
        


        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name should have at least 2 characters.'
        elif not FIRST_NAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = 'First name must consist of only letters'
        
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name should have at least 2 characters.'
        elif not LAST_NAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = 'Last name must consist of only letters and space or dash characters'

        if len(post_data['email']) < 1:
            errors['email'] = 'Email is required'
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Please enter a valid email address'
        
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords must match'

        return errors

    def login_validator(self, postData):
        errors ={}
        logged_user=User.objects.filter(email=postData['email'])
        if logged_user:
            user=logged_user[0]
        else:
            errors['email']='There is no user that matches this email. Please register.'
            return errors
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            return errors
        else:
            errors['password']='This password does not match this email. Please try again.'
            return errors
    

    def book_validator(self, postData):
        errors = {}
        if len(postData['title'])<1:
            errors['title']="You must include the title."
        if len(postData['description'])<5:
            errors['description']="Your description must be a little longer."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 64)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Book(models.Model):
    title=models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
    user_who_like = models.ManyToManyField(User, related_name="liked_books")
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()