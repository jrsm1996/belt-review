from __future__ import unicode_literals
from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateRegistration(self, form_data):
        errors = []
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('The email you entered is not in valid email format.')
        else:
            user = User.objects.filter(email = form_data['email'])
            if user:
                errors.append('The email you entered has already been used to create an account')
        if form_data['first_name'] < 1:
            errors.append('Please enter a first name that is 2 or more characters.')
        if form_data['last_name'] < 1:
            errors.append('Please enter a last name that is 2 or more characters.')
        if form_data['password'] < 8:
            errors.append('Please enter a password that is 8 or more characters')
        else:
            if form_data['password'] != form_data['confirm_password']:
                errors.append('The password and confirm password fields must match.')
        return errors

    def validateLogin(self, form_data):
        errors = []
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('The email you entered is not in valid email format.')
        else:
            user = User.objects.filter(email = form_data['email']).first()
            if user:
                password = str(form_data['password'])
                hashed_pw = bcrypt.hashpw(password, str(user.password))
                if hashed_pw != user.password:
                    errors.append('The password you entered is invalid.')
            else:
                errors.append('The email you entered is not in our database.')
        return errors

    def createUser(self, form_data):
        password = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.create(
            first_name = form_data['first_name'],
            last_name = form_data['last_name'],
            email = form_data['email'],
            password = hashed_pw
        )
        return user

    def currentUser(self, request):
        return User.objects.get(id = request.session['user_id'])

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    friends = models.ManyToManyField("self", related_name="friended_by")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Secret(models.Model):
     content = models.TextField()
     user = models.ForeignKey(User, related_name = "secrets")
     liked_by = models.ManyToManyField(User, related_name="likes")
     created_at = models.DateTimeField(auto_now_add = True)
     updated_at = models.DateTimeField(auto_now = True)
