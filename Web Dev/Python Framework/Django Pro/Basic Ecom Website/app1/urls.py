from . import views
from django.urls import path

urlpatterns = [
    path('', views.index,name="appHome"),
    path('/about', views.about,name="appAbout"),
    path('/contact', views.contact,name="appContact"),
    path('/tracker', views.tracker,name="appTracker"),
]