from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Post, Group
from .forms import PostForm


def index(request):
    post_list = Post.objects.select_related('group').order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('posts:index')

        return render(request, 'new_post.html', {'form': form})

    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    user = get_user_model()
    user_posts = get_object_or_404(user, username=username)
    posts = user_posts.posts.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'user_posts': user_posts,
                                            'page': page})


def post_view(request, username, post_id):
    user = get_user_model()
    user_posts = get_object_or_404(user, username=username)
    post = user_posts.posts.get(id=post_id)
    return render(request, 'post.html', {'user_posts': user_posts,
                                         'post': post})


@login_required
def post_edit(request, username, post_id):
    user = get_user_model()
    user_post = get_object_or_404(user, username=username)
    post = user_post.posts.get(id=post_id)

    form = PostForm(instance=post)

    if request.method == 'GET':
        if request.user.id != user_post.id:
            return redirect(f'/{username}/{post_id}')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/{username}/{post_id}')

        return render(request, 'new_post.html', {'form': form,
                                                 'edit_mode': True})

    return render(request, 'new_post.html', {'form': form,
                                             'edit_mode': True})
