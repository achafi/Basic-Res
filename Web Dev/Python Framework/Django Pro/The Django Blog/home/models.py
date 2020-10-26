from django.db import models

# Create your models here.

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 40 ,default='N/A')
    email = models.CharField(max_length = 40 ,default='N/A')
    phone = models.CharField(max_length = 13 ,default='N/A')
    desc = models.TextField( )
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name