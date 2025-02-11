from django.urls import path
from .views import create_task, get_tasks, get_task, update_task, delete_task

urlpatterns = [
    path("tasks/", get_tasks, name="task-list"),
    path("tasks/create/", create_task, name="create-task"),
    path("tasks/<int:task_id>/", get_task, name="task-detail"),
    path("tasks/<int:task_id>/update/", update_task, name="update-task"),
    path("tasks/<int:task_id>/delete/", delete_task, name="delete-task"),
]

