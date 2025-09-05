from django.contrib import admin
from .models import Character

@admin.register(Character)

class CharacterAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "status", "species", "origin_name")
    search_fields = ("name", "origin_name")
    list_filter = ("status", "species")