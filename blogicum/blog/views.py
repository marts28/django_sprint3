from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    current_time = timezone.now()
    posts = Post.objects.select_related('category').filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).select_related('author'
                     ).select_related('location').order_by('-pub_date')[:5]

    context = {
        'post_list': posts,
    }

    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'

    current_time = timezone.now()

    post = get_object_or_404(
        Post, id=pk, pub_date__lte=current_time,
        is_published=True, category__is_published=True
    )

    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'

    category = get_object_or_404(Category,
                                 slug=category_slug, is_published=True)

    current_time = timezone.now()
    post_list = Post.objects.select_related('category').filter(
        pub_date__lte=current_time,
        is_published=True,
        category__slug=category_slug
    ).select_related('author').select_related('location')

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
