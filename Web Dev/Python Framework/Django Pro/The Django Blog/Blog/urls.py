from django.urls import path, include
from Blog import views

urlpatterns = [
    path('blogcomments',views.blogcomments, name='blogcomments'),
    path('',views.blog, name='blog'),
    path('<str:slug>',views.post, name='post'),
]
