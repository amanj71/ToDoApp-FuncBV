from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import random
from Accounts.models import MyUser, Profile
from ...models import Category, Task
class Command(BaseCommand):
    help = "Create Dummy Data and Insert Them to Database :)"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()
    
    def handle(self, *args, **options):
        user = MyUser.objects.create_user(email=self.fake.email(), password='123') # replaced create method by create_user #in MyUser modelmanager class
        user.is_active = True
        profile = Profile.objects.get(profile_user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.gender = random.choice(['F', 'M', 'O'])
        profile.date_of_birth = self.fake.date_of_birth()
        user.save()
        profile.save()
        cat_choice = 'Test ' + user.email.split('@')[0]
        category_choice_list = ['Career', 'Work', 'Test', 'Study', cat_choice, 'Athletic', 'Lesiure'] 
        for _ in range(3):
            name=random.choice(category_choice_list)
            Category.objects.create(creator=profile, name=name)
            category_choice_list.remove(name)
        for _ in range(6):
            Task.objects.create( # Task model requires author, title, status, category and importance
                author = profile,
                title = ' '.join(self.fake.words()),
                status = random.choice(['F', 'P', 'C']),
                category = random.choice(Category.objects.filter(creator=profile)),
                importance = random.choice(['H', 'M', 'L'])
            )
