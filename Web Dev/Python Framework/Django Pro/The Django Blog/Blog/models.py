from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Blogs(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 40 ,default='N/A')
    email = models.CharField(max_length = 40 ,default='N/A')
    author = models.CharField(max_length = 40 ,default='N/A')
    content = models.TextField( )
    slug = models.CharField(max_length=100)
    time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + 'by '+ self.author


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Blogs, on_delete = models.CASCADE)
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null = True)
    timeC = models.DateTimeField(default = now)

    def __str__(self):
        return self.comment[0:10] + "... by " + self.user.username