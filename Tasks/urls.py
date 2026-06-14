from django.urls import path, include
from . import views

app_name = 'Tasks'

urlpatterns = [
    # task app APIs
    path('api/v0/', include("Tasks.api.v0.urls")),
    # Target UI/UD target design
    path('target-design/', views.target_design, name='target-design'),
    # task views based api
    path('list/', views.api_task_list, name='api-task-list'),
    # task views
    path('', views.task_list, name='task-list' ),
    path('<int:pk>/', views.task_detail, name='task-detail'),
    path('<int:pk>/edit/', views.task_edit, name='task-edit'),
    path('<int:pk>/delete/', views.task_delete, name='task-delete'),
]