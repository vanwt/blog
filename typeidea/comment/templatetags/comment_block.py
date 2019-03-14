from django import template

from ..forms import CommentForm
from ..models import Comment

#注册一个自定义签的装饰器
register = template.Library()

#传一个参数 是你自定义展示模块的位置
@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target':target,
        'comment_form':CommentForm,
        'comment_list':Comment.get_by_target(target)
    }