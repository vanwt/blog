from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    '''
    1. 用来自动补充文章分类标签友联这些model的owner字段
    2. 用来针对quesyset 过滤只能换换是当前用户创建的标签
    '''
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        print(request.user)
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)