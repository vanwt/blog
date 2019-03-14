from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class':'form-control','style':'width:60%'}
        )
    )
    email = forms.CharField(
        label='邮箱',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class':'form-control','style':"width:60%"}
        )
    )
    website = forms.CharField(
        label='网站',
        widget=forms.widgets.URLInput(
            attrs={'class':'form-control','style':'width:60%'}
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'class':'form-control','rows':6,'cols':60}
        )
    )

    #对数据的一些验证 类似 flask-wtf 的validat_%
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 2:
            raise forms.ValidationError('内容长度太短!')
        return content
    class Meta:
        model = Comment
        fields = ['nickname','email','website','content']
