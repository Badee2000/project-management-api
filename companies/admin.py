from django.contrib import admin
from .models import Company

# Register your models here.


@admin.register(Company)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee_count']
