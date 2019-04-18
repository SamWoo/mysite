from django import forms

from comment.models import Comment


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            # 为各个需要渲染的字段指定渲染成什么html组件，主要是为了添加css样式。
            # 例如 user_name 渲染后的html组件如下：
            # <input type="text" class="form-control" placeholder="Username" aria-describedby="sizing-addon1">
            # 'user_name': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': "请输入昵称",
            #     'aria-describedby': "sizing-addon1",
            # }),
            'content': forms.Textarea(attrs={
                'placeholder': '请输入评论...',
                'rows': '5',
                'cols':'100',
                # 'style': 'margin: 4px;border-radius: 4px;',
                'id': 'comment',
                'name': 'comment',
                'class': 'form-control'
            }),
        }
