from django.urls import path, include
from . import views

app_name = 'Tasks'

urlpatterns = [
    path('api/v0/', include("Tasks.api.v0.urls")),
    path('', views.task_list, name='task-list' ),
    path('<int:pk>/', views.task_detail, name='task-detail'),
    path('<int:pk>/edit/', views.task_edit, name='task-edit'),
    path('<int:pk>/delete/', views.task_delete, name='task-delete'),
]