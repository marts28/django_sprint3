from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    posts = filter_query(
        Post.objects.select_related('location', 'category', 'author')
    )[:5]

    context = {
        'post_list': posts,
    }

    return render(request, template, context)


def post_detail(request, post_id):
    current_time = timezone.now()

    post = get_object_or_404(
        Post,
        id=post_id,
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    )
    template = 'blog/detail.html'
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'

    category = get_object_or_404(Category,
                                 slug=category_slug, is_published=True)

    post_list = filter_query(
        category.posts.select_related('location', 'category', 'author'),
        True
    )

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)


def filter_query(query_set, is_category=False):
    current_time = timezone.now()
    if is_category:
        return query_set.filter(pub_date__lte=current_time,
                                is_published=True)
    else:
        return query_set.filter(pub_date__lte=current_time,
                                is_published=True,
                                category__is_published=True)
