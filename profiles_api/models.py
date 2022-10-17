from email.policy import default
from enum import unique
from django.db import models

# standard base classes need to use when overriding and customizing defauly django user model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    
    def create_user(self, email, name, password=None):
        """create a new user profile"""
        if not email:
            raise ValueError("Users must have a valid email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self.db)

        return user
    

    def create_superuser(self, email, name, password):
        """Create a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user



# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True) # email field
    name = models.CharField(max_length=255) # name field
    is_active = models.BooleanField(default=True) # users id are activated by default
    is_staff = models.BooleanField(default=False) # staff user for django admin, false by default

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' # email will required
    REQUIRED_FIELDS = ['name'] # other info that are atlease required

    def get_full_name(self):
        """retrieve full name of the user"""
        return self.name
    
    def get_short_name(self):
        """retrieve should name of the user"""
        return self.name
    
    def __str__(self):
        """return string representation of our user"""
        return self.email