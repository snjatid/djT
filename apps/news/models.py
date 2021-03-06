from django.db import models

# 新闻标签model

class NewTag(models.Model):
    name = models.CharField(max_length=30)
    # 创建时间
    create_data = models.DateTimeField(auto_now_add=True)
    # 用于判断是否删除 ，删除了设置为False updata(id_delete=False)
    is_delete = models.BooleanField(default=True)


# 新闻model

class News(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    # 缩略图的url地址
    thumbnail_url = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)
    # on_delete=models.SET_NULL 置空
    tag = models.ForeignKey("NewTag", on_delete=models.CASCADE)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)

    class Meta:

        # 新闻倒序 -id 默认是正序  ["-id"]
        ordering = ("-id",)


# 新闻评论model
class NewsComment(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    # 新闻评论所属的新闻
    author = models.ForeignKey('account.User', on_delete=models.CASCADE)
    # 通过新闻找评论 用comments 没写related_name用News_set,反向查找的名子
    news = models.ForeignKey("News", on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ['-id']
