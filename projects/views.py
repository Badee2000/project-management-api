from rest_framework import generics, permissions, status, response
from .serializers import ProjectSerializer
from .models import Project
from rest_framework import permissions
from users.permissions import IsVerified, IsManager, IsOwnerOrManager
from .permissions import IsOwnerOrManagerOrBelongsTo
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound

# Create your views here.


# NEEDS EDITING
###############
class CreateProject(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsOwnerOrManager]
###############


class ListProjects(generics.ListAPIView):
    serializer_class = ProjectSerializer
    # To be able to show "YOUR" projects, you need to be a manager in the facility.
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsOwnerOrManager]
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10

    # Query only projects that belong to the manager.
    # Or to the company if the request from the owner.

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(manager=user) | Q(company__owner=user))


class DetailProject(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsOwnerOrManagerOrBelongsTo]

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except NotFound:
            return response.Response({'error': 'There is no company with this id'}, status=status.HTTP_404_NOT_FOUND)
