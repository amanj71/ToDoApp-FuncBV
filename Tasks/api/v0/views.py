from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .serializers import TaskSerializer
from Tasks.models import Category, Task
from Accounts.models import Profile

## Write your Functional views here
@login_required
@api_view(['GET', 'POST'])
def api_task_list(request):
    if request.method == "GET":
        queryset = Task.objects.filter(author=Profile.objects.get(profile_user=request.user))
        serializer = TaskSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)

@login_required
@api_view()
def api_task_detail(request, pk):
    profile_determine = Profile.objects.get(profile_user=request.user)
    task = get_object_or_404(Task, id=pk)
    if profile_determine == task.author:
        serializer = TaskSerializer(task, context={'request': request})
        return Response(serializer.data)
    else:
        raise PermissionDenied('You have not permission to see task details')

@login_required
@api_view(['GET', 'PUT'])
def api_task_edit(request, pk):
    profile_determine = Profile.objects.get(profile_user=request.user)
    task = get_object_or_404(Task, id=pk)
    if profile_determine == task.author:
        if request.method == 'PUT':
            serializer = TaskSerializer(task, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        serializer = TaskSerializer(task, context={'request': request})
        return Response(serializer.data)
    else:
        raise PermissionDenied('You have not permission to Edit task details')

@login_required
@api_view(['GET', 'DELETE'])
def api_task_delete(request, pk):
    profile_determine = Profile.objects.get(profile_user=request.user)
    task = get_object_or_404(Task, id=pk)
    if profile_determine == task.author:
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        raise PermissionDenied('You have not permission to delete task')