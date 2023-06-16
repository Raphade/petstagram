from django.core.paginator import Paginator
from django.db.models.functions import TruncDate
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from users_pet.models import Profile
from .forms import PostForm, CommentForm
from .models import Post, Comment


# Create your views here.
def home(request):
    comment_form = CommentForm()
    req_user = request.user
    liked_posts = []
    if req_user.is_authenticated:
        profile = get_object_or_404(Profile, user=req_user)
        subscribed_profiles = Profile.objects.filter(user=req_user).exclude(pk=profile.pk)
        liked_posts = profile.liked_posts.all()
        if subscribed_profiles.exists():
            # Posts des eingeloggten Benutzers abrufen und nach Erstellungsdatum sortieren
            posts = Post.objects.filter(poster__in=profile.subscribed.all()).order_by('-date')
        else:
            # Zufällige Posts abrufen, sortiert nach absteigendem Erstellungsdatum
            # Auf maximal 100 Posts pro Tag begrenzen
            posts = Post.objects.annotate(truncated_date=TruncDate('date')).order_by('?')
            post_dates = posts.values('date').annotate(count=Count('id'))
            for post_date in post_dates:
                if post_date['count'] > 100:
                    posts = posts.filter(date=post_date['date'])[:100]
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
    return render(request, 'posts/home.html', {'page_obj': page_obj, 'liked_posts': liked_posts,
                                               'comment_form': comment_form})


@login_required()
def like_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.profile
        if user_profile in post.post_likes.all():
            post.post_likes.remove(user_profile)
            message = 'unliked.'
        else:
            post.post_likes.add(user_profile)
            message = 'liked.'
        return JsonResponse({'message': message})
    return JsonResponse({'message': 'Invalid request.'})


@login_required()
def like_comment(request, post_id, comment_id):
    if request.method == 'POST' and request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
        user_profile = request.user.profile
        if user_profile in comment.comment_likes.all():
            comment.comment_likes.remove(user_profile)
            message = 'unliked.'
        else:
            comment.comment_likes.add(user_profile)
            message = 'liked.'
        return JsonResponse({'message': message})
    return JsonResponse({'message': 'Invalid request.'})


def get_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id)
        comments = post.comment_set.all()
        comments_user = comments.filter(commenter=request.user.profile).order_by('-comment_likes', 'date')
        comments_all = comments.exclude(commenter=request.user.profile)
        comments_all = comments_all.order_by('comment_likes', '-date')
        comments_req = list(comments_user) + list(comments_all)
        comments_data = []

        for comment in comments_req:
            comment_liked = comment.comment_likes.filter(id=request.user.profile.id).exists()
            comment_data = {
                'comment_id': comment.id,
                'commenter_profile_picture': comment.commenter.profile_picture.url,
                'commenter_username': comment.commenter.user.username,
                'text': comment.text,
                'comment_likes_count': comment.comment_likes.count(),
                'comment_date': comment.date,
                'comment_liked': comment_liked,
            }
            comments_data.append(comment_data)
        post_data = {
            'post_id': post.id,
            'media': post.media.url,
            'poster_profile_picture': post.poster.profile_picture.url,
            'poster_username': post.poster.user.username,
            'comments': comments_data,
        }
        print(post.poster)
    return JsonResponse({'post': post_data})


@login_required()
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # Get the current instance object to display in the template
            post.poster = get_object_or_404(Profile, user=request.user)
            post.save()
            return render(request, 'posts/createpost.html', {'title': 'Create Post', 'form': form, 'post': post})
        else:
            print(form.errors)
    else:
        form = PostForm()
        return render(request, 'posts/createpost.html', {'title': 'Create Post', 'form': form})


def about(request):
    return render(request, 'posts/about.html', {'title': 'About'})


def search(request, query):
    if request.method == 'GET':
        if query == "all":
            profiles = Profile.objects.all()
        else:
            profiles = Profile.objects.filter(user__username__icontains=query)
        # posts = Post.objects.filter(caption__icontains=query)
        return render(request, 'posts/search.html', {'profiles': profiles, 'query': query})


def profile(request, user_id):
    user = get_object_or_404(Profile, pk=user_id)
    print(user)
    user_posts_list = Post.objects.filter(poster=user).order_by('-date')
    paginator = Paginator(user_posts_list, 10)  # Show 10 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user': profile,
        'user_posts': page_obj,
    }
    return render(request, 'posts/profile.html', {'user': user, 'user_posts': page_obj})


@login_required
def comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        print("POST IST ANGEKOMMEN")
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            print("FORM IST VALID")
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.commenter = request.user.profile
            new_comment.save()
            return JsonResponse({
                'success': True,
                'comment': {
                    'commenter_username': new_comment.commenter.user.username,
                    'commenter_profile_picture': new_comment.commenter.profile_picture.url,
                    'text': new_comment.text,
                    'comment_likes_count': new_comment.comment_likes.count(),
                }
            })
    else:
        return HttpResponseRedirect('/')

    @login_required()
    def sub_profile(request, user_id):
        user = Profile.objects.get(pk=request.user.id)
        to_sub = Profile.objects.get(pk=user_id)
        user.subscribed.add(to_sub)
        user.save()

        return profile(request, user_id)

    @login_required()
    def unsub_profile(request, user_id):
        user = Profile.objects.get(pk=request.user.id)
        to_unsub = Profile.objects.get(pk=user_id)
        user.subscribed.remove(to_unsub)
        user.save()

        return profile(request, user_id)

    @login_required()
    def sub_s_profile(request, user_id, query):
        user = Profile.objects.get(pk=request.user.id)
        to_sub = Profile.objects.get(pk=user_id)
        print(to_sub)
        user.subscribed.add(to_sub)
        user.save()

        return search(request, query)

    @login_required()
    def unsub_s_profile(request, user_id, query):
        user = Profile.objects.get(pk=request.user.id)
        to_unsub = Profile.objects.get(pk=user_id)
        user.subscribed.remove(to_unsub)
        user.save()

        return search(request, query)

    @login_required
    def comment(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        if request.method == 'POST':
            print("POST IST ANGEKOMMEN")
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                print("FORM IST VALID")
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.commenter = request.user.profile
                new_comment.save()
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'commenter_username': new_comment.commenter.user.username,
                        'commenter_profile_picture': new_comment.commenter.profile_picture.url,
                        'text': new_comment.text,
                        'comment_likes_count': new_comment.comment_likes.count(),
                    }
                })
        else:
            return HttpResponseRedirect('/')
