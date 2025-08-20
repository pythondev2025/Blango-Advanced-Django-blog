from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.template import Library
from blog.models import Post 


register = Library()
user_model = get_user_model()


 # in this way the custom name of filter is passed if we pass the name arg rather than defult fn name
@register.simple_tag(name="author_details_tag", takes_context=True)
def author_details(context):
    # taking in the context passed to the templates without passing in the any argument to tag
    request = context["request"]
    current_user = request.user
    post = context["post"]
    author = post.author

    if not isinstance(author, user_model):
        # return the empty string as safe default for avoiding errors
        return ""
    
    # inspite of escaping and then marking safe we would directly use format_html which act similar 
    # like formatted string, first the html is passed and then the arguments if any
    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"
    
    if author.email:
        prefix = format_html("<a href='mailto: {}'>", author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""
    
    if author == current_user:
        return format_html("{}<strong>me</strong>{}", prefix, suffix)
    else:
        return format_html("{} {} {}", prefix, name, suffix)


@register.simple_tag(name="row")
def row_div(extra_classes=""):
    return format_html("<div class='row {}'>", extra_classes)


@register.simple_tag(name="endrow")
def endrow_div():
    return format_html("</div>")


@register.simple_tag(name="col")
def row_div(extra_classes=""):
    return format_html("<div class='col {}'>", extra_classes)


@register.simple_tag(name="endcol")
def endcol_div():
    return format_html("</div>")


@register.inclusion_tag("components/post-list.html")
def recent_posts(post):
    # total_posts = Post
    posts = Post.objects.exclude(pk=post.pk)[:6]
    print("function loaded")
    return {
        "title": "Recent Posts",
        "posts": posts,
    }
