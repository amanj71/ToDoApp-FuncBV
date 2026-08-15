from django.db import models
from Accounts.models import Profile
from django.contrib.auth import get_user_model

MyUser = get_user_model()

# Create your models here.
class Category(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICE = {
        "F": "Future",
        "P": "Pending",
        "C": "Completed",
    }
    TASK_IMPORTANCE_CHOICE = {
        "H": "High",
        "M": "Medium",
        "L": "Low",
    }
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    importance = models.CharField(max_length=1, choices=TASK_IMPORTANCE_CHOICE)
    
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(blank=True, null=True)

class PageVisit(models.Model):
    path = models.TextField(blank=True, null=True) # col
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)

    