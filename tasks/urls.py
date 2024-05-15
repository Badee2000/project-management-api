from django.urls import path
from .views import ListTasks, CreateTask, DetailTask


urlpatterns = [
    path('', ListTasks.as_view()),
    path('create/', CreateTask.as_view()),
    path('<int:pk>/', DetailTask.as_view()),
]
