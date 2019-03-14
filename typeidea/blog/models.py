from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#类别表
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除')
    )
    #用户名
    name = models.CharField(max_length=50,verbose_name='名称')
    #状态
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    #是否是导航栏
    is_nav = models.BooleanField(default=False,verbose_name='是否为导航栏')
    #作者
    owner = models.ForeignKey(User,verbose_name='作者')
    #创建时间
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'category'
        verbose_name = verbose_name_plural = '分类'
    def __str__(self):
        return self.name
    @classmethod
    def get_navs(cls):
        categories = Category.objects.filter(status=cls.STATUS_NORMAL)
        nav_category = []
        normal_category = []
        for cate in categories:
            if cate.is_nav:
                nav_category.append(cate)
            else:
                normal_category.append(cate)

        return {
            'navs':nav_category,
            'categories':normal_category
        }
#标签表
class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    name = models.CharField(max_length=10, verbose_name='名称')
    # 状态
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    # 是否是导航栏
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航栏')
    # 作者
    owner = models.ForeignKey(User, verbose_name='作者')
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tag'
        verbose_name = verbose_name_plural = '标签'
    def __str__(self):
        return self.name
#文章
class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT,'草稿')
    )
    title = models.CharField(max_length=255,verbose_name='标题')
    desc = models.CharField(max_length=1024,blank=True,verbose_name='摘要')
    content = models.TextField(verbose_name='正文',help_text="正文必须是MarkDown格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS)
    category = models.ForeignKey(Category,verbose_name='分类')
    #和标签是多对多关系
    tag = models.ManyToManyField(Tag,verbose_name='标签')
    # 合作者是一对多关系
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    #阅读量,访问量
    pv = models.PositiveIntegerField(default=0)
    uv = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'post'
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']#根据ID降序排列
    #自定义一个查询标签的方法
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list= []
        else:
            #解决了n+1问题，查询所有的文章同时把所有的 owner category查询出来
            #post_set 是一对多 django自动创建的函数
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('category','owner')
        return post_list,tag
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            # post_set 是django 一对多映射自动生成的一个参数
            post_list = category.post_set.filter(status = Post.STATUS_NORMAL).select_related('owner')
            print(post_list)

        return post_list,category

    @classmethod
    def latest_posts(cls):#查询出所有是状态正确的博客
        return cls.objects.filter(status = cls.STATUS_NORMAL)

    @classmethod
    def hot_post(cls):
        return cls.object.filter(status=cls.STATUS_NORMAL).order_by('-pv')