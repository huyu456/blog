from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

    # 获取博客分类的数量
    def blog_count(self):
        return self.blog_set.count()


class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(verbose_name='缩略图',upload_to='images')
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog:%s>"%self.title

    def get_read_num(self):
        try:
            return self.readnum.read_num
        except:
            return 0
    # 按创建时间倒序排列

    class Meta:
        ordering = ['-created_time']


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING,)#  1对1
    # on_delete=models.DO_NOTHING)指定删除行为对于博客无影响

    def __str__(self):
        return str(self.blog)
