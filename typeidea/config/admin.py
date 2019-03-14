from django.contrib import admin
from .models import SideBar,Link
from base_admin import BaseOwnerAdmin
# Register your models here.

@admin.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ['title','href','status','weight','created_time']

    fields = ['title','href','status','weight']

@admin.register(SideBar)
class SideBar(BaseOwnerAdmin):
    list_display = ['title','display_type','content','created_time']
    fields = ('title','display_type','content')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBar,self).save_model(request,obj,form,change)
