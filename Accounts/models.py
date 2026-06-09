from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver 

# Create your model managers here.
class CustomUserManager(BaseUserManager):
    """
    This class manages our custom User Model instead of default django User manager
    """
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email),)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, password.
        """
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

# Create your models here.
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    This class is a substitution for default Django User authenctication
    """
    email = models.EmailField(max_length=250, unique=True)
    date_of_created = models.DateTimeField(auto_now_add=True)
    date_of_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Profile(models.Model):
    GENDER_CHOICES = {
        "F": "Female",
        "M": "Man",
        "O": "Other"
    }
    profile_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_joined = models.DateTimeField(auto_now_add=True)
    date_of_edited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.profile_user.email
    
@receiver(post_save, sender=MyUser)
def auto_create_profile(sender, instance, created, **kwargs):
    """
    This function is a signal func, which creates a profile object of the Profile class,
    automatically after resigning a new user.
    """
    if created:
        Profile.objects.create(profile_user=instance)