from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post
from .forms import PostForm


def home_feed_view(request):
    posts = Post.objects.filter(status='published')

    context = {
        'title': 'Feed',
        'posts': posts,
    }

    return render(request, 'blog/home_feed.html', context)


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    context = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'blog/post.html', context)


@login_required(login_url='accounts:login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'published'
            post.save()
            messages.success(request, 'Post created')
            return redirect('/')
    else:
        form = PostForm()

    context = {
        'title': 'Create Post',
        'header': 'Create Post',
        'form': form,
    }

    return render(request, 'blog/post_form.html', context)


@login_required(login_url='accounts:login')
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated')
            return redirect('/')
    else:
        form = PostForm(instance=post)

    context = {
        'title': 'Create Post',
        'header': 'Edit Post',
        'form': form,
    }

    return render(request, 'blog/post_form.html', context)


@login_required(login_url='accounts:login')
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        try:
            post.delete()
            messages.info(request, 'Post deleted')
            return redirect('/')
        except Post.DoesNotExist:
            messages.warning(request, 'Post does not exist')
            return redirect('/')

    context = {
        'title': 'Delete Post',
        'post': post,
    }

    return render(request, 'blog/delete_post.html', context)
