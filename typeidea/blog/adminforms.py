from django import forms
class PostAdminForm(forms.ModelForm):
    '''
    相当于覆盖了django的原生模块，在这之前desc模块是一个text的input框
    当用了adminform就可以吧desc这个框改成多文本输入框
    需要在定义的adminform中:
    form = PostAdminForm
    '''
    desc = forms.CharField(widget=forms.Textarea,label='摘要',required=False)