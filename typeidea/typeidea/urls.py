"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from custom_site import custom_site
from blog.views import  *
from config.views import *
from comment.views import *

urlpatterns = [
    #主页
    url(r'^$',IndexView.as_view(),name='index'),
    #分类页
    url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(),name='category-list'),
    #我们在地址栏写的参数会传递到类中存放在 self.kwargs中，是一个字典
    url(r'^tag/(?P<tag_id>\d+)/$',TagView.as_view(),name='tag-list'),
    url(r'^post/(?P<pk>\d+)/$',PostDetailView.as_view(),name='post-detail'),
    #搜索
    url(r'^search/$',SearchView.as_view(),name='search'),
    #作者页面
    url(r'^about/(?P<id>\d+)/$',AuthorView.as_view(),name='author-id'),
    #友情链接
    url(r'^links/$',LinkListView.as_view(),name='links'),
    #评论
    url(r'^comment/$',CommentView.as_view(),name='comment'),
    url(r'^super_admin/',admin.site.urls,name='super-admin'),
    url(r'^admin/', custom_site.urls,name='admin'),#引入我们自定义的site
]
