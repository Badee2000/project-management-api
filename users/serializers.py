from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import Invitation


class CustomUserDetailsSerializer(UserDetailsSerializer):
    # remaining_tasks = serializers.SerializerMethodField()

    # def get_remaining_tasks(self, obj):
    #     return obj.remaining_tasks()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + \
            ('position', 'remaining_tasks')
        read_only_fields = ('position',)


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient_email', 'accepted']
        extra_kwargs = {'sender': {'read_only': True}}
