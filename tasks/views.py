from django.shortcuts import render
from .serializers import TaskSerializer, TaskCreateSerializer
from rest_framework import generics, status, response
from rest_framework.response import Response
from rest_framework import permissions
from users.permissions import IsVerified, IsOwnerOrManager
from .permissions import IsOwnerOrManagerOrBelongsTo
from .models import Task
from rest_framework.pagination import LimitOffsetPagination
from projects.models import Project
from users.models import CustomUser
from rest_framework.exceptions import NotFound

# Create your views here.


# NEEDS EDITING
###############
class CreateTask(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsOwnerOrManager]
###############


class ListTasks(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerified]
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10

    def get_queryset(self):
        user = self.request.user
        if user.position == 'manager':
            return Task.objects.filter(project__manager=user)
        elif user.position == 'employee':
            return Task.objects.filter(assigned_to=user)
        elif user.position == 'owner':
            return Task.objects.filter(project__company=user.company)


class DetailTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsOwnerOrManagerOrBelongsTo]

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except NotFound:
            return response.Response({'error': 'There is no company with this id'}, status=status.HTTP_404_NOT_FOUND)
