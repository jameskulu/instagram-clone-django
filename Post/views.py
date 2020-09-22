from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Tag, Comment
from .forms import PostForm
from django.contrib.auth.models import User
from Users.models import Profile
from itertools import chain
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


@login_required
def index(request):
    users = User.objects.exclude(username=request.user)[:5]
    profile = Profile.objects.get(user=request.user)
    followed_user = [
        followed_user for followed_user in profile.following.all()]
    all_posts = []
    for f in followed_user:
        p = Profile.objects.get(user=f)
        p_posts = p.post_set.all()
        all_posts.append(p_posts)
    my_posts = profile.post_set.all()
    all_posts.append(my_posts)

    if len(all_posts) > 0:
        qs = sorted(chain(*all_posts), reverse=True,
                    key=lambda obj: obj.date_created)

    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 2)
    try:
        paginated_post = paginator.page(page)
    except PageNotAnInteger:
        paginated_post = paginator.page(1)
    except EmptyPage:
        paginated_post = paginator.page(paginator.num_pages)

    posts_count = 0
    for a in qs:
        post = Post.objects.get(id=a.id)
        if post.archive == False:
            posts_count += 1

    context = {
        'all_posts': paginated_post,
        'users': users,
        'posts_count': posts_count
    }
    return render(request, 'Post/index.html', context)


@login_required
def likes(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        likes_obj = request.POST.get('like_name')
        obj = Post.objects.get(id=likes_obj)
        if profile.user in obj.likes.all():
            obj.likes.remove(profile.user)
        else:
            obj.likes.add(profile.user)

        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def dislikes(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        dislikes_obj = request.POST.get('dislike_name')
        obj = Post.objects.get(id=dislikes_obj)
        if profile.user in obj.dislikes.all():
            obj.dislikes.remove(profile.user)
        else:
            obj.dislikes.add(profile.user)

        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def upload(request):
    user = request.user
    tag_obj = []
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            caption = form.cleaned_data.get('caption')
            file = form.cleaned_data.get('file')

            tags_form = form.cleaned_data.get('tag')
            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(name=tag)
                tag_obj.append(t)

            p = Post.objects.create(
                caption=caption, user=user.userprofile, file=file)
            # obj = form.save(commit=False)
            # obj.tag.set(tag_obj)
            # obj.user = user.profile
            p.tag.set(tag_obj)
            p.save()
            return redirect('home')
    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'Post/upload.html', context)


@login_required
def tag_page(request, tag_slug):
    tags = Post.objects.filter(tag__name=tag_slug, archive=False)
    tags_count = tags.count
    page = request.GET.get('page', 1)
    paginator = Paginator(tags, 2)
    try:
        paginated_post = paginator.page(page)
    except PageNotAnInteger:
        paginated_post = paginator.page(1)
    except EmptyPage:
        paginated_post = paginator.page(paginator.num_pages)

    context = {
        'tags': paginated_post,
        'tag_slug': tag_slug,
        'tags_count': tags_count
    }
    return render(request, 'Post/tags.html', context)


@login_required
def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-date_created')

    context = {
        'post': post,
    }
    return render(request, 'Post/detail.html', context)


@login_required
def comment(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        comment_value = request.POST.get('comment-input')
        Comment.objects.create(content=comment_value,
                               user=request.user, post=post)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def update(request, pk):
    post = Post.objects.get(pk=pk)
    if post.user.user == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = PostForm(instance=post)
    else:
        return HttpResponse('You are not authorized to view this page.')
    context = {
        'form': form
    }
    return render(request, 'Post/upload.html', context)


@login_required
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    if post.user.user == request.user:
        post.delete()
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.user == request.user:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def search(request):
    my_profile = Profile.objects.get(user=request.user)

    value = request.GET.get('s')
    if value == '':
        return redirect(request.META.get('HTTP_REFERER'))

    users = User.objects.filter(username__icontains=value)
    context = {
        'users': users,
        'value': value
    }
    return render(request, 'Post/search.html', context)


@login_required()
def save(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    user = request.user
    if posts.save_post.filter(id=user.id).exists():
        posts.save_post.remove(user)
    else:
        posts.save_post.add(user)
    return redirect(request.META.get('HTTP_REFERER'))
