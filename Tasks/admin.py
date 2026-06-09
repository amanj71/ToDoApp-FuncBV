from django.contrib import admin
from .models import Category, Task

# Create your adminModels here
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'category', 'status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'name']


# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)