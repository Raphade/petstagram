
from . import views
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .serializer import UserViewSet, PostViewSet, ProfileViewSet, CommentViewSet

# Source: https://www.django-rest-framework.org/
# Serializers define the API representation.




# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# Adding API Routes
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'comments', CommentViewSet)
print(router.urls)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.home, name='posts-home'),
    path('about/', views.about, name='posts-about'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('posts/<int:post_id>/comment/<int:comment_id>/like/', views.like_comment, name='like-comment'),
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
