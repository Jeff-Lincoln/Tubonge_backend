# main_app/admin.py
from django.contrib import admin
from .models import StreamUser

@admin.register(StreamUser)
class StreamUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'created_at', 'last_active')
    search_fields = ('user_id', 'name', 'email')
