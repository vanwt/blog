from django.contrib import admin
# from .custom_site import custom_site
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.
from custom_site import custom_site

from base_admin import BaseOwnerAdmin
from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from django.contrib.admin.models import LogEntry #引入登陆日志

class PostInline(admin.TabularInline):
    #定义这个后可以在下面的admin中修改Post的内容
    fields = ['title','desc']
    extra = 1
    model = Post

@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline,]
    list_display = ('name','status','is_nav','created_time')
    fields = ('name','status','is_nav')

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)

    def __str__(self):
        return self.name

@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    def __str__(self):
        return self.name




#重写过滤机制，加入自己定义的过滤
class CategoryFilter(admin.SimpleListFilter):
    '''自定义用户只显示当前用户分类'''
    title = '过滤分类器'
    #查询是URL参数
    parameter_name = 'owner_category'

    #返回要查询的内容和要展示的ID
    def lookups(self, request, model_admin):
        #查询出当前用户id的编号和分类名
        return Category.objects.filter(owner=request.user).values_list('id','name')
    #根据urlquery的的内容返回列表数据
    #比如查询id是1 的使用 ，url后的query 是 ？owner_category = 1
    # 那么self.value()这里拿到的就是1 ,此时就会根据1来过滤query set
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ['title','category','status','created_time','owner','operator']
    list_display_links = []
    list_filter = [CategoryFilter]
    search_fields = ['title','category']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True
    exclude = ('owner',)
    # fields = (
    #     ('category','title'),'desc','status','content','tag'
    # )
    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields': (('category','title'),'status')
        }),
        ('内容',{
            'fields':('desc','content')
        }),
        ('额外的信息',{
            'classes':('collapse',),
            'fields':('tag',)
        })
    )
    filter_vertical = ('tag',)
    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',reverse('cus_admin:blog_post_change',args=(obj.id,))
        )
    #指定表头的展示文案
    operator.short_description = '操作'

@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_id','object_repr','action_flag','user','change_message']
