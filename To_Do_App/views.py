from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from Accounts.models import Profile
from Tasks.models import PageVisit

## Create your functionality views here.

def visit_home(request):
    visit_obj = PageVisit.objects.create(path='home/')
    content = {
        'counter': PageVisit.objects.all().count(),
    }
    return render(request, 'tasks/task_list.html', content)
