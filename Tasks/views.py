from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from Accounts.models import Profile
from .models import Task
from .forms import TaskForm

# Create your functionality views here.
@login_required
def task_list(request):
    profile_determine = Profile.objects.get(profile_user=request.user)
    if request.method == 'GET':
        task_form = TaskForm(user=request.user)
        tasks = Task.objects.filter(author=profile_determine)
        content = {
            'tasks': tasks,
            'task_form': task_form,
              }
        return render(request, 'tasks/task_list.html', content)
    elif request.method == 'POST':
        instance = Task(author=profile_determine)
        task_form = TaskForm(request.POST or None, instance=instance)
        if task_form.is_valid():
            task_form.save()
            messages.success(request, 'New Task Added')
        return redirect('/tasks/')

@login_required
def task_detail(request, pk):
    profile_determine = Profile.objects.get(profile_user=request.user)
    task = get_object_or_404(Task, pk=pk)
    if profile_determine == task.author:  #determine Logined User is equal Author user!
        content = {'task': task}
        return render(request, 'tasks/task_detail.html', content)
    else:
        raise PermissionDenied('You Have No Permission To See This Task!')

@login_required
def task_edit(request, pk):
    profile_determine = Profile.objects.get(pk=request.user.id)
    task = get_object_or_404(Task, pk=pk)
    if profile_determine == task.author:  #determine Logined User is equal Author user!
        if request.method == "GET":
            task_form = TaskForm(instance=task, user=request.user)
            content = {'task_form': task_form}
            return render(request, 'tasks/task_edit.html', content)
        elif request.method == "POST":
            task_form = TaskForm(request.POST or None, instance=task)
            if task_form.is_valid():
                task_form.save()
                messages.success(request, 'Task Editted Correctly')
            return redirect('/tasks/')
    else:
        raise PermissionDenied('You Can not Edit this task')
@login_required
def task_delete(request, pk):
    profile_determine = Profile.objects.get(pk=request.user.id)
    task = get_object_or_404(Task, pk=pk)
    if profile_determine == task.author:  #determine Logined User is equal Author user!
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        messages.success(request, 'Task Deleted')
        return redirect('/tasks/')
    else:
        raise PermissionDenied('You Can Not Delete This Task!')