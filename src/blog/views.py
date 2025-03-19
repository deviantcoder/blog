from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post
from .forms import PostForm
from .documents import PostDocument


def home_feed_view(request):
    posts = Post.objects.filter(status='published').order_by('-created')

    context = {
        'title': 'Feed',
        'posts': posts,
        'recent_posts': request.session.get('recent_posts', [])
    }

    return render(request, 'blog/home_feed.html', context)


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_authenticated:
        recent_posts = request.session.get('recent_posts', [])
        post_id = str(post.id)

        if post_id not in recent_posts:
            recent_posts.append(post_id)
            request.session['recent_posts'] = recent_posts[:5]

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
            post.author = request.user.profile
            post.status = 'published'
            post.save()
            messages.success(request, 'Post created')
            return redirect('blog:view_post', post.slug)
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
            return redirect('blog:view_post', post.slug)
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


def search(request):
    query = request.GET.get('query', '').strip()
    posts = PostDocument.search().filter('term', status='published')

    if query:
        posts = posts.query(
            'multi_match',
            query=query,
            fields=['title^2', 'content'],
            fuzziness='AUTO'
        ).sort('-created')

    post_ids = [hit.id for hit in posts]

    post_queryset = Post.objects.filter(id__in=post_ids).order_by('-created') if post_ids else Post.objects.none()

    context = {
        'search_query': query or 'Search',
        'posts': post_queryset,
        'query': query,
        'recent_posts': request.session.get('recent_posts', [])
    }

    return render(request, 'blog/search.html', context)
