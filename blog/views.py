import logging
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CommentForm
# from django.http import HttpResponse
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers
# from django.core.cache import cache


# cache.get_many()
logger = logging.getLogger(__name__)


# decorators for cache
# @cache_page(300)
# @vary_on_headers("Cookie")    # this would prevent every user from showing the same cookie cache which 
# stores the user information
def index(request):
    posts = (
        Post.objects.filter(published_at__lte=timezone.now())
        .select_related("author")
        .only("slug", "title", "author", "published_at", "summary", "content", )
        # .defer("created_at", "modified_at")
    )
   
    logger.info("%d present", len(posts))
    # return HttpResponse(str(request.user))    # this was added to check the vulnerability of using cache
    return render(request, "blog/index.html", {
        "posts": posts
    })


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # deals with adding the comment
    if request.user.is_authenticated and request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.creator = request.user
                comment.content_object = post
                comment.save()
                logger.info("%s just added the comment", request.user.username)    # logging the info of comment
                return redirect(request.path_info)
            else:
                comment_form = CommentForm(request.POST)
        elif request.method == "GET":
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, "blog/post-details.html", {
        "post": post,
        "comment_form": comment_form,
    })
