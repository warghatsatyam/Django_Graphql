from django.db import models

# Create your models here.


# myapp/models.py

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=70)
    content = models.TextField(verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]


