from django.shortcuts import render,redirect
from django.views.generic import TemplateView
# Create your views here.
from .models import *
from .forms import *
class CommentView(TemplateView):
    http_method_names = ['post'] #设置接受请求为post
    template_name = 'comment/result.html'

    def post(self,request,*args,**kwargs):

        comment_form = CommentForm(request.POST)
        target = request.POST.get('target',None)
        print(target)
        # print(target)
        # print(comment_form.data)
        # print(comment_form.is_valid())
        # print(comment_form.errors)
        # print(comment_form.cleaned_data)


        if comment_form.is_valid():

             instance = comment_form.save(commit=False) #获取数据生成数据库对象，但不提交
             instance.target = target
             instance.save()
             succeed = True
             return redirect(target)
        else:
            succeed = False

        context = {
            'succeed':succeed,
            'form':CommentForm,
            'target':target,
        }
        return self.render_to_response(context)
