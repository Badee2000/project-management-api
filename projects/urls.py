from django.urls import path
from .views import ListProjects, CreateProject, DetailProject


urlpatterns = [
    path('', ListProjects.as_view()),
    path('create/', CreateProject.as_view()),
    path('<int:pk>/', DetailProject.as_view()),
    # path('/<int:id>',)
]
