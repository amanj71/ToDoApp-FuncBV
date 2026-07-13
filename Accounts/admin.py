from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Profile

# create your custome models here.
class MyUserAdmin(UserAdmin):
    """
    A class to register our custom user model in django admin panel.
    """
    list_display = ('email', 'is_superuser', 'is_staff', 'is_active', 'date_of_created')
    list_filter = ('email', 'is_superuser', 'is_active')
    searching_field = ('email',)
    ordering = ('date_of_created',)
    
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_staff", "is_superuser", "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    filter_horizontal = []

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['profile_user__email', 'first_name', 'gender']
    ordering = ['date_of_joined']

## Register Your model here
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile, ProfileAdmin)