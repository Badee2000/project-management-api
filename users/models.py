from django.db import models
from django.contrib.auth.models import AbstractUser
from companies.models import Company
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False)
    # edit the view when creating a company with that user, so we can assign him to a company.
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    manager = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    # When creating a company, the user automatically will be an owner.
    position = models.CharField(max_length=50, choices=(
        ('manager', 'Manager'), ('employee', 'Employee'), ('owner', 'Owner')), default='employee')
    verified = models.BooleanField(default=False)

    # I want to count the remaining tasks for a user.

    def remaining_tasks(self):
        return self.tasks.filter(status='pending').count()


class Invitation(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient_email = models.EmailField()
    accepted = models.BooleanField(default=False)
    token = models.CharField(max_length=64, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'from {self.sender} to {self.recipient_email}'
