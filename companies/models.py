from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Company(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='companies', null=True)
    employee_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name
