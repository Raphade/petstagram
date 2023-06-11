from django.core.paginator import Paginator
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from posts.models import Post


# Create your views here.
def home(request):
    user = request.user
    liked_posts = []
    # Überprüfen, ob der Benutzer eingeloggt ist
    if user.is_authenticated and user.profile.subscribed.all():
        # Posts des eingeloggten Benutzers abrufen und nach Erstellungsdatum sortieren
        posts = Post.objects.filter(poster__in=user.profile.subscribed.all()).order_by('-date')
        liked_posts = user.profile.liked_posts.all()
    else:
        # Zufällige Posts abrufen, sortiert nach absteigendem Erstellungsdatum
        # Auf maximal 100 Posts pro Tag begrenzen
        posts = Post.objects.annotate(truncated_date=TruncDate('date')).order_by('?')
        post_dates = posts.values('date').annotate(count=Count('id'))
        for post_date in post_dates:
            if post_date['count'] > 100:
                posts = posts.filter(date=post_date['date'])[:100]

    # Pagination einrichten
    print(posts)
    paginator = Paginator(posts, 10)  # Anzahl der Posts pro Seite festlegen

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/home.html', {'page_obj': page_obj, 'liked_posts': liked_posts})


def like_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.profile
        if user_profile in post.post_likes.all():
            post.post_likes.remove(user_profile)
            message = 'Post unliked.'
        else:
            post.post_likes.add(user_profile)
            message = 'Post liked.'
        return JsonResponse({'message': message})
    return JsonResponse({'message': 'Invalid request.'})


def get_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id)
        comments = post.comment_set.all()
        comments_data = []
        for comment in comments:
            comment_data = {
                'commenter_profile_picture': comment.commenter.profile_picture.url,
                'commenter_username': comment.commenter.user.username,
                'text': comment.text,
                'comment_likes_count': comment.comment_likes.count(),
            }
            comments_data.append(comment_data)
        post_data = {
            'media': post.media.url,
            'poster_profile_picture': post.poster.profile_picture.url,
            'poster_username': post.poster.user.username,
            'comments': comments_data,
        }
        print(post.poster)
    return JsonResponse({'post': post_data})


def about(request):
    return render(request, 'posts/about.html', {'title': 'About'})
