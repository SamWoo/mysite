import markdown
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import FormView
from django.views.generic.base import logger

from blog.models import Blog
from comment.forms import BlogCommentForm
from comment.models import Comment


class CommentPostView(FormView):
    # 指定使用的是哪个form
    form_class = BlogCommentForm
    # 指定评论提交成功后跳转渲染的模板文件。
    # 我们的评论表单放在detail.html中，评论成功后返回到原始提交页面。
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        """提交的数据验证合法后的逻辑"""

        # 首先根据 url 传入的参数（在 self.kwargs 中）获取到被评论的文章
        target_article = get_object_or_404(Blog, pk=self.kwargs['article_id'])

        # 调用ModelForm的save方法保存评论，设置commit=False则先不保存到数据库，
        # 而是返回生成的comment实例，直到真正调用save方法时才保存到数据库。
        comment = form.save(commit=False)
        text = comment.content

        # 把评论和文章关联
        comment.article = target_article
        if self.request.user.is_authenticated:
            comment.user = self.request.user
            print(comment.user)

        parent = None
        if text.startswith('@['):
            import ast
            parent_str = text[1:text.find(':')]
            parent_id = ast.literal_eval(parent_str)[1]
            text = text[text.find(':') + 1:]
            try:
                parent = Comment.objects.get(pk=parent_id)
            except Comment.DoesNotExist:
                return HttpResponse(u'引用评论错误!!')

        if not text:
            logger.error(u'[CommentControl]当前用户输入空评论:[{}]'.format(comment.user.username))
            return HttpResponse(u'请输入评论内容!!')

        comment.content = markdown.markdown(text,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
        comment.parent = parent
        comment.save()

        # 评论生成成功，重定向到被评论的文章页面
        self.success_url = target_article.get_absolute_url() + "#" + str(comment.pk)
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        """提交的数据验证不合法后的逻辑"""
        target_article = get_object_or_404(Blog, pk=self.kwargs['article_id'])

        # 不保存评论，回到原来提交评论的文章详情页面
        context = {
            'form': form,
            'article': target_article,
            'comment_list': target_article.comment_set.all()
        }
        return render(self.request, 'blog/detail.html', context=context)
