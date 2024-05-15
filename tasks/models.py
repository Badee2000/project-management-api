from django.db import models
from projects.models import Project
from users.models import CustomUser
# Create your models here.


class Task(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.IntegerField(
        choices=((1, 'High'), (2, 'Medium'), (3, 'Low')))
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name='tasks')
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')))

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title
