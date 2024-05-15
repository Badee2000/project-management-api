from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'owner', 'employee_count']
        extra_kwargs = {'owner': {'read_only': True}}

    def validate(self, data):
        print(self)
        if data['employee_count'] <= 0:
            raise serializers.ValidationError(
                {'employee_count': 'Bruh, a negative employee_count!!!'})
        return data
