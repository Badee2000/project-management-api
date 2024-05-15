from django.urls import path
from .views import InviteUserView, AcceptInvitationView, ListAccounts, DetailAccount

urlpatterns = [
    path('users/', ListAccounts.as_view()),
    path('users/<int:pk>', DetailAccount.as_view()),
    path('invite/', InviteUserView.as_view(), name='invite_user'),
    path('invite/<str:token>/accept/',
         AcceptInvitationView.as_view(), name='accept_invitation'),

]
