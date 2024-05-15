from django.urls import path
from .views import ListCompanies, CreateCompany, DetailCompany


urlpatterns = [
    path('', ListCompanies.as_view()),
    path('create/', CreateCompany.as_view()),
    path('<int:pk>/', DetailCompany.as_view()),
]
