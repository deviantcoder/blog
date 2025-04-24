from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings

from elastic_transport import ConnectionError

from core.utils import paginate

from .documents import PostDocument
from .filters import PostFilter
from .forms import PostForm
from .models import Comment, Post, Tag, Upvote

User = get_user_model()


def posts_list(request):
    posts_filter = PostFilter(
        request.GET,
        queryset=Post.objects.filter(status='published').order_by('-created')
    )

    paginator = Paginator(posts_filter.qs, settings.PAGE_SIZE)
    posts = paginator.page(1)

    context = {
        'posts': posts,
        'title': 'Feed',
        'filter': posts_filter,
        'recent_posts': request.session.get('recent_posts', []),
    }

    if request.htmx:
        return render(request, 'blog/partials/posts-container.html', context)

    return render(request, 'blog/posts-list.html', context)


def get_posts(request):
    page = request.GET.get('page', 1)

    posts_filter = PostFilter(
        request.GET,
        queryset=Post.objects.filter(status='published').order_by('-created')
    )

    paginator = Paginator(posts_filter.qs, settings.PAGE_SIZE)

    context = {
        'posts': paginator.page(page),
    }

    return render(request, 'blog/partials/posts-container.html#post_list', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_authenticated:
        recent_posts = request.session.get('recent_posts', [])
        post_id = str(post.id)

        if post_id not in recent_posts:
            recent_posts.append(post_id)
            request.session['recent_posts'] = recent_posts[:10]

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
            post.status = 'draft' if 'save_draft' in request.POST else 'published'
            post.save()

            tags_input = form.cleaned_data['tags']

            if tags_input:
                tag_names = [name.strip() for name in tags_input.split(',') if name.strip()][:5]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    post.tags.add(tag)

            messages.success(request, f'Post {'saved as draft' if post.status == 'draft' else 'published'}')

            return redirect('blog:post_detail', post.slug)
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
            post = form.save(commit=False)
            post.status = 'draft' if 'save_draft' in request.POST else 'published'
            post.save()

            post.tags.clear()
            tags_input = form.cleaned_data['tags']

            if tags_input:
                tag_names = [name.strip() for name in tags_input.split(',') if name.strip()][:5]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    post.tags.add(tag)

            messages.success(request, f'Post {'saved as draft' if post.status == 'draft' else 'published'}')
            
            return redirect('blog:post_detail', post.slug)
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
    try:
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

        posts_filter = PostFilter(
            request.GET,
            queryset=post_queryset
        )

        context = {
            'title': 'Search',
            'search_query': query or 'Search',
            'filter': posts_filter,
            'query': query,
            'recent_posts': request.session.get('recent_posts', [])
        }

        return render(request, 'blog/search.html', context)
    except ConnectionError:
        return render(request, '404.html')


@login_required(login_url='accounts:login')
def create_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        body = request.POST.get('body', '')
        parent_id = request.POST.get('parent_id', None)

        if body:
            parent = Comment.objects.get(id=parent_id) if parent_id else None

            Comment.objects.create(
                author=request.user.profile,
                post=post,
                body=body,
                parent=parent,
            )
            
            messages.success(request, 'Comment created')
        else:
            messages.warning(request, 'Comment cannot be empty')
        
        return redirect('blog:post_detail', slug)


@login_required(login_url='accounts:login')
def upvote_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    profile = request.user.profile

    if post.upvotes.filter(profile=profile).exists():
        post.upvotes.get(profile=profile).delete()
        messages.success(request, 'Upvote removed')
    else:
        Upvote.objects.create(
            post=post,
            profile=profile
        )
        messages.success(request, 'Post upvoted')

    return redirect('blog:post_detail', slug)


@login_required(login_url='accounts:login')
def user_settings(request):
    user = request.user
    if request.method == 'POST':
        if 'update_username' in request.POST:
            new_username = request.POST.get('username')

            if not new_username:
                messages.warning(request, 'Username cannot be empty')
            elif new_username == user.username:
                messages.warning(request, 'This is already your username')
            elif User.objects.filter(username=new_username).exists():
                messages.warning(request, 'This username is already taken')
            else:
                user.username = new_username
                user.save()
                messages.success(request, 'Username updated')

            return redirect('blog:settings')
    
        if 'update_image' in request.POST:
            new_image = request.FILES.get('image')

            if new_image:
                user.profile.image = new_image
                user.profile.save()
                messages.success(request, 'Profile picture updated')

            return redirect('blog:settings')

    context = {
        'title': 'Settings',
        'published_posts': Post.objects.filter(author=request.user.profile, status='published'),
        'draft_posts': Post.objects.filter(author=request.user.profile, status='draft'),
    }

    return render(request, 'blog/settings.html', context)


@login_required(login_url='accounts:login')
def publish_draft(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id') or None
        post = get_object_or_404(Post, id=post_id)

        if post.status == 'draft':
            post.status = 'published'

        post.save()

        messages.success(request, f'Published draft: {request.POST.get('post_id')}')
        
        return redirect('blog:settings')

    return redirect('blog:settings')


def tag_search(request):
    query = request.GET.get('q', '').strip()

    if query:
        tags = Tag.objects.filter(name__icontains=query)[:10]
    else:
        tags = Tag.objects.all()[:10]

    return JsonResponse([{'id': tag.name, 'text': tag.name} for tag in tags], safe=False)