from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from Post.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def profile(request, username):
    userr = User.objects.get(username=username)
    users = Profile.objects.get(user=userr.id)
    posts = Post.objects.filter(user=users).order_by('-date_created')
    posts_count = Post.objects.filter(
        user=users, archive=False).order_by('-date_created').count()
    my_profile = Profile.objects.get(user=request.user)

    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 2)

    try:
        paginated_post = paginator.page(page)
    except PageNotAnInteger:
        paginated_post = paginator.page(1)
    except EmptyPage:
        paginated_post = paginator.page(paginator.num_pages)

    context = {
        'users': userr,
        'posts': paginated_post,
        'posts_count': posts_count
    }
    if users.user in my_profile.following.all():
        follow = True
    else:
        follow = False
    context['follow'] = follow
    return render(request, 'Users/profile.html', context)


@login_required
def follow_unfollow(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        follow_user = request.POST.get('follow-btn')
        obj = Profile.objects.get(id=follow_user)
        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile', pk=my_profile.id)


@login_required
def edit_profile(request):
    edit_profile_msg = ''
    message = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST,
                             instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully')
            return redirect('profile', username=request.user)
        else:
            edit_profile_msg = 'Username is already taken'
            # return redirect('edit-profile')

        if edit_profile_msg:
            message = edit_profile_msg

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    print(edit_profile_msg)
    context = {
        'message': message,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'Users/edit_profile.html', context)


# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(
#                 request, 'Your password was successfully updated!')
#             return redirect('manage-profile')

#     else:
#         form = PasswordChangeForm(request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, 'Users/change_password.html', context)

@login_required
def archive(request):
    posts = Post.objects.filter(archive=True)
    context = {
        'posts': posts
    }
    return render(request, 'Users/archive.html', context)


def archive_toggle(request, pk):
    post = Post.objects.get(pk=pk)
    if post.archive == False:
        post.archive = True
        post.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        post.archive = False
        post.save()
        return redirect(request.META.get('HTTP_REFERER'))


def save_posts(request):
    posts = Post.objects.filter(save_post__id=request.user.id)
    context = {
        'posts': posts
    }
    return render(request, 'Users/save_post.html', context)
