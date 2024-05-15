from django.contrib import admin
from .models import CustomUser, Invitation
# Register your models here.


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'first_name', 'last_name',
              'email', 'password', 'position', 'verified', 'company', 'manager']
    list_display = ['username', 'email', 'position',
                    'verified', 'company', 'manager']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    fields = ['sender', 'recipient_email', 'accepted', 'token']
    list_display = ['sender', 'recipient_email', 'accepted']
