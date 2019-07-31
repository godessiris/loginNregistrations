from __future__ import unicode_literals
from django.db import models



# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0: 
            errors["first_name"] = "First name is required!!"
        elif len(postData['first_name']) < 2: 
            errors["firstname"] = "First name should be greater than two characters"
        elif postData["first_name"].isalpha() == False:
            errors["isa_fn"] = "Alphabet characters only for First Name"
        if len(postData['last_name']) == 0: 
            errors["last_name"] = "Last name is required!!"
        elif len(postData['last_name']) < 2: 
            errors["lastname"] = "Last Name shoudl be greater than two characters"
        elif postData["last_name"].isalpha() == False:
            errors["isa_ln"] = "Alphabet characters only for Last Name"
        if len(postData['email']) == 0:
            errors["email"] = "please enter an email"
        if len(Registration.objects.filter(email = postData['email'])) > 0:
            errors['reg_email'] = "Email already exist, please Log In"
        if len(postData['password']) == 0:
            errors["password"] = "please enter a password"
        elif len(postData['password']) < 8:
            errors["short_pw"] ="Password needs to be more than 8 characters long"
        elif postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password does not match!"

        return errors

    def login_validator(self, postData):
        errors = {}
        if len(Registration.objects.filter(email = postData['email'])) == 0:
            errors['invalid_e'] = "Invalid login credentials." 
        else: 
            user =Registration.objects.get(email = postData['email'])
            if postData['password'] is user.password:
                print("Password accepted, loggin in...")
            else:
                errors["invalid"] = "Invalid login credentials."       

        return errors

class Registration (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday= models.DateTimeField("%mm-%dd-%yyyy", null="True")
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

    def __repr__(self):
        return f"<Registration object: {self.email} ({self.id})>"
