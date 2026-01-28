from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_, name="login"),
    path('logout', logout_, name="logout"),
    path('user', users, name="users"),
    path('create_user', create_user, name="create_user"),
    path('delete_user/<int:id>', delete_user, name="delete_user"),
    path('', admins, name="admins"),
    path('create_admin', create_admin, name="create_admin"),
    path('delete_admin//<int:id>', delete_admin, name="delete_admin"),
    path('task', tasks, name="tasks"),
    path('create_task', create_task, name="create_task"),
    path('delete_task/<int:id>', delete_task, name="delete_task"),
    path('task-report', task_reports, name="task_reports"),
]