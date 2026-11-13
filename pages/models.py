from django.db import models

# 1. جدول التصنيفات الجديد
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 2. جدول المقالات (تم إضافة حقل التصنيف)
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    
    # ربط المقال بالتصنيف. (null=True تعني أنه يمكن أن يكون بدون تصنيف)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 3. جدول التعليقات
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تعليق بواسطة {self.name} على {self.article.title}"