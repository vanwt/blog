from django.shortcuts import render, HttpResponse
from comment.forms import *
from comment.models import Comment
from .models import Tag, Post,Category
from django.db.models import Q
from django.views.generic import DeleteView,ListView
from django.shortcuts import get_object_or_404
#引入django定义的模板视图
from config.models import *

# Create your views here.
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list,category = Post.get_by_category(category_id)
#     else:
#         #如果都没有参数就把所有的查询出来
#         post_list = Post.latest_posts()
#
#     #传到前端的数据
#     context = {
#         'post_list':post_list,
#         'tag':tag,
#         'category':category,
#         'sidebars':SideBar.get_all()
#     }
#     context.update(Category.get_navs())
#     return render(request,'blog/list.html',context=context)

#使用ListViews处理带分页的数据很合适
# class PostListView(ListView):
#     queryset = Post.latest_posts() #获取数据
#     paginate_by = 1 #设置页数，可自定义
#     content_object_name = 'post_list' #这里如果不设置，默认就是object_list
#     template_name = 'blog/list.html' #设置模板
# def post_detazil(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {'post':post, 'sidebars':SideBar.get_all()}
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html',context=context)
# def links(request):
#     pass

# class PostDetailView(DeleteView):
    # #django都给我们封装好了方法，只需要简单的调用'''
    # model = Post # model属性指定当前View要使用的Model
    # #queryset 跟model一样，二选一，为了精确查找
    # # queryset = Post.objects.filter(status = Post.STATUS_NORMAL)
    # #模板名称
    # template_name = 'blog/detail.html'
    # #get_queryset 接口 ，用来获取数据
    # #get_object 接口 根据url参数，从queryset获取对应的实例
    # #get_context_data 获取从模板渲染的所有上下文
#所有用到的参数
class CommonViewMixin:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars':SideBar.get_all()
        })
        context.update(
            Category.get_navs()
        )
        return context
    #把数据都封装到此实例汇总
#主页
class IndexView(CommonViewMixin,ListView):
    queryset = Post.latest_posts() #获取数据
    #查询出来的数据自动封装在conetxt中，可以自定义添加重写

    paginate_by = 5 #设置页数，可自定义
    content_object_name = 'post_list' #这里如果不设置，默认就是object_list
    template_name = 'blog/list.html' #设置模板

    #书上讲的方法并没有写 获取顶部和底部，侧边栏
    #自己重写这个方法添加回去
    # 或者时候继承自自己定义的CommonViewMixin
    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data()
    #     context.update(Category.get_navs())
    #     context.update({'sidebars':SideBar.get_all()})
    #     return context

#分类筛选页
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data()
        category_id = self.kwargs.get('category_id')
        print(self.kwargs)
        category = get_object_or_404(Category,pk=category_id)
        context.update({'category':category})
        return context
    def get_queryset(self):
        '''重写queryset 根据分类过滤'''
        queryset =super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

#标签筛选页
class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        tag_id = self.kwargs.get('tag_id')
        #self.kwargs 中存放了前端传过来的参数
        tag = get_object_or_404(Tag,pk=tag_id)
        context.update({
            'tag':tag
        })
        return context
    def get_queryset(self):
        '''重写queryset根据标签过滤'''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

#博客内容详情页
class PostDetailView(CommonViewMixin,DeleteView):
    '''django都给我们封装好了方法，只需要简单的调用'''
    queryset = Post.latest_posts()
    content_object_name = 'post'

    #模板名称
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'pk'

    #因为需要评论记录所以重写 get_context_data
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form':CommentForm,
    #         'comment_list':Comment.get_by_target(self.request.path)
    #     })
    #     print(self.request.path)
    #     return context

#搜索功能
class SearchView(IndexView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword','')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

#作者ID 通过作者查看博客
class AuthorView(IndexView):
    # 只需要过滤数据源就行
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('id')
        return queryset.filter(owner_id = author_id)