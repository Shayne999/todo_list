from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path("tasks/", list_tasks, name="task-list"),
    path("tasks/create/", create_task, name="create-task"),
    path("tasks/<int:task_id>/", get_task, name="task-detail"),
    path("tasks/<int:task_id>/update/", update_task, name="update-task"),
    path("tasks/<int:task_id>/delete/", delete_task, name="delete-task"),
    path('logout/', user_logout, name='user-logout')
]

