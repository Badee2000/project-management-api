from rest_framework import serializers
from .models import Task
from projects.models import Project
from users.models import CustomUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# NEEDS EDITING
###############
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description',
                  'priority', 'assigned_to', 'status']
###############
