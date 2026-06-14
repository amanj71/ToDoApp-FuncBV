from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema

from .serializers import TaskSerializer
from Tasks.models import Category, Task
from Accounts.models import Profile

## Write your Functional views here

@swagger_auto_schema(
    method='post',
    request_body=TaskSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
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

@swagger_auto_schema(method='put', request_body=TaskSerializer, responses={200: 'Updated successfully'})
@swagger_auto_schema(method='delete', responses={204: 'Deleted successfully'})
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def api_task_detail(request, pk):
    profile_determine = Profile.objects.get(profile_user=request.user)
    task = get_object_or_404(Task, id=pk)
    if profile_determine == task.author:  
        if request.method == "PUT":
            serializer = TaskSerializer(task, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        elif request.method == "DELETE":
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = TaskSerializer(task, context={'request': request})
        return Response(serializer.data)
    else:
        raise PermissionDenied('You have not permission to see task details')




