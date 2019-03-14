from django.contrib import admin
from .models import Comment
from base_admin import BaseOwnerAdmin

# Register your models here.
@admin.register(Comment)
class CommitAdmin(admin.ModelAdmin):
    list_display = ['target','nickname','content','website','created_time']
    list_display_links = ['target','nickname']


