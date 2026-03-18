from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'created_at', 'updated_at']
    search_fields = ['email', 'username']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']
