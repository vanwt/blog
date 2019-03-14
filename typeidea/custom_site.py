from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_title = '博客管理后台'
    site_header = 'Blog后台管理'#登陆时的样式
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')
