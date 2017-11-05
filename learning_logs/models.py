from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """用户学习的主题"""
    owner = models.ForeignKey(User)
    text = models.CharField('主题', max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text


class Entry(models.Model):
    """用户记录的具体条目"""
    topic = models.ForeignKey(Topic, verbose_name='主题')
    text = models.TextField('详细内容')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """返回模型的字符串表示"""
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text
