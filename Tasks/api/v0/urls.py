from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_task_list, name='api-task-list'),
    path('<int:pk>/', views.api_task_detail, name='api-task-detail'),
]
