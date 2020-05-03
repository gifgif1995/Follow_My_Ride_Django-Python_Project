from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name needs to be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name needs to be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        elif len(self.filter(email=postData['email'])) > 0:
            errors['email']= "This email address already has an account"
        if len(postData['password']) < 8:
            errors['password'] = "Password needs to be at least 8 characters"
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match!" 
        if len(postData['username']) < 4:
            errors['username'] = "Username must be at least 4 characters long!"
        elif len(User.objects.filter(username=postData['username'])) > 0:
            errors['username'] = "Username already taken!"
        return errors

    def validate_login(self, postData):
        errors = {}
        user = self.filter(email = postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email address is not valid!"
        elif not user:
            errors['email'] = "This email does not exist!"
        else:
            if len(postData['password']) < 8:
                errors['email'] = "Password needs to be at least 8 characters"
            elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors['password'] = "This is not a valid password"
        return errors
        
    def validate_update(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name needs to be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name needs to be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        elif len(self.filter(email=postData['email'])) > 0:
            errors['email']= "This email address already has an account"
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


