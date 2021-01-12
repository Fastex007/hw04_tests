from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Post, Group
from .forms import PostForm


POSTS_PER_PAGE = 10


def index(request):
    post_list = Post.objects.select_related('group').all()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group,
                                          'page': page,
                                          'paginator': paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('index')

        return render(request, 'new_post.html', {'form': form})

    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    user = get_user_model()
    user_posts = get_object_or_404(user, username=username)
    posts = user_posts.posts.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'user_posts': user_posts,
                                            'page': page,
                                            'paginator': paginator})


def post_view(request, username, post_id):
    user = get_user_model()
    user_posts = get_object_or_404(user, username=username)
    post = user_posts.posts.get(id=post_id)
    return render(request, 'post.html', {'user_posts': user_posts,
                                         'post': post})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.id != post.author_id:
        return redirect(
            reverse(
                'post',
                kwargs={'username': username, 'post_id': post_id}
            )
        )

    form = PostForm(request.POST or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    'post',
                    kwargs={'username': username, 'post_id': post_id}
                )
            )
    return render(request, 'new_post.html', {'form': form,
                                             'edit_mode': True,
                                             'post': post})


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)