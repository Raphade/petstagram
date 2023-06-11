from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='posts-home'),
    path('about/', views.about, name='posts-about'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('posts/<int:post_id>/', views.get_post, name='get-post'),
]
