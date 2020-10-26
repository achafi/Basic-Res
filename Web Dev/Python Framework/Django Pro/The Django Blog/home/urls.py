from django.urls import path, include
from home import views

urlpatterns = [
    path('',views.home, name='home'),
    path('contact',views.contact, name='contact'),
    path('about',views.about, name='about'),
    path('search',views.search, name='search'),
    path('signup',views.SignUpP, name='SignUpP'),
    path('login',views.loginP, name='loginP'),
    path('logout',views.logoutP, name='logoutP'),
]
