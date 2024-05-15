from django.db import models
from django.contrib.auth import get_user_model
from companies.models import Company
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='projects')

    manager = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='projects')
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name
