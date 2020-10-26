from django.contrib import admin
from Blog.models import Blogs, BlogComment

# Register your models here.
admin.site.register((Blogs, BlogComment))