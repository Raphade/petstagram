from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='posts-home'),
    path('about/', views.about, name='posts-about'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('posts/<int:post_id>/comment/<int:comment_id>/like', views.like_comment, name='like-comment'),
    path('posts/<int:post_id>/', views.get_post, name='get-post'),
    path('posts/', views.create_post, name='create-post'),
    path('search/<str:query>/', views.search, name='search-profiles'),
    path('profile/<int:user_id>/', views.profile, name='load-profile'),
    path('sub_profile/<int:user_id>/', views.sub_profile, name='subscribe-profile'),
    path('unsub_profile/<int:user_id>/', views.unsub_profile, name='unsubscribe-profile'),
    path('sub_profile/<int:user_id>/<str:query>', views.sub_s_profile, name='subscribe-search-profile'),
    path('unsub_profile/<int:user_id>/<str:query>', views.unsub_s_profile, name='unsubscribe-search-profile'),
    path('posts/<int:post_id>/comment/', views.comment, name='comment-post'),
]
