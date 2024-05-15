from django.shortcuts import render
from rest_framework import generics
from .models import Company
from rest_framework import permissions, response, status, serializers
from .serializers import CompanySerializer
from users.permissions import IsVerified
from .permissions import IsCompanyOwner
from rest_framework.exceptions import NotFound

# Create your views here.


class ListCompanies(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, permissions.IsAdminUser]


class DetailCompany(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    model = Company
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsCompanyOwner]

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except NotFound:
            return response.Response({'error': 'There is no company with this id'}, status=status.HTTP_404_NOT_FOUND)


class CreateCompany(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsVerified]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.validated_data

        # Get the user who created the company
        user = self.request.user

        # Set the user's position to 'owner'
        if not user.company:
            # Create a new instance of the Company model
            company_instance = Company.objects.create(**company)
            user.position = 'owner'
            user.company = company_instance['name']
            user.save()

            return response.Response({'message': 'Company created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return response.Response({'message': 'You cannot be an employee in a company and an owner of another company at the same time!'}, status=status.HTTP_400_BAD_REQUEST)
