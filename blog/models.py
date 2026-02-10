from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    img_url = models.ImageField(null=True,upload_to='posts/images')
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    is_published = models.BooleanField(default=False)

    @property
    def formated_img_url(self):
        if not self.img_url:
            return None
        url = self.img_url if str(self.img_url).startswith(('http://','https://')) else self.img_url.url
        return url
    def __str__(self):
        return self.title

class AboutUs(models.Model):
    content = models.TextField()
