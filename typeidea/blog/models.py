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

    class Meta:
        db_table = 'post'
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']#根据ID降序排列
