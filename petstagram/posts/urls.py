from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='posts-home'),
    path('about/', views.about, name='posts-about'),
]