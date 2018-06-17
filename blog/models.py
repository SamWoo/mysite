from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.
from django.utils.html import strip_tags
import markdown
from mdeditor.fields import MDTextField


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(verbose_name='文章类别', max_length=20)

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(verbose_name='文章标签', max_length=20)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    """
    博客
    """
    title = models.CharField(verbose_name='标题', max_length=100)
    content = MDTextField(verbose_name='正文', default='')
    excerpt = models.CharField(verbose_name='摘要', max_length=200, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    click_nums = models.IntegerField(verbose_name='点击量', default=0)
    comment_nums = models.IntegerField(verbose_name='评论', default=0)
    category = models.ForeignKey(Category, verbose_name='文章类别', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')

    class Meta:
        verbose_name = "我的博客"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        '''
        自定义 get_absolute_url 方法
        记得从 django.urls 中导入 reverse 函数
        :return:
        '''
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        '''
        自动截取生成文章摘要
        '''
        # 如果没有填写摘要
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.fenced_code'
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.content))[:150]
            # 调用父类的 save 方法将数据保存到数据库中
        super(Blog, self).save(*args, **kwargs)

    def get_previous(self):
        '''
        获取前一篇
        :param pk:
        :return:
        '''
        try:
            return self.__class__.objects.filter(id__lt=self.id).order_by('-id')[0]
        except:
            return '没有了!!'

    def get_next(self):
        '''
        获取后一篇
        :param pk:
        :return:
        '''
        try:
            return self.__class__.objects.filter(id__gt=self.id).order_by('-id')[0]
        except:
            return '没有了!!'

    def increase_views(self):
        '''
        统计文章点击率
        '''
        self.click_nums += 1
        self.save(update_fields=['click_nums'])
