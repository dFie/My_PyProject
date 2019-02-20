from django.db import models
from user.models import User

class Post(models.Model):
    class Meta:
        db_table = 'post'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, null=False)
    postdate = models.DateTimeField(null=False)
    # 从post查作者，从post查内容
    author = models.ForeignKey(User)    # 指定外键，migrate会生成author_id字段
    # self.content可以访问Content实例，其内容是self.content.content

    def __repr__(self):
        return '<Post {} {} {}>'.format(self.id, self.title, self.author_id, self.content)

    __str__ = __repr__


class Content(models.Model):
    class Meta:
        db_table = 'content'

    # 没有主键，会自动创建一个自增主键  # id 字段
    post = models.OneToOneField(Post, to_field='id')   # 1对1，这边会有一个外键引用post.id；# post_id字段
    content = models.TextField(null=False)  # content字段

    def __repr__(self):
        return '<Content {} {}>'.format(self.post.id, self.content[:20])

    __str__ = __repr__
